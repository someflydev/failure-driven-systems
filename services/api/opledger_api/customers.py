"""Customer boundary: customer identity and duplicate email rules."""

from fastapi import APIRouter, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from opledger_api.models import Customer
from opledger_api.schemas import (
    CustomerCreate,
    CustomerList,
    CustomerRead,
    ErrorResponse,
)
from opledger_api.shared import (
    LimitQuery,
    OffsetQuery,
    SessionDependency,
    error_response,
)

router = APIRouter(tags=["opsledger"])


def get_customer_or_404(customer_id: int, session: Session) -> Customer:
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise error_response(
            status.HTTP_404_NOT_FOUND,
            "customer_not_found",
            "Customer was not found.",
        )
    return customer


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
