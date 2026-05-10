from datetime import UTC, datetime
from time import monotonic

import pytest
from fastapi.testclient import TestClient

from reporting_service.config import get_settings
from reporting_service.main import create_app


def valid_render_payload() -> dict[str, object]:
    return {
        "contract_version": "report-rendering.v1",
        "report_type": "work_request_summary",
        "generated_at": datetime(2026, 1, 1, 12, 0, tzinfo=UTC).isoformat(),
        "total_work_requests": 3,
        "by_status": {
            "open": 1,
            "in_progress": 1,
            "resolved": 1,
            "cancelled": 0,
        },
        "status_event_count": 5,
    }


def test_reporting_service_renders_contract_payload() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/reports/work-requests/summary/render",
        json=valid_render_payload(),
        headers={"X-Correlation-ID": "corr-reporting-1"},
    )

    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == "corr-reporting-1"
    assert response.json() == {
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


def test_reporting_service_rejects_invalid_contract_payload() -> None:
    client = TestClient(create_app())
    payload = valid_render_payload()
    payload["by_status"] = {"open": 3}

    response = client.post("/reports/work-requests/summary/render", json=payload)

    assert response.status_code == 422


def test_reporting_service_accepts_additive_request_field() -> None:
    client = TestClient(create_app())
    payload = valid_render_payload() | {"requested_by": "operator@example.com"}

    response = client.post("/reports/work-requests/summary/render", json=payload)

    assert response.status_code == 200
    assert response.json()["total_work_requests"] == 3
    assert "requested_by" not in response.json()


def test_reporting_service_ignores_failure_mode_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("OPLEDGER_ENVIRONMENT", "local")
    monkeypatch.setenv("OPLEDGER_REPORTING_FAILURE_MODE", "http_500")
    monkeypatch.setenv("OPLEDGER_REPORTING_FAILURE_INJECTION_ENABLED", "false")
    client = TestClient(create_app())

    response = client.post(
        "/reports/work-requests/summary/render",
        json=valid_render_payload(),
    )

    assert response.status_code == 200
    get_settings.cache_clear()


def test_reporting_service_injects_500_only_when_enabled_locally(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("OPLEDGER_ENVIRONMENT", "local")
    monkeypatch.setenv("OPLEDGER_REPORTING_FAILURE_MODE", "http_500")
    monkeypatch.setenv("OPLEDGER_REPORTING_FAILURE_INJECTION_ENABLED", "true")
    client = TestClient(create_app())

    response = client.post(
        "/reports/work-requests/summary/render",
        json=valid_render_payload(),
    )

    assert response.status_code == 500
    assert response.json()["failure_mode"] == "http_500"
    get_settings.cache_clear()


def test_reporting_service_injects_malformed_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("OPLEDGER_ENVIRONMENT", "local")
    monkeypatch.setenv("OPLEDGER_REPORTING_FAILURE_MODE", "malformed_response")
    monkeypatch.setenv("OPLEDGER_REPORTING_FAILURE_INJECTION_ENABLED", "true")
    client = TestClient(create_app())

    response = client.post(
        "/reports/work-requests/summary/render",
        json=valid_render_payload(),
    )

    assert response.status_code == 200
    assert response.text == "{not valid json"
    get_settings.cache_clear()


def test_reporting_service_injects_incompatible_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("OPLEDGER_ENVIRONMENT", "local")
    monkeypatch.setenv("OPLEDGER_REPORTING_FAILURE_MODE", "incompatible_response")
    monkeypatch.setenv("OPLEDGER_REPORTING_FAILURE_INJECTION_ENABLED", "true")
    client = TestClient(create_app())

    response = client.post(
        "/reports/work-requests/summary/render",
        json=valid_render_payload(),
    )

    assert response.status_code == 200
    assert response.json()["contract_version"] == "report-rendering.v2"
    get_settings.cache_clear()


def test_reporting_service_injects_delay_only_when_enabled_locally(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    get_settings.cache_clear()
    monkeypatch.setenv("OPLEDGER_ENVIRONMENT", "local")
    monkeypatch.setenv("OPLEDGER_REPORTING_FAILURE_MODE", "delay")
    monkeypatch.setenv("OPLEDGER_REPORTING_FAILURE_DELAY_SECONDS", "0.01")
    monkeypatch.setenv("OPLEDGER_REPORTING_FAILURE_INJECTION_ENABLED", "true")
    client = TestClient(create_app())

    started_at = monotonic()
    response = client.post(
        "/reports/work-requests/summary/render",
        json=valid_render_payload(),
    )

    assert response.status_code == 200
    assert monotonic() - started_at >= 0.01
    get_settings.cache_clear()
