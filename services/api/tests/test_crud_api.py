from collections.abc import Callable
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from opledger_api import routes
from opledger_api.models import ReportJob, WorkRequestStatusEvent

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
        "/reports/jobs?limit=0",
        "/reports/jobs?limit=101",
        "/reports/jobs?offset=-1",
        "/notification-attempts?limit=0",
        "/notification-attempts?limit=101",
        "/notification-attempts?offset=-1",
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


def test_work_request_summary_report_counts_existing_data(
    client: TestClient,
    create_customer: Callable[[str], JsonObject],
    create_work_request: Callable[[int, str, str], JsonObject],
) -> None:
    first_customer = create_customer("summary-one@example.com")
    second_customer = create_customer("summary-two@example.com")
    open_request = create_work_request(
        resource_id(first_customer), "open", "Inspect router"
    )
    create_work_request(resource_id(second_customer), "resolved", "Replace cable")
    status_response = client.patch(
        f"/work-requests/{open_request['id']}/status",
        json={"status": "in_progress", "reason": "Technician accepted dispatch."},
    )

    response = client.post("/reports/work-requests/summary")

    assert status_response.status_code == 200
    assert response.status_code == 200
    body = response.json()
    assert body["total_work_requests"] == 2
    assert body["by_status"] == {
        "open": 0,
        "in_progress": 1,
        "resolved": 1,
        "cancelled": 0,
    }
    assert body["status_event_count"] == 1
    assert body["generated_at"]


