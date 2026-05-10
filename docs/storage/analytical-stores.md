# Analytical Stores

## Problem This Paradigm Solves

Analytical stores solve large scans, aggregations, time-series exploration,
business intelligence, and historical reporting without overloading the
transactional database. They are optimized for reading many rows, not for
owning current workflow state.

## What OpsLedger Would Gain

OpsLedger might gain faster long-range reporting if the team needed dashboards
over millions of status events, report job attempts, notification outcomes, or
customer work trends. An analytical store could protect Postgres from expensive
ad hoc scans and support product or operations analysis.

The current system only has a small dashboard read model and local performance
baselines. That does not justify ClickHouse, a warehouse, or a separate BI
pipeline yet. Postgres queries, indexes, and rebuildable projections are the
right first tools.

## What OpsLedger Would Pay Operationally

OpsLedger would pay for extraction, loading, schema evolution, backfills,
freshness monitoring, access control, cost controls, and reconciliation with
Postgres. Operators would need to answer whether a number came from current
transactional state, a read model, a cache, or an analytical snapshot.

## Failure Modes

- Freshness gap: analytical dashboards lag current work request state.
- Backfill error: historical aggregates are silently wrong.
- Double counting: retries or duplicate events inflate metrics.
- Expensive query: analysis workload overwhelms the analytical store or budget.
- Wrong decision surface: operators use stale analytics to make current
  workflow decisions.
- Source confusion: teams stop knowing whether Postgres or the warehouse is
  authoritative for a number.

## Interview Explanation Prompts

- Why is the current dashboard read model not the same as a warehouse?
- What dataset size or query pattern would push OpsLedger toward analytics?
- How would you keep analytical numbers reconciled with Postgres?
- Which questions must still use transactional source-of-truth endpoints?
- What would you do before adding ClickHouse or a managed warehouse?
