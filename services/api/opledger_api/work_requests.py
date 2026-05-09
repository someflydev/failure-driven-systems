"""Work request boundary: workflow state and status history ownership."""

from typing import Annotated

from fastapi import APIRouter, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from opledger_api.customers import get_customer_or_404
from opledger_api.models import WorkRequest, WorkRequestStatusEvent
from opledger_api.schemas import (
    ErrorResponse,
    WorkRequestCreate,
    WorkRequestList,
    WorkRequestRead,
    WorkRequestStatus,
    WorkRequestStatusEventList,
    WorkRequestStatusUpdate,
)
from opledger_api.shared import (
    LimitQuery,
    OffsetQuery,
    SessionDependency,
    error_response,
)

router = APIRouter(tags=["opsledger"])

TERMINAL_WORK_REQUEST_STATUSES: set[WorkRequestStatus] = {"resolved", "cancelled"}


def get_work_request_or_404(work_request_id: int, session: Session) -> WorkRequest:
    work_request = session.get(WorkRequest, work_request_id)
    if work_request is None:
        raise error_response(
            status.HTTP_404_NOT_FOUND,
            "work_request_not_found",
            "Work request was not found.",
        )
    return work_request


@router.post(
    "/work-requests",
    response_model=WorkRequestRead,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"model": ErrorResponse}},
)
def create_work_request(
    payload: WorkRequestCreate, session: SessionDependency
) -> WorkRequest:
    get_customer_or_404(payload.customer_id, session)
    work_request = WorkRequest(
        customer_id=payload.customer_id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
    )
    session.add(work_request)
    session.commit()
    session.refresh(work_request)
    return work_request


@router.get(
    "/work-requests/{work_request_id}",
    response_model=WorkRequestRead,
    responses={404: {"model": ErrorResponse}},
)
def get_work_request(work_request_id: int, session: SessionDependency) -> WorkRequest:
    return get_work_request_or_404(work_request_id, session)


@router.get("/work-requests", response_model=WorkRequestList)
def list_work_requests(
    session: SessionDependency,
    status_filter: Annotated[WorkRequestStatus | None, Query(alias="status")] = None,
    limit: LimitQuery = 50,
    offset: OffsetQuery = 0,
) -> dict[str, object]:
    statement = select(WorkRequest).order_by(WorkRequest.id).limit(limit).offset(offset)
    if status_filter is not None:
        statement = statement.where(WorkRequest.status == status_filter)
    work_requests = session.scalars(statement).all()
    return {"items": work_requests, "limit": limit, "offset": offset}


@router.patch(
    "/work-requests/{work_request_id}/status",
    response_model=WorkRequestRead,
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
)
def update_work_request_status(
    work_request_id: int,
    payload: WorkRequestStatusUpdate,
    session: SessionDependency,
) -> WorkRequest:
    work_request = get_work_request_or_404(work_request_id, session)
    if (
        work_request.status in TERMINAL_WORK_REQUEST_STATUSES
        and payload.status != work_request.status
    ):
        raise error_response(
            status.HTTP_409_CONFLICT,
            "invalid_status_transition",
            "Resolved or cancelled work requests cannot change status.",
            {"from": work_request.status, "to": payload.status},
        )

    old_status = work_request.status
    work_request.status = payload.status
    session.add(
        WorkRequestStatusEvent(
            work_request_id=work_request.id,
            old_status=old_status,
            new_status=payload.status,
            reason=payload.reason,
        )
    )
    session.commit()
    session.refresh(work_request)
    return work_request


@router.get(
    "/work-requests/{work_request_id}/status-events",
    response_model=WorkRequestStatusEventList,
    responses={404: {"model": ErrorResponse}},
)
def list_work_request_status_events(
    work_request_id: int,
    session: SessionDependency,
    limit: LimitQuery = 50,
    offset: OffsetQuery = 0,
) -> dict[str, object]:
    get_work_request_or_404(work_request_id, session)
    events = session.scalars(
        select(WorkRequestStatusEvent)
        .where(WorkRequestStatusEvent.work_request_id == work_request_id)
        .order_by(WorkRequestStatusEvent.id)
        .limit(limit)
        .offset(offset)
    ).all()
    return {"items": events, "limit": limit, "offset": offset}
