"""Derived read models for dashboard-style access patterns."""

import argparse
import json
import logging
from datetime import UTC, datetime
from typing import Any, cast

from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder
from redis.exceptions import RedisError
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from opledger_api.cache import get_redis_connection
from opledger_api.config import Settings
from opledger_api.db import get_session
from opledger_api.metrics import record_cache_access
from opledger_api.models import (
    WORK_REQUEST_STATUSES,
    Customer,
    CustomerWorkRequestStats,
    WorkRequest,
    WorkRequestStatusEvent,
)
from opledger_api.schemas import CustomerWorkRequestStatsList
from opledger_api.shared import (
    LimitQuery,
    OffsetQuery,
    SessionDependency,
    SettingsDependency,
)

router = APIRouter(tags=["opsledger"])
logger = logging.getLogger("opledger_api.read_models")

CUSTOMER_STATS_CACHE_ENDPOINT = "dashboard_customer_work_request_stats"
CUSTOMER_STATS_CACHE_KEY_PREFIX = "opledger:v1:dashboard:customer-work-request-stats"


def rebuild_customer_work_request_stats(
    session: Session,
) -> list[CustomerWorkRequestStats]:
    """Rebuild dashboard stats from source-of-truth customer and work tables."""
    session.execute(delete(CustomerWorkRequestStats))

    customers = session.scalars(select(Customer).order_by(Customer.id)).all()
    rebuilt_at = datetime.now(UTC)

    status_counts: dict[int, dict[str, int]] = {}
    status_rows = session.execute(
        select(
            WorkRequest.customer_id,
            WorkRequest.status,
            func.count(WorkRequest.id),
        ).group_by(WorkRequest.customer_id, WorkRequest.status)
    ).all()
    for customer_id, status, count in status_rows:
        customer_counts = status_counts.setdefault(
            customer_id,
            {status_name: 0 for status_name in WORK_REQUEST_STATUSES},
        )
        customer_counts[status] = count

    event_counts: dict[int, int] = {}
    event_rows = session.execute(
        select(
            WorkRequest.customer_id,
            func.count(WorkRequestStatusEvent.id),
        )
        .join(
            WorkRequestStatusEvent,
            WorkRequestStatusEvent.work_request_id == WorkRequest.id,
        )
        .group_by(WorkRequest.customer_id)
    ).all()
    for customer_id, count in event_rows:
        event_counts[customer_id] = count

    stats_rows: list[CustomerWorkRequestStats] = []
    for customer in customers:
        counts = status_counts.get(
            customer.id,
            {status_name: 0 for status_name in WORK_REQUEST_STATUSES},
        )
        stats_rows.append(
            CustomerWorkRequestStats(
                customer_id=customer.id,
                total_work_requests=sum(counts.values()),
                open_count=counts["open"],
                in_progress_count=counts["in_progress"],
                resolved_count=counts["resolved"],
                cancelled_count=counts["cancelled"],
                status_event_count=event_counts.get(customer.id, 0),
                rebuilt_at=rebuilt_at,
            )
        )

    session.add_all(stats_rows)
    session.commit()
    invalidate_customer_work_request_stats_cache()
    return stats_rows


def customer_stats_response(
    stats: CustomerWorkRequestStats,
    customer: Customer,
) -> dict[str, Any]:
    return {
        "customer_id": stats.customer_id,
        "customer_name": customer.name,
        "customer_email": customer.email,
        "total_work_requests": stats.total_work_requests,
        "open_count": stats.open_count,
        "in_progress_count": stats.in_progress_count,
        "resolved_count": stats.resolved_count,
        "cancelled_count": stats.cancelled_count,
        "status_event_count": stats.status_event_count,
        "rebuilt_at": stats.rebuilt_at,
    }


def customer_stats_cache_key(limit: int, offset: int) -> str:
    return f"{CUSTOMER_STATS_CACHE_KEY_PREFIX}:limit={limit}:offset={offset}"


