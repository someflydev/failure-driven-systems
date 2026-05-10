# Worker Stalled Incident

Use this scenario to practice response when jobs are accepted but no worker is
making progress.

## Goal

Stop the worker, enqueue reports, distinguish accepted work from completed
work, and write status updates that do not overpromise.

## Preconditions

- Local Docker stack is available.
- Migrations have been applied.
- You understand `docs/async/phase-2-job-lifecycle.md`.
- You understand `exercises/phase-4/01-follow-a-request-through-logs.md`.

## Steps

Start the stack and apply migrations:

```sh
./scripts/dev-up.sh
./scripts/migrate.sh --compose
```

Stop only the worker:

```sh
docker compose stop worker
```

Enqueue two reports with correlation IDs:

```sh
curl -sS -X POST \
  -H 'X-Correlation-ID: incident-worker-stalled-1' \
  http://localhost:18080/reports/work-requests/summary/jobs
curl -sS -X POST \
  -H 'X-Correlation-ID: incident-worker-stalled-2' \
  http://localhost:18080/reports/work-requests/summary/jobs
```

Inspect status surfaces:

```sh
curl -sS http://localhost:18080/reports/jobs
curl -sS http://localhost:18080/reports/jobs/{id}
curl -sS http://localhost:18080/reports/jobs/{id}/result
docker compose logs --tail=100 api
docker compose logs --tail=100 worker
curl -sS http://localhost:18080/metrics
```

Restart the worker, then watch the same job IDs finish:

```sh
docker compose start worker
curl -sS http://localhost:18080/reports/jobs/{id}
docker compose logs --tail=150 worker
```

## Expected Observations

- The API can return `202 Accepted` while the worker is stopped.
- Jobs stay visible through `/reports/jobs` with `status=queued`.
- The result endpoint returns `409 report_result_unavailable` before success.
- API request logs include enqueue traffic and the supplied correlation IDs.
- Worker logs are absent or stale while the worker is stopped, then show
  `report_job_started` and `report_job_succeeded` after restart.
- API metrics may show enqueue requests, but durable status is the reliable
  cross-process surface for specific stalled jobs.

## Status Update Practice

Write a first update that says report generation is delayed, not that report
data is lost. Write a second update after the worker restarts and durable job
status proves recovery.

## Explain What Happened

- Which facts prove work was accepted?
- Which facts prove work was not progressing?
- Why is `queued` not proof that a worker is healthy?
- What would be a reasonable next check if jobs stayed queued after restart?

## Cleanup

```sh
docker compose start worker
./scripts/dev-down.sh
```
