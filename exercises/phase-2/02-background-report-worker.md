# Background Report Worker

## Phase

Phase 2: Async After Synchronous Pain. This exercise belongs here because the
learner has already measured synchronous report latency and can now move that
work into an explicit background worker.

## Concepts

- Redis-backed queues as transport, not source of truth.
- Worker processes that share the current codebase and database.
- Durable job status in Postgres.
- Request latency versus completion latency.
- Operational visibility when a worker is stopped.

## Prerequisites

- `exercises/phase-2/01-synchronous-report-pain.md`
- `exercises/TEMPLATE.md`
- `services/api/opledger_api/routes.py`
- `services/api/opledger_api/report_jobs.py`
- `services/api/opledger_api/worker.py`
- `services/api/opledger_api/models.py`
- `services/api/opledger_api/config.py`
- `docker-compose.yml`
- `docs/TECH_STACK.md`
- Local API, Postgres, Redis, and migration workflow.

## Build/Change Task

Generate the work request summary report through the queued path instead of the
synchronous request path. Start Postgres, Redis, the API, and the worker. Seed
customers and work requests, enqueue a report with
`POST /reports/work-requests/summary/jobs`, and use the returned job identifier
with `GET /reports/jobs/{report_job_id}` until the job reaches `finished`.

Compare this with the synchronous `POST /reports/work-requests/summary` route.
Record the HTTP response time for enqueueing, the later completion state, and
the persisted report payload.

## Constraints

- Do not add retries.
- Do not add idempotency or duplicate suppression.
- Do not extract a reporting service.
- Do not store authoritative report status only in Redis.
- Do not add Kubernetes or deployment orchestration.
- Keep Postgres as the durable record of report job requests and outcomes.
- Treat Redis as queue transport only.

## Failure Modes

- Returning success from the enqueue endpoint without a durable `report_jobs`
  row.
- Treating an RQ job id as the only inspectable status handle.
- Assuming queued work is complete when the enqueue request returns.
- Losing pending Redis jobs and having no Postgres evidence that work was
  requested.
- Running the API but forgetting the worker, leaving jobs in `queued`.
- Adding retries before duplicate execution and idempotency risks are discussed.

## Expected Reasoning

After completing the work, explain why the enqueue request can return quickly
while the report is still unfinished. Identify which state lives in Postgres,
which state lives temporarily in Redis, and what a user can inspect if Redis or
the worker is unavailable.

Explain why this phase keeps the worker in the same codebase instead of
extracting a reporting service.

## Verification

- Run `./scripts/verify.sh`.
- Start the local Docker stack with `./scripts/dev-up.sh`.
- Apply migrations with `./scripts/migrate.sh --compose`.
- Seed at least two customers and work requests through the API.
- Call `POST /reports/work-requests/summary` and record the synchronous
  response.
- Call `POST /reports/work-requests/summary/jobs` and record the returned job
  id and response time.
- Call `GET /reports/jobs/{report_job_id}` until the job is `finished` and
  confirm `result_json` contains the report.
- Stop only the worker, enqueue another report, and confirm the job remains
  `queued` until a worker is running again.
- Inspect Postgres and confirm report job rows persist independently of Redis.

## Reflection Questions

- What got faster for the HTTP caller when the report moved to the queue?
- What got more complicated operationally?
- Why is Redis not the system of record for report status?
- What does the user see when the worker is stopped?
- What new duplicate execution risks will matter before retries are added?
- Why is a second process different from a second service?

## LLM Usage

Use an LLM after collecting your own timing and status evidence. Ask it to
challenge whether your observations prove the request path improved, whether
your source-of-truth explanation is precise, and what failure modes remain
before retries are safe. Do not ask it to invent operational evidence.

## Path-Specific Extensions

Backend: add a focused test around job status inspection and explain why it
does not require a live Redis instance.

Operations: stop the worker, enqueue work, inspect logs and database rows, then
restart the worker and observe recovery.

Architecture: draw the synchronous report path and the queued report path, then
mark where Postgres and Redis are used.

Interview: practice explaining why the worker shares the API codebase and why
service extraction is still deferred.

## Deployment/Debugging Actions If Relevant

Run the worker locally with:

```sh
./scripts/worker.sh
```

Run the full local Docker stack with:

```sh
./scripts/dev-up.sh
```

In Docker Compose, the `worker` service processes the same `reports` queue that
the API uses. If jobs stay `queued`, check that Redis is healthy, migrations
have run, the worker is running, and `OPLEDGER_REDIS_URL` points at the same
Redis instance for both API and worker.
