# Metrics

OpsLedger exposes lightweight Prometheus-compatible text metrics from the API
and reporting service at `/metrics`. These endpoints are intended for local or
internal network access. Do not publish them directly to the internet without an
authenticating proxy or network rule; metric labels can reveal route names,
status patterns, and operational shape even when they avoid customer data.

The implementation uses a small in-process registry instead of a full
observability stack. That is enough for Phase 4 because the questions are
practical: is traffic arriving, are requests slow, are jobs completing, and is
the reporting boundary failing?

## Metric Reference

`opledger_http_requests_total{service,method,path,status}`

- Question: How many requests is each service handling, and what statuses are
  they returning?
- Labels: `service` is `opledger-api` or `opledger-reporting`; `path` uses the
  FastAPI route template, not raw IDs.
- Use it to compare request rate and response status mix.

`opledger_http_request_duration_seconds_bucket|count|sum{service,method,path}`

- Question: Which API or reporting routes are slow?
- Labels avoid customer IDs by using route templates.
- Use histogram buckets for rough latency shape and `sum / count` for average
  latency over a short local window.

`opledger_api_errors_total{service,method,path,status}`

- Question: Which routes are producing server-side failures?
- Counts HTTP `5xx` responses and unhandled exceptions observed by middleware.
- This is not a validation-error counter; `4xx` responses are usually caller or
  domain feedback, not service failure.

`opledger_report_jobs_queued_total{report_type}`

- Question: Are report jobs making it from the API into Redis?
- Incremented only after the durable job exists and the Redis job ID is saved.
- If this stays flat while enqueue requests fail, inspect API logs and durable
  failed jobs for queue-unavailable evidence.

`opledger_report_jobs_completed_total{report_type,status}`

- Question: Are report jobs succeeding or failing?
- `status` is `succeeded` or `failed`.
- The durable `/reports/jobs` endpoint remains the source of truth for specific
  job IDs, attempt counts, last error, and result availability.

`opledger_worker_job_failures_total{job_type,error_class}`

- Question: Is the worker failing job attempts, and what broad class of failure
  is it seeing?
- `error_class` is a Python exception class such as `ReportingServiceError` or
  `ValueError`. Do not add raw error messages as labels.

`opledger_reporting_service_call_duration_seconds_bucket|count|sum{report_type,outcome}`

- Question: Is the worker's call to the extracted reporting service slow?
- `outcome` is `succeeded` or `failed`.
- Use this with reporting service request latency to distinguish slow network
  calls from slow rendering.

`opledger_reporting_service_failures_total{report_type,reason}`

- Question: Why is the worker failing at the reporting boundary?
- Reasons are bounded values such as `timeout`, `non_2xx_status_503`,
  `invalid_response_json`, and `invalid_response_contract`.

`opledger_notification_attempts_total{channel,status}`

- Question: Are report-completion notification attempts succeeding or failing?
- Current `channel` is `local_log`; `status` is `sent` or `failed`.
- Durable notification attempts remain available at `/notification-attempts`
  for specific target inspection.

`opledger_cache_access_total{endpoint,outcome}`

- Question: Is the deliberately cached dashboard endpoint hitting Redis,
  missing Redis, bypassing cache, or falling back because Redis is unavailable?
- Current `endpoint` is `dashboard_customer_work_request_stats`.
- `outcome` is a bounded value such as `hit`, `miss`, `bypass`,
  `unavailable`, or `write_failed`.
- Use it with `docs/performance/caching.md` to compare cache behavior with
  source-of-truth reads and read-model staleness.

## Worker Exposure Limitation

The RQ worker is not an HTTP service, so it does not expose its own `/metrics`
endpoint. Its job outcome, worker failure, reporting-call, and notification
metrics are in-process counters inside the worker process. In the current local
setup, durable status queries are the reliable cross-process inspection surface:

- `GET /reports/jobs`
- `GET /reports/jobs/{report_job_id}`
- `GET /notification-attempts`

A later phase can justify a push gateway, sidecar exporter, or dedicated worker
metrics port. Phase 4 deliberately avoids that extra moving part.

## Label Rules

- Use route templates, not raw URLs with IDs.
- Do not label by customer ID, work request ID, report job ID, email, request
  ID, correlation ID, idempotency key, or error message.
- Keep reason and status labels bounded to known categories.
- Add a metric only when it answers an operational question you would act on.
