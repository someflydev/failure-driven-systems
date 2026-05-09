"""Async job boundary: durable report job state and queue coordination."""

from datetime import UTC, datetime

from fastapi import APIRouter, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from opledger_api.models import ReportJob
from opledger_api.report_jobs import (
    WORK_REQUEST_SUMMARY_REPORT,
    enqueue_work_request_summary_report,
)
from opledger_api.schemas import (
    ErrorResponse,
    ReportJobList,
    ReportJobRead,
    WorkRequestSummaryReport,
)
from opledger_api.shared import (
    IdempotencyKeyHeader,
    LimitQuery,
    OffsetQuery,
    SessionDependency,
    SettingsDependency,
    error_response,
)

router = APIRouter(tags=["opsledger"])


@router.post(
    "/reports/work-requests/summary/jobs",
    response_model=ReportJobRead,
    status_code=status.HTTP_202_ACCEPTED,
    responses={503: {"model": ErrorResponse}},
)
def enqueue_work_request_summary_report_job(
    session: SessionDependency,
    settings: SettingsDependency,
    idempotency_key: IdempotencyKeyHeader = None,
) -> ReportJob:
    if idempotency_key is not None:
        existing_report_job = session.scalar(
            select(ReportJob).where(
                ReportJob.report_type == WORK_REQUEST_SUMMARY_REPORT,
                ReportJob.idempotency_key == idempotency_key,
            )
        )
        if existing_report_job is not None:
            return existing_report_job

    report_job = ReportJob(
        report_type=WORK_REQUEST_SUMMARY_REPORT,
        status="queued",
        idempotency_key=idempotency_key,
    )
    session.add(report_job)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        if idempotency_key is not None:
            existing_report_job = session.scalar(
                select(ReportJob).where(
                    ReportJob.report_type == WORK_REQUEST_SUMMARY_REPORT,
                    ReportJob.idempotency_key == idempotency_key,
                )
            )
            if existing_report_job is not None:
                return existing_report_job
        raise
    session.refresh(report_job)

    try:
        redis_job_id = enqueue_work_request_summary_report(report_job.id, settings)
    except Exception as exc:
        now = datetime.now(UTC)
        report_job.status = "failed"
        report_job.error_message = exc.__class__.__name__
        report_job.last_error = exc.__class__.__name__
        report_job.finished_at = now
        report_job.last_failed_at = now
        session.commit()
        raise error_response(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "report_queue_unavailable",
            "Report queue is unavailable.",
            {"report_job_id": report_job.id},
        ) from exc

    report_job.redis_job_id = redis_job_id
    session.commit()
    session.refresh(report_job)
    return report_job


@router.get(
    "/reports/jobs",
    response_model=ReportJobList,
)
def list_report_jobs(
    session: SessionDependency,
    limit: LimitQuery = 20,
    offset: OffsetQuery = 0,
) -> dict[str, object]:
    report_jobs = session.scalars(
        select(ReportJob)
        .order_by(ReportJob.created_at.desc(), ReportJob.id.desc())
        .limit(limit)
        .offset(offset)
    ).all()
    return {"items": report_jobs, "limit": limit, "offset": offset}


def get_report_job(report_job_id: int, session: SessionDependency) -> ReportJob:
    report_job = session.get(ReportJob, report_job_id)
    if report_job is None:
        raise error_response(
            status.HTTP_404_NOT_FOUND,
            "report_job_not_found",
            "Report job was not found.",
        )
    return report_job


@router.get(
    "/reports/jobs/{report_job_id}",
    response_model=ReportJobRead,
    responses={404: {"model": ErrorResponse}},
)
def get_report_job_status(report_job_id: int, session: SessionDependency) -> ReportJob:
    return get_report_job(report_job_id, session)


@router.get(
    "/reports/jobs/{report_job_id}/result",
    response_model=WorkRequestSummaryReport,
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
)
def get_report_job_result(
    report_job_id: int, session: SessionDependency
) -> dict[str, object]:
    report_job = get_report_job(report_job_id, session)
    if report_job.status != "succeeded" or report_job.result_json is None:
        raise error_response(
            status.HTTP_409_CONFLICT,
            "report_result_unavailable",
            "Report result is not available yet.",
            {"report_job_id": report_job.id, "status": report_job.status},
        )
    return report_job.result_json
