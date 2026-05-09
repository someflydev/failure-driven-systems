#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.."

case "${1:-}" in
  stop)
    docker compose stop redis
    ;;
  start)
    docker compose start redis worker
    ;;
  status)
    docker compose ps redis worker
    ;;
  *)
    cat <<'USAGE'
Usage: scripts/scenarios/phase2_redis_down.sh stop|start|status

Stops, starts, or inspects the Phase 2 Redis service and worker.
It does not remove volumes. Read scenarios/phase-2/redis-unavailable.md first.
USAGE
    ;;
esac
