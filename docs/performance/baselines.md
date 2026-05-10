# Performance Baselines

Phase 5 starts with measurement before intervention. OpsLedger now has enough
read paths, report job state, metrics, and small-VPS constraints that a slow
endpoint should be investigated before adding cache, indexes, or read models.

## Tool Choice

Use `scripts/perf/baseline.py` for the first baselines. It is a small Python
script that uses only the standard library, so it adds no benchmarking
framework, no new runtime dependency, and no extra container. That fits the
repo because the goal is learner evidence, not maximum load generation.

The script is intentionally conservative:

- Defaults target `http://127.0.0.1:18080`.
- Requests are sequential.
- Default rate is `1` request per second.
- Rate is capped at `5` requests per second.
- Duration is capped at `60` seconds.
- Non-local targets require `--allow-non-local`.
- Write-oriented scenarios require `--allow-writes`.

These limits are part of the lesson. They keep a tiny local stack or Dokku VPS
from being turned into a stress-test target by accident.

## Scenarios

List work requests:

```sh
scripts/perf/baseline.py list-work-requests
```

Create a small deterministic read fixture locally:

```sh
scripts/perf/baseline.py seed-read-fixture --allow-writes
```

Create work requests at a low rate only when you have chosen a safe local
customer ID:

```sh
scripts/perf/baseline.py create-work-requests --customer-id 1 --allow-writes
```

Poll a known report job status:

```sh
scripts/perf/baseline.py poll-report-job --report-job-id 1
```

Write raw samples to CSV when you want evidence for a note or review:

```sh
scripts/perf/baseline.py list-work-requests \
  --duration-seconds 20 \
  --output-csv /tmp/opledger-list-work-requests.csv
```

## Local Workflow

1. Start the local stack.
2. Run migrations.
3. Create or confirm a small set of customers and work requests.
4. Capture `/metrics` before the run.
5. Run one baseline scenario.
6. Capture `/metrics` after the run.
7. Record latency, status mix, error count, dataset size, and any obvious log
   evidence.

Useful commands:

```sh
./scripts/dev-up.sh
./scripts/migrate.sh --compose
curl -s http://127.0.0.1:18080/metrics
scripts/perf/baseline.py list-work-requests
curl -s http://127.0.0.1:18080/metrics
```

Use `--dry-run` to check script safety settings without sending requests:

```sh
scripts/perf/baseline.py list-work-requests --dry-run
```

## VPS Workflow

Run VPS baselines only against a deployment you own and only during a quiet
learning window. A non-local run must be explicit:

```sh
scripts/perf/baseline.py list-work-requests \
  --base-url http://opledger-api.YOUR_DOKKU_DOMAIN \
  --allow-non-local \
  --duration-seconds 10 \
  --rate 1
```

For Dokku, inspect app health and logs before and after:

```sh
curl -i http://opledger-api.YOUR_DOKKU_DOMAIN/health/ready
dokku logs opledger-api --tail
```

Do not run write scenarios against a shared, public, or production-like target
unless the exercise explicitly says to do so, the dataset is disposable, and you
have a cleanup plan. The default Phase 5 path does not need remote writes.

## What Not To Do On A Tiny Server

- Do not raise rate or duration to chase impressive numbers.
- Do not point generic load tools at the VPS without bounded settings.
- Do not run write scenarios against real customer-like data.
- Do not test through public routes that expose `/metrics`.
- Do not run multiple load tools at the same time.
- Do not start optimization until baseline evidence names the slow path and the
  suspected cause.

## Recording Results

Record enough context for another engineer to interpret the result:

- Date and environment: local Compose or Dokku VPS.
- Git commit or branch.
- Scenario command.
- Dataset size: approximate customers, work requests, report jobs, and status
  events.
- Request count, status mix, errors, average latency, p50, p95, and max.
- Relevant `/metrics` snippets before and after.
- One suspected bottleneck, written as a hypothesis.
- The next measurement you would run before changing code.

Example result note:

```text
Scenario: list-work-requests
Environment: local Compose
Dataset: 1 customer, 5 work requests, 0 report jobs
Command: scripts/perf/baseline.py list-work-requests --duration-seconds 10
Result: 10 requests, 10 ok, 0 errors, avg 12.4 ms, p95 18.7 ms
Metrics checked: opledger_http_request_duration_seconds for GET /work-requests
Hypothesis: no bottleneck yet; dataset is too small to justify optimization
Next measurement: repeat after a larger local fixture or query-plan inspection
```

## Before Optimizing

An acceptable Phase 5 optimization proposal must cite a baseline. For example:

- The measured endpoint and dataset.
- The current latency or error behavior.
- The suspected database query, serialization path, network call, or worker
  path.
- Why cache, an index, pagination change, or read model fits that measured
  pressure.
- What new failure mode the optimization introduces.

If the baseline does not show pressure, the correct conclusion is to keep the
system simple and gather better evidence later.
