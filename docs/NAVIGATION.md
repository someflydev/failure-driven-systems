# Navigation

Use this as the single map of the repository's major learning artifacts.

## Start Here

- `README.md`: public entrypoint, constraints, local start, and major paths.
- `AGENT.md`: instructions for prompt-driven coding-assistant sessions.
- `docs/DOCTRINE.md`: learning doctrine and boundaries.
- `docs/ASSISTANT_WORKFLOW.md`: how learners should use LLMs without
  outsourcing reasoning.
- `docs/REPO_MAP.md`: detailed repository structure.
- `docs/SYSTEM_EVOLUTION.md`: how OpsLedger changes across phases.

## Curriculum

- `curriculum/README.md`: six-phase concept sequence.
- `curriculum/PHASE_PLAN.md`: OpsLedger capabilities, allowed concepts,
  disallowed concepts, failure experiences, and explanation outcomes.
- `lessons/phase-1/README.md` through `lessons/phase-6/README.md`: phase
  indexes in intended learner order.

## OpsLedger System

- `services/api/`: FastAPI API, models, routes, worker-facing modules, tests,
  and migrations.
- `services/reporting/`: stateless reporting service used for the Phase 3
  boundary exercise.
- `docs/DOMAIN.md`: domain boundaries and conceptual entities.
- `docs/data-models/phase-1.md`: relational model foundation.
- `docs/architecture/current-system.md`: current Phase 6 system snapshot.
- `docs/architecture/modular-monolith.md`: module-boundary guide.
- `docs/contracts/`: report-rendering contract and compatibility playbook.
- `docs/async/`: job lifecycle, idempotency, and side-effect guidance.

## Operations And Deployment

- `deploy/dokku/`: first VPS deployment path and checklist.
- `deploy/k3s/`: later k3s learning path, checklist, and starter manifests.
- `docs/deployment/dokku-vs-k3s.md`: platform comparison.
- `docs/runbooks/DB_CONNECTIVITY.md`: database readiness troubleshooting.
- `ops/runbooks/`: incident runbooks for API, reporting, and stuck jobs.
- `ops/incidents/`: status update and postmortem templates.
- `ops/dashboards/README.md`: internal dashboard and metrics guidance.

## Observability And Performance

- `docs/observability/logging-and-correlation.md`: structured logs and
  correlation IDs.
- `docs/observability/metrics.md`: lightweight internal metrics surfaces.
- `docs/performance/baselines.md`: safe local baseline measurement.
- `docs/performance/query-inspection.md`: query-plan inspection.
- `docs/performance/read-models.md`: derived dashboard read model.
- `docs/performance/caching.md`: one bounded Redis cache and staleness risks.

## Architecture Decisions

- `docs/adr/TEMPLATE.md`: ADR template.
- `docs/adr/0001-report-rendering-boundary.md`: reporting boundary decision.
- `docs/adr/0002-fastapi-python-primary-stack.md`: primary stack decision.
- `docs/adr/0003-postgres-source-of-truth.md`: durable truth decision.
- `docs/adr/0004-redis-queue-cache-postgres-durability.md`: Redis ownership.
- `docs/adr/0005-dokku-first-deployment.md`: first deployment path.
- `docs/adr/0006-k3s-later-orchestration-learning-path.md`: later
  orchestration path.
- `docs/storage/`: datastore comparison and refusal guidance.
- `docs/languages/`: runtime and polyglot tradeoff guidance.

## Practice And Assessment

- `exercises/TEMPLATE.md`: canonical exercise structure.
- `exercises/phase-*/`: hands-on phase exercises and capstones.
- `scenarios/phase-*/`: guided failure scenarios.
- `reviews/checklists/`: review gates for API, async, boundaries, incidents,
  performance, architecture, and system-wide readiness.
- `reviews/rubrics/`: capstone rubrics.
- `reviews/llm/`: templates for LLM critique, interviews, log analysis, and
  incident review.
- `quizzes/`: phase quizzes.
- `interviews/`: phase interviews, role-track interviews, and mock panels.

## Role Paths And Portfolio

- `paths/README.md`: role-overlay index.
- `paths/backend-python.md`: backend/Python emphasis.
- `paths/data-backend.md`: data/backend emphasis.
- `paths/distributed-systems.md`: distributed systems emphasis.
- `paths/generalist-backend.md`: generalist backend emphasis.
- `paths/architecture-decisions.md`: architecture decision emphasis.
- `paths/shared-capstone.md`: shared portfolio defense.
- `docs/PORTFOLIO_GUIDE.md`: public presentation guidance.
- `RELEASE_CHECKLIST.md`: public-readiness checklist.

## Prompt History

- `.prompts/README.md`: prompt sequence summary.
- `.prompts/PROMPT_01.txt` through `.prompts/PROMPT_40.txt`: prompt-driven
  development history.
