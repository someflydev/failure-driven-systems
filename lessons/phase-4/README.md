# Phase 4 Lesson Path

Phase 4 teaches practical observability and incident response after OpsLedger
has enough moving parts for naive logs to become ambiguous. The goal is not a
large observability stack; it is reliable evidence that fits a small VPS and
helps an operator explain what happened.

## Initial Path

1. Read `docs/observability/logging-and-correlation.md` to understand the JSON
   log shape, request IDs, correlation IDs, and secret-safety boundaries.
2. Revisit `scenarios/phase-2/worker-unavailable.md` and
   `scenarios/phase-3/reporting-timeout.md` with correlation IDs in mind.
3. Complete `exercises/phase-4/01-follow-a-request-through-logs.md` by running
   a report job and building a short evidence timeline.
4. Use `ops/runbooks/phase-1-first-response.md` and
   `ops/runbooks/dokku-api-incident.md` as examples of evidence-first
   operations before writing broader Phase 4 runbooks.

## Observability Focus

Learners should be able to explain:

- Why Phase 1 request logs were adequate before workers and service boundaries.
- How one `correlation_id` follows a report from API request to durable job,
  worker attempt, reporting service call, and final status.
- Why structured logs are useful before metrics, tracing, dashboards, or alert
  rules.
- Which facts should never be logged, copied into tickets, or pasted into LLM
  prompts.
- What questions remain unanswered until metrics or tracing are justified.

Future Phase 4 lessons may add metrics, alerting, incident reviews, rollback
practice, and postmortems. They should stay grounded in observed failures and
small-system operational constraints.
