# OpsLedger Storage Decision Guide

OpsLedger currently uses Postgres as the durable source of truth and Redis for
ephemeral queue and cache coordination. This guide compares storage paradigms
against that actual system. It is not a shopping list for new infrastructure.

The default answer for OpsLedger is still: keep facts in Postgres, use Redis
only where disposable coordination or cache speed is worth the operational
cost, and add another datastore only when a named workload creates pressure
Postgres cannot satisfy cleanly.

## Current Ownership

- Postgres owns customer identity, work request state, status history, report
  job state, notification attempts, and the rebuildable dashboard read model.
- Redis owns RQ queue coordination and one short-lived dashboard response cache.
- The reporting service owns no data. It renders a complete snapshot sent by
  the worker.
- Logs and metrics provide evidence, not authoritative state.

## Decision Questions

Before adding a datastore to OpsLedger, answer these questions with evidence:

1. What specific read, write, search, analytical, queue, or retrieval problem
   is painful today?
2. Which current OpsLedger artifact proves the pressure: baseline, query plan,
   incident, scenario, metric, log, or database state?
3. Which fact would the new store own, or is it only a derived copy?
4. How will stale, missing, duplicate, or conflicting data be detected?
5. What does a one-person or small-team operator now have to deploy, back up,
   monitor, secure, upgrade, and restore?
6. What is the rollback path if the store causes more pain than it removes?
7. Why is a Postgres table, index, read model, query change, or Redis cache not
   enough?

If these answers are weak, OpsLedger should not add another datastore.

## Comparison Index

- `docs/storage/relational-postgres.md`
- `docs/storage/document-stores.md`
- `docs/storage/key-value-and-cache.md`
- `docs/storage/queues-and-streams.md`
- `docs/storage/search-indexes.md`
- `docs/storage/analytical-stores.md`
- `docs/storage/vector-storage.md`
- `docs/storage/when-not-to-add-a-datastore.md`

## Interview Framing

A strong OpsLedger storage answer starts with the workload and current
ownership, then names the tradeoff. For example: "Postgres is the right source
of truth because the system needs transactions, constraints, migrations, and
repairable state. Redis is useful only because report work and dashboard cache
responses can tolerate disposable coordination. I would add another store only
after evidence shows one current path cannot be made reliable or fast enough
inside those boundaries."
