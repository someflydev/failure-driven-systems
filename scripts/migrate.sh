#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

revision="${1:-head}"

if [[ "${revision}" == "--compose" ]]; then
    revision="${2:-head}"
    docker compose exec api uv run --no-sync alembic -c services/api/alembic.ini upgrade "${revision}"
else
    uv run alembic -c services/api/alembic.ini upgrade "${revision}"
fi
