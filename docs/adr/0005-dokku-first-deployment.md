# ADR 0005: Dokku-First Deployment Strategy

## Status

Accepted

## Context

The baseline environment is one Linux VPS with 4 GB RAM, 3 vCPUs, Docker, and
Dokku. The learning goal is to make deploys, config, logs, migrations, process
state, and rollback visible before introducing orchestration.

Relevant artifacts include `deploy/dokku/README.md`,
`deploy/dokku/checklist.md`, the repo-root `Dockerfile`, `docs/CONSTRAINTS.md`,
and `docs/SYSTEM_EVOLUTION.md`.

## Decision

Use Dokku as the first deployment strategy. The documented path deploys the API
from the root `Dockerfile`, links a Dokku Postgres service, runs migrations
explicitly, checks health endpoints, inspects logs, and records rollback
evidence.

k3s, managed platforms, and multi-service production manifests remain out of
scope until a later prompt creates the need.

## Alternatives Considered

- Docker Compose on the VPS: simple and close to local development, but it does
  less to teach app-level deploys, config, logs, process management, and image
  rollback.
- k3s first: useful later, but it would hide early lessons behind Kubernetes
  objects before learners understand the smaller operational model.
- Managed PaaS: practical for teams that want less server ownership, but the
  curriculum intentionally exposes VPS responsibilities.
- Raw systemd and Docker commands: transparent, but more bespoke than needed
  for the first deployment path.

## Consequences

Dokku keeps the deployment target small and concrete. Learners see app config,
service linking, migrations, health checks, logs, and rollback without needing
a cluster.

The tradeoff is limited orchestration capability. The current docs should not
claim a full Dokku production topology for API, worker, Redis, and reporting
service until that has been written and exercised.

## Failure Modes

- Bad config: the app may boot incorrectly or fail readiness until env vars are
  fixed and the process restarts.
- Failed migration: the image can run against an incompatible schema.
- Missing Postgres link: `DATABASE_URL` is absent or wrong.
- Bad deploy: a new image may fail boot or regress behavior.
- Resource pressure: a tiny VPS can run out of memory or CPU before a larger
  platform would.

## Operational Cost

Operators must maintain one VPS, Dokku, Docker, the Dokku Postgres plugin,
secrets, domain/proxy settings, image tags, migrations, logs, and backups. This
is lower than running a cluster, but it is still real operational ownership.

## Rollback Or Reversal

For config issues, restore the previous value and restart. For bad images,
deploy a known-good tag or revert the Git commit and redeploy. For schema
issues, prefer forward repair unless a down migration has been proven safe.
Moving away from Dokku later requires new deployment docs, runbooks, secrets
handling, migration workflow, and rollback practice.

## Interview Defense

Dokku fits the current system because the team and workload are small, and the
lesson is operational discipline rather than orchestration. I would move to
k3s or a managed platform only when process count, release coordination,
isolation, scheduling, or operational toil exceeds what Dokku can clearly
handle.
