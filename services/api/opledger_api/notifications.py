"""Notification boundary: durable side-effect attempts and local delivery adapter."""

import logging
from datetime import UTC, datetime

from fastapi import APIRouter, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from opledger_api.metrics import record_notification_attempt
from opledger_api.models import NotificationAttempt, ReportJob
from opledger_api.schemas import NotificationAttemptList
from opledger_api.shared import LimitQuery, OffsetQuery, SessionDependency

REPORT_COMPLETED_NOTIFICATION_RECIPIENT = "operator@example.com"
LOCAL_LOG_NOTIFICATION_CHANNEL = "local_log"
LOCAL_NOTIFICATION_FAILURE_RECIPIENT = "fail-notification@example.com"

router = APIRouter(tags=["opsledger"])
logger = logging.getLogger("opledger_api.notifications")


class LocalNotificationDeliveryError(RuntimeError):
    """Raised by the local adapter when deterministic failure is requested."""


class LocalNotificationAdapter:
    """Fake notification adapter that logs instead of calling an external provider."""

    def send(self, attempt: NotificationAttempt) -> None:
        if attempt.recipient == LOCAL_NOTIFICATION_FAILURE_RECIPIENT:
            raise LocalNotificationDeliveryError("Local notification send failed.")

        logger.info(
            "notification_sent",
            extra={
                "event": "notification_sent",
                "target_type": attempt.target_type,
                "target_id": attempt.target_id,
                "channel": attempt.channel,
                "recipient": attempt.recipient,
                "idempotency_key": attempt.idempotency_key,
            },
        )


def report_completed_notification_key(report_job_id: int) -> str:
    return f"report_job:{report_job_id}:completed"


def notify_report_completed(
    session: Session,
    report_job: ReportJob,
    recipient: str = REPORT_COMPLETED_NOTIFICATION_RECIPIENT,
    adapter: LocalNotificationAdapter | None = None,
) -> NotificationAttempt:
    idempotency_key = report_completed_notification_key(report_job.id)
    existing_attempt = session.scalar(
        select(NotificationAttempt).where(
            NotificationAttempt.idempotency_key == idempotency_key
        )
    )
    if existing_attempt is not None:
        return existing_attempt

    attempt = NotificationAttempt(
        target_type="report_job",
        target_id=report_job.id,
        channel=LOCAL_LOG_NOTIFICATION_CHANNEL,
        recipient=recipient,
        status="pending",
        idempotency_key=idempotency_key,
    )
    session.add(attempt)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        existing_attempt = session.scalar(
            select(NotificationAttempt).where(
                NotificationAttempt.idempotency_key == idempotency_key
            )
        )
        if existing_attempt is not None:
            return existing_attempt
        raise
    session.refresh(attempt)

    resolved_adapter = adapter or LocalNotificationAdapter()
    try:
        resolved_adapter.send(attempt)
    except Exception as exc:
        attempt.status = "failed"
        attempt.error = exc.__class__.__name__
        attempt.sent_at = None
        session.commit()
        session.refresh(attempt)
        logger.info(
            "notification_failed",
            extra={
                "event": "notification_failed",
                "target_type": attempt.target_type,
                "target_id": attempt.target_id,
                "channel": attempt.channel,
                "recipient": attempt.recipient,
                "idempotency_key": attempt.idempotency_key,
                "error": attempt.error,
            },
        )
        record_notification_attempt(attempt.channel, "failed")
        return attempt

    attempt.status = "sent"
    attempt.error = None
    attempt.sent_at = datetime.now(UTC)
    session.commit()
    session.refresh(attempt)
    record_notification_attempt(attempt.channel, "sent")
    return attempt


@router.get("/notification-attempts", response_model=NotificationAttemptList)
def list_notification_attempts(
    session: SessionDependency,
    target_type: str | None = Query(default=None, max_length=64),
    target_id: int | None = Query(default=None, gt=0),
    limit: LimitQuery = 20,
    offset: OffsetQuery = 0,
) -> dict[str, object]:
    statement = (
        select(NotificationAttempt)
        .order_by(NotificationAttempt.created_at.desc(), NotificationAttempt.id.desc())
        .limit(limit)
        .offset(offset)
    )
    if target_type is not None:
        statement = statement.where(NotificationAttempt.target_type == target_type)
    if target_id is not None:
        statement = statement.where(NotificationAttempt.target_id == target_id)

    attempts = session.scalars(statement).all()
    return {"items": attempts, "limit": limit, "offset": offset}
