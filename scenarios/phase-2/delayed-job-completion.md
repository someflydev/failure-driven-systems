# Delayed Job Completion Scenario

Use this scenario to practice user-visible consistency while background work is
slow but still healthy.

## Goal

Delay report generation locally, poll job status while the worker is busy, and
write accurate user-facing language for a report that is accepted but not ready.

## Preconditions

- Local Docker stack is available.
- Migrations have been applied.
- You understand `202 Accepted` from
  `docs/async/phase-2-job-lifecycle.md`.

## Steps

Start the stack, apply migrations, and stop the worker for a short interval so
the accepted job cannot complete immediately:

```sh
./scripts/dev-up.sh
./scripts/migrate.sh --compose
docker compose stop worker
```

Enqueue a report:

```sh
curl -sS -X POST http://localhost:18080/reports/work-requests/summary/jobs
```

Poll status and result while no worker is available:

```sh
curl -sS http://localhost:18080/reports/jobs/{id}
curl -sS http://localhost:18080/reports/jobs/{id}/result
```

Wait at least 30 seconds before restarting the worker. During that wait, write
the exact user-facing text you would show for a report that was accepted but is
not ready.

```sh
docker compose start worker
```

Poll again until the job completes:

```sh
curl -sS http://localhost:18080/reports/jobs/{id}
curl -sS http://localhost:18080/reports/jobs/{id}/result
```

Expected observations:

- The enqueue response is not the report result.
- Status may stay `queued` while the worker is unavailable and briefly become
  `running` after the worker starts.
- The result endpoint must reject early reads with
  `report_result_unavailable`.
- A slow successful job should eventually reach `succeeded`.

## Explain What Happened

- What did the API promise when it returned `202 Accepted`?
- What should a caller do while the result is unavailable?
- Why would it be misleading to show stale or invented report data?
- Which status fields help distinguish slow progress from terminal failure?

## Cleanup

```sh
./scripts/dev-down.sh
```
