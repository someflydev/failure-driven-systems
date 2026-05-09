# Redis Unavailable Scenario

Use this scenario to understand the hard limit of Phase 2 async work when Redis
is unavailable.

## Goal

Stop Redis, attempt to enqueue a report job, inspect the API response and
durable row, then restart Redis and confirm enqueueing works again.

## Preconditions

- Local Docker stack is available.
- Migrations have been applied.
- Postgres remains available.

## Steps

Start the stack and apply migrations:

```sh
./scripts/dev-up.sh
./scripts/migrate.sh --compose
```

Stop Redis:

```sh
docker compose stop redis
```

Attempt to enqueue a report:

```sh
curl -i -X POST http://localhost:18080/reports/work-requests/summary/jobs
```

Expected observations:

- The API returns `503 Service Unavailable` with
  `report_queue_unavailable`.
- The response details include a `report_job_id` because the API persisted a
  durable row before enqueueing failed.
- That row is marked `failed` with queue failure evidence.
- Synchronous database-backed routes may still work if they do not need Redis.
- Background report execution cannot progress because Redis coordinates queue
  delivery.

Inspect the failed job:

```sh
curl -sS http://localhost:18080/reports/jobs/{report_job_id}
```

Restart Redis and the worker:

```sh
docker compose start redis worker
```

Enqueue a fresh report and confirm it can complete:

```sh
curl -sS -X POST http://localhost:18080/reports/work-requests/summary/jobs
curl -sS http://localhost:18080/reports/jobs/{new_id}
```

## Limits To State Clearly

The app can still:

- answer liveness checks;
- answer readiness if Postgres is reachable and the readiness check does not
  include Redis;
- serve routes that only need Postgres;
- expose persisted report job rows.

The app cannot:

- enqueue new background report work successfully;
- rely on Redis as durable user-visible status;
- complete queued report work without a running Redis-backed worker path;
- guarantee that pending Redis queue entries survived Redis loss.

## Cleanup

```sh
docker compose start redis worker
./scripts/dev-down.sh
```