def test_work_request_summary_report_does_not_delay_by_default(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_sleep(_seconds: int) -> None:
        raise AssertionError("report delay should be disabled by default")

    monkeypatch.setattr(routes, "sleep", fail_sleep)

    response = client.post("/reports/work-requests/summary?delay_seconds=1")

    assert response.status_code == 200
    assert response.json()["total_work_requests"] == 0


def test_work_request_summary_report_job_can_be_enqueued_and_inspected(
    client: TestClient,
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_enqueue(report_job_id: int, _settings: object) -> str:
        return f"rq-job-{report_job_id}"

    monkeypatch.setattr(routes, "enqueue_work_request_summary_report", fake_enqueue)

    enqueue_response = client.post("/reports/work-requests/summary/jobs")

    assert enqueue_response.status_code == 202
    body = enqueue_response.json()
    assert body["id"] == 1
    assert body["report_type"] == "work_request_summary"
    assert body["status"] == "queued"
    assert body["redis_job_id"] == "rq-job-1"
    assert body["result_json"] is None
    assert body["attempt_count"] == 0
    assert body["last_error"] is None

    report_job = db_session.get(ReportJob, 1)
    assert report_job is not None
    assert report_job.status == "queued"
    assert report_job.redis_job_id == "rq-job-1"

    get_response = client.get("/reports/jobs/1")

    assert get_response.status_code == 200
    assert get_response.json()["redis_job_id"] == "rq-job-1"


def test_same_report_idempotency_key_returns_same_job(
    client: TestClient,
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    enqueue_calls: list[int] = []

    def fake_enqueue(report_job_id: int, _settings: object) -> str:
        enqueue_calls.append(report_job_id)
        return f"rq-job-{report_job_id}"

    monkeypatch.setattr(routes, "enqueue_work_request_summary_report", fake_enqueue)

    first_response = client.post(
        "/reports/work-requests/summary/jobs",
        headers={"Idempotency-Key": "summary-request-1"},
    )
    second_response = client.post(
        "/reports/work-requests/summary/jobs",
        headers={"Idempotency-Key": "summary-request-1"},
    )

    assert first_response.status_code == 202
    assert second_response.status_code == 202
    assert second_response.json() == first_response.json()
    assert enqueue_calls == [1]
    report_jobs = db_session.scalars(select(ReportJob)).all()
    assert len(report_jobs) == 1
    assert report_jobs[0].idempotency_key == "summary-request-1"


def test_different_report_idempotency_key_creates_new_job(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_enqueue(report_job_id: int, _settings: object) -> str:
        return f"rq-job-{report_job_id}"

    monkeypatch.setattr(routes, "enqueue_work_request_summary_report", fake_enqueue)

    first_response = client.post(
        "/reports/work-requests/summary/jobs",
        headers={"Idempotency-Key": "summary-request-1"},
    )
    second_response = client.post(
        "/reports/work-requests/summary/jobs",
        headers={"Idempotency-Key": "summary-request-2"},
    )

    assert first_response.status_code == 202
    assert second_response.status_code == 202
    assert first_response.json()["id"] == 1
    assert second_response.json()["id"] == 2
    assert first_response.json()["idempotency_key"] == "summary-request-1"
    assert second_response.json()["idempotency_key"] == "summary-request-2"


def test_report_job_idempotency_is_enforced_by_database(
    db_session: Session,
) -> None:
    first = ReportJob(
        report_type="work_request_summary",
        status="queued",
        idempotency_key="same-request",
    )
    duplicate = ReportJob(
        report_type="work_request_summary",
        status="queued",
        idempotency_key="same-request",
    )
    db_session.add(first)
    db_session.commit()

    db_session.add(duplicate)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_recent_report_jobs_are_listed_newest_first(
    client: TestClient,
    db_session: Session,
) -> None:
    first = ReportJob(report_type="work_request_summary", status="queued")
    second = ReportJob(report_type="work_request_summary", status="failed")
    db_session.add_all([first, second])
    db_session.commit()

    response = client.get("/reports/jobs?limit=10&offset=0")

    assert response.status_code == 200
    body = response.json()
    assert [item["id"] for item in body["items"]] == [2, 1]
    assert body["limit"] == 10
    assert body["offset"] == 0


def test_completed_report_output_can_be_fetched_when_durable_result_exists(
    client: TestClient,
    db_session: Session,
) -> None:
    generated_at = datetime.now(UTC).isoformat()
    report_job = ReportJob(
        report_type="work_request_summary",
        status="succeeded",
        result_json={
            "generated_at": generated_at,
            "total_work_requests": 3,
            "by_status": {
                "open": 1,
                "in_progress": 1,
                "resolved": 1,
                "cancelled": 0,
            },
            "status_event_count": 2,
        },
    )
    db_session.add(report_job)
    db_session.commit()

    response = client.get("/reports/jobs/1/result")

    assert response.status_code == 200
    body = response.json()
    assert datetime.fromisoformat(body["generated_at"].replace("Z", "+00:00"))
    assert body["total_work_requests"] == 3
    assert body["by_status"] == {
        "open": 1,
        "in_progress": 1,
        "resolved": 1,
        "cancelled": 0,
    }
    assert body["status_event_count"] == 2


def test_report_output_is_unavailable_until_succeeded_with_result(
    client: TestClient,
    db_session: Session,
) -> None:
    report_job = ReportJob(report_type="work_request_summary", status="running")
    db_session.add(report_job)
    db_session.commit()

    response = client.get("/reports/jobs/1/result")

    assert response.status_code == 409
    assert response.json()["error"] == {
        "code": "report_result_unavailable",
        "message": "Report result is not available yet.",
        "details": {"report_job_id": 1, "status": "running"},
    }


def test_report_queue_failure_is_persisted_and_reported(
    client: TestClient,
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_enqueue(_report_job_id: int, _settings: object) -> str:
        raise ConnectionError("redis unavailable")

    monkeypatch.setattr(routes, "enqueue_work_request_summary_report", fail_enqueue)

    response = client.post("/reports/work-requests/summary/jobs")

    assert response.status_code == 503
    assert response.json()["error"] == {
        "code": "report_queue_unavailable",
        "message": "Report queue is unavailable.",
        "details": {"report_job_id": 1},
    }
    report_job = db_session.get(ReportJob, 1)
    assert report_job is not None
    assert report_job.status == "failed"
    assert report_job.error_message == "ConnectionError"
    assert report_job.last_error == "ConnectionError"
    assert report_job.last_failed_at is not None


def test_failed_report_job_representation_includes_error(
    client: TestClient,
    db_session: Session,
) -> None:
    report_job = ReportJob(
        report_type="work_request_summary",
        status="failed",
        error_message="RuntimeError",
    )
    db_session.add(report_job)
    db_session.commit()

    response = client.get("/reports/jobs/1")

    assert response.status_code == 200
    assert response.json()["status"] == "failed"
    assert response.json()["error_message"] == "RuntimeError"
    assert response.json()["last_error"] is None
    assert response.json()["attempt_count"] == 0
    assert response.json()["result_json"] is None


def test_missing_report_job_returns_consistent_not_found(client: TestClient) -> None:
    response = client.get("/reports/jobs/999")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "report_job_not_found"
