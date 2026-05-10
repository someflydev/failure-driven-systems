"""Add filtered work request list index."""

from collections.abc import Sequence

from alembic import op

revision: str = "0009_work_request_list_index"
down_revision: str | Sequence[str] | None = "0008_report_job_correlation_id"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(
        "ix_work_requests_status_created_at_id",
        "work_requests",
        ["status", "created_at", "id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_work_requests_status_created_at_id",
        table_name="work_requests",
    )
