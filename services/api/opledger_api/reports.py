"""Reports boundary: pure report rendering over existing source-of-truth data."""

from datetime import UTC, datetime
from time import sleep

from fastapi import APIRouter, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from opledger_api.models import (
    WORK_REQUEST_STATUSES,
    WorkRequest,
    WorkRequestStatusEvent,
)
from opledger_api.schemas import WorkRequestSummaryReport
from opledger_api.shared import SessionDependency, SettingsDependency

router = APIRouter(tags=["opsledger"])


def build_work_request_summary_report(session: Session) -> dict[str, object]:
    total_work_requests = session.scalar(select(func.count(WorkRequest.id))) or 0
    status_counts = dict.fromkeys(WORK_REQUEST_STATUSES, 0)
    status_rows = session.execute(
        select(WorkRequest.status, func.count(WorkRequest.id)).group_by(
            WorkRequest.status
        )
    ).all()
    for status_value, count in status_rows:
        status_counts[status_value] = count

    status_event_count = (
        session.scalar(select(func.count(WorkRequestStatusEvent.id))) or 0
    )

    return {
        "generated_at": datetime.now(UTC),
        "total_work_requests": total_work_requests,
        "by_status": status_counts,
        "status_event_count": status_event_count,
    }


@router.post(
    "/reports/work-requests/summary",
    response_model=WorkRequestSummaryReport,
)
def create_work_request_summary_report(
    session: SessionDependency,
    settings: SettingsDependency,
    delay_seconds: int = Query(default=0, ge=0, le=30),
) -> dict[str, object]:
    if settings.report_delay_enabled and delay_seconds > 0:
        sleep(min(delay_seconds, settings.report_max_delay_seconds))

    return build_work_request_summary_report(session)
