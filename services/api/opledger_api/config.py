from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings for local development and deployment."""

    app_name: str = "OpsLedger API"
    environment: str = "local"

    model_config = SettingsConfigDict(env_prefix="OPLEDGER_")


@lru_cache
def get_settings() -> Settings:
    return Settings()
