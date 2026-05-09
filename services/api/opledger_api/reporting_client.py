"""HTTP client for the extracted report-rendering service."""

from dataclasses import dataclass

import httpx

from opledger_api.report_contracts import (
    WorkRequestSummaryRenderRequest,
    WorkRequestSummaryReport,
)


@dataclass(frozen=True)
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
) -> WorkRequestSummaryReport:
    url = f"{base_url.rstrip('/')}/reports/work-requests/summary/render"
    try:
        response = httpx.post(
            url,
            json=request.model_dump(mode="json"),
            timeout=timeout_seconds,
        )
        response.raise_for_status()
    except httpx.TimeoutException as exc:
        raise ReportingServiceError("timeout") from exc
    except httpx.HTTPStatusError as exc:
        raise ReportingServiceError(f"http_{exc.response.status_code}") from exc
    except httpx.RequestError as exc:
        raise ReportingServiceError(exc.__class__.__name__) from exc

    try:
        return WorkRequestSummaryReport.model_validate(response.json())
    except ValueError as exc:
        raise ReportingServiceError("invalid_response") from exc
