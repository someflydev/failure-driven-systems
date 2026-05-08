from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, datetime

import pytest
from sqlalchemy.orm import Session

from opledger_api import report_jobs
from opledger_api.models import ReportJob


def patch_report_job_session(
    monkeypatch: pytest.MonkeyPatch, db_session: Session
) -> None:
    @contextmanager
    def fake_get_session() -> Generator[Session]:
        yield db_session

    monkeypatch.setattr(report_jobs, "get_session", fake_get_session)


def test_report_worker_marks_job_running_then_succeeded_with_result(
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report_job = ReportJob(report_type="work_request_summary", status="queued")
    db_session.add(report_job)
    db_session.commit()
    patch_report_job_session(monkeypatch, db_session)

    def fake_build_report(_session: Session) -> dict[str, object]:
        running_job = db_session.get(ReportJob, report_job.id)
        assert running_job is not None
        assert running_job.status == "running"
        assert running_job.started_at is not None
        return {
            "generated_at": datetime.now(UTC),
            "total_work_requests": 0,
            "by_status": {
                "open": 0,
                "in_progress": 0,
                "resolved": 0,
                "cancelled": 0,
            },
            "status_event_count": 0,
        }

    monkeypatch.setattr(
        report_jobs, "build_work_request_summary_report", fake_build_report
    )

    report_jobs.generate_work_request_summary_report_job(report_job.id)

    db_session.refresh(report_job)
    assert report_job.status == "succeeded"
    assert report_job.finished_at is not None
    assert report_job.error_message is None
    assert report_job.result_json is not None
    assert isinstance(report_job.result_json["generated_at"], str)


def test_report_worker_marks_job_failed_when_generation_raises(
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report_job = ReportJob(report_type="work_request_summary", status="queued")
    db_session.add(report_job)
    db_session.commit()
    patch_report_job_session(monkeypatch, db_session)

    def fail_build_report(_session: Session) -> dict[str, object]:
        raise ValueError("report failed")

    monkeypatch.setattr(
        report_jobs, "build_work_request_summary_report", fail_build_report
    )

    with pytest.raises(ValueError, match="report failed"):
        report_jobs.generate_work_request_summary_report_job(report_job.id)

    db_session.refresh(report_job)
    assert report_job.status == "failed"
    assert report_job.error_message == "ValueError"
    assert report_job.finished_at is not None
    assert report_job.result_json is None


def test_report_worker_raises_for_missing_durable_job(
    monkeypatch: pytest.MonkeyPatch,
    db_session: Session,
) -> None:
    patch_report_job_session(monkeypatch, db_session)

    with pytest.raises(RuntimeError, match="ReportJob 999 was not found"):
        report_jobs.generate_work_request_summary_report_job(999)
