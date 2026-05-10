# Report Jobs Stuck Runbook

Use this when report jobs are accepted but remain `queued` or `running` longer
than expected. The goal is to gather evidence and restore progress without
changing product code during the incident.

## Scope

This runbook covers local or small-deployment report jobs backed by Postgres,
Redis/RQ, the worker process, and optionally the reporting service. It does not
require production traffic, destructive database actions, or new
infrastructure.

## First Checks

Check API readiness:

```sh
curl -i http://127.0.0.1:18080/health/ready
```

List recent jobs:

```sh
curl -sS http://127.0.0.1:18080/reports/jobs
```

Inspect one affected job:

```sh
curl -sS http://127.0.0.1:18080/reports/jobs/{report_job_id}
curl -sS http://127.0.0.1:18080/reports/jobs/{report_job_id}/result
```

Record `id`, `status`, `correlation_id`, `redis_job_id`, `attempt_count`,
`started_at`, `finished_at`, `last_failed_at`, and `last_error`.

## Logs

Inspect recent process logs:

```sh
docker compose logs --tail=150 api
docker compose logs --tail=150 worker
docker compose logs --tail=150 reporting
```

Look for these events:

- `event=http_request` for enqueue and status endpoints.
- `event=report_job_started`.
- `event=report_job_succeeded`.
- `event=report_job_failed`.
- Reporting service `event=http_request` for
  `/reports/work-requests/summary/render`.
- `event=notification_sent` or `event=notification_failed` only after a report
  succeeds.

Filter by the job's `correlation_id` when possible.

## Metrics

Inspect raw metrics:

```sh
curl -sS http://127.0.0.1:18080/metrics
curl -sS http://127.0.0.1:18081/metrics
```

Useful exposed API signals:

- `opledger_report_jobs_queued_total`
- `opledger_http_requests_total`

Worker job outcome, worker failure, reporting-call, and notification counters
are recorded in the worker process, but the current worker does not expose an
HTTP `/metrics` endpoint. Use `/reports/jobs/{id}` for job-specific truth and
`/notification-attempts` for durable notification evidence.

## Interpretations

Queued with no worker logs:

- The API and Redis may have accepted work, but no worker is processing it.
- Check whether the worker process is running.
- In local Compose, `docker compose ps worker` and
  `docker compose start worker` are reasonable non-destructive actions.

Running with old `started_at`:

- The worker may be hung in report generation or waiting on the reporting
  service.
- Check worker logs and reporting service logs for the same `correlation_id`.
- Check reporting service HTTP latency metrics if the request reached the
  service.

Failed with `last_error`:

- The job reached a terminal failed state.
- Use `last_error`, worker `error_class`, and reporting failure metrics to
  distinguish timeout, non-2xx response, invalid JSON, invalid contract, or
  local failure injection.

Succeeded but notification failed:

- Report generation recovered or was not affected.
- Inspect `/notification-attempts` before widening the incident scope.

## Mitigation

- Restart a stopped local worker after recording evidence.
- Remove local failure injection and restart the stack if the incident was a
  drill.
- If the reporting service is failing, use
  `ops/runbooks/reporting-service-down.md`.
- Do not mark a job `succeeded` by hand or fabricate `result_json`.
- Do not delete Redis jobs or database rows to make dashboards look clean.

## Status Update

Use `ops/incidents/TEMPLATE_incident_status_update.md`. Include:

- User-visible impact.
- Number or sample of affected jobs.
- Current evidence source.
- Current hypothesis.
- Next action and next update time.

## Resolution Checks

- A newly enqueued report reaches `succeeded`.
- A previously stuck job either reaches `succeeded` or has a clear terminal
  `failed` state.
- Worker logs show recent `report_job_succeeded` or bounded failure evidence.
- New durable jobs stop accumulating the same `last_error`.
- Status updates reflect the verified state, not only a restarted process.
