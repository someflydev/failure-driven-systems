# Failure-Driven Systems

Failure-Driven Systems is a learning platform for building practical backend,
data/backend, distributed systems, platform, and architecture judgment through
constrained, observable practice.

This repository is not a toy tutorial collection. It is the doctrine,
curriculum frame, navigable skeleton, and initial OpsLedger API scaffold for a
public learning project where concepts are earned through experience: learners
hit friction, name the failure, recognize the pattern, vary the situation,
explain the tradeoff, and defend the decision under questioning.

## Who It Is For

This project is for engineers who want stronger production judgment, especially:

- Backend engineers moving beyond endpoint implementation.
- Data/backend engineers who need source-of-truth, ingestion, and reliability
  instincts.
- Generalist platform engineers practicing deployment, operations, and incident
  response on modest infrastructure.
- Interview candidates who need to explain architecture decisions from concrete
  experience instead of memorized diagrams.

## What Makes It Different

The platform starts from a deliberately constrained environment: one Linux VPS
with 4 GB RAM, 3 vCPUs, Dokku installed, Docker available, and k3s available
later. The constraint is part of the curriculum. Learners must make small,
defensible choices before reaching for distributed machinery.

The doctrine favors:

- Failure before abstraction.
- Friction before naming.
- A modular monolith before service sprawl.
- Postgres as the source of truth.
- Redis only after a later failure creates the need.
- Dokku before k3s.
- LLMs as reviewers, interviewers, and critics, not ghostwriters.

LLMs are part of the learning environment, but their use is constrained by the
doctrine. Learners should struggle first, ask for critique second, request
explanation third, and compare solutions only after a serious attempt.

## System Domain

All later lessons build one evolving system: OpsLedger, a small internal
operations workflow platform for tracking customer work requests, status
changes, operational notes, generated reports, and later notifications.

OpsLedger is deliberately ordinary. It supports concrete CRUD early, then
naturally creates pressure for transactions, background jobs, side effects,
module boundaries, observability, read models, caching, and architecture
defense. See `docs/DOMAIN.md` for the domain boundaries and conceptual
entities.

## Local Development

The initial OpsLedger API scaffold lives in `services/api/` and uses Python
3.12 with repo-root `uv` tooling.

```sh
uv venv --python 3.12
uv sync
./scripts/verify.sh
```

Run the minimal API locally with:

```sh
uv run uvicorn opledger_api.main:app --app-dir services/api --host 127.0.0.1 --port 18080 --reload
```

The liveness endpoint is available at `GET /health/live`. It intentionally does
not require a database or other external service. The readiness endpoint at
`GET /health/ready` checks Postgres connectivity.

### Local Docker Compose

Phase 1 local container development uses Docker Compose with only the API and
Postgres:

```sh
cp .env.example .env
./scripts/dev-up.sh
```

The `.env.example` values are local placeholders. Replace them for your own
machine and do not commit a real `.env` file.

In another shell, apply migrations explicitly:

```sh
./scripts/migrate.sh --compose
```

Then check the service:

```sh
curl -i http://127.0.0.1:18080/health/live
curl -i http://127.0.0.1:18080/health/ready
```

Run the repository verification gate from the host:

```sh
./scripts/verify.sh
```

Stop the local containers with:

```sh
./scripts/dev-down.sh
```

For Phase 1 operational practice, use:

- `deploy/dokku/README.md` for the first VPS deployment path.
- `deploy/dokku/checklist.md` for deploy preflight and post-deploy checks.
- `docs/runbooks/DB_CONNECTIVITY.md` for database readiness troubleshooting.
- `ops/runbooks/phase-1-first-response.md` for first-response checks.
- `ops/runbooks/dokku-api-incident.md` for Dokku API incidents.
- `scenarios/phase-1/db-unavailable.md` for a guided database outage drill.
- `exercises/phase-1/04-db-down-debugging.md` for the learner exercise tied to
  that drill.
- `exercises/phase-1/05-local-container-workflow.md` for the Compose workflow
  exercise.
- `exercises/phase-1/06-dokku-first-deploy.md` for the first Dokku deployment
  exercise.

## Phase Sequence

The curriculum progresses through six phases:

1. Single service fundamentals.
2. Async work after synchronous pain appears.
3. Careful boundaries before service extraction.
4. Observability, operations, and incidents.
5. Performance, caching, and read models when justified by measured pressure.
6. Architecture defense, system design, and interview readiness.

Additional directories and application code should appear only when later
prompts justify them. This repository should remain easy to navigate, honest
about what exists, and strict about teaching judgment before tooling.
