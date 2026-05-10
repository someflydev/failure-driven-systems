# Phase 4 Lesson Path

Phase 4 teaches practical observability and incident response after OpsLedger
has enough moving parts for naive logs to become ambiguous. The goal is not a
large observability stack; it is reliable evidence that fits a small VPS and
helps an operator explain what happened.

## Initial Path

1. Read `docs/observability/logging-and-correlation.md` to understand the JSON
   log shape, request IDs, correlation IDs, and secret-safety boundaries.
2. Read `docs/observability/metrics.md` to understand the current practical
   metrics, label boundaries, and internal-only `/metrics` exposure.
3. Revisit `scenarios/phase-2/worker-unavailable.md` and
   `scenarios/phase-3/reporting-timeout.md` with correlation IDs in mind.
4. Complete `exercises/phase-4/01-follow-a-request-through-logs.md` by running
   a report job and building a short evidence timeline.
5. Complete `exercises/phase-4/02-meaningful-metrics.md` by breaking the
   reporting dependency, observing metrics, and tying them back to durable job
   status.
6. Read `ops/runbooks/report-jobs-stuck.md` and
   `ops/runbooks/reporting-service-down.md` to practice evidence-first
   operational checks for the async reporting workflow.
7. Run one incident scenario from `scenarios/phase-4/` and complete
   `exercises/phase-4/03-incident-debugging-drill.md` with status updates,
   evidence, and a short postmortem.
8. Use `reviews/checklists/incident-review.md` to critique the incident
   response quality after the learner has written their own timeline.
9. Complete `exercises/phase-4/04-phase-4-capstone.md`, then score it with
   `reviews/rubrics/phase-4-capstone.md`.
10. Use `quizzes/phase-4.md` and
    `interviews/phase-4-operational-debugging.md` to practice short-answer and
    mock interview defense from the incident evidence.

## Observability Focus

Learners should be able to explain:

- Why Phase 1 request logs were adequate before workers and service boundaries.
- How one `correlation_id` follows a report from API request to durable job,
  worker attempt, reporting service call, and final status.
- Why structured logs are useful before metrics, tracing, dashboards, or alert
  rules.
- Which request, job, reporting-boundary, and notification metrics answer
  concrete debugging questions without measuring everything.
- Which facts should never be logged, copied into tickets, or pasted into LLM
  prompts.
- What questions remain unanswered until alerting, tracing, or dedicated worker
  metrics exposure is justified.
- How concise status updates, runbooks, and postmortems keep incident learning
  grounded in observed evidence.
- How LLMs can act as incident commanders, log-analysis helpers, and
  postmortem critics only after the learner provides bounded evidence and a
  hypothesis.

Future Phase 4 lessons may add alerting and rollback practice. They should stay
grounded in observed failures and small-system operational constraints.
