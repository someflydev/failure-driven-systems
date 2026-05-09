from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from opledger_api.report_contracts import (
    REPORT_RENDERING_CONTRACT_VERSION,
    WORK_REQUEST_SUMMARY_REPORT,
    WorkRequestSummaryRenderRequest,
    WorkRequestSummaryReport,
)
from opledger_api.reports import render_work_request_summary_report


def valid_render_request_payload() -> dict[str, object]:
    return {
        "contract_version": REPORT_RENDERING_CONTRACT_VERSION,
        "report_type": WORK_REQUEST_SUMMARY_REPORT,
        "generated_at": datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
        "total_work_requests": 3,
        "by_status": {
            "open": 1,
            "in_progress": 1,
            "resolved": 1,
            "cancelled": 0,
        },
        "status_event_count": 5,
    }


def test_render_request_requires_contract_fields() -> None:
    payload = valid_render_request_payload()
    del payload["total_work_requests"]

    with pytest.raises(ValidationError) as exc_info:
        WorkRequestSummaryRenderRequest.model_validate(payload)

    assert "total_work_requests" in str(exc_info.value)


def test_render_request_rejects_unknown_extra_fields() -> None:
    payload = valid_render_request_payload() | {"renderer_timeout_ms": 5000}

    with pytest.raises(ValidationError) as exc_info:
        WorkRequestSummaryRenderRequest.model_validate(payload)

    assert "renderer_timeout_ms" in str(exc_info.value)


def test_render_request_accepts_backward_compatible_optional_fields() -> None:
    payload = valid_render_request_payload() | {"requested_by": "operator@example.com"}

    request = WorkRequestSummaryRenderRequest.model_validate(payload)

    assert request.requested_by == "operator@example.com"


def test_render_response_rejects_unknown_extra_fields() -> None:
    payload = valid_render_request_payload() | {"warnings": [], "debug_trace_id": "abc"}

    with pytest.raises(ValidationError) as exc_info:
        WorkRequestSummaryReport.model_validate(payload)

    assert "debug_trace_id" in str(exc_info.value)


def test_render_response_requires_contract_fields() -> None:
    payload = valid_render_request_payload() | {"warnings": []}
    del payload["status_event_count"]

    with pytest.raises(ValidationError) as exc_info:
        WorkRequestSummaryReport.model_validate(payload)

    assert "status_event_count" in str(exc_info.value)


def test_render_request_counts_must_match_total() -> None:
    payload = valid_render_request_payload()
    payload["total_work_requests"] = 99

    with pytest.raises(ValidationError, match="Status counts"):
        WorkRequestSummaryRenderRequest.model_validate(payload)


def test_render_output_is_deterministic_for_known_input() -> None:
    request = WorkRequestSummaryRenderRequest.model_validate(
        valid_render_request_payload()
    )

    report = render_work_request_summary_report(request)

    assert report.model_dump(mode="json") == {
        "contract_version": "report-rendering.v1",
        "report_type": "work_request_summary",
        "generated_at": "2026-01-01T12:00:00Z",
        "total_work_requests": 3,
        "by_status": {
            "open": 1,
            "in_progress": 1,
            "resolved": 1,
            "cancelled": 0,
        },
        "status_event_count": 5,
        "warnings": [],
    }
