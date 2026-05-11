# Dokku vs k3s Defense

## Phase

Phase 6: architecture defense, system design, and interview readiness.

This exercise belongs here because the learner can now compare a simple VPS app
platform with a small Kubernetes distribution against the actual OpsLedger API,
worker, reporting service, Postgres, Redis, logs, metrics, and deployment
constraints.

## Concepts

- Deployment platform tradeoffs.
- Orchestration concepts and operational cost.
- Stateless versus stateful service placement.
- Rollout and rollback reasoning.
- Secrets, networking, and observability boundaries.
- Small-team fit and refusal of premature complexity.

## Prerequisites

Read these before starting:

- `deploy/dokku/README.md`
- `deploy/dokku/checklist.md`
- `deploy/k3s/README.md`
- `deploy/k3s/checklist.md`
- `docs/deployment/dokku-vs-k3s.md`
- `docs/architecture/current-system.md`
- `docs/adr/0005-dokku-first-deployment.md`
- `docs/adr/0006-k3s-later-orchestration-learning-path.md`
- `docs/CONSTRAINTS.md`
- `exercises/phase-6/01-decision-memo-defense.md`

You should also understand the current roles of the API, worker, reporting
service, Postgres, Redis, health endpoints, metrics endpoints, and explicit
Alembic migrations.

## Build/Change Task

Write a deployment-platform defense for OpsLedger.

Your defense must include:

- the current deployment baseline and why Dokku came first;
- what k3s would teach that Dokku does not;
- when k3s would be worth the added cost;
- when Dokku remains the better production choice;
- how the API, worker, and reporting service map to k3s objects;
- why Postgres and Redis are not automatically moved in-cluster;
- how migrations, secrets, health checks, logs, rollouts, and rollback differ;
- how `/metrics` should be accessed safely;
- at least five failure modes;
- a two-minute interview answer.

## Constraints

- Do not make k3s required for earlier phases.
- Do not remove or weaken the Dokku path.
- Do not add Helm, operators, service mesh, managed Kubernetes, or a cloud
  platform requirement.
- Do not include real secrets.
- Do not expose `/metrics` through public ingress.
- Do not claim Kubernetes solves schema rollback, duplicate worker execution,
  database backups, or Redis durability by itself.
- Do not let an LLM write the first draft of your defense.

## Failure Modes

- The answer treats k3s as automatically more professional than Dokku.
- The answer ignores the 4 GB RAM, 3 vCPU VPS constraint.
- The answer moves Postgres or Redis in-cluster without backup, restore,
  persistent volume, and resource reasoning.
- Worker replicas are increased without discussing idempotency and durable job
  state.
- `kubectl rollout undo` is treated as safe despite incompatible migrations.
- Secrets are committed in manifests or copied into durable notes.
- Metrics endpoints are exposed publicly.
- The learner cannot explain what evidence would keep Dokku as the better
  production fit.

## Expected Reasoning

After completing the exercise, you should be able to defend Dokku as the early
default, explain k3s as a later orchestration lesson, and compare both options
using actual OpsLedger constraints instead of generic platform preference.

## Verification

- Run `./scripts/verify.sh`.
- Confirm your defense cites at least four concrete OpsLedger artifacts.
- Confirm the defense says k3s is introduced later and is not the default
  starting path.
- Confirm resource warnings fit a 4 GB VPS.
- Confirm no real secrets, application dependencies, Helm charts, or generated
  manifests were added.
- Confirm metrics and debug-style endpoints remain internal by default.

## Reflection Questions

- Which OpsLedger failure or operating pressure would make k3s worth studying?
- What does Dokku make easier during an early incident?
- What does k3s make easier during a multi-process rollout?
- Why is moving Postgres into Kubernetes a separate stateful decision?
- How would you prove a rollback is safe after a migration?
- What would make you recommend staying on Dokku for production?

## LLM Usage

Use an LLM only after writing your own defense. Ask it to challenge unsupported
claims about scale, rollback, secrets, metrics exposure, Postgres placement,
Redis durability, and team fit. Do not ask it to choose the platform for you.

## Path-Specific Extensions

Backend path: map the API, worker, reporting service, Postgres, and Redis
dependencies to concrete health and failure behavior.

Operations path: rehearse the k3s checklist on a disposable environment and
record sanitized rollout, health, logs, and rollback evidence.

Architecture path: write an ADR that rejects k3s for production today while
preserving it as a later learning path.

Interview path: answer the prompts in
`interviews/phase-6-deployment-platforms.md` without notes.

## Deployment/Debugging Actions If Relevant

No production deployment is required. If using a disposable k3s environment,
record only sanitized evidence: image tag, rollout status, health endpoint
status, relevant log event names, pod status, and resource observations. Do not
record connection strings or secret values.
