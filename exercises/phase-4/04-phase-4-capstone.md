# Phase 4 Capstone

## Phase

Phase 4: Observability And Incidents. This capstone belongs here because the
learner should now be able to investigate OpsLedger failures using logs,
metrics, health checks, durable status, incident communication, and skeptical
LLM critique without outsourcing the reasoning.

## Concepts

- Evidence-first incident response
- Correlation IDs and timelines
- Metrics, health checks, and durable state
- User impact communication
- Postmortem quality
- Secret-safe LLM-assisted debugging
- Scope control under operational pressure

## Prerequisites

- `docs/observability/logging-and-correlation.md`
- `docs/observability/metrics.md`
- `docs/ASSISTANT_WORKFLOW.md`
- `exercises/phase-4/01-follow-a-request-through-logs.md`
- `exercises/phase-4/02-meaningful-metrics.md`
- `exercises/phase-4/03-incident-debugging-drill.md`
- `ops/incidents/TEMPLATE_incident_status_update.md`
- `ops/incidents/TEMPLATE_postmortem.md`
- `reviews/checklists/incident-review.md`
- `reviews/rubrics/phase-4-capstone.md`
- `reviews/llm/TEMPLATE_incident_commander.md`
- `reviews/llm/TEMPLATE_log_analysis_helper.md`
- `reviews/llm/TEMPLATE_postmortem_critique.md`

You should know how to run the local Compose stack, apply migrations, enqueue
report jobs, inspect report job status, inspect notification attempts, read
structured logs, and query `/metrics`.

## Build/Change Task

Create a Phase 4 incident evidence package. Run either:

- two different Phase 4 incident scenarios, or
- one Phase 4 incident scenario deeply enough to compare two hypotheses and two
  evidence surfaces.

Use scenarios from `scenarios/phase-4/`:

- `scenarios/phase-4/reporting-service-latency-incident.md`
- `scenarios/phase-4/worker-stalled-incident.md`
- `scenarios/phase-4/noisy-nonfatal-errors.md`
- `scenarios/phase-4/ambiguous-logs-before-correlation.md`

Your evidence package must include:

- The scenario names and commands you ran.
- The affected job ID, notification attempt ID, endpoint, or correlation ID.
- Bounded sanitized log excerpts.
- A small metrics snapshot when the scenario uses metrics.
- Durable status evidence from `/reports/jobs`, `/reports/jobs/{id}`,
  `/reports/jobs/{id}/result`, or `/notification-attempts`.
- Two incident status updates.
- A timeline of observed facts with evidence sources.
- Two hypotheses: one current hypothesis and one discarded hypothesis.
- A postmortem draft written before LLM critique.
- A short note explaining what the LLM critique changed, if anything.

## Constraints

- Do not add runtime code, services, dashboards, tracing, alerts,
  infrastructure, or dependencies.
- Do not create canned final answers for the scenarios.
- Do not paste secrets, tokens, full connection strings, request bodies, raw
  customer data, or full environment dumps into notes or LLM prompts.
- Do not ask an LLM for analysis until you have collected evidence and written
  your own hypothesis.
- Do not claim resolution until durable status, recent logs, and user-visible
  workflow behavior support it.
- Keep evidence bounded by time window, service, ID, and question.

## Failure Modes

- Treating API `202 Accepted` as proof that report generation completed.
- Treating green readiness as proof that the workflow is healthy.
- Treating metrics as job-specific truth instead of shape and trend evidence.
- Building a timeline without correlation IDs or naming what is ambiguous.
- Letting an LLM invent root cause, impact, or action items.
- Proposing broad platform work that the incident evidence does not justify.
- Including secrets or excessive raw logs in the evidence package.

## Expected Reasoning

After completing the capstone, explain:

- Which user workflow was affected and how you know.
- Which evidence surface you checked first and why.
- What logs, metrics, health checks, and durable state each proved or could not
  prove.
- How a correlation ID changed confidence in the timeline.
- Which hypothesis was ruled out and by what evidence.
- Why the follow-up is appropriately small for the observed incident.
- How LLM critique helped without replacing your own conclusion.

## Verification

Run:

```sh
./scripts/verify.sh
```

Manual checks:

- The evidence package references real Phase 4 scenario surfaces.
- Status updates include impact, evidence, hypothesis, action now, and next
  update time.
- The postmortem timeline exists before any LLM critique notes.
- LLM prompts include bounded evidence and the learner's own hypothesis.
- No notes or prompts include secrets, full connection strings, request bodies,
  raw customer data, or full environment dumps.

Review:

- Score the work with `reviews/rubrics/phase-4-capstone.md`.
- Use `reviews/checklists/incident-review.md` to identify weak claims before
  revising the postmortem.

## Reflection Questions

- What was your first useful signal, and what did it fail to prove?
- Which signal was noisy, ambiguous, or misleading?
- What changed your mind during the investigation?
- What would you tell a user while the incident is still unresolved?
- What action item did you reject because the evidence did not justify it?
- What would make a heavier observability stack worth revisiting later?

## LLM Usage

Use LLMs only after collecting evidence and writing your own hypothesis. Good
uses include:

- Ask `reviews/llm/TEMPLATE_incident_commander.md` to challenge your next
  check.
- Ask `reviews/llm/TEMPLATE_log_analysis_helper.md` to identify ambiguity in
  bounded logs.
- Ask `reviews/llm/TEMPLATE_postmortem_critique.md` to find unsupported claims
  in your draft.

Do not ask for unlimited diagnosis, final scenario answers, invented logs,
invented metrics, or a completed postmortem.

## Path-Specific Extensions

Backend: add one focused regression test only if the incident proves a real
code risk.

Operations: turn the investigation into a short runbook amendment with exact
checks and resolution criteria.

Architecture: explain whether the reporting service boundary helped or hurt
debugging, using incident evidence.

Interview: answer three questions from
`interviews/phase-4-operational-debugging.md` using only your evidence package.

## Deployment/Debugging Actions If Relevant

Use local Compose and scenario commands only:

```sh
./scripts/dev-up.sh
./scripts/migrate.sh --compose
docker compose logs --tail=150 api
docker compose logs --tail=150 worker
docker compose logs --tail=150 reporting
./scripts/dev-down.sh
```

For scenarios that use failure injection or stop processes, confirm cleanup
returns the local stack to the default state.
