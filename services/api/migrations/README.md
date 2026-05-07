# API Migrations

Alembic migrations for the OpsLedger API live here.

Create a migration after models are introduced:

```sh
uv run alembic -c services/api/alembic.ini revision --autogenerate -m "describe change"
```

Run migrations against the configured database:

```sh
DATABASE_URL=postgresql+psycopg://localhost:55432/opledger \
  uv run alembic -c services/api/alembic.ini upgrade head
```

Phase 1 starts with customers and work requests. Migration files should keep
deterministic revision identifiers and names so learners can compare schema
history without generated noise.
