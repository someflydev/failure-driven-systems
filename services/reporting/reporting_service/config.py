from functools import lru_cache
from typing import Literal

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ReportingFailureMode = Literal[
    "none",
    "delay",
    "http_500",
    "malformed_response",
    "incompatible_response",
]

LOCAL_FAILURE_INJECTION_ENVIRONMENTS = {"local", "local-docker", "test", "development"}


class ReportingServiceSettings(BaseSettings):
    environment: str = Field(
        default="local",
        validation_alias=AliasChoices("ENVIRONMENT", "OPLEDGER_ENVIRONMENT"),
    )
    failure_injection_enabled: bool = Field(
        default=False,
        validation_alias=AliasChoices(
            "REPORTING_FAILURE_INJECTION_ENABLED",
            "OPLEDGER_REPORTING_FAILURE_INJECTION_ENABLED",
        ),
    )
    failure_mode: ReportingFailureMode = Field(
        default="none",
        validation_alias=AliasChoices(
            "REPORTING_FAILURE_MODE",
            "OPLEDGER_REPORTING_FAILURE_MODE",
        ),
    )
    failure_delay_seconds: float = Field(
        default=0.0,
        ge=0,
        le=30,
        validation_alias=AliasChoices(
            "REPORTING_FAILURE_DELAY_SECONDS",
            "OPLEDGER_REPORTING_FAILURE_DELAY_SECONDS",
        ),
    )

    model_config = SettingsConfigDict(env_prefix="OPLEDGER_", populate_by_name=True)

    @property
    def local_failure_injection_active(self) -> bool:
        return (
            self.failure_injection_enabled
            and self.environment in LOCAL_FAILURE_INJECTION_ENVIRONMENTS
        )


@lru_cache
def get_settings() -> ReportingServiceSettings:
    return ReportingServiceSettings()
