#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

case "${1:-}" in
  stop)
    docker compose stop worker
    ;;
  start)
    docker compose start worker
    ;;
  status)
    docker compose ps worker
    ;;
  *)
    cat <<'USAGE'
Usage: scripts/scenarios/phase2_worker_down.sh stop|start|status

Stops, starts, or inspects only the Phase 2 Compose worker service.
Read scenarios/phase-2/worker-unavailable.md before using this helper.
USAGE
    ;;
esac
