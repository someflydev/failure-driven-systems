import json
import logging
from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from datetime import UTC, datetime
from time import perf_counter
from uuid import uuid4

from fastapi import Request
from starlette.responses import Response

REQUEST_ID_HEADER = "x-request-id"
CORRELATION_ID_HEADER = "x-correlation-id"
REQUEST_ID_RESPONSE_HEADER = "X-Request-ID"
CORRELATION_ID_RESPONSE_HEADER = "X-Correlation-ID"
LOG_RECORD_RESERVED_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "taskName",
    "thread",
    "threadName",
}
LOG_CONTEXT_ATTRS = {"service", "environment", "request_id", "correlation_id"}

request_id_context: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None,
)
correlation_id_context: ContextVar[str | None] = ContextVar(
    "correlation_id",
    default=None,
)
service_context: ContextVar[str | None] = ContextVar("service", default=None)
environment_context: ContextVar[str | None] = ContextVar(
    "environment",
    default=None,
)

logger = logging.getLogger("opledger_api.requests")


class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname.lower(),
            "logger": record.name,
            "message": record.getMessage(),
        }
        if service_context.get() is not None:
            payload["service"] = service_context.get()
        if environment_context.get() is not None:
            payload["environment"] = environment_context.get()
        if request_id_context.get() is not None:
            payload["request_id"] = request_id_context.get()
        if correlation_id_context.get() is not None:
            payload["correlation_id"] = correlation_id_context.get()

        for key, value in record.__dict__.items():
            if key in LOG_RECORD_RESERVED_ATTRS or key in LOG_CONTEXT_ATTRS:
                continue
            if key.startswith("_"):
                continue
            payload[key] = value

        if record.exc_info and record.exc_info[0] is not None:
            payload["error_class"] = record.exc_info[0].__name__

        return json.dumps(payload, sort_keys=True, default=str)


def configure_logging(
    *,
    service: str = "opledger-api",
    environment: str = "local",
) -> None:
    service_context.set(service)
    environment_context.set(environment)
    root_logger = logging.getLogger()
    if root_logger.handlers:
        for handler in root_logger.handlers:
            handler.setFormatter(JsonLogFormatter())
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(JsonLogFormatter())
        root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    logging.getLogger("opledger_api").setLevel(logging.INFO)
    logging.getLogger("reporting_service").setLevel(logging.INFO)


def new_request_id() -> str:
    return uuid4().hex


def current_request_id() -> str | None:
    return request_id_context.get()


def current_correlation_id() -> str | None:
    return correlation_id_context.get()


def set_log_context(
    *,
    service: str | None = None,
    environment: str | None = None,
    request_id: str | None = None,
    correlation_id: str | None = None,
) -> None:
    if service is not None:
        service_context.set(service)
    if environment is not None:
        environment_context.set(environment)
    request_id_context.set(request_id)
    correlation_id_context.set(correlation_id)


async def log_request(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    started_at = perf_counter()
    request_id = request.headers.get(REQUEST_ID_HEADER) or new_request_id()
    correlation_id = request.headers.get(CORRELATION_ID_HEADER) or request_id
    request_id_token = request_id_context.set(request_id)
    correlation_id_token = correlation_id_context.set(correlation_id)
    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "http_request_failed",
            extra={
                "event": "http_request_failed",
                "method": request.method,
                "path": request.url.path,
                "status": 500,
                "duration_ms": round(duration_ms, 2),
            },
        )
        request_id_context.reset(request_id_token)
        correlation_id_context.reset(correlation_id_token)
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    response.headers[REQUEST_ID_RESPONSE_HEADER] = request_id
    response.headers[CORRELATION_ID_RESPONSE_HEADER] = correlation_id
    logger.info(
        "http_request",
        extra={
            "event": "http_request",
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": round(duration_ms, 2),
        },
    )
    request_id_context.reset(request_id_token)
    correlation_id_context.reset(correlation_id_token)
    return response
