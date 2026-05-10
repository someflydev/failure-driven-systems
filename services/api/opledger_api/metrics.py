from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from threading import Lock

from fastapi.responses import Response

PROMETHEUS_CONTENT_TYPE = "text/plain; version=0.0.4; charset=utf-8"
HTTP_DURATION_BUCKETS = (0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
REPORTING_CALL_BUCKETS = (0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0)


MetricLabels = tuple[tuple[str, str], ...]


class MetricsRegistry:
    def __init__(self) -> None:
        self._lock = Lock()
        self._counters: defaultdict[str, defaultdict[MetricLabels, float]] = (
            defaultdict(lambda: defaultdict(float))
        )
        self._histograms: defaultdict[
            str, defaultdict[MetricLabels, dict[float, int]]
        ] = defaultdict(lambda: defaultdict(dict))
        self._histogram_sums: defaultdict[str, defaultdict[MetricLabels, float]] = (
            defaultdict(lambda: defaultdict(float))
        )
        self._histogram_counts: defaultdict[str, defaultdict[MetricLabels, int]] = (
            defaultdict(lambda: defaultdict(int))
        )
        self._histogram_buckets: dict[str, tuple[float, ...]] = {}

    def increment(
        self,
        name: str,
        labels: dict[str, str] | None = None,
        amount: float = 1.0,
    ) -> None:
        label_key = self._label_key(labels)
        with self._lock:
            self._counters[name][label_key] += amount

    def observe(
        self,
        name: str,
        value: float,
        buckets: Iterable[float],
        labels: dict[str, str] | None = None,
    ) -> None:
        bucket_values = tuple(sorted(buckets))
        label_key = self._label_key(labels)
        with self._lock:
            existing_buckets = self._histogram_buckets.setdefault(name, bucket_values)
            if existing_buckets != bucket_values:
                raise ValueError(
                    f"Histogram {name} was observed with different buckets."
                )

            bucket_counts = self._histograms[name][label_key]
            if not bucket_counts:
                for bucket in bucket_values:
                    bucket_counts[bucket] = 0
            for bucket in bucket_values:
                if value <= bucket:
                    bucket_counts[bucket] += 1
            self._histogram_sums[name][label_key] += value
            self._histogram_counts[name][label_key] += 1

    def render(self) -> str:
        lines: list[str] = []
        with self._lock:
            for name in sorted(self._counters):
                for labels, value in sorted(self._counters[name].items()):
                    lines.append(f"{name}{self._format_labels(labels)} {value:g}")

            for name in sorted(self._histograms):
                buckets = self._histogram_buckets[name]
                for labels, bucket_counts in sorted(self._histograms[name].items()):
                    for bucket in buckets:
                        bucket_labels = labels + (("le", f"{bucket:g}"),)
                        lines.append(
                            f"{name}_bucket{self._format_labels(bucket_labels)} "
                            f"{bucket_counts[bucket]}"
                        )
                    infinity_labels = labels + (("le", "+Inf"),)
                    count = self._histogram_counts[name][labels]
                    lines.append(
                        f"{name}_bucket{self._format_labels(infinity_labels)} {count}"
                    )
                    lines.append(f"{name}_count{self._format_labels(labels)} {count}")
                    total = self._histogram_sums[name][labels]
                    lines.append(f"{name}_sum{self._format_labels(labels)} {total:g}")

        return "\n".join(lines) + "\n"

    def reset(self) -> None:
        with self._lock:
            self._counters.clear()
            self._histograms.clear()
            self._histogram_sums.clear()
            self._histogram_counts.clear()
            self._histogram_buckets.clear()

    @staticmethod
    def _label_key(labels: dict[str, str] | None) -> MetricLabels:
        if labels is None:
            return ()
        return tuple(sorted((key, str(value)) for key, value in labels.items()))

    @staticmethod
    def _format_labels(labels: MetricLabels) -> str:
        if not labels:
            return ""
        formatted_labels = []
        for key, value in labels:
            escaped_value = value.replace("\\", "\\\\").replace('"', '\\"')
            formatted_labels.append(f'{key}="{escaped_value}"')
        formatted = ",".join(formatted_labels)
        return f"{{{formatted}}}"


metrics_registry = MetricsRegistry()


def metrics_response() -> Response:
    return Response(
        content=metrics_registry.render(),
        media_type=PROMETHEUS_CONTENT_TYPE,
    )


def record_http_request(
    *,
    service: str,
    method: str,
    path: str,
    status_code: int,
    duration_seconds: float,
) -> None:
    labels = {
        "service": service,
        "method": method,
        "path": path,
        "status": str(status_code),
    }
    metrics_registry.increment("opledger_http_requests_total", labels)
    metrics_registry.observe(
        "opledger_http_request_duration_seconds",
        duration_seconds,
        HTTP_DURATION_BUCKETS,
        {
            "service": service,
            "method": method,
            "path": path,
        },
    )
    if status_code >= 500:
        metrics_registry.increment(
            "opledger_api_errors_total",
            {
                "service": service,
                "method": method,
                "path": path,
                "status": str(status_code),
            },
        )


def record_report_job_queued(report_type: str) -> None:
    metrics_registry.increment(
        "opledger_report_jobs_queued_total",
        {"report_type": report_type},
    )


def record_report_job_completed(report_type: str, status: str) -> None:
    metrics_registry.increment(
        "opledger_report_jobs_completed_total",
        {"report_type": report_type, "status": status},
    )


def record_worker_job_failure(job_type: str, error_class: str) -> None:
    metrics_registry.increment(
        "opledger_worker_job_failures_total",
        {"job_type": job_type, "error_class": error_class},
    )


def record_reporting_service_call(
    *,
    report_type: str,
    outcome: str,
    duration_seconds: float,
) -> None:
    metrics_registry.observe(
        "opledger_reporting_service_call_duration_seconds",
        duration_seconds,
        REPORTING_CALL_BUCKETS,
        {"report_type": report_type, "outcome": outcome},
    )


def record_reporting_service_failure(report_type: str, reason: str) -> None:
    metrics_registry.increment(
        "opledger_reporting_service_failures_total",
        {"report_type": report_type, "reason": reason},
    )


def record_notification_attempt(channel: str, status: str) -> None:
    metrics_registry.increment(
        "opledger_notification_attempts_total",
        {"channel": channel, "status": status},
    )


def record_cache_access(endpoint: str, outcome: str) -> None:
    metrics_registry.increment(
        "opledger_cache_access_total",
        {"endpoint": endpoint, "outcome": outcome},
    )
