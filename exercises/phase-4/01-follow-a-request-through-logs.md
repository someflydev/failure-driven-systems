# Follow A Request Through Logs

## Phase

Phase 4: Observability And Incidents. This work belongs here because async jobs
and the reporting service have made one user action span several processes.

## Concepts

- Structured logs
- Request IDs
- Correlation IDs
- Async job evidence
- Incident timelines
- Secret-safe operational notes

## Prerequisites

- `docs/observability/logging-and-correlation.md`
- `docs/async/phase-2-job-lifecycle.md`
- `docs/contracts/report-rendering-v1.md`
- `scenarios/phase-2/worker-unavailable.md`
- `scenarios/phase-3/reporting-timeout.md`
- Local Docker Compose workflow and migrations

## Build/Change Task

Run one report job and collect enough evidence to trace it from the API enqueue
request through worker execution and, when configured, the reporting service.
Use a caller-supplied `X-Correlation-ID` so every process should log the same
workflow identifier.

Write a short incident-style timeline that names the API response, durable
`report_jobs` state, worker logs, reporting service logs, and final job result.

## Constraints

- Do not add Prometheus, tracing, dashboards, or a log aggregation service.
- Do not log request bodies, credentials, tokens, full connection strings, or
  raw exception text.
- Do not treat Redis as the source of truth for user-visible job status.
- Keep the evidence small enough that a human can inspect it in terminal logs.

## Failure Modes

- The API generates a job but the worker logs cannot be connected to it.
- A retry creates several attempts with no shared workflow identifier.
- The reporting service times out but the evidence does not show which job was
  affected.
- Notes include secrets copied from config output or exception text.
- The timeline describes guesses instead of observable facts.

## Expected Reasoning

After completing the exercise, explain why request IDs and correlation IDs are
different, why the correlation ID is persisted on the job row, and why this was
introduced after async and service-boundary failures rather than in Phase 1.

## Verification

- Run `./scripts/verify.sh`.
- Start the local stack and apply migrations.
- Enqueue a report with `X-Correlation-ID: corr-demo-1`.
- Confirm the API response and `GET /reports/jobs/{id}` include
  `correlation_id`.
- Confirm API, worker, and reporting logs contain `correlation_id`.
- Confirm no copied evidence includes a full `DATABASE_URL` or secrets.

## Reflection Questions

- Which single field let you connect the HTTP request, worker attempt, and
  reporting service call?
- What could you prove from Postgres even if Redis was unavailable?
- What timing question is still hard to answer without metrics or traces?
- What would make a larger observability stack worth its operational cost?

## LLM Usage

Use an LLM as an incident-review partner after collecting evidence. Ask it to
challenge unsupported claims, identify missing timestamps or IDs, and point out
any secret-handling risks. Do not ask it to invent a timeline you did not
observe.

## Path-Specific Extensions

Backend: add one focused test around a missing or caller-supplied correlation
ID.

Operations: repeat the exercise during the reporting timeout scenario and
compare successful and failed timelines.

Architecture: write a short note explaining why correlation IDs are useful even
if the reporting service is folded back into the monolith.

Interview: practice explaining why logs, metrics, and traces answer different
debugging questions.

## Deployment/Debugging Actions If Relevant

Use local Compose logs first:

```sh
docker compose logs --tail=100 api
docker compose logs --tail=100 worker
docker compose logs --tail=100 reporting
```

Filter by the chosen `correlation_id` and record only sanitized evidence.
