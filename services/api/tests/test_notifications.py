from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from opledger_api import report_jobs
from opledger_api.models import NotificationAttempt, ReportJob
from opledger_api.notifications import (
    LOCAL_NOTIFICATION_FAILURE_RECIPIENT,
    notify_report_completed,
    report_completed_notification_key,
)


def successful_report() -> dict[str, object]:
    return {
        "generated_at": datetime.now(UTC),
        "total_work_requests": 0,
        "by_status": {
            "open": 0,
            "in_progress": 0,
            "resolved": 0,
            "cancelled": 0,
        },
        "status_event_count": 0,
    }


def patch_report_job_session(
    monkeypatch: pytest.MonkeyPatch, db_session: Session
) -> None:
    @contextmanager
    def fake_get_session() -> Generator[Session]:
        yield db_session

    monkeypatch.setattr(report_jobs, "get_session", fake_get_session)


def test_report_completion_creates_sent_notification_attempt(
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report_job = ReportJob(report_type="work_request_summary", status="queued")
    db_session.add(report_job)
    db_session.commit()
    patch_report_job_session(monkeypatch, db_session)
    monkeypatch.setattr(
        report_jobs,
        "build_work_request_summary_report",
        lambda _session: successful_report(),
    )

    report_jobs.generate_work_request_summary_report_job(report_job.id)

    attempt = db_session.scalar(select(NotificationAttempt))
    assert attempt is not None
    assert attempt.target_type == "report_job"
    assert attempt.target_id == report_job.id
    assert attempt.channel == "local_log"
    assert attempt.recipient == "operator@example.com"
    assert attempt.status == "sent"
    assert attempt.idempotency_key == report_completed_notification_key(report_job.id)
    assert attempt.error is None
    assert attempt.sent_at is not None


def test_duplicate_notification_trigger_returns_existing_attempt(
    db_session: Session,
) -> None:
    report_job = ReportJob(report_type="work_request_summary", status="succeeded")
    db_session.add(report_job)
    db_session.commit()

    first_attempt = notify_report_completed(db_session, report_job)
    second_attempt = notify_report_completed(db_session, report_job)
    attempts = db_session.scalars(select(NotificationAttempt)).all()

    assert first_attempt.id == second_attempt.id
    assert len(attempts) == 1
    assert attempts[0].status == "sent"


def test_failed_local_notification_adapter_path_is_visible(
    db_session: Session,
) -> None:
    report_job = ReportJob(report_type="work_request_summary", status="succeeded")
    db_session.add(report_job)
    db_session.commit()

    attempt = notify_report_completed(
        db_session,
        report_job,
        recipient=LOCAL_NOTIFICATION_FAILURE_RECIPIENT,
    )

    assert attempt.status == "failed"
    assert attempt.error == "LocalNotificationDeliveryError"
    assert attempt.sent_at is None


def test_notification_attempts_are_visible_through_api(
    client: TestClient,
    db_session: Session,
) -> None:
    report_job = ReportJob(report_type="work_request_summary", status="succeeded")
    db_session.add(report_job)
    db_session.commit()
    attempt = notify_report_completed(db_session, report_job)

    response = client.get(
        f"/notification-attempts?target_type=report_job&target_id={report_job.id}"
    )

    assert response.status_code == 200
    assert response.json()["items"] == [
        {
            "id": attempt.id,
            "target_type": "report_job",
            "target_id": report_job.id,
            "channel": "local_log",
            "recipient": "operator@example.com",
            "status": "sent",
            "idempotency_key": report_completed_notification_key(report_job.id),
            "error": None,
            "created_at": response.json()["items"][0]["created_at"],
            "sent_at": response.json()["items"][0]["sent_at"],
        }
    ]
