# Redis Cache Unavailable Scenario

Use this scenario to confirm that Redis cache failure degrades the dashboard
read path without corrupting Postgres source-of-truth data.

## Purpose

Prove that the cached dashboard endpoint can fall back to the derived read model
when Redis is unavailable.

## Setup

Start the local stack, run migrations, create data, rebuild the read model, and
warm the dashboard cache:

```sh
./scripts/dev-up.sh
./scripts/migrate.sh --compose
scripts/rebuild-read-models.sh
curl -s "http://127.0.0.1:18080/dashboard/customer-work-request-stats?limit=50&offset=0"
```

Capture the source-of-truth state:

```sh
curl -s "http://127.0.0.1:18080/work-requests?limit=10&offset=0"
```

## Trigger

Stop Redis while leaving the API and Postgres running:

```sh
docker compose stop redis
```

Read the cached dashboard endpoint again:

```sh
curl -i "http://127.0.0.1:18080/dashboard/customer-work-request-stats?limit=50&offset=0"
```

## Evidence To Collect

- HTTP status and body from the dashboard endpoint while Redis is down.
- API logs containing `customer_stats_cache_unavailable`.
- `/metrics` lines with `outcome="unavailable"` if available from the API
  process.
- Source-of-truth reads from `GET /work-requests`.
- Any durable database evidence proving source tables were not changed by the
  cache outage.

## Expected Result

The dashboard endpoint should return data from Postgres-backed read-model state
when Postgres is available. Redis outage should not create, update, delete, or
repair source-of-truth rows. If the read model is stale, the endpoint may still
return stale data; that is a read-model freshness issue, not source data
corruption.

Restart Redis:

```sh
docker compose start redis
```

Then read the dashboard again to repopulate cache on a miss.

## Cleanup

Make sure Redis is running again before continuing Phase 2 report queue
exercises:

```sh
docker compose ps
```

## Reflection

- What did the cache outage break?
- What source-of-truth data remained correct?
- Which metric or log would tell an operator Redis is hurting dashboard cache?
- Why would returning `503` for this dashboard be a different product decision?
