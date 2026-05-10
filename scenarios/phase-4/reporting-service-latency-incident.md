# Reporting Service Latency Incident

Use this scenario to practice incident response when the reporting service is
slow enough to break report generation while the API still accepts work.

## Goal

Create a controlled latency incident, publish short status updates, and prove
the root cause with logs, metrics, and durable report job status.

## Preconditions

- Local Docker stack is available.
- Migrations can be applied.
- You understand `docs/observability/logging-and-correlation.md`.
- You understand `docs/observability/metrics.md`.
- The worker calls the reporting service through
  `OPLEDGER_REPORT_RENDERING_SERVICE_URL`.

## Steps

Start the stack with reporting service delay longer than the worker timeout:

```sh
OPLEDGER_REPORTING_FAILURE_INJECTION_ENABLED=true \
OPLEDGER_REPORTING_FAILURE_MODE=delay \
OPLEDGER_REPORTING_FAILURE_DELAY_SECONDS=5 \
OPLEDGER_REPORT_RENDERING_SERVICE_TIMEOUT_SECONDS=1 \
./scripts/dev-up.sh
./scripts/migrate.sh --compose
```

Capture baseline health and metrics:

```sh
curl -i http://localhost:18080/health/ready
curl -i http://localhost:18081/health/ready
curl -sS http://localhost:18080/metrics
curl -sS http://localhost:18081/metrics
```

Enqueue a report with a correlation ID:

```sh
curl -sS -X POST \
  -H 'X-Correlation-ID: incident-latency-1' \
  http://localhost:18080/reports/work-requests/summary/jobs
```

Before changing code, observe:

```sh
curl -sS http://localhost:18080/reports/jobs/{id}
curl -sS http://localhost:18080/reports/jobs/{id}/result
docker compose logs --tail=150 worker
docker compose logs --tail=150 reporting
curl -sS http://localhost:18080/metrics
curl -sS http://localhost:18081/metrics
```

## Expected Observations

- `/health/ready` can stay `200` for both API and reporting service because the
  service is alive even though rendering is too slow for the worker timeout.
- The enqueue request can return `202 Accepted`.
- The durable report job should move to `failed` after the worker attempt and
  include timeout evidence in `last_error`.
- Worker logs should include `event=report_job_started` and
  `event=report_job_failed` with `correlation_id=incident-latency-1`.
- Reporting service request logs should include the render route,
  `correlation_id=incident-latency-1`, and high `duration_ms`.
- API metrics should show report enqueue traffic, while the durable job
  `last_error` shows the worker's timeout reason. Reporting service metrics
  and logs should show the slow render request if the request reached the
  service.

## Status Update Practice

Write two updates using `ops/incidents/TEMPLATE_incident_status_update.md`:

1. First update after you know reports are failing but before root cause is
   confirmed.
2. Second update after you connect worker timeout evidence to slow reporting
   service logs and metrics.

## Explain What Happened

- Which user workflow was affected?
- Why did API readiness stay healthy?
- Which metric or log proved the latency was at the reporting boundary?
- Which durable job fields prove the affected report's final state?
- What would you monitor after removing the injected delay?

## Cleanup

```sh
./scripts/dev-down.sh
```
