from collections.abc import Callable

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from opledger_api.models import WorkRequestStatusEvent

JsonObject = dict[str, object]


def resource_id(resource: JsonObject) -> int:
    value = resource["id"]
    assert isinstance(value, int)
    return value


def test_customer_create_get_and_list(
    client: TestClient,
    create_customer: Callable[[], JsonObject],
) -> None:
    created = create_customer()

    get_response = client.get(f"/customers/{created['id']}")
    list_response = client.get("/customers?limit=10&offset=0")

    assert get_response.status_code == 200
    assert get_response.json()["email"] == "ops@example.com"
    assert list_response.status_code == 200
    assert list_response.json()["items"] == [get_response.json()]
    assert list_response.json()["limit"] == 10
    assert list_response.json()["offset"] == 0


def test_duplicate_customer_email_returns_conflict(
    client: TestClient,
    create_customer: Callable[[], JsonObject],
) -> None:
    create_customer()

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
    create_customer: Callable[[], JsonObject],
    create_work_request: Callable[[int], JsonObject],
) -> None:
    customer = create_customer()
    work_request = create_work_request(resource_id(customer))

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


def test_status_filter_returns_only_matching_work_requests(
    client: TestClient,
    create_customer: Callable[[str], JsonObject],
    create_work_request: Callable[[int, str, str], JsonObject],
) -> None:
    first_customer = create_customer("ops-one@example.com")
    second_customer = create_customer("ops-two@example.com")
    open_request = create_work_request(resource_id(first_customer), "open", "Open work")
    in_progress_request = create_work_request(
        resource_id(second_customer), "in_progress", "Active work"
    )

    open_response = client.get("/work-requests?status=open&limit=10&offset=0")
    active_response = client.get("/work-requests?status=in_progress&limit=10&offset=0")

    assert open_response.status_code == 200
    assert active_response.status_code == 200
    assert [item["id"] for item in open_response.json()["items"]] == [
        open_request["id"]
    ]
    assert [item["id"] for item in active_response.json()["items"]] == [
        in_progress_request["id"]
    ]


def test_list_endpoints_reject_pagination_out_of_bounds(
    client: TestClient,
    create_customer: Callable[[], JsonObject],
    create_work_request: Callable[[int], JsonObject],
) -> None:
    customer = create_customer()
    work_request = create_work_request(resource_id(customer))

    paths = [
        "/customers?limit=0",
        "/customers?limit=101",
        "/customers?offset=-1",
        "/work-requests?limit=0",
        "/work-requests?limit=101",
        "/work-requests?offset=-1",
        f"/work-requests/{work_request['id']}/status-events?limit=0",
        f"/work-requests/{work_request['id']}/status-events?limit=101",
        f"/work-requests/{work_request['id']}/status-events?offset=-1",
    ]

    for path in paths:
        response = client.get(path)
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "validation_failed"


def test_status_update_creates_status_event(
    client: TestClient,
    create_customer: Callable[[], JsonObject],
    create_work_request: Callable[[int], JsonObject],
) -> None:
    customer = create_customer()
    work_request = create_work_request(resource_id(customer))

    update_response = client.patch(
        f"/work-requests/{work_request['id']}/status",
        json={"status": "in_progress", "reason": "Technician started work."},
    )
    events_response = client.get(f"/work-requests/{work_request['id']}/status-events")

    assert update_response.status_code == 200
    assert events_response.status_code == 200
    assert events_response.json()["items"] == [
        {
            "id": 1,
            "work_request_id": work_request["id"],
            "old_status": "open",
            "new_status": "in_progress",
            "reason": "Technician started work.",
            "created_at": events_response.json()["items"][0]["created_at"],
        }
    ]


def test_status_update_for_missing_work_request_fails_cleanly(
    client: TestClient,
) -> None:
    response = client.patch(
        "/work-requests/999/status",
        json={"status": "in_progress", "reason": "Technician started work."},
    )

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "work_request_not_found",
            "message": "Work request was not found.",
            "details": None,
        }
    }


def test_status_event_list_for_missing_work_request_fails_cleanly(
    client: TestClient,
) -> None:
    response = client.get("/work-requests/999/status-events")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "work_request_not_found"


def test_missing_work_request_status_update_does_not_create_orphan_events(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.patch(
        "/work-requests/999/status",
        json={"status": "in_progress", "reason": "Technician started work."},
    )
    status_events = db_session.scalars(select(WorkRequestStatusEvent)).all()

    assert response.status_code == 404
    assert status_events == []


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


def test_terminal_status_cannot_transition(
    client: TestClient,
    create_customer: Callable[[], JsonObject],
    create_work_request: Callable[[int, str], JsonObject],
) -> None:
    customer = create_customer()
    work_request = create_work_request(resource_id(customer), "resolved")

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
