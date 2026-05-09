# Duplicate Job Execution Scenario

Use this scenario to verify that repeated execution of an already completed
report job does not overwrite completed output or create duplicate local
notification attempts.

## Goal

Complete a report job, trigger the worker function for the same durable job id
again in a local shell, and inspect the stored result and notification attempt.

## Preconditions

- Local dependencies are available through Docker Compose.
- Migrations have been applied.
- You understand `docs/async/idempotency.md`.

## Steps

Start the stack and apply migrations:

```sh
./scripts/dev-up.sh
./scripts/migrate.sh --compose
```

Enqueue a report and let the worker complete it:

```sh
curl -sS -X POST http://localhost:18080/reports/work-requests/summary/jobs
curl -sS http://localhost:18080/reports/jobs/{id}
curl -sS http://localhost:18080/notification-attempts?target_type=report_job\&target_id={id}
```

After the job reaches `succeeded`, run the same worker function against the same
job id from the host:

```sh
DATABASE_URL=postgresql+psycopg://opledger:opledger_local_password@localhost:55432/opledger \
OPLEDGER_REDIS_URL=redis://localhost:56379/0 \
uv run python -c 'from opledger_api.report_jobs import generate_work_request_summary_report_job; generate_work_request_summary_report_job(1)'
```

Replace `1` with the completed report job id.

Inspect the job and notification attempts again:

```sh
curl -sS http://localhost:18080/reports/jobs/{id}
curl -sS http://localhost:18080/notification-attempts?target_type=report_job\&target_id={id}
```

Expected observations:

- `attempt_count` does not increase after the completed-output guard returns.
- `result_json` remains the original completed output.
- There is still one notification attempt for
  `report_job:{id}:completed`.

## Explain What Happened

- Which guard prevents rebuilding a completed report?
- Which durable key prevents a duplicate notification attempt?
- Why are request idempotency, job idempotency, and side-effect idempotency
  separate concerns?
- What duplicate risk would remain if the worker crashed before creating the
  notification attempt?

## Cleanup

```sh
./scripts/dev-down.sh
```
