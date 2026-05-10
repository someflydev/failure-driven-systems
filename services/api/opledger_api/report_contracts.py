"""Versioned report rendering contracts shared by report callers and renderers."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

REPORT_RENDERING_CONTRACT_VERSION: Literal["report-rendering.v1"] = (
    "report-rendering.v1"
)
WORK_REQUEST_SUMMARY_REPORT: Literal["work_request_summary"] = "work_request_summary"
REQUIRED_WORK_REQUEST_STATUSES = ("open", "in_progress", "resolved", "cancelled")

WorkRequestStatus = Literal["open", "in_progress", "resolved", "cancelled"]
ReportRenderingContractVersion = Literal["report-rendering.v1"]
ReportRenderingType = Literal["work_request_summary"]


class WorkRequestSummaryRenderRequest(BaseModel):
    contract_version: ReportRenderingContractVersion = REPORT_RENDERING_CONTRACT_VERSION
    report_type: ReportRenderingType = WORK_REQUEST_SUMMARY_REPORT
    generated_at: datetime
    total_work_requests: int = Field(ge=0)
    by_status: dict[WorkRequestStatus, int]
    status_event_count: int = Field(ge=0)
    requested_by: str | None = None

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="after")
    def status_counts_are_complete_and_consistent(
        self,
    ) -> "WorkRequestSummaryRenderRequest":
        if set(self.by_status) != set(REQUIRED_WORK_REQUEST_STATUSES):
            raise ValueError("Status counts must include every work request status.")
        if any(count < 0 for count in self.by_status.values()):
            raise ValueError("Status counts cannot be negative.")
        if sum(self.by_status.values()) != self.total_work_requests:
            raise ValueError("Status counts must add up to total_work_requests.")
        return self


class WorkRequestSummaryReport(BaseModel):
    contract_version: ReportRenderingContractVersion = REPORT_RENDERING_CONTRACT_VERSION
    report_type: ReportRenderingType = WORK_REQUEST_SUMMARY_REPORT
    generated_at: datetime
    total_work_requests: int = Field(ge=0)
    by_status: dict[WorkRequestStatus, int]
    status_event_count: int = Field(ge=0)
    warnings: list[str] = Field(default_factory=list)

    model_config = ConfigDict(extra="ignore")

    @model_validator(mode="after")
    def status_counts_are_complete_and_consistent(self) -> "WorkRequestSummaryReport":
        if set(self.by_status) != set(REQUIRED_WORK_REQUEST_STATUSES):
            raise ValueError("Status counts must include every work request status.")
        if any(count < 0 for count in self.by_status.values()):
            raise ValueError("Status counts cannot be negative.")
        if sum(self.by_status.values()) != self.total_work_requests:
            raise ValueError("Status counts must add up to total_work_requests.")
        return self
