"""Rename report job lifecycle statuses."""

from collections.abc import Sequence

from alembic import op

revision: str = "0004_report_job_status_names"
down_revision: str | Sequence[str] | None = "0003_report_jobs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint("ck_report_jobs_status", "report_jobs", type_="check")
    op.execute("update report_jobs set status = 'running' where status = 'started'")
    op.execute("update report_jobs set status = 'succeeded' where status = 'finished'")
    op.create_check_constraint(
        "ck_report_jobs_status",
        "report_jobs",
        "status in ('queued', 'running', 'succeeded', 'failed')",
    )


def downgrade() -> None:
    op.drop_constraint("ck_report_jobs_status", "report_jobs", type_="check")
    op.execute("update report_jobs set status = 'started' where status = 'running'")
    op.execute("update report_jobs set status = 'finished' where status = 'succeeded'")
    op.create_check_constraint(
        "ck_report_jobs_status",
        "report_jobs",
        "status in ('queued', 'started', 'finished', 'failed')",
    )
