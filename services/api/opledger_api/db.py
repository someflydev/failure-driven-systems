from functools import lru_cache

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from opledger_api.config import Settings, get_settings


class Base(DeclarativeBase):
    """Base class for future SQLAlchemy models."""


DatabaseTarget = dict[str, str | int | None]


class DatabaseReadinessError(RuntimeError):
    """Raised when a lightweight database readiness check fails."""

    def __init__(
        self,
        error_class: str,
        target: DatabaseTarget | None = None,
    ) -> None:
        super().__init__(error_class)
        self.error_class = error_class
        self.target = target or {}


@lru_cache
def _cached_engine(database_url: str, connect_timeout_seconds: int) -> Engine:
    return create_engine(
        database_url,
        connect_args={"connect_timeout": connect_timeout_seconds},
        pool_pre_ping=True,
    )


def get_engine(settings: Settings | None = None) -> Engine:
    resolved_settings = settings or get_settings()
    return _cached_engine(
        sqlalchemy_database_url(resolved_settings.database_url),
        resolved_settings.database_connect_timeout_seconds,
    )


@lru_cache
def _cached_sessionmaker(
    database_url: str, connect_timeout_seconds: int
) -> sessionmaker[Session]:
    return sessionmaker(
        bind=_cached_engine(database_url, connect_timeout_seconds),
        autoflush=False,
        expire_on_commit=False,
    )


def get_sessionmaker(settings: Settings | None = None) -> sessionmaker[Session]:
    resolved_settings = settings or get_settings()
    return _cached_sessionmaker(
        sqlalchemy_database_url(resolved_settings.database_url),
        resolved_settings.database_connect_timeout_seconds,
    )


def get_session(settings: Settings | None = None) -> Session:
    return get_sessionmaker(settings)()


def sqlalchemy_database_url(database_url: str) -> str:
    if database_url.startswith("postgres://"):
        return f"postgresql+psycopg://{database_url.removeprefix('postgres://')}"
    if database_url.startswith("postgresql://"):
        return f"postgresql+psycopg://{database_url.removeprefix('postgresql://')}"
    return database_url


def database_target(database_url: str) -> DatabaseTarget:
    url = make_url(sqlalchemy_database_url(database_url))
    return {
        "driver": url.drivername,
        "host": url.host,
        "port": url.port,
        "database": url.database,
    }


def check_database_readiness(settings: Settings | None = None) -> DatabaseTarget:
    resolved_settings = settings or get_settings()
    try:
        target = database_target(resolved_settings.database_url)
    except Exception as exc:
        raise DatabaseReadinessError(exc.__class__.__name__) from exc

    try:
        with get_engine(resolved_settings).connect() as connection:
            connection.execute(text("select 1"))
    except SQLAlchemyError as exc:
        raise DatabaseReadinessError(exc.__class__.__name__, target) from exc

    return target
