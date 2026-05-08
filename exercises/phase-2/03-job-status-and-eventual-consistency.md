# Job Status and Eventual Consistency

## Phase

Phase 2: Async After Synchronous Pain. This exercise belongs here because the
learner has moved report work behind a queue and must now design what users see
while completion is delayed.

## Concepts

- `202 Accepted` versus completed work.
- Durable job state in Postgres.
- Redis/RQ as ephemeral queue coordination.
- User-visible eventual consistency.
- Polling status without overstating certainty.
- Completed output availability as a separate fact from accepted work.

## Prerequisites

- `exercises/phase-2/01-synchronous-report-pain.md`
- `exercises/phase-2/02-background-report-worker.md`
- `docs/async/phase-2-job-lifecycle.md`
- `exercises/TEMPLATE.md`
- `services/api/opledger_api/routes.py`
- `services/api/opledger_api/report_jobs.py`
- `services/api/opledger_api/models.py`
- `services/api/opledger_api/schemas.py`
- `services/api/tests/test_crud_api.py`
- `services/api/tests/test_report_jobs.py`
- Local API, Postgres, Redis, worker, and migration workflow.

## Build/Change Task

Use the queued work request summary report path and observe the full job
lifecycle. Enqueue a report, inspect the returned job id, poll
`GET /reports/jobs/{report_job_id}`, list recent jobs with `GET /reports/jobs`,
and fetch completed output with `GET /reports/jobs/{report_job_id}/result` only
after the job reaches `succeeded`.

Write a short explanation of what the API has promised at each point:

- when the enqueue request returns `202 Accepted`
- while the job is `queued`
- while the job is `running`
- when the job is `failed`
- when the job is `succeeded` and result output exists

## Constraints

- Do not add retries.
- Do not add idempotency or duplicate suppression.
- Do not store authoritative job state in Redis.
- Do not report a successful result before `result_json` exists in Postgres.
- Do not replace polling with webhooks or realtime notifications.
- Keep the report worker inside the existing API codebase.

## Failure Modes

- Treating `202 Accepted` as if the user already has a report.
- Showing a "complete" state when the durable output is still missing.
- Using Redis or an RQ id as the only user-facing source of truth.
- Hiding queue enqueue failures instead of persisting a failed job row.
- Leaving a user with no way to distinguish queued, running, failed, and
  succeeded work.
- Forgetting that a queued Postgres row may outlive ephemeral Redis state.

## Expected Reasoning

After completing the work, explain why asynchronous systems require an explicit
user-facing state model. Describe what "accepted" means, why the caller must
poll or otherwise wait for completion, and why a completed report requires both
`status = succeeded` and durable output in Postgres.

Explain what a user can safely infer when Redis is unavailable, when the worker
is stopped, and when a job is failed.

## Verification

- Run `./scripts/verify.sh`.
- Start the local stack with `./scripts/dev-up.sh`.
- Apply migrations with `./scripts/migrate.sh --compose`.
- Enqueue a report with `POST /reports/work-requests/summary/jobs`.
- Confirm `GET /reports/jobs/{report_job_id}` shows `queued`, `running`,
  `succeeded`, or `failed` from Postgres.
- Confirm `GET /reports/jobs` includes the recent job.
- Confirm `GET /reports/jobs/{report_job_id}/result` does not return output
  before durable output exists.
- Stop the worker, enqueue a report, and explain why `queued` does not prove
  the report will finish without a worker.

## Reflection Questions

- What exactly did the API accept when it returned `202 Accepted`?
- Why is a job id different from a report result?
- Which statuses are user-visible, and what should the UI say for each?
- Why is Redis useful even though it is not durable truth?
- What would be misleading about returning report output from queue metadata?
- What future retry or idempotency work would change the lifecycle?

## LLM Usage

Use an LLM as a reviewer after you have captured your own status observations.
Ask it to challenge your explanation of "accepted", identify where your UI
language might overpromise, and find any path where the API could report
success before Postgres has output. Do not ask it to invent lifecycle evidence.

## Path-Specific Extensions

Backend: add or review tests for each durable status and for result
unavailability before completion.

Operations: stop Redis or the worker and compare what disappears from runtime
coordination with what remains inspectable in Postgres.

Architecture: diagram the enqueue, worker, status, and result paths, marking
which component owns each fact.

Interview: practice explaining `202 Accepted` and eventual consistency without
using vague phrases like "it happens in the background" as the whole answer.

## Deployment/Debugging Actions If Relevant

Run the API, Postgres, Redis, and worker locally with:

```sh
./scripts/dev-up.sh
```

Run migrations with:

```sh
./scripts/migrate.sh --compose
```

If a job stays `queued`, verify that the worker is running, Redis is reachable,
both API and worker use the same Redis URL and queue name, and the durable row
exists in Postgres.
