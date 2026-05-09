"""Pure report rendering functions with no database or network dependencies."""

from opledger_api.report_contracts import (
    WorkRequestSummaryRenderRequest,
    WorkRequestSummaryReport,
)


def render_work_request_summary_report(
    request: WorkRequestSummaryRenderRequest,
) -> WorkRequestSummaryReport:
    return WorkRequestSummaryReport(**request.model_dump(exclude={"requested_by"}))
