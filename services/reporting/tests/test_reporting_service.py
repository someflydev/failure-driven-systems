from datetime import UTC, datetime

from fastapi.testclient import TestClient

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
    )

    assert response.status_code == 200
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
