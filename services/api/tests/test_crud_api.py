from collections.abc import Generator
from typing import cast

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from opledger_api.db import Base, get_db_session
from opledger_api.main import create_app

JsonObject = dict[str, object]


@pytest.fixture()
def client() -> Generator[TestClient]:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(engine)

    app = create_app()

    def override_session() -> Generator[Session]:
        with SessionLocal() as session:
            yield session

    app.dependency_overrides[get_db_session] = override_session

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(engine)


def create_customer(
    client: TestClient, email: str = "ops@example.com"
) -> dict[str, object]:
    response = client.post(
        "/customers",
        json={"name": "Acme Operations", "email": email},
    )
    assert response.status_code == 201
    return cast(JsonObject, response.json())


def create_work_request(
    client: TestClient,
    customer_id: int,
    status: str = "open",
) -> dict[str, object]:
    response = client.post(
        "/work-requests",
        json={
            "customer_id": customer_id,
            "title": "Replace scanner",
            "description": "Warehouse scanner stopped booting.",
            "status": status,
        },
    )
    assert response.status_code == 201
    return cast(JsonObject, response.json())


def resource_id(resource: JsonObject) -> int:
    value = resource["id"]
    assert isinstance(value, int)
    return value


def test_customer_create_get_and_list(client: TestClient) -> None:
    created = create_customer(client)

    get_response = client.get(f"/customers/{created['id']}")
    list_response = client.get("/customers?limit=10&offset=0")

    assert get_response.status_code == 200
    assert get_response.json()["email"] == "ops@example.com"
    assert list_response.status_code == 200
    assert list_response.json()["items"] == [get_response.json()]
    assert list_response.json()["limit"] == 10
    assert list_response.json()["offset"] == 0


def test_duplicate_customer_email_returns_conflict(client: TestClient) -> None:
    create_customer(client)

    response = client.post(
        "/customers",
        json={"name": "Duplicate Acme", "email": "ops@example.com"},
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "duplicate_customer_email"


def test_customer_not_found_uses_consistent_error_shape(client: TestClient) -> None:
    response = client.get("/customers/999")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "customer_not_found",
            "message": "Customer was not found.",
            "details": None,
        }
    }


def test_validation_failure_uses_consistent_error_shape(client: TestClient) -> None:
    response = client.post(
        "/customers",
        json={"name": "", "email": "not-an-email"},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_failed"
    assert response.json()["error"]["details"]


def test_work_request_create_get_list_filter_and_status_update(
    client: TestClient,
) -> None:
    customer = create_customer(client)
    work_request = create_work_request(client, resource_id(customer))

    get_response = client.get(f"/work-requests/{work_request['id']}")
    list_response = client.get("/work-requests?status=open&limit=5&offset=0")
    update_response = client.patch(
        f"/work-requests/{work_request['id']}/status",
        json={"status": "in_progress"},
    )

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Replace scanner"
    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.json()["items"]] == [
        work_request["id"]
    ]
    assert list_response.json()["limit"] == 5
    assert list_response.json()["offset"] == 0
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "in_progress"


def test_work_request_requires_existing_customer(client: TestClient) -> None:
    response = client.post(
        "/work-requests",
        json={
            "customer_id": 999,
            "title": "Replace scanner",
            "description": "Warehouse scanner stopped booting.",
        },
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "customer_not_found"


def test_terminal_status_cannot_transition(client: TestClient) -> None:
    customer = create_customer(client)
    work_request = create_work_request(client, resource_id(customer), status="resolved")

    response = client.patch(
        f"/work-requests/{work_request['id']}/status",
        json={"status": "open"},
    )

    assert response.status_code == 409
    assert response.json()["error"] == {
        "code": "invalid_status_transition",
        "message": "Resolved or cancelled work requests cannot change status.",
        "details": {"from": "resolved", "to": "open"},
    }
