# Incident Debugging Drill

## Phase

Phase 4: Observability And Incidents. This exercise belongs here because the
system now has enough moving parts for incident response to require logs,
metrics, durable status, and concise communication.

## Concepts

- Incident triage
- Status updates
- Hypothesis-driven debugging
- Correlation IDs
- Metrics versus durable status
- Postmortems
- LLM review after learner-owned evidence gathering

## Prerequisites

- `docs/observability/logging-and-correlation.md`
- `docs/observability/metrics.md`
- `exercises/phase-4/01-follow-a-request-through-logs.md`
- `exercises/phase-4/02-meaningful-metrics.md`
- `ops/incidents/TEMPLATE_incident_status_update.md`
- `ops/incidents/TEMPLATE_postmortem.md`
- `ops/runbooks/report-jobs-stuck.md`
- `ops/runbooks/reporting-service-down.md`

You should know how to start the Compose stack, run migrations, enqueue report
jobs, inspect `/reports/jobs`, inspect `/notification-attempts`, read Compose
logs, and query `/metrics`.

## Build/Change Task

Run one Phase 4 incident scenario and produce an evidence package. Choose one:

- `scenarios/phase-4/reporting-service-latency-incident.md`
- `scenarios/phase-4/worker-stalled-incident.md`
- `scenarios/phase-4/noisy-nonfatal-errors.md`
- `scenarios/phase-4/ambiguous-logs-before-correlation.md`

Your evidence package must include:

- Two incident status updates written during the drill.
- The affected endpoint, job ID, or notification attempt ID.
- The correlation ID when the workflow has one.
- The logs, metrics, and durable status surfaces you used.
- One discarded hypothesis and the evidence that ruled it out.
- A short postmortem after the timeline is complete.

## Constraints

- Do not add product features, infrastructure, dashboards, alerts, or tracing.
- Do not require production traffic.
- Do not run destructive cleanup against Postgres, Redis, or Docker volumes.
- Do not paste secrets, full connection strings, request bodies, or customer
  data into notes.
- Do not ask an LLM to write the postmortem before you create your own
  timeline.

## Failure Modes

- Declaring the incident resolved because a process restarted, without checking
  durable status or fresh logs.
- Treating API `202 Accepted` as proof that report generation completed.
- Confusing notification side-effect failures with report generation failures.
- Using metrics for job-specific truth instead of `/reports/jobs/{id}`.
- Writing status updates that omit impact, next action, or next update time.
- Inventing a root cause that is not supported by observed evidence.

## Expected Reasoning

After completing the exercise, explain:

- Which user workflow was affected.
- Which signals were symptoms and which signal proved root cause.
- Why the durable status endpoint mattered even when logs and metrics existed.
- How the `correlation_id` changed your confidence in the timeline.
- What follow-up is justified by the incident and what would be overbuilding.

## Verification

Run:

```sh
./scripts/verify.sh
```

Manual checks:

- The chosen scenario was run locally or a blocker was documented.
- The status updates are short and timestamped.
- The evidence references real repo surfaces: structured logs, `/metrics`,
  `/health/*`, `/reports/jobs`, `/reports/jobs/{id}/result`, or
  `/notification-attempts`.
- The postmortem timeline is written before any LLM critique.
- The action items are small and tied to observed evidence.

## Reflection Questions

- What was the first useful signal?
- What signal was noisy, ambiguous, or misleading?
- What did you believe at first that turned out wrong?
- What would you say to a customer while the incident is still unresolved?
- Which follow-up would you reject because it adds complexity without evidence?

## LLM Usage

Use an LLM only after you have written the timeline and first postmortem draft.
Ask it to review for unsupported claims, missing timestamps, weak status
updates, secret-handling risks, and action items that do not match the evidence.
Do not ask it to invent logs, metric output, impact, or root cause.

## Path-Specific Extensions

Backend: add one focused regression test only if the scenario revealed a real
code risk.

Operations: turn one scenario into a reusable command checklist for a future
on-call handoff.

Architecture: write a short note explaining whether the reporting service
extraction helped or hurt incident response.

Interview: explain the incident in five sentences using impact, evidence, root
cause, mitigation, and follow-up.

## Deployment/Debugging Actions If Relevant

Use local Compose only:

```sh
./scripts/dev-up.sh
./scripts/migrate.sh --compose
docker compose logs --tail=150 api
docker compose logs --tail=150 worker
docker compose logs --tail=150 reporting
./scripts/dev-down.sh
```

For scenarios that use failure injection, confirm injection is disabled again
after cleanup.
