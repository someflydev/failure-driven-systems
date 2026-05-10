from collections.abc import Callable
from typing import cast

import pytest
from fastapi.testclient import TestClient
from redis.exceptions import RedisError
from sqlalchemy import select
from sqlalchemy.orm import Session

from opledger_api import read_models
from opledger_api.config import get_settings
from opledger_api.metrics import metrics_registry
from opledger_api.models import CustomerWorkRequestStats
from opledger_api.read_models import rebuild_customer_work_request_stats

JsonObject = dict[str, object]


class FakeRedisCache:
    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.ttls: dict[str, int] = {}
        self.get_calls = 0
        self.setex_calls = 0
        self.delete_calls = 0
        self.fail_get = False

    def get(self, name: str) -> str | None:
        self.get_calls += 1
        if self.fail_get:
            raise RedisError("redis unavailable")
        return self.values.get(name)

    def setex(self, name: str, time: int, value: str) -> object:
        self.setex_calls += 1
        self.values[name] = value
        self.ttls[name] = time
        return True

    def delete(self, *names: str) -> int:
        self.delete_calls += 1
        deleted = 0
        for name in names:
            if name in self.values:
                deleted += 1
            self.values.pop(name, None)
            self.ttls.pop(name, None)
        return deleted

    def scan_iter(self, match: str) -> object:
        prefix = match.removesuffix("*")
        return iter(key for key in self.values if key.startswith(prefix))


def resource_id(resource: JsonObject) -> int:
    value = resource["id"]
    assert isinstance(value, int)
    return value


def test_customer_work_request_stats_can_be_rebuilt_from_source_data(
    client: TestClient,
    db_session: Session,
    create_customer: Callable[[str], JsonObject],
    create_work_request: Callable[[int, str, str], JsonObject],
) -> None:
    first_customer = create_customer("read-model-one@example.com")
    second_customer = create_customer("read-model-two@example.com")
    open_request = create_work_request(
        resource_id(first_customer), "open", "Inspect router"
    )
    create_work_request(resource_id(first_customer), "resolved", "Replace cable")
    create_work_request(resource_id(second_customer), "cancelled", "Retire scanner")

    status_response = client.patch(
        f"/work-requests/{open_request['id']}/status",
        json={"status": "in_progress", "reason": "Technician accepted dispatch."},
    )

    assert status_response.status_code == 200

    rebuilt_rows = rebuild_customer_work_request_stats(db_session)
    response = client.get("/dashboard/customer-work-request-stats?limit=10&offset=0")

    assert len(rebuilt_rows) == 2
    assert response.status_code == 200
    body = response.json()
    assert body["limit"] == 10
    assert body["offset"] == 0
    assert body["items"] == [
        {
            "customer_id": first_customer["id"],
            "customer_name": first_customer["name"],
            "customer_email": first_customer["email"],
            "total_work_requests": 2,
            "open_count": 0,
            "in_progress_count": 1,
            "resolved_count": 1,
            "cancelled_count": 0,
            "status_event_count": 1,
            "rebuilt_at": body["items"][0]["rebuilt_at"],
        },
        {
            "customer_id": second_customer["id"],
            "customer_name": second_customer["name"],
            "customer_email": second_customer["email"],
            "total_work_requests": 1,
            "open_count": 0,
            "in_progress_count": 0,
            "resolved_count": 0,
            "cancelled_count": 1,
            "status_event_count": 0,
            "rebuilt_at": body["items"][1]["rebuilt_at"],
        },
    ]


