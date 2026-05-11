# Python And FastAPI

## Where It Fits Today

Python 3.12 with FastAPI is the primary OpsLedger application stack. It runs
the API, worker codebase, report rendering implementation, tests, scripts, and
verification workflow. This keeps early learning focused on backend behavior
instead of cross-language coordination.

## Strengths

- FastAPI exposes typed request and response models, OpenAPI docs, dependency
  injection, and ordinary HTTP behavior.
- SQLAlchemy, Alembic, pytest, Ruff, mypy, and `uv` give a practical backend
  workflow with visible migrations and tests.
- Python is readable for learners inspecting transactions, status changes,
  report jobs, retries, logs, and metrics.
- The same report rendering logic can run in-process for tests or behind the
  stateless reporting HTTP boundary.

## Weaknesses

- CPU-heavy rendering can tie up worker capacity unless measured and bounded.
- Runtime type errors remain possible if schemas, mypy, and tests are weak.
- High concurrency or tight latency targets may require careful worker counts,
  profiling, async discipline, or a different runtime for a narrow component.
- Packaging discipline matters; dependency drift can break local verification
  or deploys.

## Runtime And Deployment Implications

OpsLedger currently has one Python dependency graph and one root `uv`
workflow. The repo-root `Dockerfile` can run the API or reporting service. The
worker runs from the same application package, which simplifies local Compose,
tests, logs, config, and incident debugging.

The cost is that the whole main path shares Python dependency and interpreter
choices. A bad dependency update can affect API, worker, and reporting paths.

## Team Productivity

Python is productive for a small team because code review can cover routes,
models, migrations, workers, and tests without language switching. It also
keeps LLM-assisted review and learner debugging grounded in one ecosystem.

The team must still enforce typing, tests, migration review, and operational
checks. Python does not protect OpsLedger from vague contracts or weak
source-of-truth discipline.

## Operability

Python fits the current observability model: JSON logs, health endpoints,
Prometheus-compatible metrics, pytest coverage, and direct inspection of
Postgres-backed state. Operators need to understand process startup, env vars,
migrations, dependency locking, and worker behavior.

## OpsLedger Fit

Keep Python for the API and worker unless a concrete problem appears. The API
owns durable mutations and database transactions, so rewriting it would be a
large migration. The stateless reporting service is the easiest candidate to
evaluate behind a stable contract, but even that should be justified by
evidence rather than novelty.

## Interview Explanation Prompts

- Why does Python fit the current API and worker?
- Which OpsLedger component would be easiest to rewrite later, and why?
- What evidence would show Python is the bottleneck instead of query shape,
  queue behavior, or service boundaries?
- How do mypy, Pydantic, and tests reduce but not eliminate runtime risk?
