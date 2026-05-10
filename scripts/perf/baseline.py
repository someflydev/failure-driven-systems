#!/usr/bin/env python3
"""Lightweight OpsLedger baseline runner.

The runner is deliberately sequential and conservative. It is intended for
Phase 5 measurement practice before any caching, indexing, or read model work.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "http://127.0.0.1:18080"
LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}
MAX_RATE_PER_SECOND = 5.0
MAX_DURATION_SECONDS = 60.0
DEFAULT_TIMEOUT_SECONDS = 5.0
FIXTURE_EMAIL = "perf-baseline@example.com"
FIXTURE_TITLE_PREFIX = "Perf baseline fixture"


@dataclass(frozen=True)
class Sample:
    scenario: str
    method: str
    path: str
    status: int
    duration_ms: float
    ok: bool


def parsed_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run safe, low-rate OpsLedger performance baselines."
    )
    parser.add_argument(
        "scenario",
        choices=[
            "list-work-requests",
            "create-work-requests",
            "poll-report-job",
            "seed-read-fixture",
        ],
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--rate", type=float, default=1.0)
    parser.add_argument("--duration-seconds", type=float, default=10.0)
    parser.add_argument(
        "--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS
    )
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--customer-id", type=int)
    parser.add_argument("--report-job-id", type=int)
    parser.add_argument("--fixture-size", type=int, default=5)
    parser.add_argument("--allow-writes", action="store_true")
    parser.add_argument("--allow-non-local", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output-csv", type=Path)
    return parser.parse_args()


def is_local_base_url(base_url: str) -> bool:
    parsed = urlparse(base_url)
    return parsed.hostname in LOCAL_HOSTS


def enforce_safety(args: argparse.Namespace) -> None:
    if args.rate <= 0:
        raise SystemExit("--rate must be greater than zero.")
    if args.rate > MAX_RATE_PER_SECOND:
        raise SystemExit(f"--rate must be <= {MAX_RATE_PER_SECOND:g}.")
    if args.duration_seconds <= 0:
        raise SystemExit("--duration-seconds must be greater than zero.")
    if args.duration_seconds > MAX_DURATION_SECONDS:
        raise SystemExit(f"--duration-seconds must be <= {MAX_DURATION_SECONDS:g}.")
    if args.timeout_seconds <= 0:
        raise SystemExit("--timeout-seconds must be greater than zero.")
    if not is_local_base_url(args.base_url) and not args.allow_non_local:
        raise SystemExit(
            "Refusing non-local target. Pass --allow-non-local explicitly."
        )
    if (
        args.scenario in {"create-work-requests", "seed-read-fixture"}
        and not args.allow_writes
    ):
        raise SystemExit("Refusing write scenario. Pass --allow-writes explicitly.")
    if args.scenario == "create-work-requests" and args.customer_id is None:
        raise SystemExit("--customer-id is required for create-work-requests.")
    if args.scenario == "poll-report-job" and args.report_job_id is None:
        raise SystemExit("--report-job-id is required for poll-report-job.")
    if args.limit < 1 or args.limit > 100:
        raise SystemExit("--limit must be between 1 and 100.")
    if args.fixture_size < 1 or args.fixture_size > 20:
        raise SystemExit("--fixture-size must be between 1 and 20.")


def request_json(
    base_url: str,
    method: str,
    path: str,
    timeout_seconds: float,
    body: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any] | None]:
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(
        base_url.rstrip("/") + path,
        data=data,
        headers=headers,
        method=method,
    )
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            raw_body = response.read()
            if not raw_body:
                return response.status, None
            return response.status, json.loads(raw_body.decode("utf-8"))
    except HTTPError as exc:
        raw_body = exc.read()
        if raw_body:
            return exc.code, json.loads(raw_body.decode("utf-8"))
        return exc.code, None
    except URLError as exc:
        raise SystemExit(f"Request failed before HTTP response: {exc}") from exc


def timed_request(
    scenario: str,
    base_url: str,
    method: str,
    path: str,
    timeout_seconds: float,
    body: dict[str, Any] | None = None,
) -> Sample:
    started = time.perf_counter()
    status, _payload = request_json(base_url, method, path, timeout_seconds, body)
    duration_ms = (time.perf_counter() - started) * 1000
    return Sample(
        scenario=scenario,
        method=method,
        path=path,
        status=status,
        duration_ms=duration_ms,
        ok=200 <= status < 400,
    )


def find_fixture_customer_id(base_url: str, timeout_seconds: float) -> int | None:
    status, payload = request_json(
        base_url,
        "GET",
        "/customers?limit=100&offset=0",
        timeout_seconds,
    )
    if status != 200 or payload is None:
        return None
    for customer in payload.get("items", []):
        if isinstance(customer, dict) and customer.get("email") == FIXTURE_EMAIL:
            customer_id = customer.get("id")
            if isinstance(customer_id, int):
                return customer_id
    return None


def ensure_fixture_customer(base_url: str, timeout_seconds: float) -> int:
    existing_customer_id = find_fixture_customer_id(base_url, timeout_seconds)
    if existing_customer_id is not None:
        return existing_customer_id

    status, payload = request_json(
        base_url,
        "POST",
        "/customers",
        timeout_seconds,
        {"name": "Performance Baseline", "email": FIXTURE_EMAIL},
    )
    if status != 201 or payload is None or not isinstance(payload.get("id"), int):
        raise SystemExit(f"Could not create fixture customer; status={status}.")
    return int(payload["id"])


def count_fixture_work_requests(base_url: str, timeout_seconds: float) -> int:
    status, payload = request_json(
        base_url,
        "GET",
        "/work-requests?limit=100&offset=0",
        timeout_seconds,
    )
    if status != 200 or payload is None:
        return 0
    count = 0
    for work_request in payload.get("items", []):
        if isinstance(work_request, dict):
            title = work_request.get("title")
            if isinstance(title, str) and title.startswith(FIXTURE_TITLE_PREFIX):
                count += 1
    return count


def seed_read_fixture(args: argparse.Namespace) -> list[Sample]:
    customer_id = ensure_fixture_customer(args.base_url, args.timeout_seconds)
    existing_count = count_fixture_work_requests(args.base_url, args.timeout_seconds)
    samples: list[Sample] = []
    for index in range(existing_count, args.fixture_size):
        samples.append(
            timed_request(
                args.scenario,
                args.base_url,
                "POST",
                "/work-requests",
                args.timeout_seconds,
                {
                    "customer_id": customer_id,
                    "title": f"{FIXTURE_TITLE_PREFIX} {index + 1}",
                    "description": "Small deterministic row for read baselines.",
                    "status": "open",
                },
            )
        )
    return samples


def scenario_request(
    args: argparse.Namespace, index: int
) -> tuple[str, str, dict[str, Any] | None]:
    if args.scenario == "list-work-requests":
        return "GET", f"/work-requests?limit={args.limit}&offset=0", None
    if args.scenario == "create-work-requests":
        assert args.customer_id is not None
        return (
            "POST",
            "/work-requests",
            {
                "customer_id": args.customer_id,
                "title": f"Perf baseline create {int(time.time())}-{index}",
                "description": "Low-rate write baseline request.",
                "status": "open",
            },
        )
    if args.scenario == "poll-report-job":
        assert args.report_job_id is not None
        return "GET", f"/reports/jobs/{args.report_job_id}", None
    raise AssertionError(f"Unhandled scenario: {args.scenario}")


def run_scenario(args: argparse.Namespace) -> list[Sample]:
    if args.scenario == "seed-read-fixture":
        return seed_read_fixture(args)

    samples: list[Sample] = []
    interval = 1.0 / args.rate
    deadline = time.monotonic() + args.duration_seconds
    index = 0
    while time.monotonic() < deadline:
        started = time.monotonic()
        method, path, body = scenario_request(args, index)
        samples.append(
            timed_request(
                args.scenario,
                args.base_url,
                method,
                path,
                args.timeout_seconds,
                body,
            )
        )
        index += 1
        sleep_seconds = interval - (time.monotonic() - started)
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)
    return samples


def percentile(values: list[float], rank: float) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    index = min(len(sorted_values) - 1, round((rank / 100) * (len(sorted_values) - 1)))
    return sorted_values[index]


def print_summary(samples: list[Sample]) -> None:
    if not samples:
        print("No requests were needed; fixture already satisfied requested size.")
        return
    durations = [sample.duration_ms for sample in samples]
    ok_count = sum(1 for sample in samples if sample.ok)
    error_count = len(samples) - ok_count
    statuses: dict[int, int] = {}
    for sample in samples:
        statuses[sample.status] = statuses.get(sample.status, 0) + 1

    print(f"scenario={samples[0].scenario}")
    print(f"requests={len(samples)} ok={ok_count} errors={error_count}")
    print(f"statuses={dict(sorted(statuses.items()))}")
    print(f"min_ms={min(durations):.2f}")
    print(f"avg_ms={statistics.fmean(durations):.2f}")
    print(f"p50_ms={percentile(durations, 50):.2f}")
    print(f"p95_ms={percentile(durations, 95):.2f}")
    print(f"max_ms={max(durations):.2f}")


def write_csv(path: Path, samples: list[Sample]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "scenario",
                "method",
                "path",
                "status",
                "duration_ms",
                "ok",
            ],
        )
        writer.writeheader()
        for sample in samples:
            writer.writerow(
                {
                    "scenario": sample.scenario,
                    "method": sample.method,
                    "path": sample.path,
                    "status": sample.status,
                    "duration_ms": f"{sample.duration_ms:.2f}",
                    "ok": str(sample.ok).lower(),
                }
            )


def main() -> int:
    args = parsed_args()
    enforce_safety(args)
    if args.dry_run:
        print(
            "dry_run=true "
            f"scenario={args.scenario} base_url={args.base_url} "
            f"rate={args.rate:g} duration_seconds={args.duration_seconds:g}"
        )
        return 0
    samples = run_scenario(args)
    print_summary(samples)
    if args.output_csv is not None:
        write_csv(args.output_csv, samples)
        print(f"csv={args.output_csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
