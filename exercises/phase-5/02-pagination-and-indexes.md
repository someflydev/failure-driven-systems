# Pagination And Indexes

## Phase

Phase 5: Performance, Caching, And Read Models. This work belongs here because
learners have already collected baseline evidence and can now connect bounded
pagination, predictable ordering, query plans, and narrowly justified indexes.

## Concepts

- Limit/offset pagination bounds
- Stable ordering across pages
- Filtered list access patterns
- `EXPLAIN` and `EXPLAIN ANALYZE`
- Composite indexes
- Index write and storage cost
- Evidence-backed optimization

## Prerequisites

Read these first:

- `docs/performance/baselines.md`
- `docs/performance/query-inspection.md`
- `docs/observability/metrics.md`
- `exercises/phase-5/01-measure-before-optimizing.md`
- `exercises/TEMPLATE.md`

You should be able to start the local stack, run migrations, seed work
requests with different statuses, run the baseline script, and connect to the
database.

## Build/Change Task

Review the `GET /work-requests` list endpoint and confirm that pagination is
bounded, ordering is predictable, and status filtering has a documented access
pattern.

Then compare the filtered list query before and after the Phase 5 index:

```sql
SELECT *
FROM work_requests
WHERE status = 'open'
ORDER BY created_at DESC, id DESC
LIMIT 50 OFFSET 0;
```

Capture either:

- before/after `EXPLAIN` or `EXPLAIN ANALYZE` output on a meaningful local
  dataset, or
- a written explanation of the expected plan improvement if your local database
  is too small to show a useful difference.

Your notes must include whether the index is actually used and why that result
does or does not justify keeping it.

## Constraints

- Do not add caching.
- Do not add read replicas.
- Do not add a read model.
- Do not add indexes for every filterable field.
- Do not claim performance improved unless you have measured before/after
  evidence.
- Keep Postgres as the system of record.

## Failure Modes

- Returning pages without a deterministic `ORDER BY`.
- Allowing unbounded limits that let one request scan or serialize too much
  data.
- Adding an index before naming the query it serves.
- Ignoring the write cost of an index on a table that receives inserts and
  status updates.
- Treating a tiny local sequential scan as proof that indexes never matter.
- Treating an index scan on a tiny local table as proof of production
  improvement.

## Expected Reasoning

After completing the work, explain:

- Why `limit` has a maximum.
- Why `ORDER BY created_at DESC, id DESC` is more predictable than relying on
  implicit database order.
- Why `status, created_at, id` matches the filtered work request list query.
- What write-side cost the index adds.
- What dataset or status distribution would make the index more or less useful.
- Why the next optimization is still not cache by default.

## Verification

Run:

```sh
./scripts/verify.sh
scripts/perf/baseline.py list-work-requests --dry-run
```

If a local database is available, also run migrations and capture a plan:

```sh
./scripts/migrate.sh --compose
psql "$DATABASE_URL"
```

Inside `psql`, inspect:

```sql
EXPLAIN
SELECT *
FROM work_requests
WHERE status = 'open'
ORDER BY created_at DESC, id DESC
LIMIT 50 OFFSET 0;
```

Your submitted evidence should include the command, dataset size, migration
state, plan summary, and whether the index was used.

## Reflection Questions

- What happens to page stability when multiple rows share the same timestamp?
- Why can an offset become expensive on a very large table?
- Which workload pays the index maintenance cost?
- When would you remove an index after adding it?
- What evidence would justify keyset pagination later?

## LLM Usage

Use an LLM as a reviewer after you have captured your own query plan or written
your own expected-plan explanation. Ask it to critique whether the index
matches the query and whether your evidence overclaims improvement. Do not ask
it to invent query plans, benchmark numbers, or production conclusions.

## Path-Specific Extensions

Backend: add tests for pagination bounds, stable ordering, and filtered list
behavior.

Operations: capture `/metrics` before and after a bounded list-work-requests
baseline and compare it with the query-plan evidence.

Architecture: write a short note explaining why cache would add derived state
and invalidation concerns that this exercise deliberately avoids.

Interview: practice defending a case where an index is reasonable but still
has to be justified by observed access patterns.

## Deployment/Debugging Actions If Relevant

Use a disposable local or owned Dokku database only. Do not run
`EXPLAIN ANALYZE` against shared or customer-like data unless you understand the
query cost and have permission.
