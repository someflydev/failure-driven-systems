"""Add local notification attempts."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0007_notification_attempts"
down_revision: str | Sequence[str] | None = "0006_report_job_idempotency"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "notification_attempts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("target_type", sa.String(length=64), nullable=False),
        sa.Column("target_id", sa.Integer(), nullable=False),
        sa.Column("channel", sa.String(length=64), nullable=False),
        sa.Column("recipient", sa.String(length=320), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("idempotency_key", sa.String(length=191), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("sent_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "target_type in ('report_job')",
            name="ck_notification_attempts_target_type",
        ),
        sa.CheckConstraint(
            "channel in ('local_log')",
            name="ck_notification_attempts_channel",
        ),
        sa.CheckConstraint(
            "status in ('pending', 'sent', 'failed')",
            name="ck_notification_attempts_status",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "idempotency_key",
            name="uq_notification_attempts_idempotency_key",
        ),
    )


def downgrade() -> None:
    op.drop_table("notification_attempts")
