import logging
from datetime import UTC, datetime
from time import perf_counter

from redis import Redis
from rq import Queue, Retry
from sqlalchemy.orm import Session

from opledger_api.config import Settings, get_settings
from opledger_api.db import get_session
from opledger_api.logging import configure_logging, set_log_context
from opledger_api.metrics import (
    record_report_job_completed,
    record_worker_job_failure,
)
from opledger_api.models import ReportJob
from opledger_api.notifications import notify_report_completed
from opledger_api.report_contracts import (
    WorkRequestSummaryRenderRequest,
    WorkRequestSummaryReport,
)
from opledger_api.report_renderer import (
    render_work_request_summary_report as render_work_request_summary_report_local,
)
from opledger_api.reporting_client import (
    ReportingServiceError,
    render_work_request_summary_report_remote,
)
from opledger_api.reports import (
    build_work_request_summary_render_request,
)

LOCAL_FAILURE_INJECTION_ENVIRONMENTS = {"local", "test"}
logger = logging.getLogger("opledger_api.worker")


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


def report_result_json(report: WorkRequestSummaryReport) -> dict[str, object]:
    return report.model_dump(mode="json")


def report_failure_message(exc: Exception) -> str:
    if isinstance(exc, ReportingServiceError):
        return str(exc)
    return exc.__class__.__name__


def render_work_request_summary_report(
    request: WorkRequestSummaryRenderRequest,
    correlation_id: str | None = None,
) -> WorkRequestSummaryReport:
    settings = get_settings()
    if settings.report_rendering_service_url:
        return render_work_request_summary_report_remote(
            request,
            base_url=settings.report_rendering_service_url,
            timeout_seconds=settings.report_rendering_service_timeout_seconds,
            correlation_id=correlation_id,
        )
    return render_work_request_summary_report_local(request)


def maybe_inject_report_failure(settings: Settings, stage: str) -> None:
    if not settings.report_failure_injection_enabled:
        return
    if settings.environment not in LOCAL_FAILURE_INJECTION_ENVIRONMENTS:
        return
    if settings.report_failure_injection_stage == stage:
        raise InjectedReportFailure(f"Injected report failure at {stage}.")


def generate_work_request_summary_report_job(report_job_id: int) -> None:
    settings = get_settings()
    configure_logging(service="opledger-worker", environment=settings.environment)
    with get_session() as session:
        report_job = session.get(ReportJob, report_job_id)
        if report_job is None:
            raise RuntimeError(f"ReportJob {report_job_id} was not found.")
        set_log_context(
            service="opledger-worker",
            environment=settings.environment,
            request_id=None,
            correlation_id=report_job.correlation_id,
        )
        try:
            if report_job.status == "succeeded" and report_job.result_json is not None:
                logger.info(
                    "report_job_duplicate_completed",
                    extra={
                        "event": "report_job_duplicate_completed",
                        "job_id": report_job.id,
                        "redis_job_id": report_job.redis_job_id,
                        "status": report_job.status,
                    },
                )
                return

            started_at = perf_counter()
            report_job.status = "running"
            report_job.attempt_count += 1
            report_job.started_at = datetime.now(UTC)
            report_job.finished_at = None
            session.commit()
            logger.info(
                "report_job_started",
                extra={
                    "event": "report_job_started",
                    "job_id": report_job.id,
                    "redis_job_id": report_job.redis_job_id,
                    "attempt_count": report_job.attempt_count,
                    "status": report_job.status,
                },
            )

            try:
                maybe_inject_report_failure(settings, "before_generation")
                render_request = build_work_request_summary_render_request(session)
                report = render_work_request_summary_report(
                    render_request,
                    correlation_id=report_job.correlation_id,
                )
                maybe_inject_report_failure(settings, "after_partial_progress")
                report_job.result_json = report_result_json(report)
                report_job.status = "succeeded"
                report_job.finished_at = datetime.now(UTC)
                report_job.error_message = None
                report_job.last_error = None
                session.commit()
            except Exception as exc:
                mark_report_job_failed(report_job, session, report_failure_message(exc))
                record_report_job_completed(report_job.report_type, "failed")
                record_worker_job_failure(
                    report_job.report_type, exc.__class__.__name__
                )
                duration_ms = (perf_counter() - started_at) * 1000
                logger.warning(
                    "report_job_failed",
                    extra={
                        "event": "report_job_failed",
                        "job_id": report_job.id,
                        "redis_job_id": report_job.redis_job_id,
                        "attempt_count": report_job.attempt_count,
                        "status": report_job.status,
                        "duration_ms": round(duration_ms, 2),
                        "error_class": exc.__class__.__name__,
                    },
                )
                raise

            duration_ms = (perf_counter() - started_at) * 1000
            logger.info(
                "report_job_succeeded",
                extra={
                    "event": "report_job_succeeded",
                    "job_id": report_job.id,
                    "redis_job_id": report_job.redis_job_id,
                    "attempt_count": report_job.attempt_count,
                    "status": report_job.status,
                    "duration_ms": round(duration_ms, 2),
                },
            )
            record_report_job_completed(report_job.report_type, "succeeded")
            notify_report_completed(session, report_job)
        finally:
            set_log_context(
                service="opledger-worker",
                environment=settings.environment,
                request_id=None,
                correlation_id=None,
            )
