"""Add customer work request stats read model."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0010_customer_work_request_stats"
down_revision: str | Sequence[str] | None = "0009_work_request_list_index"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "customer_work_request_stats",
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("total_work_requests", sa.Integer(), nullable=False),
        sa.Column("open_count", sa.Integer(), nullable=False),
        sa.Column("in_progress_count", sa.Integer(), nullable=False),
        sa.Column("resolved_count", sa.Integer(), nullable=False),
        sa.Column("cancelled_count", sa.Integer(), nullable=False),
        sa.Column("status_event_count", sa.Integer(), nullable=False),
        sa.Column("rebuilt_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            name="fk_customer_work_request_stats_customer_id",
        ),
        sa.PrimaryKeyConstraint("customer_id"),
    )


def downgrade() -> None:
    op.drop_table("customer_work_request_stats")
