from fastapi import FastAPI

from opledger_api.config import get_settings
from opledger_api.health import router as health_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    app.include_router(health_router)

    @app.get("/")
    def root() -> dict[str, str]:
        return {"service": settings.app_name, "status": "ok"}

    return app


app = create_app()
