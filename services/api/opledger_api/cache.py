"""Redis cache helpers for deliberately cached read paths."""

from collections.abc import Iterator
from typing import Protocol, cast

from redis import Redis

from opledger_api.config import Settings, get_settings


class RedisCacheClient(Protocol):
    def get(self, name: str) -> str | bytes | None: ...

    def setex(self, name: str, time: int, value: str) -> object: ...

    def delete(self, *names: str) -> int: ...

    def scan_iter(self, match: str) -> Iterator[str | bytes]: ...


def get_redis_connection(settings: Settings | None = None) -> RedisCacheClient:
    resolved_settings = settings or get_settings()
    return cast(
        RedisCacheClient,
        Redis.from_url(resolved_settings.redis_url, decode_responses=True),
    )
