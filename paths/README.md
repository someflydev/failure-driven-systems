# Role Path Overlays

Role paths route learners through the same OpsLedger system with different
emphasis. They are overlays on the existing phase sequence, not separate
codebases, alternate projects, or forks of the exercises.

Every path should still preserve the core learning shape:

- Build against the same API, worker, reporting service, Postgres, Redis, logs,
  metrics, deployment notes, and review materials.
- Cite existing exercises, scenarios, reviews, interviews, and docs instead of
  copying them into a role-specific track.
- Produce portfolio artifacts from concrete OpsLedger work, not generic system
  design diagrams.
- Treat optional extensions as optional. A learner should be able to defend a
  strong path without completing every extension.

## Available Paths

- `paths/backend-python.md`: Python/FastAPI backend implementation, data
  integrity, tests, async jobs, and service-boundary judgment.
- `paths/data-backend.md`: source of truth, query shape, read models,
  staleness, rebuilds, and datastore restraint.
- `paths/distributed-systems.md`: async work, partial failure, retries,
  contracts, incidents, and operational debugging.
- `paths/generalist-backend.md`: broad backend ownership across implementation,
  deployment, operations, performance, and explanation.
- `paths/architecture-decisions.md`: decision memos, ADRs, tradeoff defense,
  rollback, and architecture interviews grounded in built artifacts.
- `paths/shared-capstone.md`: final cross-path portfolio defense using the
  same OpsLedger evidence package.

## How To Use A Path

1. Complete the phase lessons in `lessons/` in order.
2. Use one path guide to bias which exercises, scenarios, reviews, and
   interviews receive extra attention.
3. Keep a role-specific evidence folder outside the repo or in personal notes:
   command output, screenshots, logs, database observations, decisions, and
   weak-area revisions.
4. Finish with `paths/shared-capstone.md` and the relevant guide in
   `interviews/role-tracks/`.

Switching paths should change emphasis, not the system being built.
