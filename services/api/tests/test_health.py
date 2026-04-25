from fastapi.testclient import TestClient

from opledger_api.main import create_app


def test_root_route_reports_service() -> None:
    client = TestClient(create_app())

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"service": "OpsLedger API", "status": "ok"}


def test_live_health_check_has_no_external_dependency() -> None:
    client = TestClient(create_app())

    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
