# ADR 0006: k3s As A Later Orchestration Learning Path

## Status

Accepted for learning

## Context

OpsLedger started with Dokku on one constrained Linux VPS because Phase 1
needed visible deploy, config, migrations, logs, health, and rollback practice
before orchestration. Later phases added Redis/RQ, a worker, a stateless
reporting service, metrics, and more operational drills.

The current practice target remains modest: one VPS with 4 GB RAM and 3 vCPUs.
k3s is available on the VPS and can teach orchestration concepts, but the
system does not have evidence that Kubernetes should replace Dokku as the
default starting path.

Relevant artifacts include `deploy/dokku/`, `deploy/k3s/`,
`docs/deployment/dokku-vs-k3s.md`, `docs/architecture/current-system.md`,
`docs/CONSTRAINTS.md`, and `docs/adr/0005-dokku-first-deployment.md`.

## Decision

Introduce k3s as a later learning path for orchestration, not as the default
production recommendation. The k3s material should use plain manifests first
and focus on the API, worker, and stateless reporting service. It should teach
Deployments, Services, ingress, replicas, rolling updates, config, secret
boundaries, health probes, logs, rollout status, rollback, and resource
pressure.

Dokku remains the first deployment path. Earlier phases must not require k3s.
The k3s starter path must not silently move Postgres or Redis in-cluster.

## Alternatives Considered

- Keep only Dokku: reasonable for the small production shape, but it would not
  teach orchestration concepts such as Services, probes, rollouts, and
  scheduler behavior.
- Replace Dokku with k3s: rejected because it would front-load Kubernetes
  complexity before learners understand the simpler deployment model.
- Add Helm immediately: rejected because templates would hide the Kubernetes
  objects learners need to read first.
- Run Postgres and Redis in-cluster by default: rejected because stateful
  services require persistent storage, backup, restore, upgrade, and resource
  planning that should be deliberate.
- Use managed Kubernetes or cloud-managed databases: useful comparisons, but
  outside the baseline self-operated VPS constraint.

## Consequences

Learners can compare simple app-platform operation with orchestration using
the same OpsLedger components. k3s makes rolling updates, replicas, internal
service discovery, readiness probes, resource requests, pod restarts, and
cluster events concrete.

The tradeoff is more operational surface: Kubernetes objects, ingress behavior,
image pulls, node pressure, config drift, and extra debugging steps. On a
4 GB VPS, the cluster overhead and app resource limits must be treated as part
of the lesson.

## Failure Modes

- Kubernetes becomes the default answer before workload or team evidence
  justifies it.
- The learner exposes `/metrics` or debug-style endpoints through public
  ingress.
- Real secrets are committed in manifests or copied into durable notes.
- Postgres is moved in-cluster without backup, restore, persistent volume, and
  migration discipline.
- Redis is treated as durable because it now runs under Kubernetes.
- Worker replicas are increased without understanding idempotency, duplicate
  execution, and side-effect protection.
- `kubectl rollout undo` is used after an incompatible migration without a
  data repair plan.
- The small VPS hits memory, CPU, disk, or image-pull pressure.

## Operational Cost

k3s adds cluster installation and upgrades, Kubernetes API health, manifests,
ingress, Services, probes, resource requests and limits, rollout monitoring,
pod event inspection, and cluster-level incident debugging. Operators need to
know both application evidence and Kubernetes evidence.

This cost is acceptable for a later learning module. It is not automatically
justified for the smallest production version of OpsLedger.

## Rollback Or Reversal

For the learning path, k3s can be ignored without affecting earlier phases or
the Dokku deployment docs. A failed k3s rollout can be reversed with deployment
rollback only when the schema and config remain compatible. If the deployment
introduced a migration, rollback must be evaluated as a data problem and may
need forward repair.

If the team decides k3s is not paying for itself, keep the Dokku path and
remove k3s from active operation while preserving the comparison docs as
architecture learning material.

## Interview Defense

k3s is useful for OpsLedger because it teaches orchestration against real
components: API, worker, reporting service, Postgres, Redis, health, metrics,
and rollouts. It is not the default because the system is small, the VPS is
constrained, and Dokku already teaches the first deployment lessons with less
operational machinery. I would recommend k3s for production only after process
count, replicas, rollout needs, scheduling, or team platform consistency
clearly outweigh the cluster cost.
