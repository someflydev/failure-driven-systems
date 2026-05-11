from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from opledger_api.config import get_settings
from opledger_api.health import router as health_router
from opledger_api.logging import configure_logging, log_request
from opledger_api.metrics import metrics_response, require_metrics_access
from opledger_api.routes import router as opsledger_router


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(service="opledger-api", environment=settings.environment)
    app = FastAPI(title=settings.app_name)

    app.middleware("http")(log_request)

    app.include_router(health_router)
    app.include_router(opsledger_router)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "error": {
                    "code": "validation_failed",
                    "message": "Request validation failed.",
                    "details": exc.errors(),
                }
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        _request: Request, exc: HTTPException
    ) -> JSONResponse:
        if isinstance(exc.detail, dict) and "error" in exc.detail:
            return JSONResponse(status_code=exc.status_code, content=exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": "http_error",
                    "message": str(exc.detail),
                    "details": None,
                }
            },
        )

    @app.get("/")
    def root() -> dict[str, str]:
        return {"service": settings.app_name, "status": "ok"}

    @app.get("/metrics")
    def metrics(request: Request) -> object:
        require_metrics_access(request, settings.metrics_access_token)
        return metrics_response()

    return app


app = create_app()
