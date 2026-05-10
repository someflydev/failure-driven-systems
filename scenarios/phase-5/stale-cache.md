# Stale Dashboard Cache Scenario

Use this scenario to observe how Redis cache staleness differs from
source-of-truth data and read-model staleness.

## Purpose

Prove that `GET /dashboard/customer-work-request-stats` can return stale
summary data while source-of-truth work request endpoints remain correct.

## Setup

Start the local stack, run migrations, and create at least one customer and one
work request. Rebuild the read model:

```sh
./scripts/dev-up.sh
./scripts/migrate.sh --compose
scripts/rebuild-read-models.sh
```

Warm the cache:

```sh
curl -s "http://127.0.0.1:18080/dashboard/customer-work-request-stats?limit=50&offset=0"
```

## Trigger

Create or update another work request for the same customer without rebuilding
the read model:

```sh
curl -s http://127.0.0.1:18080/work-requests
```

Then read the dashboard again:

```sh
curl -s "http://127.0.0.1:18080/dashboard/customer-work-request-stats?limit=50&offset=0"
```

## Evidence To Collect

- Dashboard response after the initial rebuild and cache warm.
- Dashboard response after the source-table change.
- `GET /work-requests?limit=10&offset=0` proving the source table changed.
- `GET /dashboard/customer-work-request-stats?bypass_cache=true` showing what
  the derived table currently says.
- `/metrics` lines for `opledger_cache_access_total`.

## Expected Result

The dashboard can show the old total. Bypassing Redis may still show the old
total if the read model has not been rebuilt. The source-of-truth work request
endpoint should show the current work request state.

After running:

```sh
scripts/rebuild-read-models.sh
```

the cache should be invalidated best-effort and the next dashboard read should
reflect the rebuilt projection.

## Cleanup

No special cleanup is needed beyond stopping the local stack if this was a
disposable local dataset:

```sh
./scripts/dev-down.sh
```

## Reflection

- Which stale interval came from Redis, and which came from the read model?
- Which endpoint should a dispatcher trust for current work?
- How long could this dashboard safely be stale?
- What user harm would make this cache unacceptable?
