from datetime import UTC, datetime

from redis import Redis
from rq import Queue
from sqlalchemy.orm import Session

from opledger_api.config import Settings, get_settings
from opledger_api.db import get_session
from opledger_api.models import ReportJob
from opledger_api.reports import build_work_request_summary_report

WORK_REQUEST_SUMMARY_REPORT = "work_request_summary"


def get_redis_connection(settings: Settings | None = None) -> Redis:
    resolved_settings = settings or get_settings()
    return Redis.from_url(resolved_settings.redis_url)


def get_report_queue(settings: Settings | None = None) -> Queue:
    resolved_settings = settings or get_settings()
    return Queue(
        name=resolved_settings.report_queue_name,
        connection=get_redis_connection(resolved_settings),
    )


def enqueue_work_request_summary_report(
    report_job_id: int,
    settings: Settings | None = None,
) -> str:
    queue = get_report_queue(settings)
    rq_job = queue.enqueue(
        generate_work_request_summary_report_job,
        report_job_id,
        retry=None,
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
    report_job.finished_at = now
    session.commit()


def report_result_json(report: dict[str, object]) -> dict[str, object]:
    result = dict(report)
    generated_at = result.get("generated_at")
    if isinstance(generated_at, datetime):
        result["generated_at"] = generated_at.isoformat()
    return result


def generate_work_request_summary_report_job(report_job_id: int) -> None:
    with get_session() as session:
        report_job = session.get(ReportJob, report_job_id)
        if report_job is None:
            raise RuntimeError(f"ReportJob {report_job_id} was not found.")

        report_job.status = "started"
        report_job.started_at = datetime.now(UTC)
        session.commit()

        try:
            report = build_work_request_summary_report(session)
            report_job.result_json = report_result_json(report)
            report_job.status = "finished"
            report_job.finished_at = datetime.now(UTC)
            report_job.error_message = None
            session.commit()
        except Exception as exc:
            mark_report_job_failed(report_job, session, exc.__class__.__name__)
            raise
