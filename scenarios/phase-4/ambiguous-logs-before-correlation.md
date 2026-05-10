# Ambiguous Logs Before Correlation

Use this scenario to see why correlation IDs matter when several report jobs
run close together.

## Goal

Run concurrent report work, compare unfiltered logs with correlation-filtered
evidence, and write a timeline that avoids unsupported claims.

## Preconditions

- Local Docker stack is available.
- Migrations have been applied.
- You understand `docs/observability/logging-and-correlation.md`.

## Steps

Start the stack and apply migrations:

```sh
./scripts/dev-up.sh
./scripts/migrate.sh --compose
```

Enqueue one report without a caller-supplied correlation ID and two with
explicit IDs:

```sh
curl -sS -X POST http://localhost:18080/reports/work-requests/summary/jobs
curl -sS -X POST \
  -H 'X-Correlation-ID: incident-correlation-a' \
  http://localhost:18080/reports/work-requests/summary/jobs
curl -sS -X POST \
  -H 'X-Correlation-ID: incident-correlation-b' \
  http://localhost:18080/reports/work-requests/summary/jobs
```

Inspect unfiltered evidence:

```sh
curl -sS http://localhost:18080/reports/jobs
docker compose logs --tail=200 api
docker compose logs --tail=200 worker
docker compose logs --tail=200 reporting
```

Then inspect one workflow by durable status and correlation ID:

```sh
curl -sS http://localhost:18080/reports/jobs/{id}
docker compose logs --tail=300 api
docker compose logs --tail=300 worker
docker compose logs --tail=300 reporting
```

Filter the log output in your terminal for `incident-correlation-a` or the
generated `correlation_id` returned by the API.

## Expected Observations

- Unfiltered logs can contain several `http_request`, `report_job_started`,
  `report_job_succeeded`, and reporting service render events close together.
- Each report job representation includes its `correlation_id`.
- API, worker, and reporting service logs include the same `correlation_id` for
  one workflow.
- Without filtering by `correlation_id`, it is easy to attach the wrong worker
  attempt or reporting service request to a job.

## Timeline Practice

Write two short timelines:

1. A deliberately cautious timeline from unfiltered logs only, naming what is
   still ambiguous.
2. A corrected timeline using one report job ID and its `correlation_id`.

## Explain What Happened

- What claim could you not safely make from unfiltered logs?
- Which field joined HTTP, worker, reporting service, and durable job evidence?
- How did the generated correlation ID differ from the caller-supplied IDs?
- Why should an LLM reviewer challenge a timeline with no IDs?

## Cleanup

```sh
./scripts/dev-down.sh
```
