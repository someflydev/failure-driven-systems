from datetime import UTC, datetime

from redis import Redis
from rq import Queue, Retry
from sqlalchemy.orm import Session

from opledger_api.config import Settings, get_settings
from opledger_api.db import get_session
from opledger_api.models import ReportJob
from opledger_api.reports import build_work_request_summary_report

WORK_REQUEST_SUMMARY_REPORT = "work_request_summary"
LOCAL_FAILURE_INJECTION_ENVIRONMENTS = {"local", "test"}


class InjectedReportFailure(RuntimeError):
    """Raised only when local/test report failure injection is enabled."""


def get_redis_connection(settings: Settings | None = None) -> Redis:
    resolved_settings = settings or get_settings()
    return Redis.from_url(resolved_settings.redis_url)


def get_report_queue(settings: Settings | None = None) -> Queue:
    resolved_settings = settings or get_settings()
    return Queue(
        name=resolved_settings.report_queue_name,
        connection=get_redis_connection(resolved_settings),
    )


def report_retry_backoff_seconds(settings: Settings) -> list[int]:
    backoff_seconds: list[int] = []
    for raw_value in settings.report_job_retry_backoff_seconds.split(","):
        value = raw_value.strip()
        if value == "":
            continue
        parsed_value = int(value)
        if parsed_value < 0:
            raise ValueError("Report retry backoff seconds cannot be negative.")
        backoff_seconds.append(parsed_value)
    return backoff_seconds


def report_retry(settings: Settings) -> Retry:
    return Retry(
        max=settings.report_job_max_attempts - 1,
        interval=report_retry_backoff_seconds(settings),
    )


def enqueue_work_request_summary_report(
    report_job_id: int,
    settings: Settings | None = None,
) -> str:
    resolved_settings = settings or get_settings()
    queue = get_report_queue(resolved_settings)
    rq_job = queue.enqueue(
        generate_work_request_summary_report_job,
        report_job_id,
        retry=report_retry(resolved_settings),
    )
    return str(rq_job.id)


def mark_report_job_failed(
    report_job: ReportJob,
    session: Session,
    error_message: str,
) -> None:
    now = datetime.now(UTC)
    report_job.status = "failed"
    report_job.error_message = error_message
    report_job.last_error = error_message
    report_job.last_failed_at = now
    report_job.finished_at = now
    session.commit()


def report_result_json(report: dict[str, object]) -> dict[str, object]:
    result = dict(report)
    generated_at = result.get("generated_at")
    if isinstance(generated_at, datetime):
        result["generated_at"] = generated_at.isoformat()
    return result


def maybe_inject_report_failure(settings: Settings, stage: str) -> None:
    if not settings.report_failure_injection_enabled:
        return
    if settings.environment not in LOCAL_FAILURE_INJECTION_ENVIRONMENTS:
        return
    if settings.report_failure_injection_stage == stage:
        raise InjectedReportFailure(f"Injected report failure at {stage}.")


def generate_work_request_summary_report_job(report_job_id: int) -> None:
    settings = get_settings()
    with get_session() as session:
        report_job = session.get(ReportJob, report_job_id)
        if report_job is None:
            raise RuntimeError(f"ReportJob {report_job_id} was not found.")

        report_job.status = "running"
        report_job.attempt_count += 1
        report_job.started_at = datetime.now(UTC)
        report_job.finished_at = None
        session.commit()

        try:
            maybe_inject_report_failure(settings, "before_generation")
            report = build_work_request_summary_report(session)
            maybe_inject_report_failure(settings, "after_partial_progress")
            report_job.result_json = report_result_json(report)
            report_job.status = "succeeded"
            report_job.finished_at = datetime.now(UTC)
            report_job.error_message = None
            report_job.last_error = None
            session.commit()
        except Exception as exc:
            mark_report_job_failed(report_job, session, exc.__class__.__name__)
            raise
