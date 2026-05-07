from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings for local development and deployment."""

    app_name: str = "OpsLedger API"
    environment: str = "local"
    database_url: str = Field(
        default="postgresql+psycopg://localhost:55432/opledger",
        validation_alias=AliasChoices("DATABASE_URL", "OPLEDGER_DATABASE_URL"),
    )
    database_connect_timeout_seconds: int = Field(
        default=3,
        validation_alias=AliasChoices(
            "DATABASE_CONNECT_TIMEOUT_SECONDS",
            "OPLEDGER_DATABASE_CONNECT_TIMEOUT_SECONDS",
        ),
    )

    model_config = SettingsConfigDict(env_prefix="OPLEDGER_", populate_by_name=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
