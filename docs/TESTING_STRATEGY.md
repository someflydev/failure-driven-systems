# Testing Strategy

OpsLedger Phase 1 uses fast local checks to teach delivery discipline without
introducing deployment or distributed-system machinery before the curriculum
needs it.

## Local Verification Entry Point

Run all local verification through:

```sh
./scripts/verify.sh
```

That script is the single documented local verification entry point. It checks
formatting, linting, static typing, and the test suite in one repeatable path so
learners do not have to remember which partial command proves a change.

## Current Test Layers

Unit-style model and schema tests cover Pydantic validation rules and
SQLAlchemy relationship behavior without starting the API. These tests are fast
and make it clear which failures are rejected before a request reaches route
code.

API tests use FastAPI's test client with an isolated in-memory SQLite database.
The shared fixtures in `services/api/tests/conftest.py` create one test
database per test, override the API database dependency, and seed customers or
work requests through HTTP so tests exercise the same validation and route code
as callers. These tests cover customer creation, duplicate email conflict,
missing records, work request creation, status filters, pagination bounds,
status transitions, status history, durable report job status, and report
result availability.

Report worker tests exercise the worker function directly against the isolated
test database. They cover running, success, failed attempts, controlled local
failure injection, attempt counts, persisted error evidence, and bounded RQ
retry configuration without requiring a live Redis server.

Database utility tests cover database URL normalization and sanitized readiness
target reporting. They protect operational behavior without requiring a real
Postgres server.

Health tests keep liveness and readiness separate. Liveness must answer without
checking external dependencies. Readiness must report database availability or a
sanitized unavailable response.

Migration checks are outside the default fast gate. The automated suite
validates model and API behavior, but it uses isolated test databases and is
not a substitute for checking Alembic against Postgres. When the Compose stack
is running, use the optional smoke check:

```sh
./scripts/smoke/postgres_migrations.sh
```

That script applies migrations inside the API container, checks
`/health/ready`, and exercises one tiny customer creation path against the
Compose Postgres database.

Manual operational checks are also intentionally small: start the API, call
`GET /health/live`, call `GET /health/ready`, and exercise one successful CRUD
path plus one predictable failure path. These checks prove the service wiring
works outside the in-process test client.

Docker Compose checks are now part of local operational verification: build and
start the current stack, run Alembic migrations explicitly, and confirm health
endpoints from the host. These local checks are not a substitute for later
deployment smoke tests.

## Deferred Layers

Deployment smoke tests are deferred until Dokku or another concrete deployment
target exists in the repository.

Scenario and incident tests are deferred until Phase 1 has enough operational
surface area to make scenario work meaningful.

Cache tests arrive with the Phase 5 cache behavior. k3s verification currently
means static manifest syntax checks and deployment checklist review; cluster
smoke tests are deferred until a prompt requires an actual k3s runtime drill.

Property-based tests are deferred unless a small, clear invariant appears that
would be better taught through generated examples than through a few readable
edge-case tests.

## Learner Habit

Before asking an LLM for more edge cases, write the test matrix yourself: name
the success path, boundary values, conflict cases, missing records, invalid
state transitions, and operational checks. Then use the LLM as a reviewer that
looks for gaps in your reasoning.
