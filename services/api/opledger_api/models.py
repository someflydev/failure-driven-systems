from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from opledger_api.db import Base

WORK_REQUEST_STATUSES = ("open", "in_progress", "resolved", "cancelled")


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
