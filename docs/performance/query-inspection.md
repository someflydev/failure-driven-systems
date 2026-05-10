# Query Inspection

Phase 5 optimization starts with measured behavior, then inspects the query
shape before changing storage. For OpsLedger, Postgres remains the source of
truth, so the first tools are SQL, `EXPLAIN`, and `EXPLAIN ANALYZE`, not cache
or read replicas.

## Hot Read Path

The current hot read path is:

```http
GET /work-requests?status=open&limit=50&offset=0
```

The API returns a bounded page of work requests in predictable recent-first
order:

```sql
SELECT *
FROM work_requests
WHERE status = 'open'
ORDER BY created_at DESC, id DESC
LIMIT 50 OFFSET 0;
```

The `id` tie-breaker matters because many local rows can share the same
database timestamp. Without a tie-breaker, adjacent pages can become unstable
when rows have equal `created_at` values.

## Inspect A Plan

Use `EXPLAIN` when you want the planner's chosen shape without running the
query:

```sql
EXPLAIN
SELECT *
FROM work_requests
WHERE status = 'open'
ORDER BY created_at DESC, id DESC
LIMIT 50 OFFSET 0;
```

Use `EXPLAIN ANALYZE` only against a safe local or disposable environment when
you want actual timing and row counts:

```sql
EXPLAIN ANALYZE
SELECT *
FROM work_requests
WHERE status = 'open'
ORDER BY created_at DESC, id DESC
LIMIT 50 OFFSET 0;
```

Record:

- Dataset size and status distribution.
- Whether the plan uses a sequential scan or an index scan.
- Whether Postgres performs a separate sort.
- Estimated rows versus actual rows.
- Planning time and execution time.
- The exact query and migration state.

## Index Added In Phase 5

The narrow index for this access pattern is:

```sql
CREATE INDEX ix_work_requests_status_created_at_id
ON work_requests (status, created_at, id);
```

This index is justified as a measured-access-pattern hypothesis: filtered work
request lists use `status`, then recent-first ordering by `created_at` and `id`.
It is not a general "make work requests fast" index, and it does not justify
adding indexes for every column.

Expected improvement to test on a meaningful dataset:

- Fewer rows scanned for selective status filters.
- Less separate sorting for `ORDER BY created_at DESC, id DESC`.
- More predictable page latency as the table grows.

Evidence still matters. If the table is tiny or most rows have the same status,
Postgres may correctly choose a sequential scan. That is not a failure; it
means the dataset does not yet prove the index is useful.

## Write-Side Tradeoff

Every index has cost:

- Inserts into `work_requests` must also write an index entry.
- Status updates must maintain this index because `status` is part of it.
- The index consumes disk and memory cache space.
- More indexes slow migrations and make writes more expensive.

Keep indexes narrow, tied to real access patterns, and removable if future
measurements show they are not earning their cost.
