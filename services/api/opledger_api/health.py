import logging
from typing import Protocol

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from opledger_api.db import DatabaseReadinessError, check_database_readiness

router = APIRouter(prefix="/health", tags=["health"])
logger = logging.getLogger("opledger_api.health")

ReadinessPayload = dict[str, str | int | None]


class ReadinessChecker(Protocol):
    def __call__(self) -> ReadinessPayload: ...


def get_readiness_checker() -> ReadinessChecker:
    return check_database_readiness


readiness_dependency = Depends(get_readiness_checker)


@router.get("/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready", response_model=None)
def ready(
    readiness_checker: ReadinessChecker = readiness_dependency,
) -> dict[str, object] | JSONResponse:
    try:
        database = readiness_checker()
    except DatabaseReadinessError as exc:
        logger.warning(
            "database_readiness_failed",
            extra={
                "event": "database_readiness_failed",
                "error_class": exc.error_class,
                "driver": exc.target.get("driver"),
                "host": exc.target.get("host"),
                "port": exc.target.get("port"),
                "database": exc.target.get("database"),
            },
        )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not_ready",
                "database": {
                    "status": "unavailable",
                    "error_class": exc.error_class,
                    **exc.target,
                },
            },
        )

    return {"status": "ok", "database": {"status": "ok", **database}}
