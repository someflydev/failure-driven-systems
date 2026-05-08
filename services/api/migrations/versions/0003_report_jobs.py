"""Add durable report job state."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_report_jobs"
down_revision: str | Sequence[str] | None = "0002_work_request_status_events"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "report_jobs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("report_type", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("redis_job_id", sa.String(length=191), nullable=True),
        sa.Column("result_json", sa.JSON(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "status in ('queued', 'started', 'finished', 'failed')",
            name="ck_report_jobs_status",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("redis_job_id", name="uq_report_jobs_redis_job_id"),
    )


def downgrade() -> None:
    op.drop_table("report_jobs")
