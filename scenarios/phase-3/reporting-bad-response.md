# Reporting Bad Response Scenario

Use this scenario to practice distinguishing service failure from contract
failure at the extracted reporting boundary.

## Goal

Force the reporting service to return a bad response, then inspect job status
and logs before changing code.

## Preconditions

- Local Docker stack is available.
- Migrations have been applied.
- The worker calls the reporting service through Docker Compose.

## Steps

Start the stack with malformed JSON injection:

```sh
OPLEDGER_REPORTING_FAILURE_INJECTION_ENABLED=true \
OPLEDGER_REPORTING_FAILURE_MODE=malformed_response \
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
curl -sS http://localhost:18080/reports/jobs/{id}/result
docker compose logs --tail=100 worker
docker compose logs --tail=100 reporting
```

Expected observations:

- The worker reaches the reporting service, but the response cannot be parsed
  as valid JSON.
- The durable job failure should identify invalid response JSON, not timeout.
- The result endpoint does not invent a report result.

Repeat with an incompatible v1 response:

```sh
docker compose down
OPLEDGER_REPORTING_FAILURE_INJECTION_ENABLED=true \
OPLEDGER_REPORTING_FAILURE_MODE=incompatible_response \
./scripts/dev-up.sh
```

Enqueue another report and inspect the same evidence. This time the response is
JSON, but it is not a valid `report-rendering.v1` response.

## Explain What Happened

- How is malformed JSON different from a valid JSON body with the wrong
  contract?
- Which error would help the on-call engineer fastest?
- Why should the worker fail the job instead of storing a partial report?
- What would a caller see while the report result is unavailable?

## Cleanup

```sh
./scripts/dev-down.sh
```
