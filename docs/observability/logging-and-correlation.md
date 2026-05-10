# Structured Logging And Correlation

Phase 4 adds structured logs because OpsLedger now has more than one runtime
path. A report request can pass through the API, Redis/RQ, a worker process,
and the reporting service before the durable job row reaches a final state.
Plain request logs were enough in Phase 1 because one process handled the
user-facing work synchronously. After async jobs and a service boundary, the
same incident can produce evidence in several processes.

## Log Format

Application logs are JSON objects written to stdout. The format stays simple so
it works in local Compose, Dokku logs, or a small VPS without requiring a log
aggregation stack.

Common fields:

- `timestamp`: UTC ISO timestamp.
- `level`: log level.
- `logger`: Python logger name.
- `service`: `opledger-api`, `opledger-worker`, or `opledger-reporting`.
- `environment`: configured OpsLedger environment.
- `event`: stable event name for filtering.
- `request_id`: one inbound HTTP request.
- `correlation_id`: one user-visible workflow across process boundaries.

HTTP request logs include `method`, `path`, `status`, and `duration_ms`.
Worker logs include `job_id`, `redis_job_id` when available, `attempt_count`,
`status`, and `duration_ms` when the attempt finishes.

Do not log request bodies, full connection strings, credentials, tokens, or
raw exception text that may contain sensitive values. Use error classes or
bounded failure reasons instead.

## Request And Correlation IDs

The API and reporting service accept `X-Request-ID` and `X-Correlation-ID`.
If the caller does not send them, the middleware generates a request ID and
uses it as the initial correlation ID. Both headers are returned on the HTTP
response.

For async report jobs:

1. The API records the active `correlation_id` on the `report_jobs` row.
2. The worker loads that durable `correlation_id` when it starts the job.
3. Worker logs include the same `correlation_id`.
4. If the worker calls the reporting service, it sends
   `X-Correlation-ID` on the HTTP request.
5. Reporting service request logs include that same `correlation_id`.
6. The final report job representation includes `correlation_id` so an
   operator can connect API responses, durable state, and logs.

## Why This Was Not Phase 1

Phase 1 had one API process and one database. Basic request logs and sanitized
readiness logs were enough to teach request handling, persistence, health, and
configuration without hiding the core system behind observability tooling.

Phase 4 introduces this after learners have already felt the ambiguity from
workers, retries, delayed completion, and a second reporting process. The
correlation fields solve an observed debugging problem instead of appearing as
architecture decoration.

## What Is Still Missing

This is not distributed tracing. It does not show parent/child spans, queue wait
time, or automatic cross-service timing waterfalls. It is also not metrics or
alerting. Those should be added only after learners can explain which user
impact or operational question the extra signal answers.

The current structure is enough to follow one report workflow through local
logs and durable state while keeping the VPS footprint small.
