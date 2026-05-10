from datetime import UTC, datetime

import httpx
import pytest

from opledger_api.report_contracts import WorkRequestSummaryRenderRequest
from opledger_api.reporting_client import (
    ReportingServiceError,
    render_work_request_summary_report_remote,
)


def render_request() -> WorkRequestSummaryRenderRequest:
    return WorkRequestSummaryRenderRequest(
        generated_at=datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
        total_work_requests=1,
        by_status={
            "open": 1,
            "in_progress": 0,
            "resolved": 0,
            "cancelled": 0,
        },
        status_event_count=2,
    )


def test_reporting_client_posts_payload_and_validates_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_timeout: object | None = None
    captured_payload: object | None = None

    def fake_post(
        url: str,
        *,
        json: object,
        timeout: float,
    ) -> httpx.Response:
        nonlocal captured_timeout, captured_payload
        assert url == "http://reporting:8001/reports/work-requests/summary/render"
        captured_timeout = timeout
        captured_payload = json
        request = httpx.Request("POST", url)
        return httpx.Response(
            200,
            request=request,
            json={
                "contract_version": "report-rendering.v1",
                "report_type": "work_request_summary",
                "generated_at": "2026-01-01T12:00:00Z",
                "total_work_requests": 1,
                "by_status": {
                    "open": 1,
                    "in_progress": 0,
                    "resolved": 0,
                    "cancelled": 0,
                },
                "status_event_count": 2,
                "warnings": [],
            },
        )

    monkeypatch.setattr(httpx, "post", fake_post)

    report = render_work_request_summary_report_remote(
        render_request(),
        base_url="http://reporting:8001/",
        timeout_seconds=1.5,
    )

    assert captured_timeout == 1.5
    assert isinstance(captured_payload, dict)
    assert report.total_work_requests == 1


def test_reporting_client_maps_timeout_to_clear_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def timeout_post(
        _url: str,
        *,
        json: object,
        timeout: float,
    ) -> httpx.Response:
        raise httpx.TimeoutException("slow")

    monkeypatch.setattr(httpx, "post", timeout_post)

    with pytest.raises(ReportingServiceError, match="timeout"):
        render_work_request_summary_report_remote(
            render_request(),
            base_url="http://reporting:8001",
            timeout_seconds=0.1,
        )


def test_reporting_client_accepts_additive_response_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def newer_renderer_post(
        url: str,
        *,
        json: object,
        timeout: float,
    ) -> httpx.Response:
        request = httpx.Request("POST", url)
        return httpx.Response(
            200,
            request=request,
            json={
                "contract_version": "report-rendering.v1",
                "report_type": "work_request_summary",
                "generated_at": "2026-01-01T12:00:00Z",
                "total_work_requests": 1,
                "by_status": {
                    "open": 1,
                    "in_progress": 0,
                    "resolved": 0,
                    "cancelled": 0,
                },
                "status_event_count": 2,
                "warnings": [],
                "renderer_build": "newer-than-client",
            },
        )

    monkeypatch.setattr(httpx, "post", newer_renderer_post)

    report = render_work_request_summary_report_remote(
        render_request(),
        base_url="http://reporting:8001",
        timeout_seconds=1.0,
    )

    assert report.total_work_requests == 1
    assert "renderer_build" not in report.model_dump()


def test_reporting_client_maps_http_status_to_clear_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def failing_post(
        _url: str,
        *,
        json: object,
        timeout: float,
    ) -> httpx.Response:
        request = httpx.Request("POST", "http://reporting/render")
        return httpx.Response(503, request=request)

    monkeypatch.setattr(httpx, "post", failing_post)

    with pytest.raises(ReportingServiceError, match="non_2xx_status_503"):
        render_work_request_summary_report_remote(
            render_request(),
            base_url="http://reporting:8001",
            timeout_seconds=1.0,
        )


def test_reporting_client_maps_malformed_json_to_clear_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def malformed_post(
        url: str,
        *,
        json: object,
        timeout: float,
    ) -> httpx.Response:
        request = httpx.Request("POST", url)
        return httpx.Response(200, request=request, content="{not valid json")

    monkeypatch.setattr(httpx, "post", malformed_post)

    with pytest.raises(ReportingServiceError, match="invalid_response_json"):
        render_work_request_summary_report_remote(
            render_request(),
            base_url="http://reporting:8001",
            timeout_seconds=1.0,
        )


def test_reporting_client_maps_incompatible_contract_to_clear_exception(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def incompatible_post(
        url: str,
        *,
        json: object,
        timeout: float,
    ) -> httpx.Response:
        request = httpx.Request("POST", url)
        return httpx.Response(
            200,
            request=request,
            json={
                "contract_version": "report-rendering.v2",
                "report_type": "work_request_summary",
            },
        )

    monkeypatch.setattr(httpx, "post", incompatible_post)

    with pytest.raises(ReportingServiceError, match="invalid_response_contract"):
        render_work_request_summary_report_remote(
            render_request(),
            base_url="http://reporting:8001",
            timeout_seconds=1.0,
        )
