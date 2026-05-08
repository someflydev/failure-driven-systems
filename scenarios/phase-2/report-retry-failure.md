# Report Retry Failure Scenario

Use this scenario to observe a report job fail, persist attempt evidence, and
retry before idempotency has been solved.

## Goal

Trigger controlled report worker failure locally, inspect durable job state, and
explain why retrying work can duplicate side effects.

## Preconditions

- Local Docker stack is available.
- Migrations have been applied.
- The injected-failure worker is the only worker consuming the report queue.
- Failure injection is enabled only in a local or test environment.

## Start The Stack

```sh
./scripts/dev-up.sh
./scripts/migrate.sh --compose
```

Stop the Compose-managed worker so it does not consume the job before the
injected-failure worker can see it:

```sh
docker compose stop worker
```

In a separate terminal, confirm the API is ready:

```sh
curl -sS http://localhost:18080/health/ready
```

## Trigger Failure Before Generation

Start the worker with failure injection enabled:

```sh
OPLEDGER_ENVIRONMENT=local \
DATABASE_URL=postgresql+psycopg://opledger:opledger_local_password@localhost:55432/opledger \
OPLEDGER_REDIS_URL=redis://localhost:56379/0 \
OPLEDGER_REPORT_FAILURE_INJECTION_ENABLED=true \
OPLEDGER_REPORT_FAILURE_INJECTION_STAGE=before_generation \
./scripts/worker.sh
```

Enqueue a report:

```sh
curl -sS -X POST http://localhost:18080/reports/work-requests/summary/jobs
```

Capture the returned `id`, then inspect status:

```sh
curl -sS http://localhost:18080/reports/jobs/1
```

Expected durable evidence:

- `status` becomes `running` during each attempt.
- `attempt_count` increments once per worker execution.
- failed attempts persist `status = failed`, `last_error`, `error_message`,
  `last_failed_at`, and `finished_at`.
- RQ retries the job according to the configured bounded retry policy.

## Observe Retry Exhaustion

Leave injection enabled and continue polling the job:

```sh
curl -sS http://localhost:18080/reports/jobs/1
```

With default settings, OpsLedger allows three total attempts: the original
attempt plus two retries. RQ receives `Retry(max=2, interval=[1, 5])`, so it
waits about 1 second before the first retry and about 5 seconds before the
second retry. After retries are exhausted, the durable row remains failed with
the final `attempt_count`.

## Observe Recovery

Stop the injected-failure worker and restart it without injection:

```sh
OPLEDGER_ENVIRONMENT=local \
DATABASE_URL=postgresql+psycopg://opledger:opledger_local_password@localhost:55432/opledger \
OPLEDGER_REDIS_URL=redis://localhost:56379/0 \
./scripts/worker.sh
```

Enqueue another report and poll its status until it reaches `succeeded`:

```sh
curl -sS -X POST http://localhost:18080/reports/work-requests/summary/jobs
curl -sS http://localhost:18080/reports/jobs/2
curl -sS http://localhost:18080/reports/jobs/2/result
```

The successful job should clear `last_error`, keep its `attempt_count`, and
persist `result_json`.

## Explain What Happened

Answer these before changing code:

- Which state came from Postgres rather than Redis?
- What did RQ retry, and how many times was it allowed to retry?
- What could duplicate if report generation later sends email, writes audit
  rows, charges a customer, or stores exported files?
- Why does recording attempts make failure visible without making retries safe?
- What would be misleading about saying "just turn on retries" here?

## Cleanup

Stop the stack when finished:

```sh
./scripts/dev-down.sh
```