def test_customer_work_request_stats_can_be_stale_before_rebuild(
    client: TestClient,
    db_session: Session,
    create_customer: Callable[[], JsonObject],
    create_work_request: Callable[[int, str, str], JsonObject],
) -> None:
    customer = create_customer()
    first_request = create_work_request(resource_id(customer), "open", "First work")
    rebuild_customer_work_request_stats(db_session)

    create_work_request(resource_id(customer), "resolved", "Second work")
    stale_response = client.get("/dashboard/customer-work-request-stats")
    source_response = client.get("/work-requests?limit=10&offset=0")
    first_request_response = client.get(f"/work-requests/{first_request['id']}")

    assert stale_response.status_code == 200
    assert stale_response.json()["items"][0]["total_work_requests"] == 1
    assert source_response.status_code == 200
    assert len(source_response.json()["items"]) == 2
    assert first_request_response.status_code == 200
    assert first_request_response.json()["status"] == "open"

    rebuild_customer_work_request_stats(db_session)
    fresh_response = client.get("/dashboard/customer-work-request-stats")

    assert fresh_response.status_code == 200
    assert fresh_response.json()["items"][0]["total_work_requests"] == 2
    assert fresh_response.json()["items"][0]["resolved_count"] == 1


def test_customer_work_request_stats_cache_hit_uses_redis_payload(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    metrics_registry.reset()
    fake_redis = FakeRedisCache()
    cache_key = read_models.customer_stats_cache_key(50, 0)
    fake_redis.values[cache_key] = (
        '{"items":[{"customer_id":1,"customer_name":"Cached Customer",'
        '"customer_email":"cached@example.com","total_work_requests":99,'
        '"open_count":99,"in_progress_count":0,"resolved_count":0,'
        '"cancelled_count":0,"status_event_count":0,'
        '"rebuilt_at":"2026-01-01T00:00:00Z"}],"limit":50,"offset":0}'
    )
    monkeypatch.setattr(
        read_models, "get_redis_connection", lambda _settings: fake_redis
    )

    response = client.get("/dashboard/customer-work-request-stats")

    assert response.status_code == 200
    assert response.json()["items"][0]["customer_name"] == "Cached Customer"
    assert fake_redis.get_calls == 1
    assert fake_redis.setex_calls == 0
    assert (
        'opledger_cache_access_total{endpoint="dashboard_customer_work_request_stats",'
        'outcome="hit"} 1'
    ) in metrics_registry.render()


def test_customer_work_request_stats_cache_miss_writes_with_ttl(
    client: TestClient,
    db_session: Session,
    create_customer: Callable[[], JsonObject],
    create_work_request: Callable[[int, str, str], JsonObject],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_redis = FakeRedisCache()
    monkeypatch.setattr(
        read_models, "get_redis_connection", lambda _settings: fake_redis
    )
    customer = create_customer()
    create_work_request(resource_id(customer), "open", "Cached miss")
    rebuild_customer_work_request_stats(db_session)

    response = client.get("/dashboard/customer-work-request-stats")

    cache_key = read_models.customer_stats_cache_key(50, 0)
    ttl_seconds = get_settings().dashboard_customer_work_request_stats_cache_ttl_seconds
    assert response.status_code == 200
    assert response.json()["items"][0]["total_work_requests"] == 1
    assert fake_redis.get_calls == 1
    assert fake_redis.setex_calls == 1
    assert fake_redis.ttls[cache_key] == ttl_seconds


def test_customer_work_request_stats_cache_can_be_bypassed(
    client: TestClient,
    db_session: Session,
    create_customer: Callable[[str, str], JsonObject],
    create_work_request: Callable[[int, str, str], JsonObject],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_redis = FakeRedisCache()
    cache_key = read_models.customer_stats_cache_key(50, 0)
    monkeypatch.setattr(
        read_models, "get_redis_connection", lambda _settings: fake_redis
    )
    customer = create_customer("fresh@example.com", "Fresh Customer")
    create_work_request(resource_id(customer), "open", "Fresh source")
    rebuild_customer_work_request_stats(db_session)
    fake_redis.values[cache_key] = (
        '{"items":[{"customer_id":1,"customer_name":"Stale Cached Customer",'
        '"customer_email":"stale@example.com","total_work_requests":10,'
        '"open_count":10,"in_progress_count":0,"resolved_count":0,'
        '"cancelled_count":0,"status_event_count":0,'
        '"rebuilt_at":"2026-01-01T00:00:00Z"}],"limit":50,"offset":0}'
    )

    response = client.get("/dashboard/customer-work-request-stats?bypass_cache=true")

    assert response.status_code == 200
    assert response.json()["items"][0]["customer_name"] == "Fresh Customer"
    assert fake_redis.get_calls == 0


def test_customer_work_request_stats_cache_can_be_stale_before_ttl_or_rebuild(
    client: TestClient,
    db_session: Session,
    create_customer: Callable[[], JsonObject],
    create_work_request: Callable[[int, str, str], JsonObject],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_redis = FakeRedisCache()
    monkeypatch.setattr(
        read_models, "get_redis_connection", lambda _settings: fake_redis
    )
    customer = create_customer()
    create_work_request(resource_id(customer), "open", "First cached work")
    rebuild_customer_work_request_stats(db_session)
    cached_response = client.get("/dashboard/customer-work-request-stats")

    create_work_request(resource_id(customer), "resolved", "Second source work")
    stale_response = client.get("/dashboard/customer-work-request-stats")
    source_response = client.get("/work-requests?limit=10&offset=0")
    bypass_response = client.get(
        "/dashboard/customer-work-request-stats?bypass_cache=true"
    )

    assert cached_response.status_code == 200
    assert stale_response.status_code == 200
    assert stale_response.json()["items"][0]["total_work_requests"] == 1
    assert source_response.status_code == 200
    assert len(source_response.json()["items"]) == 2
    assert bypass_response.status_code == 200
    assert bypass_response.json()["items"][0]["total_work_requests"] == 1


def test_customer_work_request_stats_rebuild_invalidates_cache(
    client: TestClient,
    db_session: Session,
    create_customer: Callable[[], JsonObject],
    create_work_request: Callable[[int, str, str], JsonObject],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_redis = FakeRedisCache()
    monkeypatch.setattr(
        read_models, "get_redis_connection", lambda _settings: fake_redis
    )
    customer = create_customer()
    create_work_request(resource_id(customer), "open", "Initial source work")
    rebuild_customer_work_request_stats(db_session)
    first_response = client.get("/dashboard/customer-work-request-stats")

    create_work_request(resource_id(customer), "resolved", "Fresh source work")
    rebuild_customer_work_request_stats(db_session)
    fresh_response = client.get("/dashboard/customer-work-request-stats")

    assert first_response.status_code == 200
    assert first_response.json()["items"][0]["total_work_requests"] == 1
    assert fake_redis.delete_calls >= 1
    assert fresh_response.status_code == 200
    assert fresh_response.json()["items"][0]["total_work_requests"] == 2


def test_customer_work_request_stats_redis_outage_falls_back_to_read_model(
    client: TestClient,
    db_session: Session,
    create_customer: Callable[[], JsonObject],
    create_work_request: Callable[[int, str, str], JsonObject],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_redis = FakeRedisCache()
    fake_redis.fail_get = True
    monkeypatch.setattr(
        read_models, "get_redis_connection", lambda _settings: fake_redis
    )
    customer = create_customer()
    create_work_request(resource_id(customer), "open", "Outage fallback")
    rebuild_customer_work_request_stats(db_session)

    response = client.get("/dashboard/customer-work-request-stats")
    stats_row = db_session.scalar(select(CustomerWorkRequestStats))

    assert response.status_code == 200
    assert response.json()["items"][0]["total_work_requests"] == 1
    assert cast(CustomerWorkRequestStats, stats_row).total_work_requests == 1


def test_rebuild_replaces_previous_customer_work_request_stats(
    client: TestClient,
    db_session: Session,
    create_customer: Callable[[], JsonObject],
    create_work_request: Callable[[int, str, str], JsonObject],
) -> None:
    customer = create_customer()
    work_request = create_work_request(resource_id(customer), "open", "First work")
    rebuild_customer_work_request_stats(db_session)

    update_response = client.patch(
        f"/work-requests/{work_request['id']}/status",
        json={"status": "resolved", "reason": "Work completed."},
    )
    rebuild_customer_work_request_stats(db_session)

    assert update_response.status_code == 200
    rows = db_session.scalars(select(CustomerWorkRequestStats)).all()
    assert len(rows) == 1
    assert rows[0].total_work_requests == 1
    assert rows[0].open_count == 0
    assert rows[0].resolved_count == 1
    assert rows[0].status_event_count == 1
