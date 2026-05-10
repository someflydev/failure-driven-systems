#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

export PYTHONPATH="services/api${PYTHONPATH:+:${PYTHONPATH}}"

uv run python -m opledger_api.read_models customer-work-request-stats
