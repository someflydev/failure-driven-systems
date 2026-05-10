from collections.abc import Callable

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from opledger_api.models import CustomerWorkRequestStats
from opledger_api.read_models import rebuild_customer_work_request_stats

JsonObject = dict[str, object]


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
