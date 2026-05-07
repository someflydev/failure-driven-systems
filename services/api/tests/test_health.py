from fastapi.testclient import TestClient

from opledger_api.db import DatabaseReadinessError
from opledger_api.health import get_readiness_checker
from opledger_api.main import create_app


def test_root_route_reports_service() -> None:
    client = TestClient(create_app())

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"service": "OpsLedger API", "status": "ok"}


def test_live_health_check_has_no_external_dependency() -> None:
    app = create_app()

    def failing_readiness() -> dict[str, str | int | None]:
        raise AssertionError("liveness must not check the database")

    app.dependency_overrides[get_readiness_checker] = lambda: failing_readiness
    client = TestClient(app)

    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_health_check_reports_database_available() -> None:
    app = create_app()

    def successful_readiness() -> dict[str, str | int | None]:
        return {
            "driver": "postgresql+psycopg",
            "host": "localhost",
            "port": 55432,
            "database": "opledger",
        }

    app.dependency_overrides[get_readiness_checker] = lambda: successful_readiness
    client = TestClient(app)

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": {
            "status": "ok",
            "driver": "postgresql+psycopg",
            "host": "localhost",
            "port": 55432,
            "database": "opledger",
        },
    }


def test_ready_health_check_reports_sanitized_database_failure() -> None:
    app = create_app()

    def failing_readiness() -> dict[str, str | int | None]:
        raise DatabaseReadinessError(
            "OperationalError",
            {
                "driver": "postgresql+psycopg",
                "host": "localhost",
                "port": 55432,
                "database": "opledger",
            },
        )

    app.dependency_overrides[get_readiness_checker] = lambda: failing_readiness
    client = TestClient(app)

    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "not_ready",
        "database": {
            "status": "unavailable",
            "error_class": "OperationalError",
            "driver": "postgresql+psycopg",
            "host": "localhost",
            "port": 55432,
            "database": "opledger",
        },
    }
