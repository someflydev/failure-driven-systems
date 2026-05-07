from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from opledger_api.db import get_db_session
from opledger_api.models import Customer, WorkRequest, WorkRequestStatusEvent
from opledger_api.schemas import (
    CustomerCreate,
    CustomerList,
    CustomerRead,
    ErrorResponse,
    WorkRequestCreate,
    WorkRequestList,
    WorkRequestRead,
    WorkRequestStatus,
    WorkRequestStatusEventList,
    WorkRequestStatusUpdate,
)

router = APIRouter(tags=["opsledger"])

SessionDependency = Annotated[Session, Depends(get_db_session)]
LimitQuery = Annotated[int, Query(ge=1, le=100)]
OffsetQuery = Annotated[int, Query(ge=0)]

TERMINAL_WORK_REQUEST_STATUSES: set[WorkRequestStatus] = {"resolved", "cancelled"}


def error_response(
    status_code: int,
    code: str,
    message: str,
    details: object | None = None,
) -> HTTPException:
    return HTTPException(
        status_code=status_code,
        detail={"error": {"code": code, "message": message, "details": details}},
    )


def get_customer_or_404(customer_id: int, session: Session) -> Customer:
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise error_response(
            status.HTTP_404_NOT_FOUND,
            "customer_not_found",
            "Customer was not found.",
        )
    return customer


def get_work_request_or_404(work_request_id: int, session: Session) -> WorkRequest:
    work_request = session.get(WorkRequest, work_request_id)
    if work_request is None:
        raise error_response(
            status.HTTP_404_NOT_FOUND,
            "work_request_not_found",
            "Work request was not found.",
        )
    return work_request


def commit_or_duplicate_email(session: Session) -> None:
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        if "uq_customers_email" in str(exc.orig) or "customers.email" in str(exc.orig):
            raise error_response(
                status.HTTP_409_CONFLICT,
                "duplicate_customer_email",
                "A customer with that email already exists.",
            ) from exc
        raise


@router.post(
    "/customers",
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"model": ErrorResponse}},
)
def create_customer(payload: CustomerCreate, session: SessionDependency) -> Customer:
    customer = Customer(name=payload.name, email=payload.email)
    session.add(customer)
    commit_or_duplicate_email(session)
    session.refresh(customer)
    return customer


@router.get(
    "/customers/{customer_id}",
    response_model=CustomerRead,
    responses={404: {"model": ErrorResponse}},
)
def get_customer(customer_id: int, session: SessionDependency) -> Customer:
    return get_customer_or_404(customer_id, session)


@router.get("/customers", response_model=CustomerList)
def list_customers(
    session: SessionDependency,
    limit: LimitQuery = 50,
    offset: OffsetQuery = 0,
) -> dict[str, object]:
    customers = session.scalars(
        select(Customer).order_by(Customer.id).limit(limit).offset(offset)
    ).all()
    return {"items": customers, "limit": limit, "offset": offset}


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