def load_customer_work_request_stats(
    session: Session,
    limit: int,
    offset: int,
) -> dict[str, object]:
    rows = session.execute(
        select(CustomerWorkRequestStats, Customer)
        .join(Customer, Customer.id == CustomerWorkRequestStats.customer_id)
        .order_by(
            CustomerWorkRequestStats.total_work_requests.desc(),
            CustomerWorkRequestStats.customer_id,
        )
        .limit(limit)
        .offset(offset)
    ).all()
    response = {
        "items": [customer_stats_response(stats, customer) for stats, customer in rows],
        "limit": limit,
        "offset": offset,
    }
    return cast(dict[str, object], jsonable_encoder(response))


def read_cached_customer_work_request_stats(
    settings: Settings,
    cache_key: str,
) -> dict[str, object] | None:
    try:
        cached_response = get_redis_connection(settings).get(cache_key)
    except RedisError as exc:
        record_cache_access(CUSTOMER_STATS_CACHE_ENDPOINT, "unavailable")
        logger.warning(
            "customer_stats_cache_unavailable",
            extra={
                "event": "customer_stats_cache_unavailable",
                "cache_key": cache_key,
                "error_class": exc.__class__.__name__,
            },
        )
        return None

    if cached_response is None:
        record_cache_access(CUSTOMER_STATS_CACHE_ENDPOINT, "miss")
        return None

    record_cache_access(CUSTOMER_STATS_CACHE_ENDPOINT, "hit")
    if isinstance(cached_response, bytes):
        cached_response = cached_response.decode("utf-8")
    return cast(dict[str, object], json.loads(cached_response))


def write_cached_customer_work_request_stats(
    settings: Settings,
    cache_key: str,
    response: dict[str, object],
) -> None:
    ttl_seconds = settings.dashboard_customer_work_request_stats_cache_ttl_seconds
    try:
        get_redis_connection(settings).setex(
            cache_key,
            ttl_seconds,
            json.dumps(response, sort_keys=True),
        )
    except RedisError as exc:
        record_cache_access(CUSTOMER_STATS_CACHE_ENDPOINT, "write_failed")
        logger.warning(
            "customer_stats_cache_write_failed",
            extra={
                "event": "customer_stats_cache_write_failed",
                "cache_key": cache_key,
                "ttl_seconds": ttl_seconds,
                "error_class": exc.__class__.__name__,
            },
        )


def invalidate_customer_work_request_stats_cache(
    settings: Settings | None = None,
) -> None:
    try:
        redis = get_redis_connection(settings)
        keys = list(redis.scan_iter(match=f"{CUSTOMER_STATS_CACHE_KEY_PREFIX}:*"))
        if keys:
            redis.delete(
                *(
                    key.decode("utf-8") if isinstance(key, bytes) else key
                    for key in keys
                )
            )
    except RedisError as exc:
        logger.warning(
            "customer_stats_cache_invalidation_failed",
            extra={
                "event": "customer_stats_cache_invalidation_failed",
                "error_class": exc.__class__.__name__,
            },
        )


@router.get(
    "/dashboard/customer-work-request-stats",
    response_model=CustomerWorkRequestStatsList,
)
def list_customer_work_request_stats(
    session: SessionDependency,
    settings: SettingsDependency,
    limit: LimitQuery = 50,
    offset: OffsetQuery = 0,
    bypass_cache: bool = Query(default=False),
) -> dict[str, object]:
    cache_key = customer_stats_cache_key(limit, offset)
    if not bypass_cache:
        cached_response = read_cached_customer_work_request_stats(settings, cache_key)
        if cached_response is not None:
            return cached_response
    else:
        record_cache_access(CUSTOMER_STATS_CACHE_ENDPOINT, "bypass")

    response = load_customer_work_request_stats(session, limit, offset)
    if not bypass_cache:
        write_cached_customer_work_request_stats(settings, cache_key, response)
    return response


def parsed_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebuild OpsLedger derived read models from source tables."
    )
    parser.add_argument(
        "model",
        choices=["customer-work-request-stats"],
        help="Derived read model to rebuild.",
    )
    return parser.parse_args()


def main() -> int:
    args = parsed_args()
    with get_session() as session:
        if args.model == "customer-work-request-stats":
            rows = rebuild_customer_work_request_stats(session)
            print(f"rebuilt customer-work-request-stats rows={len(rows)}")
            return 0
    raise AssertionError(f"unhandled read model: {args.model}")


if __name__ == "__main__":
    raise SystemExit(main())
