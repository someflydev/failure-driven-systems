# Lightweight Metrics Dashboard Sketch

OpsLedger does not require Grafana or a Prometheus container for Phase 4. If
you do run a local Prometheus later, start with a few panels or ad hoc queries
that answer specific debugging questions.

## API Traffic

Request rate by route:

```promql
sum by (service, method, path) (rate(opledger_http_requests_total[5m]))
```

Server error rate by route:

```promql
sum by (service, method, path, status) (rate(opledger_api_errors_total[5m]))
```

Approximate p95 route latency:

```promql
histogram_quantile(
  0.95,
  sum by (service, method, path, le) (
    rate(opledger_http_request_duration_seconds_bucket[5m])
  )
)
```

## Report Jobs

Queued reports:

```promql
sum by (report_type) (rate(opledger_report_jobs_queued_total[5m]))
```

Succeeded versus failed report jobs:

```promql
sum by (report_type, status) (rate(opledger_report_jobs_completed_total[5m]))
```

Worker failures by broad exception class:

```promql
sum by (job_type, error_class) (rate(opledger_worker_job_failures_total[5m]))
```

## Reporting Boundary

Reporting service call failures by reason:

```promql
sum by (report_type, reason) (
  rate(opledger_reporting_service_failures_total[5m])
)
```

Average reporting service call latency by outcome:

```promql
sum by (report_type, outcome) (
  rate(opledger_reporting_service_call_duration_seconds_sum[5m])
)
/
sum by (report_type, outcome) (
  rate(opledger_reporting_service_call_duration_seconds_count[5m])
)
```

## Notifications

Notification attempts by result:

```promql
sum by (channel, status) (rate(opledger_notification_attempts_total[5m]))
```

## Local Scrape Checks

Without Prometheus, inspect the raw endpoint directly:

```sh
curl -s http://127.0.0.1:18080/metrics
curl -s http://127.0.0.1:18081/metrics
```

Treat these as internal endpoints. If a production deployment exposes them,
put them behind private networking, firewall rules, an authenticating proxy, or
set `OPLEDGER_METRICS_ACCESS_TOKEN` and pass the token as a bearer token or
`X-OpsLedger-Metrics-Token` header.
