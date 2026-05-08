# Phase 2 Job Lifecycle

OpsLedger report generation is asynchronous in Phase 2, but job truth remains
durable. Redis coordinates queued execution. Postgres records what the user can
trust.

## Lifecycle

`ReportJob` rows move through these statuses:

- `queued`: the API accepted the report request, persisted a `report_jobs` row,
  and attempted to hand execution to Redis/RQ.
- `running`: a worker loaded the durable job row and started generating the
  report. Each transition into `running` increments `attempt_count`.
- `succeeded`: the worker finished generation and committed `result_json` in
  Postgres.
- `failed`: enqueueing or report generation failed, and the row contains an
  `error_message` and `last_error` for inspection. A failed worker attempt can
  be retried by RQ, so a row may move from `failed` back to `running` before it
  eventually reaches `succeeded` or exhausts retries.

The enqueue endpoint returns `202 Accepted` because the request has been
accepted for later work. It does not mean the report exists yet.

## Ownership

Postgres owns durable user-visible state:

- report job id
- report type
- current status
- Redis job id, when enqueueing reached Redis
- attempt count
- start, finish, and last failure timestamps
- failure representation through `error_message` and `last_error`
- completed report output

Redis owns ephemeral coordination:

- queue membership
- worker delivery
- RQ's temporary execution metadata
- retry scheduling between worker attempts

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

## Retry Behavior

Report jobs use explicit bounded RQ retries. OpsLedger configures
`OPLEDGER_REPORT_JOB_MAX_ATTEMPTS=3` by default, which means one original
attempt plus two retries. The retry object passed to RQ is
`Retry(max=2, interval=[1, 5])` when defaults are used. RQ's `Retry.max` counts
retry executions after the original attempt, not total attempts. RQ's
`interval` values are seconds to wait before retrying; when retry counts exceed
the number of configured intervals, RQ reuses the last interval value.

The default retry backoff is configured through
`OPLEDGER_REPORT_JOB_RETRY_BACKOFF_SECONDS=1,5`. The list must contain
non-negative integers. Empty values are ignored. Retries are never unbounded;
`OPLEDGER_REPORT_JOB_MAX_ATTEMPTS` is validated between 2 and 10.

RQ jobs have no retry policy when `retry=None` is passed. When an RQ `Retry`
object is used, the library default `interval` is `0`, meaning retry without a
delay. OpsLedger does not rely on that default; it passes the configured
interval list explicitly.

Every worker attempt persists evidence before report generation begins:

- `attempt_count` increments once per worker execution.
- `started_at` records the most recent attempt start time.
- `finished_at` is cleared when a new attempt starts and records the latest
  terminal success or failure time.
- `last_failed_at` records the most recent failed worker attempt.
- `last_error` records the exception class from the most recent failed attempt
  and is cleared on success.

This state is intentionally not enough to make retries idempotent. A retry can
run report code more than once. Before adding duplicate suppression, learners
should inspect which side effects could be repeated.

## Local Failure Injection

Report worker failure injection is disabled by default and limited to
`environment = local` or `environment = test`. Enable it only for local learning
or tests:

```sh
OPLEDGER_REPORT_FAILURE_INJECTION_ENABLED=true
OPLEDGER_REPORT_FAILURE_INJECTION_STAGE=before_generation
```

Supported stages are:

- `none`: no injected failure.
- `before_generation`: fail after the worker marks the durable job `running`
  and increments `attempt_count`, before report generation runs.
- `after_partial_progress`: fail after the report is built but before the
  durable result is committed.

If these settings are accidentally enabled outside local/test, the worker
ignores the injection. Real worker exceptions are still persisted as failed
attempt evidence and then re-raised so RQ can apply the bounded retry policy.
