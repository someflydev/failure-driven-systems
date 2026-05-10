import logging
from typing import Any, cast

import pytest
from fastapi.testclient import TestClient

from opledger_api.db import DatabaseReadinessError
from opledger_api.health import get_readiness_checker
from opledger_api.main import create_app


def test_root_route_reports_service() -> None:
    client = TestClient(create_app())

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"service": "OpsLedger API", "status": "ok"}


def test_request_logging_includes_method_path_and_status(
    caplog: pytest.LogCaptureFixture,
) -> None:
    client = TestClient(create_app())

    with caplog.at_level(logging.INFO, logger="opledger_api.requests"):
        response = client.get(
            "/health/live",
            headers={"X-Request-ID": "req-1", "X-Correlation-ID": "corr-1"},
        )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "req-1"
    assert response.headers["X-Correlation-ID"] == "corr-1"
    request_log = next(
        record
        for record in caplog.records
        if getattr(record, "event", None) == "http_request"
    )
    request_log_fields = cast(Any, request_log)
    assert request_log_fields.method == "GET"
    assert request_log_fields.path == "/health/live"
    assert request_log_fields.status == 200


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


def test_ready_health_check_logs_sanitized_database_failure(
    caplog: pytest.LogCaptureFixture,
) -> None:
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

    with caplog.at_level(logging.WARNING, logger="opledger_api.health"):
        response = client.get("/health/ready")

    assert response.status_code == 503
    readiness_log = next(
        record
        for record in caplog.records
        if getattr(record, "event", None) == "database_readiness_failed"
    )
    readiness_log_fields = cast(Any, readiness_log)
    assert readiness_log_fields.error_class == "OperationalError"
    assert readiness_log_fields.host == "localhost"
    assert "postgresql+psycopg://localhost:55432/opledger" not in caplog.text
