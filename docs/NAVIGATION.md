# Navigation

Use this as the single map of the repository's major learning artifacts.

## Start Here

- [README.md](../README.md): public entrypoint, constraints, local start, and major paths.
- [AGENT.md](../AGENT.md): instructions for prompt-driven coding-assistant sessions.
- [docs/DOCTRINE.md](DOCTRINE.md): learning doctrine and boundaries.
- [docs/ASSISTANT_WORKFLOW.md](ASSISTANT_WORKFLOW.md): how learners should use LLMs without
  outsourcing reasoning.
- [docs/REPO_MAP.md](REPO_MAP.md): detailed repository structure.
- [docs/SYSTEM_EVOLUTION.md](SYSTEM_EVOLUTION.md): how OpsLedger changes across phases.

## Curriculum

- [curriculum/README.md](../curriculum/README.md): six-phase concept sequence.
- [curriculum/PHASE_PLAN.md](../curriculum/PHASE_PLAN.md): OpsLedger capabilities, allowed concepts,
  disallowed concepts, failure experiences, and explanation outcomes.
- [lessons/phase-1/README.md](../lessons/phase-1/README.md) through
  [lessons/phase-6/README.md](../lessons/phase-6/README.md): phase
  indexes in intended learner order.

## OpsLedger System

- [services/api/](../services/api/): FastAPI API, models, routes, worker-facing modules, tests,
  and migrations.
- [services/reporting/](../services/reporting/): stateless reporting service used for the Phase 3
  boundary exercise.
- [docs/DOMAIN.md](DOMAIN.md): domain boundaries and conceptual entities.
- [docs/data-models/phase-1.md](data-models/phase-1.md): relational model foundation.
- [docs/architecture/current-system.md](architecture/current-system.md): current Phase 6 system snapshot.
- [docs/architecture/modular-monolith.md](architecture/modular-monolith.md): module-boundary guide.
- [docs/contracts/](contracts/): report-rendering contract and compatibility playbook.
- [docs/async/](async/): job lifecycle, idempotency, and side-effect guidance.

## Operations And Deployment

- [deploy/dokku/](../deploy/dokku/): first VPS deployment path and checklist.
- [deploy/k3s/](../deploy/k3s/): later k3s learning path, checklist, and starter manifests.
- [docs/deployment/dokku-vs-k3s.md](deployment/dokku-vs-k3s.md): platform comparison.
- [docs/runbooks/DB_CONNECTIVITY.md](runbooks/DB_CONNECTIVITY.md): database readiness troubleshooting.
- [ops/runbooks/](../ops/runbooks/): incident runbooks for API, reporting, and stuck jobs.
- [ops/incidents/](../ops/incidents/): status update and postmortem templates.
- [ops/dashboards/README.md](../ops/dashboards/README.md): internal dashboard and metrics guidance.

## Observability And Performance

- [docs/observability/logging-and-correlation.md](observability/logging-and-correlation.md): structured logs and
  correlation IDs.
- [docs/observability/metrics.md](observability/metrics.md): lightweight internal metrics surfaces.
- [docs/performance/baselines.md](performance/baselines.md): safe local baseline measurement.
- [docs/performance/query-inspection.md](performance/query-inspection.md): query-plan inspection.
- [docs/performance/read-models.md](performance/read-models.md): derived dashboard read model.
- [docs/performance/caching.md](performance/caching.md): one bounded Redis cache and staleness risks.

## Architecture Decisions

- [docs/adr/TEMPLATE.md](adr/TEMPLATE.md): ADR template.
- [docs/adr/0001-report-rendering-boundary.md](adr/0001-report-rendering-boundary.md): reporting boundary decision.
- [docs/adr/0002-fastapi-python-primary-stack.md](adr/0002-fastapi-python-primary-stack.md): primary stack decision.
- [docs/adr/0003-postgres-source-of-truth.md](adr/0003-postgres-source-of-truth.md): durable truth decision.
- [docs/adr/0004-redis-queue-cache-postgres-durability.md](adr/0004-redis-queue-cache-postgres-durability.md): Redis ownership.
- [docs/adr/0005-dokku-first-deployment.md](adr/0005-dokku-first-deployment.md): first deployment path.
- [docs/adr/0006-k3s-later-orchestration-learning-path.md](adr/0006-k3s-later-orchestration-learning-path.md): later
  orchestration path.
- [docs/storage/](storage/): datastore comparison and refusal guidance.
- [docs/languages/](languages/): runtime and polyglot tradeoff guidance.

## Practice And Assessment

- [exercises/TEMPLATE.md](../exercises/TEMPLATE.md): canonical exercise structure.
- [exercises/phase-*/](../exercises/): hands-on phase exercises and capstones.
- [scenarios/phase-*/](../scenarios/): guided failure scenarios.
- [reviews/checklists/](../reviews/checklists/): review gates for API, async, boundaries, incidents,
  performance, architecture, and system-wide readiness.
- [reviews/rubrics/](../reviews/rubrics/): capstone rubrics.
- [reviews/llm/](../reviews/llm/): templates for LLM critique, interviews, log analysis, and
  incident review.
- [quizzes/](../quizzes/): phase quizzes.
- [interviews/](../interviews/): phase interviews, role-track interviews, and mock panels.

## Role Paths And Portfolio

- [paths/README.md](../paths/README.md): role-overlay index.
- [paths/backend-python.md](../paths/backend-python.md): backend/Python emphasis.
- [paths/data-backend.md](../paths/data-backend.md): data/backend emphasis.
- [paths/distributed-systems.md](../paths/distributed-systems.md): distributed systems emphasis.
- [paths/generalist-backend.md](../paths/generalist-backend.md): generalist backend emphasis.
- [paths/architecture-decisions.md](../paths/architecture-decisions.md): architecture decision emphasis.
- [paths/shared-capstone.md](../paths/shared-capstone.md): shared portfolio defense.
- [docs/PORTFOLIO_GUIDE.md](PORTFOLIO_GUIDE.md): public presentation guidance.
- [RELEASE_CHECKLIST.md](../RELEASE_CHECKLIST.md): public-readiness checklist.

## Prompt History

- [.prompts/README.md](../.prompts/README.md): prompt sequence summary.
- [.prompts/PROMPT_01.txt](../.prompts/PROMPT_01.txt) through
  [.prompts/PROMPT_40.txt](../.prompts/PROMPT_40.txt): prompt-driven
  development history.
