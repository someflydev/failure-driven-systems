# Reporting Service Down Runbook

Use this when report jobs fail at the extracted reporting service boundary.
The service may be unavailable, slow, returning `5xx`, or returning a response
that violates `report-rendering.v1`.

## First Checks

Check reporting service health:

```sh
curl -i http://127.0.0.1:18081/health/live
curl -i http://127.0.0.1:18081/health/ready
```

Check API health and recent jobs:

```sh
curl -i http://127.0.0.1:18080/health/ready
curl -sS http://127.0.0.1:18080/reports/jobs
```

Inspect one failed job:

```sh
curl -sS http://127.0.0.1:18080/reports/jobs/{report_job_id}
```

Record `status`, `correlation_id`, `attempt_count`, `last_error`,
`last_failed_at`, and `finished_at`.

## Logs

Inspect worker and reporting service logs:

```sh
docker compose logs --tail=150 worker
docker compose logs --tail=150 reporting
```

Look for:

- Worker `event=report_job_failed`.
- Worker `error_class=ReportingServiceError`.
- Reporting service `event=http_request` for
  `/reports/work-requests/summary/render`.
- Shared `correlation_id` between the failed job, worker logs, and reporting
  service request logs.
- Reporting request `status` and `duration_ms`.

## Metrics

Inspect both metric surfaces:

```sh
curl -sS http://127.0.0.1:18080/metrics
curl -sS http://127.0.0.1:18081/metrics
```

Useful exposed signals:

- Reporting service `opledger_http_requests_total`
- Reporting service `opledger_http_request_duration_seconds_*`
- API `opledger_http_requests_total`
- API `opledger_report_jobs_queued_total`

Worker-side reporting failure counters are implemented in the worker process,
but the current worker does not expose an HTTP `/metrics` endpoint. Use the
failed job's `last_error`, worker logs, and reporting service HTTP logs for the
specific reason: `timeout`, `non_2xx_status_*`, `invalid_response_json`, or
`invalid_response_contract`.

## Interpretations

Health fails:

- The reporting service process is not serving correctly.
- Check process state and startup logs before changing API code.

Health passes but worker records `timeout`:

- The reporting service is live but too slow for
  `OPLEDGER_REPORT_RENDERING_SERVICE_TIMEOUT_SECONDS`.
- Compare reporting service `duration_ms` with worker timeout configuration.

Health passes and worker records `non_2xx_status_*`:

- The reporting service answered with an error response.
- Inspect reporting service logs for the same `correlation_id`.

Health passes and worker records invalid JSON or invalid contract:

- The service responded, but the worker rejected the response.
- Check `docs/contracts/report-rendering-v1.md` before changing schemas or
  storing partial data.

No reporting service logs for the correlation ID:

- The worker may not be configured to call the service, or the network request
  may fail before reaching it.
- Check `OPLEDGER_REPORT_RENDERING_SERVICE_URL` in sanitized form.

## Mitigation

- For local drills, disable reporting failure injection and restart the stack.
- If a recent deployment caused the issue, prefer restoring the last known
  working reporting service version or config before broad code changes.
- If the separate service is not needed for the current lesson or environment,
  removing `OPLEDGER_REPORT_RENDERING_SERVICE_URL` returns the worker to the
  in-process renderer.
- Do not increase timeouts blindly; first prove the service is slow and decide
  whether longer waits are acceptable for users.
- Do not weaken contract validation to store bad report data.

## Resolution Checks

- `/health/live` and `/health/ready` return `200`.
- A new report job reaches `succeeded`.
- Worker logs show `report_job_succeeded` for a new `correlation_id`.
- Reporting service logs show a render request with successful status and
  acceptable `duration_ms`.
- New failed jobs stop accumulating the same `last_error`.

## Follow-Up

Write a postmortem using `ops/incidents/TEMPLATE_postmortem.md` only after the
learner has built their own timeline from status, logs, and metrics.
