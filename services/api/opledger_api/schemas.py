from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

WorkRequestStatus = Literal["open", "in_progress", "resolved", "cancelled"]
EmailText = Annotated[
    str,
    Field(min_length=3, max_length=320, pattern=r"^[^@\s]+@[^@\s]+$"),
]


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailText


class CustomerRead(BaseModel):
    id: int
    name: str
    email: EmailText
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CustomerList(BaseModel):
    items: list[CustomerRead]
    limit: int
    offset: int


class WorkRequestCreate(BaseModel):
    customer_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1)
    status: WorkRequestStatus = "open"


class WorkRequestRead(BaseModel):
    id: int
    customer_id: int
    title: str
    description: str
    status: WorkRequestStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkRequestList(BaseModel):
    items: list[WorkRequestRead]
    limit: int
    offset: int


class WorkRequestStatusUpdate(BaseModel):
    status: WorkRequestStatus
    reason: str = Field(
        default="Status updated through API.",
        min_length=1,
        max_length=500,
    )


class WorkRequestStatusEventRead(BaseModel):
    id: int
    work_request_id: int
    old_status: WorkRequestStatus
    new_status: WorkRequestStatus
    reason: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkRequestStatusEventList(BaseModel):
    items: list[WorkRequestStatusEventRead]
    limit: int
    offset: int


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: object | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail
