from collections.abc import Callable, Generator
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
def db_sessionmaker() -> Generator[sessionmaker[Session]]:
    """Create one isolated in-memory database per test."""
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(engine)

    try:
        yield SessionLocal
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture()
def db_session(db_sessionmaker: sessionmaker[Session]) -> Generator[Session]:
    """Expose the test database for assertions that cannot be made through HTTP."""
    with db_sessionmaker() as session:
        yield session


@pytest.fixture()
def client(db_sessionmaker: sessionmaker[Session]) -> Generator[TestClient]:
    """Run the FastAPI app against the isolated test database."""
    app = create_app()

    def override_session() -> Generator[Session]:
        with db_sessionmaker() as session:
            yield session

    app.dependency_overrides[get_db_session] = override_session

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def create_customer(client: TestClient) -> Callable[[str, str], JsonObject]:
    """Seed a customer through the API so tests use production validation paths."""

    def _create_customer(
        email: str = "ops@example.com",
        name: str = "Acme Operations",
    ) -> JsonObject:
        response = client.post("/customers", json={"name": name, "email": email})
        assert response.status_code == 201
        return cast(JsonObject, response.json())

    return _create_customer


@pytest.fixture()
def create_work_request(
    client: TestClient,
) -> Callable[[int, str, str], JsonObject]:
    """Seed a work request through the API so database and schema rules both run."""

    def _create_work_request(
        customer_id: int,
        status: str = "open",
        title: str = "Replace scanner",
    ) -> JsonObject:
        response = client.post(
            "/work-requests",
            json={
                "customer_id": customer_id,
                "title": title,
                "description": "Warehouse scanner stopped booting.",
                "status": status,
            },
        )
        assert response.status_code == 201
        return cast(JsonObject, response.json())

    return _create_work_request


def resource_id(resource: JsonObject) -> int:
    value = resource["id"]
    assert isinstance(value, int)
    return value
