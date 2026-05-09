from fastapi import FastAPI

from opledger_api.report_contracts import (
    WorkRequestSummaryRenderRequest,
    WorkRequestSummaryReport,
)
from opledger_api.report_renderer import render_work_request_summary_report


def create_app() -> FastAPI:
    app = FastAPI(title="OpsLedger Reporting Service")

    @app.get("/")
    def root() -> dict[str, str]:
        return {"service": "OpsLedger Reporting Service", "status": "ok"}

    @app.get("/health/live")
    def live() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/ready")
    def ready() -> dict[str, str]:
        return {"status": "ok"}

    @app.post(
        "/reports/work-requests/summary/render",
        response_model=WorkRequestSummaryReport,
    )
    def render_summary_report(
        request: WorkRequestSummaryRenderRequest,
    ) -> WorkRequestSummaryReport:
        return render_work_request_summary_report(request)

    return app


app = create_app()
