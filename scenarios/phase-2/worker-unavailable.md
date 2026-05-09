# Worker Unavailable Scenario

Use this scenario to observe what happens when report jobs can be accepted but
no worker is available to execute them.

## Goal

Stop the worker, enqueue a report job, inspect durable status, then restart the
worker and watch the same job complete.

## Preconditions

- Local Docker stack is available.
- Migrations have been applied.
- Redis and Postgres are running.

## Steps

Start the stack and apply migrations:

```sh
./scripts/dev-up.sh
./scripts/migrate.sh --compose
```

In another terminal, stop only the worker:

```sh
docker compose stop worker
```

Enqueue a report:

```sh
curl -sS -X POST http://localhost:18080/reports/work-requests/summary/jobs
```

Capture the returned `id`, then poll durable status:

```sh
curl -sS http://localhost:18080/reports/jobs/{id}
curl -sS http://localhost:18080/reports/jobs/{id}/result
```

Expected observations:

- The enqueue request can return `202 Accepted` while no worker is running.
- The durable row remains inspectable through Postgres.
- The result endpoint returns `409 report_result_unavailable` until the worker
  succeeds.
- `queued` does not prove that a worker is currently making progress.

Restart the worker:

```sh
docker compose start worker
```

Poll status again until it reaches `succeeded`, then fetch the result:

```sh
curl -sS http://localhost:18080/reports/jobs/{id}
curl -sS http://localhost:18080/reports/jobs/{id}/result
```

## Explain What Happened

- Which facts remained available while the worker was stopped?
- Why is Redis not the user-facing status API?
- What user message would be honest while a job is accepted but not complete?
- What operational alert or runbook step would help if jobs stayed queued?

## Cleanup

```sh
docker compose start worker
./scripts/dev-down.sh
```
