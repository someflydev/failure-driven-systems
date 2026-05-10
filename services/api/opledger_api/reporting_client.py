"""HTTP client for the extracted report-rendering service."""

from dataclasses import dataclass
from json import JSONDecodeError

import httpx
from pydantic import ValidationError

from opledger_api.report_contracts import (
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
    try:
        response = httpx.post(
            url,
            json=request.model_dump(mode="json"),
            headers=headers,
            timeout=timeout_seconds,
        )
        response.raise_for_status()
    except httpx.TimeoutException as exc:
        raise ReportingServiceError("timeout") from exc
    except httpx.HTTPStatusError as exc:
        raise ReportingServiceError(
            f"non_2xx_status_{exc.response.status_code}"
        ) from exc
    except httpx.RequestError as exc:
        raise ReportingServiceError(f"request_error_{exc.__class__.__name__}") from exc

    try:
        response_payload = response.json()
    except JSONDecodeError as exc:
        raise ReportingServiceError("invalid_response_json") from exc

    try:
        return WorkRequestSummaryReport.model_validate(response_payload)
    except ValidationError as exc:
        raise ReportingServiceError("invalid_response_contract") from exc
