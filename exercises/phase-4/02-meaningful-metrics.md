# Meaningful Metrics For A Report Failure

## Phase

Phase 4: Observability And Incidents. This exercise belongs here because the
system now has an API, Redis queue, worker, reporting service, durable job
status, structured logs, and enough failure modes that metrics can answer
questions logs alone make slow.

## Concepts

- Prometheus-style counters and histograms
- Request rate, error rate, and latency
- Job outcome metrics versus durable job status
- Low-cardinality labels
- Internal-only metrics exposure
- Dependency failure diagnosis

## Prerequisites

Read these first:

- `docs/observability/logging-and-correlation.md`
- `docs/observability/metrics.md`
- `ops/dashboards/README.md`
- `exercises/phase-4/01-follow-a-request-through-logs.md`
- `scenarios/phase-3/reporting-timeout.md`

You should know how to start the Compose stack, run migrations, enqueue report
jobs, inspect `/reports/jobs`, and read API, worker, and reporting service logs.

## Build/Change Task

Break the reporting dependency in a controlled local way, observe the metrics,
and write a short incident note explaining what changed.

1. Start the local stack and run migrations.
2. Confirm the API and reporting service expose `/metrics` internally.
3. Capture baseline metric snippets for HTTP request totals, request latency,
   report jobs, reporting service calls, and notification attempts.
4. Enable one local reporting-service failure mode such as timeout, HTTP 500,
   malformed JSON, or incompatible response.
5. Enqueue a report job and let the worker process it.
6. Capture the changed metrics and the durable job status.
7. Explain which metric moved first, which metric proved the user-visible
   impact, and which durable endpoint gave job-specific evidence.

## Constraints

- Do not add Grafana, Prometheus, tracing, new containers, or alerting rules.
- Do not add labels containing customer IDs, report job IDs, request IDs,
  correlation IDs, idempotency keys, emails, or raw error messages.
- Do not treat `/metrics` as a public endpoint.
- Do not replace durable status queries with metrics. Metrics show shape;
  durable records show specific job evidence.

## Failure Modes

- Counting every possible event instead of the few signals operators need.
- Using raw paths or IDs as labels and creating high-cardinality metrics.
- Seeing a flat API error count and wrongly concluding the system is healthy
  while async report jobs are failing later in the worker.
- Relying on worker in-process counters after a restart without checking
  durable `/reports/jobs` state.
- Exposing metrics publicly because they look less sensitive than logs.

## Expected Reasoning

After completing the exercise, you should be able to explain:

- Why enqueue success, worker failure, and reporting-service failure are
  different signals.
- Why a report can fail without the original HTTP enqueue request returning
  `5xx`.
- Why route-template labels are acceptable but raw report job IDs are not.
- Which metric would support an alert later, and what human check should still
  happen before changing code.
- Why the worker limitation is acceptable in Phase 4 and what extra component a
  later phase would need for scrapeable worker metrics.

## Verification

Run:

```sh
./scripts/verify.sh
```

Manual checks:

```sh
curl -s http://127.0.0.1:18080/metrics
curl -s http://127.0.0.1:18081/metrics
curl -s http://127.0.0.1:18080/reports/jobs
curl -s http://127.0.0.1:18080/notification-attempts
```

Your evidence should include:

- One baseline metrics snippet.
- One after-failure metrics snippet.
- The affected report job status and `last_error`.
- The reporting failure reason or timeout evidence.
- A statement that no high-cardinality labels were added.

## Reflection Questions

- Which metric would have helped you notice the problem fastest?
- Which metric was insufficient without durable job status?
- What changed when the reporting service failed: API request metrics, worker
  metrics, reporting-service call metrics, or notification metrics?
- What would be risky about exposing `/metrics` publicly?
- If the worker restarts, which evidence survives and which evidence resets?

## LLM Usage

Use an LLM as a reviewer after you gather evidence. Ask it to critique whether
your incident note distinguishes request health, queue acceptance, worker
execution, reporting dependency failure, and durable job status. Do not ask it
to invent metric output or explain a failure you did not reproduce.

## Path-Specific Extensions

Backend: add a narrow test for one metric that protects against a regression in
labels or status counting.

Operations: turn one query from `ops/dashboards/README.md` into a proposed alert
condition and write the manual confirmation step that must follow it.

Architecture: write a short note on when a worker metrics endpoint, push
gateway, or sidecar exporter would be worth the extra moving part.

Interview: explain why metrics complement but do not replace logs, correlation
IDs, and durable state.

## Deployment/Debugging Actions If Relevant

Keep `/metrics` reachable only from local or internal networks. For Dokku or a
future production deployment, document the proxy or firewall rule before
enabling external scraping.
