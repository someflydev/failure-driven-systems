# Phase 2 Job Lifecycle

OpsLedger report generation is asynchronous in Phase 2, but job truth remains
durable. Redis coordinates queued execution. Postgres records what the user can
trust.

## Lifecycle

`ReportJob` rows move through these statuses:

- `queued`: the API accepted the report request, persisted a `report_jobs` row,
  and attempted to hand execution to Redis/RQ.
- `running`: a worker loaded the durable job row and started generating the
  report.
- `succeeded`: the worker finished generation and committed `result_json` in
  Postgres.
- `failed`: enqueueing or report generation failed, and the row contains an
  `error_message` for inspection.

The enqueue endpoint returns `202 Accepted` because the request has been
accepted for later work. It does not mean the report exists yet.

## Ownership

Postgres owns durable user-visible state:

- report job id
- report type
- current status
- Redis job id, when enqueueing reached Redis
- start and finish timestamps
- failure representation
- completed report output

Redis owns ephemeral coordination:

- queue membership
- worker delivery
- RQ's temporary execution metadata

Redis is not the source of truth. If Redis is restarted, flushed, or otherwise
loses pending work, the Postgres `report_jobs` row still shows that a report was
requested and did not reach `succeeded`.

## API Expectations

Users can safely assume:

- `POST /reports/work-requests/summary/jobs` creates an inspectable job record
  before returning.
- `GET /reports/jobs/{report_job_id}` reports the durable job state from
  Postgres.
- `GET /reports/jobs` lists recent durable report jobs.
- `GET /reports/jobs/{report_job_id}/result` returns a report only after the
  durable row is `succeeded` and `result_json` exists.

Users should not assume:

- `202 Accepted` means report generation has started.
- `queued` means Redis still has a deliverable job.
- an RQ job id is a durable user-facing status handle.
- a worker crash or Redis loss will be hidden by the status API.

The result endpoint must not report success early. Until Postgres contains the
completed report output, the API should tell the caller the result is
unavailable rather than inventing success from queue or worker metadata.
