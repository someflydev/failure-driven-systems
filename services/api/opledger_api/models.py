from datetime import datetime

from sqlalchemy import (
    JSON,
    CheckConstraint,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from opledger_api.db import Base

WORK_REQUEST_STATUSES = ("open", "in_progress", "resolved", "cancelled")
REPORT_JOB_STATUSES = ("queued", "running", "succeeded", "failed")


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = (UniqueConstraint("email", name="uq_customers_email"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    work_requests: Mapped[list["WorkRequest"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan",
    )


class WorkRequest(Base):
    __tablename__ = "work_requests"
    __table_args__ = (
        CheckConstraint(
            "status in ('open', 'in_progress', 'resolved', 'cancelled')",
            name="ck_work_requests_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", name="fk_work_requests_customer_id_customers"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    customer: Mapped[Customer] = relationship(back_populates="work_requests")
    status_events: Mapped[list["WorkRequestStatusEvent"]] = relationship(
        back_populates="work_request",
        cascade="all, delete-orphan",
    )


class WorkRequestStatusEvent(Base):
    __tablename__ = "work_request_status_events"
    __table_args__ = (
        CheckConstraint(
            "old_status in ('open', 'in_progress', 'resolved', 'cancelled')",
            name="ck_work_request_status_events_old_status",
        ),
        CheckConstraint(
            "new_status in ('open', 'in_progress', 'resolved', 'cancelled')",
            name="ck_work_request_status_events_new_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    work_request_id: Mapped[int] = mapped_column(
        ForeignKey(
            "work_requests.id",
            name="fk_work_request_status_events_work_request_id_work_requests",
        ),
        nullable=False,
    )
    old_status: Mapped[str] = mapped_column(String(32), nullable=False)
    new_status: Mapped[str] = mapped_column(String(32), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    work_request: Mapped[WorkRequest] = relationship(back_populates="status_events")


class ReportJob(Base):
    __tablename__ = "report_jobs"
    __table_args__ = (
        CheckConstraint(
            "status in ('queued', 'running', 'succeeded', 'failed')",
            name="ck_report_jobs_status",
        ),
        UniqueConstraint("redis_job_id", name="uq_report_jobs_redis_job_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    report_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="queued")
    redis_job_id: Mapped[str | None] = mapped_column(String(191), nullable=True)
    result_json: Mapped[dict[str, object] | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    started_at: Mapped[datetime | None] = mapped_column(nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(nullable=True)
