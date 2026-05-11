# Failure-Driven Systems

Failure-Driven Systems is a public learning repo for building backend,
distributed systems, operations, and architecture judgment through constrained
practice. The method is simple: encounter a real failure, describe what broke,
make the smallest defensible change, verify it, and explain the tradeoff.

The project is for engineers who want production judgment beyond tutorial
implementation: backend developers, data/backend engineers, generalists who
own deploys and incidents, and interview candidates who need concrete stories
instead of memorized diagrams.

## OpsLedger

All phases build one evolving system: OpsLedger, a small internal operations
workflow app for customers, work requests, status history, reports,
notifications, operational evidence, and later architecture defense.

OpsLedger starts as one FastAPI service backed by Postgres. Later phases add
async report work, one narrow reporting-service boundary, observability,
measured performance work, a bounded Redis cache, and architecture review. None
of those are defaults; each appears only after the repo creates the failure or
pressure that makes it worth discussing.

## Learning Path

1. Single service fundamentals: CRUD, transactions, tests, logs, Postgres, and
   Dokku deployment.
2. Async after synchronous pain: Redis/RQ worker flow, durable job status,
   retries, idempotency, and side-effect reasoning.
3. Careful boundaries: modular monolith first, contract thinking, and one
   stateless reporting-service extraction to study the cost of a split.
4. Observability and incidents: structured logs, metrics, runbooks, scenarios,
   incident timelines, and postmortems.
5. Performance, caching, and read models: baselines before optimization,
   indexes, derived state, cache staleness, and Redis outage behavior.
6. Architecture and interviews: ADRs, datastore/runtime/platform tradeoffs,
   system-wide review, and mock panels grounded in OpsLedger evidence.

Start with `lessons/phase-1/README.md`. Use `curriculum/README.md` and
`curriculum/PHASE_PLAN.md` for the full sequence.

## Constraints

The baseline environment is intentionally modest: one Linux VPS with about 4 GB
RAM, 3 vCPUs, Docker, Dokku for the first deployment path, and k3s available
later as an orchestration learning path. The constraint is part of the lesson:
Postgres remains the source of truth, Redis is used only for bounded queue or
cache coordination, and k3s is not the early default.

## Local Start

Install dependencies and run the verification gate:

```sh
uv venv --python 3.12
uv sync
./scripts/verify.sh
```

Run the API locally:

```sh
uv run uvicorn opledger_api.main:app --app-dir services/api --host 127.0.0.1 --port 18080 --reload
```

Run the local container stack:

```sh
cp .env.example .env
./scripts/dev-up.sh
./scripts/migrate.sh --compose
curl -i http://127.0.0.1:18080/health/live
curl -i http://127.0.0.1:18080/health/ready
```

The `.env.example` values are local placeholders. Do not commit a real `.env`.

## Where To Go

- `docs/NAVIGATION.md`: map of major artifacts.
- `docs/DOMAIN.md`: OpsLedger domain model and boundaries.
- `docs/REPO_MAP.md`: repository structure and responsibilities.
- `exercises/`: learner tasks for each phase.
- `scenarios/`: guided failure drills.
- `reviews/`: checklists, rubrics, and LLM critique templates.
- `quizzes/`: phase self-checks.
- `interviews/`: mock interviews and role-track panels.
- `paths/`: role overlays for backend/Python, data/backend, distributed
  systems, generalist backend, and architecture decisions.
- `deploy/dokku/`: first VPS deployment path.
- `deploy/k3s/`: later orchestration learning path.
- `docs/PORTFOLIO_GUIDE.md`: how to present the work publicly.

## LLM Boundaries

LLMs are reviewers, interviewers, critics, and debugging partners here. They
should not replace the learner's reasoning or generate unexamined answer keys.
Make a serious attempt first, collect evidence, ask for critique, revise, and
then defend the decision in your own words.
