"""Add work request status event history."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_work_request_status_events"
down_revision: str | Sequence[str] | None = "0001_phase_1_core_models"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "work_request_status_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("work_request_id", sa.Integer(), nullable=False),
        sa.Column("old_status", sa.String(length=32), nullable=False),
        sa.Column("new_status", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "old_status in ('open', 'in_progress', 'resolved', 'cancelled')",
            name="ck_work_request_status_events_old_status",
        ),
        sa.CheckConstraint(
            "new_status in ('open', 'in_progress', 'resolved', 'cancelled')",
            name="ck_work_request_status_events_new_status",
        ),
        sa.ForeignKeyConstraint(
            ["work_request_id"],
            ["work_requests.id"],
            name="fk_work_request_status_events_work_request_id_work_requests",
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("work_request_status_events")
