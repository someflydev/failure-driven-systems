import logging
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from opledger_api.models import NotificationAttempt, ReportJob

REPORT_COMPLETED_NOTIFICATION_RECIPIENT = "operator@example.com"
LOCAL_LOG_NOTIFICATION_CHANNEL = "local_log"
LOCAL_NOTIFICATION_FAILURE_RECIPIENT = "fail-notification@example.com"

logger = logging.getLogger("opledger_api.notifications")


class LocalNotificationDeliveryError(RuntimeError):
    """Raised by the local adapter when deterministic failure is requested."""


class LocalNotificationAdapter:
    """Fake notification adapter that logs instead of calling an external provider."""

    def send(self, attempt: NotificationAttempt) -> None:
        if attempt.recipient == LOCAL_NOTIFICATION_FAILURE_RECIPIENT:
            raise LocalNotificationDeliveryError("Local notification send failed.")

        logger.info(
            "event=notification_sent target_type=%s target_id=%s channel=%s "
            "recipient=%s idempotency_key=%s",
            attempt.target_type,
            attempt.target_id,
            attempt.channel,
            attempt.recipient,
            attempt.idempotency_key,
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
            "event=notification_failed target_type=%s target_id=%s channel=%s "
            "recipient=%s idempotency_key=%s error=%s",
            attempt.target_type,
            attempt.target_id,
            attempt.channel,
            attempt.recipient,
            attempt.idempotency_key,
            attempt.error,
        )
        return attempt

    attempt.status = "sent"
    attempt.error = None
    attempt.sent_at = datetime.now(UTC)
    session.commit()
    session.refresh(attempt)
    return attempt
