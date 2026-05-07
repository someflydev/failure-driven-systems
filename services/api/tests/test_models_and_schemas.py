import pytest
from pydantic import ValidationError

from opledger_api.models import Customer, WorkRequest, WorkRequestStatusEvent
from opledger_api.schemas import (
    CustomerCreate,
    WorkRequestCreate,
    WorkRequestStatusUpdate,
)


def test_customer_schema_requires_valid_email() -> None:
    with pytest.raises(ValidationError):
        CustomerCreate(name="Acme Operations", email="not-an-email")


def test_work_request_schema_rejects_unknown_status() -> None:
    with pytest.raises(ValidationError):
        WorkRequestCreate.model_validate(
            {
                "customer_id": 1,
                "title": "Replace scanner",
                "description": "Warehouse scanner stopped booting.",
                "status": "waiting",
            }
        )


def test_work_request_status_update_accepts_reason() -> None:
    payload = WorkRequestStatusUpdate(
        status="in_progress",
        reason="Technician started work.",
    )

    assert payload.reason == "Technician started work."


def test_models_capture_customer_work_request_relationship() -> None:
    customer = Customer(name="Acme Operations", email="ops@example.com")
    request = WorkRequest(
        title="Replace scanner",
        description="Warehouse scanner stopped booting.",
        status="open",
    )

    customer.work_requests.append(request)

    assert request.customer is customer
    assert request.customer_id is None
    assert customer.work_requests == [request]


def test_models_capture_work_request_status_event_relationship() -> None:
    request = WorkRequest(
        title="Replace scanner",
        description="Warehouse scanner stopped booting.",
        status="open",
    )
    status_event = WorkRequestStatusEvent(
        old_status="open",
        new_status="in_progress",
        reason="Technician started work.",
    )

    request.status_events.append(status_event)

    assert status_event.work_request is request
    assert status_event.work_request_id is None
    assert request.status_events == [status_event]
