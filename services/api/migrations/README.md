# API Migrations

Alembic migrations for the OpsLedger API live here.

Create a migration after models are introduced:

```sh
uv run alembic -c services/api/alembic.ini revision --autogenerate -m "describe change"
```

Run migrations against the configured database:

```sh
DATABASE_URL=postgresql+psycopg://localhost:5432/opledger \
  uv run alembic -c services/api/alembic.ini upgrade head
```

This phase intentionally has no domain tables yet, so `versions/` starts empty.
The `.gitkeep` file only keeps the directory present for future revisions.
