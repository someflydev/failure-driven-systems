# ADR 0003: Postgres As Source Of Truth

## Status

Accepted

## Context

OpsLedger stores customer identity, work request lifecycle state, status
events, report job status, notification attempts, and the Phase 5 customer
dashboard read model. The system needs transactions, constraints, migrations,
repairable state, and direct inspection by a learner or small operator.

Relevant artifacts include `services/api/migrations/versions/`,
`services/api/opledger_api/models.py`, `docs/data-models/phase-1.md`,
`docs/async/phase-2-job-lifecycle.md`, and
`docs/performance/read-models.md`.

## Decision

Use Postgres as the durable source of truth. Redis, report output rendering,
metrics, logs, and derived read models can support the system, but they do not
replace authoritative Postgres records.

## Alternatives Considered

- Redis as primary store: simpler for queues and cache, but too weak for
  durable relational ownership, migrations, and repairable history.
- Document database: could store flexible records, but the current domain is
  relational and benefits from foreign keys, uniqueness, and transactions.
- Event store first: useful in event-centered systems, but it would add
  conceptual and operational weight before OpsLedger needs it.
- Managed cloud database: operationally attractive, but the baseline curriculum
  intentionally keeps database ownership visible on a self-operated VPS.

## Consequences

Postgres makes transactions and source-of-truth boundaries visible. It supports
explicit migrations, relational constraints, query-plan inspection, derived
read-model rebuilds, and durable report job evidence.

The tradeoff is that schema changes require migration discipline, Postgres
outages are hard dependencies for the API, and a tiny VPS can become database
limited if queries, indexes, connection counts, or read models are handled
carelessly.

## Failure Modes

- Postgres unavailable: readiness fails and durable API behavior stops.
- Bad migration: deploy may succeed while new routes fail against the schema.
- Slow queries: user-visible latency rises until query shape, indexes, or read
  models are addressed with evidence.
- Derived read model stale: dashboard output can lag source tables until
  rebuild or refresh logic catches up.

## Operational Cost

Operators must run Alembic migrations, protect connection strings, inspect
readiness, manage backups outside this scaffold, and understand rollback as a
data decision rather than just an image deploy. On Dokku, `DATABASE_URL` comes
from the Postgres service link described in `deploy/dokku/README.md`.

## Rollback Or Reversal

Application rollbacks are usually possible through a tagged image or Git
revert, but schema rollback is not automatically safe. Risky changes should
prefer forward-compatible migrations and forward repair. Moving facts out of
Postgres would require a migration plan, dual-read or dual-write period, and a
clear new owner for each fact.

## Interview Defense

Postgres is the right default here because OpsLedger is fact-heavy, small, and
operated by a small team that needs inspectable durable state more than exotic
scale. I would consider another store only for a specific workload with
measured pressure and a clear ownership model that Postgres cannot satisfy.
