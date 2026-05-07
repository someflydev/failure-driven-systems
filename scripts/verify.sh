#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
