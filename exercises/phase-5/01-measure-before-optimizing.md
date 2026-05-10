# Measure Before Optimizing

## Phase

Phase 5: Performance, Caching, And Read Models. This exercise belongs here
because learners must collect latency and error evidence before changing query
shape, adding indexes, introducing cache, or creating derived read models.

## Concepts

- Baseline latency measurement
- Low-rate load testing
- Error rate and status mix
- Dataset size and repeatability
- Bottleneck hypotheses
- Measurement before optimization

## Prerequisites

Read these first:

- `curriculum/PHASE_PLAN.md`
- `docs/performance/baselines.md`
- `docs/observability/metrics.md`
- `docs/observability/logging-and-correlation.md`
- `deploy/dokku/README.md`
- `exercises/TEMPLATE.md`

You should know how to start the local stack, run migrations, create customers
and work requests, enqueue or inspect report jobs, and read `/metrics`.

## Build/Change Task

Collect baseline evidence for at least two OpsLedger paths before changing any
application code:

1. `GET /work-requests`
2. `GET /reports/jobs/{report_job_id}` when a report job exists

Optionally measure low-rate `POST /work-requests` only in a disposable local
environment after explicitly opting in to writes.

For each measured path, record:

- The exact command.
- Dataset size.
- Request count.
- Status mix.
- Error count.
- Average latency, p50, p95, and max.
- Relevant `/metrics` before and after.
- One suspected bottleneck or a clear statement that the data is too small to
  justify an optimization.

Then write a short recommendation naming the next measurement or inspection
step. Do not implement the optimization in this exercise.

## Constraints

- Do not add caching.
- Do not add indexes.
- Do not add read models.
- Do not raise the load-test rate above the script cap.
- Do not target a non-local URL without `--allow-non-local`.
- Do not run write scenarios without `--allow-writes`.
- Do not run write scenarios against shared, production-like, or customer-like
  data.
- Do not claim an endpoint is slow without recording the dataset and observed
  latency.

## Failure Modes

- Optimizing an empty or tiny dataset and learning the wrong lesson.
- Treating one slow request as proof without repeating a small baseline.
- Ignoring `4xx` or `5xx` statuses while reporting only latency.
- Hitting the VPS too hard and creating an artificial incident.
- Adding Redis, cache, or denormalized state before explaining source of truth
  and rebuild behavior.
- Letting an LLM invent benchmark numbers instead of using measured evidence.

## Expected Reasoning

After completing the exercise, explain:

- Which endpoint you measured and why.
- Whether the measured behavior shows real pressure.
- Which source-of-truth tables are involved.
- What you suspect is slow and what evidence supports that suspicion.
- What measurement would come next before changing code.
- Why the first answer might be "do nothing yet."

## Verification

Run:

```sh
./scripts/verify.sh
scripts/perf/baseline.py list-work-requests --dry-run
```

Manual checks:

```sh
curl -s http://127.0.0.1:18080/metrics
scripts/perf/baseline.py seed-read-fixture --allow-writes
scripts/perf/baseline.py list-work-requests
scripts/perf/baseline.py poll-report-job --report-job-id YOUR_REPORT_JOB_ID
```

Your submitted evidence should include:

- Two baseline summaries.
- The relevant metrics snippets.
- Dataset size notes.
- One bottleneck hypothesis or one explicit no-optimization-yet conclusion.
- Confirmation that no cache, index, or read model was added.

## Reflection Questions

- What changed between an empty dataset and a seeded dataset?
- Which metric helped validate your script output?
- Which result surprised you, and what would you measure next?
- What would make an index justified?
- What would make cache justified?
- What stale-data or rebuild problem would a read model introduce?

## LLM Usage

Use an LLM only after you have measurements. Ask it to critique whether your
baseline evidence supports your bottleneck hypothesis and whether your proposed
next measurement is specific enough. Do not ask it to choose an optimization
before you provide the measured endpoint, dataset size, status mix, and latency
summary.

## Path-Specific Extensions

Backend: inspect the SQL emitted by one measured path and compare it with the
latency result before proposing an index.

Operations: run the read-only baseline against your Dokku VPS at `1` request
per second for `10` seconds, then record health and log evidence before and
after.

Architecture: write a short memo explaining why a cache or read model would be
derived state and how it would be rebuilt from Postgres.

Interview: practice explaining a performance investigation where the first
decision was not to optimize.

## Deployment/Debugging Actions If Relevant

For a VPS run, target only your own Dokku app, keep the default low rate, pass
`--allow-non-local` explicitly, and inspect health and logs before and after.
Do not run write scenarios on the VPS unless the data is disposable and the
exercise explicitly asks for that risk.
