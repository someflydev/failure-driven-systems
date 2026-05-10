# Reporting Timeout Scenario

Use this scenario to observe a slow extracted reporting service before changing
code.

## Goal

Delay the reporting service long enough for the worker's remote render timeout
to fire, then inspect the durable report job evidence and worker logs.

## Preconditions

- Local Docker stack is available.
- Migrations have been applied.
- You understand the report job lifecycle from
  `docs/async/phase-2-job-lifecycle.md`.
- The worker is configured to call the reporting service through
  `OPLEDGER_REPORT_RENDERING_SERVICE_URL`.

## Steps

Start the stack with an injected reporting delay longer than the worker timeout:

```sh
OPLEDGER_REPORTING_FAILURE_INJECTION_ENABLED=true \
OPLEDGER_REPORTING_FAILURE_MODE=delay \
OPLEDGER_REPORTING_FAILURE_DELAY_SECONDS=5 \
OPLEDGER_REPORT_RENDERING_SERVICE_TIMEOUT_SECONDS=1 \
./scripts/dev-up.sh
./scripts/migrate.sh --compose
```

Enqueue a report:

```sh
curl -sS -X POST http://localhost:18080/reports/work-requests/summary/jobs
```

Before changing code, observe:

```sh
curl -sS http://localhost:18080/reports/jobs/{id}
docker compose logs --tail=100 worker
docker compose logs --tail=100 reporting
```

Expected observations:

- The API can accept the job because Postgres and Redis are available.
- The worker records a failed attempt when the reporting call exceeds the
  configured timeout.
- The job's failure evidence should distinguish timeout from a 500 or invalid
  response.
- The result endpoint still rejects early reads with
  `report_result_unavailable`.

## Explain What Happened

- Which process was slow?
- Which timeout bounded the wait?
- What did the user already receive when the job was accepted?
- What user-visible message would be honest while the job is failed or retrying?
- Why would automatic broad retries be risky without idempotency reasoning?

## Cleanup

```sh
./scripts/dev-down.sh
```
