# Derived Read Models

## Phase

Phase 5: Performance, Caching, And Read Models. This work belongs here because
learners have measured read behavior, inspected query shape, and can now study
derived data before adding cache.

## Concepts

- Derived read models
- Source-of-truth ownership
- Explicit rebuild commands
- Stale dashboard data
- Eventual consistency without new infrastructure
- Read optimization tradeoffs

## Prerequisites

Read these first:

- `docs/performance/baselines.md`
- `docs/performance/query-inspection.md`
- `docs/performance/read-models.md`
- `docs/async/phase-2-job-lifecycle.md`
- `exercises/phase-5/01-measure-before-optimizing.md`
- `exercises/phase-5/02-pagination-and-indexes.md`
- `exercises/TEMPLATE.md`

You should be able to create customers and work requests, update work request
status, run migrations, and compare dashboard output with source-of-truth API
responses.

## Build/Change Task

Use the `customer_work_request_stats` read model as a dashboard projection.

1. Create at least two customers.
2. Create work requests with different statuses.
3. Run the read-model rebuild command.
4. Read `GET /dashboard/customer-work-request-stats`.
5. Create or update another work request without rebuilding.
6. Read the dashboard endpoint again and prove it is stale.
7. Read `GET /work-requests` or `GET /work-requests/{id}` and prove the
   source-of-truth endpoint is correct.
8. Rebuild the read model and confirm the dashboard catches up.

Write a short note explaining which user or operator could be misled by the
stale dashboard and which endpoint they should trust for current workflow
truth.

## Constraints

- Do not replace `customers`, `work_requests`, or
  `work_request_status_events`.
- Do not add Redis cache or any new datastore.
- Do not hide staleness behind automatic triggers.
- Do not treat `customer_work_request_stats` as authoritative.
- Do not update source-of-truth endpoints to read from the derived table.
- Keep the rebuild path explicit and repeatable.

## Failure Modes

- A dashboard row lags behind newly created work.
- A status count stays wrong after a status update until rebuild.
- A failed or partial rebuild leaves dashboard output incomplete.
- Learners or users treat fast dashboard data as current truth.
- The rebuild query duplicates ownership by copying facts that should remain
  authoritative in source tables.
- Tests assert only the happy path and never prove stale behavior.

## Expected Reasoning

After completing the work, explain:

- Which tables own the authoritative facts.
- Which facts the read model derives and why those facts are rebuildable.
- Why stale data is possible before rebuild.
- What user impact stale dashboard data could have.
- Why source-of-truth endpoints must remain correct.
- Why this read model is different from adding cache.
- What monitoring or admin evidence would matter before using the pattern in a
  production system.

## Verification

Run:

```sh
./scripts/verify.sh
scripts/rebuild-read-models.sh
```

Manual checks:

```sh
curl -s http://127.0.0.1:18080/dashboard/customer-work-request-stats
curl -s http://127.0.0.1:18080/work-requests?limit=10
```

Your submitted evidence should include:

- Dashboard output immediately after a rebuild.
- Dashboard output after a source-table change but before rebuild.
- Source-of-truth output proving the current state.
- Dashboard output after the second rebuild.
- A short user-impact explanation for the stale interval.

## Reflection Questions

- Which endpoint should a dispatcher trust during active work?
- How long could this dashboard be stale before it becomes harmful?
- What would make an automatic updater worth its complexity?
- What would make a full rebuild too expensive?
- How would you detect that the projection disagrees with source tables?
- Why is this not a cache, even though it is derived data?

## LLM Usage

Use an LLM as a reviewer after you have captured your stale-data evidence. Ask
it to critique whether your ownership explanation is clear and whether your
user-impact note names a concrete risk. Do not ask it to invent API output,
database rows, or rebuild results.

## Path-Specific Extensions

Backend: add or review a test that proves stale dashboard data before rebuild
and fresh dashboard data after rebuild.

Operations: write a short runbook note for when the dashboard appears wrong
but work request detail pages are correct.

Architecture: compare this explicit rebuild design with a trigger-based
projection and name the operational tradeoffs.

Interview: practice explaining why a system can deliberately serve stale
dashboard data while preserving correct workflow state.

## Deployment/Debugging Actions If Relevant

Run migrations before using the dashboard endpoint, then run
`scripts/rebuild-read-models.sh` in the target environment. If dashboard totals
look wrong, compare them with `GET /work-requests` before changing code.
