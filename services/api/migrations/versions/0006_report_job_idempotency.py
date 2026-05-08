"""Add report job idempotency key."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0006_report_job_idempotency"
down_revision: str | Sequence[str] | None = "0005_report_job_attempt_metadata"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "report_jobs",
        sa.Column("idempotency_key", sa.String(length=191), nullable=True),
    )
    op.create_unique_constraint(
        "uq_report_jobs_report_type_idempotency_key",
        "report_jobs",
        ["report_type", "idempotency_key"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_report_jobs_report_type_idempotency_key",
        "report_jobs",
        type_="unique",
    )
    op.drop_column("report_jobs", "idempotency_key")
