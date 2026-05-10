import time

from fastapi import FastAPI
from fastapi.responses import JSONResponse, Response

from opledger_api.logging import configure_logging, log_request
from opledger_api.report_contracts import (
    WorkRequestSummaryRenderRequest,
    WorkRequestSummaryReport,
)
from opledger_api.report_renderer import render_work_request_summary_report
from reporting_service.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(service="opledger-reporting", environment=settings.environment)
    app = FastAPI(title="OpsLedger Reporting Service")
    app.middleware("http")(log_request)

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
    ) -> WorkRequestSummaryReport | JSONResponse | Response:
        if settings.local_failure_injection_active:
            if settings.failure_mode == "delay":
                time.sleep(settings.failure_delay_seconds)
            elif settings.failure_mode == "http_500":
                return JSONResponse(
                    status_code=500,
                    content={
                        "detail": "Injected reporting service failure.",
                        "failure_mode": settings.failure_mode,
                    },
                )
            elif settings.failure_mode == "malformed_response":
                return Response(
                    content="{not valid json",
                    media_type="application/json",
                )
            elif settings.failure_mode == "incompatible_response":
                return JSONResponse(
                    status_code=200,
                    content={
                        "contract_version": "report-rendering.v2",
                        "report_type": "work_request_summary",
                        "generated_at": request.generated_at.isoformat(),
                    },
                )

        return render_work_request_summary_report(request)

    return app


app = create_app()
