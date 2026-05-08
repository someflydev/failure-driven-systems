from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, datetime

import pytest
from rq import Retry
from sqlalchemy.orm import Session

from opledger_api import report_jobs
from opledger_api.config import Settings
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
        assert running_job.attempt_count == 1
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
    assert report_job.last_error is None
    assert report_job.last_failed_at is None
    assert report_job.attempt_count == 1
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
    assert report_job.last_error == "ValueError"
    assert report_job.last_failed_at is not None
    assert report_job.finished_at is not None
    assert report_job.attempt_count == 1
    assert report_job.result_json is None


def test_report_worker_retry_attempt_count_changes_after_failure(
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report_job = ReportJob(report_type="work_request_summary", status="queued")
    db_session.add(report_job)
    db_session.commit()
    patch_report_job_session(monkeypatch, db_session)

    build_calls = 0

    def flaky_build_report(_session: Session) -> dict[str, object]:
        nonlocal build_calls
        build_calls += 1
        if build_calls == 1:
            raise ValueError("first attempt failed")
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
        report_jobs, "build_work_request_summary_report", flaky_build_report
    )

    with pytest.raises(ValueError, match="first attempt failed"):
        report_jobs.generate_work_request_summary_report_job(report_job.id)

    db_session.refresh(report_job)
    assert report_job.status == "failed"
    assert report_job.attempt_count == 1
    assert report_job.last_error == "ValueError"

    report_jobs.generate_work_request_summary_report_job(report_job.id)

    db_session.refresh(report_job)
    assert report_job.status == "succeeded"
    assert report_job.attempt_count == 2
    assert report_job.last_error is None
    assert report_job.result_json is not None


def test_duplicate_report_worker_execution_keeps_existing_output(
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report_job = ReportJob(report_type="work_request_summary", status="queued")
    db_session.add(report_job)
    db_session.commit()
    patch_report_job_session(monkeypatch, db_session)

    build_calls = 0

    def fake_build_report(_session: Session) -> dict[str, object]:
        nonlocal build_calls
        build_calls += 1
        return {
            "generated_at": datetime(2026, 1, 1, tzinfo=UTC),
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
    original_result = report_job.result_json

    report_jobs.generate_work_request_summary_report_job(report_job.id)
    db_session.refresh(report_job)

    assert build_calls == 1
    assert report_job.status == "succeeded"
    assert report_job.attempt_count == 1
    assert report_job.result_json == original_result


def test_report_failure_injection_records_error(
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report_job = ReportJob(report_type="work_request_summary", status="queued")
    db_session.add(report_job)
    db_session.commit()
    patch_report_job_session(monkeypatch, db_session)
    monkeypatch.setattr(
        report_jobs,
        "get_settings",
        lambda: Settings(
            environment="test",
            report_failure_injection_enabled=True,
            report_failure_injection_stage="before_generation",
        ),
    )

    with pytest.raises(report_jobs.InjectedReportFailure):
        report_jobs.generate_work_request_summary_report_job(report_job.id)

    db_session.refresh(report_job)
    assert report_job.status == "failed"
    assert report_job.error_message == "InjectedReportFailure"
    assert report_job.last_error == "InjectedReportFailure"
    assert report_job.attempt_count == 1
    assert report_job.last_failed_at is not None


def test_report_failure_injection_is_ignored_outside_local_and_test(
    db_session: Session,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report_job = ReportJob(report_type="work_request_summary", status="queued")
    db_session.add(report_job)
    db_session.commit()
    patch_report_job_session(monkeypatch, db_session)
    monkeypatch.setattr(
        report_jobs,
        "get_settings",
        lambda: Settings(
            environment="production",
            report_failure_injection_enabled=True,
            report_failure_injection_stage="before_generation",
        ),
    )

    report_jobs.generate_work_request_summary_report_job(report_job.id)

    db_session.refresh(report_job)
    assert report_job.status == "succeeded"
    assert report_job.attempt_count == 1


def test_report_job_enqueue_uses_bounded_retry_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_retry: object | None = None

    class FakeRedisJob:
        id = "rq-job-1"

    class FakeQueue:
        def enqueue(
            self, _func: object, _report_job_id: int, **kwargs: object
        ) -> object:
            nonlocal captured_retry
            captured_retry = kwargs["retry"]
            return FakeRedisJob()

    monkeypatch.setattr(report_jobs, "get_report_queue", lambda _settings: FakeQueue())

    redis_job_id = report_jobs.enqueue_work_request_summary_report(
        1,
        Settings(
            report_job_max_attempts=4,
            report_job_retry_backoff_seconds="2,4,8",
        ),
    )

    assert redis_job_id == "rq-job-1"
    assert isinstance(captured_retry, Retry)
    assert captured_retry.max == 3
    assert captured_retry.intervals == [2, 4, 8]


def test_report_retry_configuration_is_finite_and_rejects_negative_backoff() -> None:
    retry = report_jobs.report_retry(
        Settings(report_job_max_attempts=2, report_job_retry_backoff_seconds="0")
    )

    assert retry.max == 1
    assert retry.intervals == [0]

    with pytest.raises(ValueError, match="cannot be negative"):
        report_jobs.report_retry(
            Settings(report_job_max_attempts=2, report_job_retry_backoff_seconds="-1")
        )


def test_report_worker_raises_for_missing_durable_job(
    monkeypatch: pytest.MonkeyPatch,
    db_session: Session,
) -> None:
    patch_report_job_session(monkeypatch, db_session)

    with pytest.raises(RuntimeError, match="ReportJob 999 was not found"):
        report_jobs.generate_work_request_summary_report_job(999)
