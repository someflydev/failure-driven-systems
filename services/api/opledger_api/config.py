from functools import lru_cache
from typing import Literal

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ReportFailureInjectionStage = Literal[
    "none",
    "before_generation",
    "after_partial_progress",
]


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
    report_delay_enabled: bool = Field(
        default=False,
        validation_alias=AliasChoices(
            "REPORT_DELAY_ENABLED",
            "OPLEDGER_REPORT_DELAY_ENABLED",
        ),
    )
    report_max_delay_seconds: int = Field(
        default=5,
        ge=0,
        le=30,
        validation_alias=AliasChoices(
            "REPORT_MAX_DELAY_SECONDS",
            "OPLEDGER_REPORT_MAX_DELAY_SECONDS",
        ),
    )
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        validation_alias=AliasChoices("REDIS_URL", "OPLEDGER_REDIS_URL"),
    )
    report_queue_name: str = Field(
        default="reports",
        validation_alias=AliasChoices(
            "REPORT_QUEUE_NAME",
            "OPLEDGER_REPORT_QUEUE_NAME",
        ),
    )
    report_job_max_attempts: int = Field(
        default=3,
        ge=2,
        le=10,
        validation_alias=AliasChoices(
            "REPORT_JOB_MAX_ATTEMPTS",
            "OPLEDGER_REPORT_JOB_MAX_ATTEMPTS",
        ),
    )
    report_job_retry_backoff_seconds: str = Field(
        default="1,5",
        validation_alias=AliasChoices(
            "REPORT_JOB_RETRY_BACKOFF_SECONDS",
            "OPLEDGER_REPORT_JOB_RETRY_BACKOFF_SECONDS",
        ),
    )
    report_failure_injection_enabled: bool = Field(
        default=False,
        validation_alias=AliasChoices(
            "REPORT_FAILURE_INJECTION_ENABLED",
            "OPLEDGER_REPORT_FAILURE_INJECTION_ENABLED",
        ),
    )
    report_failure_injection_stage: ReportFailureInjectionStage = Field(
        default="none",
        validation_alias=AliasChoices(
            "REPORT_FAILURE_INJECTION_STAGE",
            "OPLEDGER_REPORT_FAILURE_INJECTION_STAGE",
        ),
    )

    model_config = SettingsConfigDict(env_prefix="OPLEDGER_", populate_by_name=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
