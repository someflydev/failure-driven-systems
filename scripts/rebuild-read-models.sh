#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

model="${1:-customer-work-request-stats}"

if [[ "${model}" == "--compose" ]]; then
    model="${2:-customer-work-request-stats}"
    docker compose exec api uv run --no-sync python -m opledger_api.read_models "${model}"
else
    export PYTHONPATH="services/api${PYTHONPATH:+:${PYTHONPATH}}"
    uv run python -m opledger_api.read_models "${model}"
fi
