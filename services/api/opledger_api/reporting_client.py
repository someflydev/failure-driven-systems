"""HTTP client for the extracted report-rendering service."""

from dataclasses import dataclass
from json import JSONDecodeError
from time import perf_counter

import httpx
from pydantic import ValidationError

from opledger_api.metrics import (
    record_reporting_service_call,
    record_reporting_service_failure,
)
from opledger_api.report_contracts import (
    WORK_REQUEST_SUMMARY_REPORT,
    WorkRequestSummaryRenderRequest,
    WorkRequestSummaryReport,
)


@dataclass
class ReportingServiceError(RuntimeError):
    """Raised when remote report rendering fails in a bounded way."""

    reason: str

    def __str__(self) -> str:
        return f"Reporting service failed: {self.reason}"


def render_work_request_summary_report_remote(
    request: WorkRequestSummaryRenderRequest,
    *,
    base_url: str,
    timeout_seconds: float,
    correlation_id: str | None = None,
) -> WorkRequestSummaryReport:
    url = f"{base_url.rstrip('/')}/reports/work-requests/summary/render"
    headers = (
        {"X-Correlation-ID": correlation_id} if correlation_id is not None else None
    )
    started_at = perf_counter()
    try:
        response = httpx.post(
            url,
            json=request.model_dump(mode="json"),
            headers=headers,
            timeout=timeout_seconds,
        )
        response.raise_for_status()
    except httpx.TimeoutException as exc:
        record_reporting_failure("timeout", started_at)
        raise ReportingServiceError("timeout") from exc
    except httpx.HTTPStatusError as exc:
        reason = f"non_2xx_status_{exc.response.status_code}"
        record_reporting_failure(reason, started_at)
        raise ReportingServiceError(reason) from exc
    except httpx.RequestError as exc:
        reason = f"request_error_{exc.__class__.__name__}"
        record_reporting_failure(reason, started_at)
        raise ReportingServiceError(reason) from exc

    try:
        response_payload = response.json()
    except JSONDecodeError as exc:
        record_reporting_failure("invalid_response_json", started_at)
        raise ReportingServiceError("invalid_response_json") from exc

    try:
        report = WorkRequestSummaryReport.model_validate(response_payload)
    except ValidationError as exc:
        record_reporting_failure("invalid_response_contract", started_at)
        raise ReportingServiceError("invalid_response_contract") from exc

    record_reporting_service_call(
        report_type=WORK_REQUEST_SUMMARY_REPORT,
        outcome="succeeded",
        duration_seconds=perf_counter() - started_at,
    )
    return report


def record_reporting_failure(reason: str, started_at: float) -> None:
    record_reporting_service_call(
        report_type=WORK_REQUEST_SUMMARY_REPORT,
        outcome="failed",
        duration_seconds=perf_counter() - started_at,
    )
    record_reporting_service_failure(WORK_REQUEST_SUMMARY_REPORT, reason)
