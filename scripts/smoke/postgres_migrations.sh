#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

email="smoke+$(date +%s)@example.invalid"

if ! docker compose ps api postgres >/dev/null 2>&1; then
    echo "Docker Compose is not available or this is not a Compose project."
    echo "Start the local stack with ./scripts/dev-up.sh, then rerun this script."
    exit 1
fi

if ! docker compose ps --services --status running | grep -Fxq 'api'; then
    echo "The api container is not running."
    echo "Start the local stack with ./scripts/dev-up.sh, then rerun this script."
    exit 1
fi

if ! docker compose ps --services --status running | grep -Fxq 'postgres'; then
    echo "The postgres container is not running."
    echo "Start the local stack with ./scripts/dev-up.sh, then rerun this script."
    exit 1
fi

./scripts/migrate.sh --compose
curl -fsS http://127.0.0.1:18080/health/ready >/dev/null
curl -fsS \
    -H 'Content-Type: application/json' \
    -d "{\"name\":\"Smoke Customer\",\"email\":\"${email}\"}" \
    http://127.0.0.1:18080/customers >/dev/null

echo "Postgres migration smoke passed."
