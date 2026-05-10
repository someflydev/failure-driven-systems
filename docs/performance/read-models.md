# Derived Read Models

Phase 5 introduces derived read models after measurement and query inspection.
A read model is stored data shaped for a read path, but it is not the source of
truth. In OpsLedger, customer dashboard stats are derived from `customers`,
`work_requests`, and `work_request_status_events`.

## Current Read Model

`customer_work_request_stats` stores one row per customer:

- total work requests
- counts by work request status
- status event count
- rebuild timestamp

The dashboard endpoint reads this table:

```http
GET /dashboard/customer-work-request-stats
```

The source-of-truth endpoints still read the authoritative tables:

```http
GET /customers
GET /work-requests
GET /work-requests/{work_request_id}
GET /work-requests/{work_request_id}/status-events
```

One owner remains responsible for each authoritative fact:

- Customer identity is owned by `customers`.
- Work request title, description, customer link, and current status are owned
  by `work_requests`.
- Status transition history is owned by `work_request_status_events`.
- `customer_work_request_stats` owns no authoritative fact; it only stores a
  rebuildable projection.

## Rebuilds

Rebuild the read model explicitly:

```sh
scripts/rebuild-read-models.sh
```

The command deletes the current projection and recalculates it from source
tables. That makes the derivation visible and reviewable. If the command is
wrong, the fix is to correct the rebuild logic and run it again; source data is
not replaced.

## Staleness

The read model is intentionally not updated by hidden triggers. That means it
can be stale:

1. Rebuild `customer_work_request_stats`.
2. Create or update a work request.
3. Read `GET /dashboard/customer-work-request-stats`.
4. Read `GET /work-requests`.

The dashboard may show the previous totals while the source endpoint already
shows the new durable truth. This is not a database bug. It is the tradeoff of
serving a pre-shaped projection.

User impact must be named in product terms. A stale dashboard might understate
open work, overstate completed work, or make a customer appear quieter than
they are. Detail pages and workflow endpoints must stay source-of-truth reads
when correctness matters more than dashboard speed.

## Different From Caching

A cache usually stores the result of a request or expensive calculation behind
the same read contract, often with eviction, time-to-live, or invalidation
rules. A read model is a named data model with its own table, rebuild logic,
endpoint, and staleness contract.

Both are derived state, but they fail differently:

- Cache failures often involve missing keys, stale keys, eviction, or stampede.
- Read-model failures often involve incomplete rebuilds, lagging projections,
  schema drift, and disagreement with source tables.

OpsLedger adds the read model before cache so learners can see derived data
ownership, rebuilds, and visible staleness without adding another datastore or
cache invalidation policy.
