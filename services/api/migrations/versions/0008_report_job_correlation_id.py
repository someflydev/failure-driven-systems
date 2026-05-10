"""Add report job correlation id."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0008_report_job_correlation_id"
down_revision: str | Sequence[str] | None = "0007_notification_attempts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "report_jobs",
        sa.Column("correlation_id", sa.String(length=64), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("report_jobs", "correlation_id")
