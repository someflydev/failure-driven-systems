"""Add report job retry attempt metadata."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0005_report_job_attempt_metadata"
down_revision: str | Sequence[str] | None = "0004_report_job_status_names"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("report_jobs", sa.Column("last_error", sa.Text(), nullable=True))
    op.add_column(
        "report_jobs",
        sa.Column("attempt_count", sa.Integer(), server_default="0", nullable=False),
    )
    op.add_column(
        "report_jobs", sa.Column("last_failed_at", sa.DateTime(), nullable=True)
    )
    op.alter_column("report_jobs", "attempt_count", server_default=None)


def downgrade() -> None:
    op.drop_column("report_jobs", "last_failed_at")
    op.drop_column("report_jobs", "attempt_count")
    op.drop_column("report_jobs", "last_error")
