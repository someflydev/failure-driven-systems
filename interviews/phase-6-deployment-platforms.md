# Phase 6 Deployment Platforms Mock Interview

Use these prompts after the learner has read `deploy/dokku/`,
`deploy/k3s/`, `docs/deployment/dokku-vs-k3s.md`, and the deployment ADRs.
The goal is to defend platform fit from OpsLedger evidence, not to recite
Kubernetes vocabulary.

## Platform Choice

### Why did OpsLedger start with Dokku instead of k3s?

Strong-answer traits:

- Names the Phase 1 goal: deploy, config, migrations, logs, health checks, and
  rollback on one VPS.
- Mentions the 4 GB RAM, 3 vCPU constraint and small-team operation.
- Says k3s is useful later, not bad.
- Avoids claiming Dokku already solves every multi-process production concern.

### When would k3s be worth introducing?

Strong-answer traits:

- Names orchestration lessons: Deployments, Services, ingress, replicas,
  probes, rolling updates, resource requests, and scheduler behavior.
- Ties the answer to API, worker, and reporting-service lifecycles.
- Requires enough operational maturity to debug the simpler path first.
- Names the added cluster cost.

## Stateless And Stateful Placement

### Which OpsLedger components map cleanly to k3s Deployments?

Strong-answer traits:

- Names API, worker, and stateless reporting service.
- Explains API and reporting Service objects for stable networking.
- Says the worker normally has no public Service.
- Mentions careful worker replica reasoning because duplicate execution and
  side effects still matter.

### Should Postgres and Redis run inside k3s?

Strong-answer traits:

- Says not by default in the starter path.
- Explains Postgres is source of truth and needs backup, restore, persistent
  volume, upgrade, and resource planning.
- Explains Redis is queue/cache coordination, not durable truth, but still
  needs memory and outage reasoning.
- Allows in-cluster stateful services as a deliberate learning extension.

## Rollout And Rollback

### What does k3s improve about rollouts?

Strong-answer traits:

- Names rollout status, ReplicaSets, readiness probes, and rolling updates.
- Explains independent rollout of API, worker, and reporting service.
- Mentions immutable image tags.
- Does not imply Kubernetes understands application contracts automatically.

### Why is `kubectl rollout undo` not enough after a bad deploy?

Strong-answer traits:

- Mentions database migrations and schema compatibility.
- Requires checking durable report job state and worker behavior.
- Prefers forward repair when down migration safety is not proven.
- Compares this to Dokku image rollback honestly.

## Secrets And Networking

### How should OpsLedger handle secrets in k3s?

Strong-answer traits:

- Says `secret.example.yaml` is a placeholder only.
- Real values must stay out of Git, commits, notes, issues, and chat.
- Mentions Kubernetes Secrets are not a full secret-management solution by
  themselves.
- Proposes a deliberate process such as external injection, sealed secrets,
  SOPS, or another controlled operator workflow.

### Should `/metrics` be public through ingress?

Strong-answer traits:

- Says no by default.
- Recommends internal access, port-forwarding, private networking, or an
  authenticated metrics stack.
- Mentions label/content exposure risk.
- Separates public API traffic from operational surfaces.

## Observability And Debugging

### What new debugging evidence does k3s add?

Strong-answer traits:

- Names pods, events, describes, rollout status, restart counts, image pull
  failures, probe failures, OOMKill, and scheduling failures.
- Keeps application logs, request IDs, correlation IDs, health, metrics, and
  durable database state in the answer.
- Explains that Kubernetes evidence complements app evidence.

### What can k3s make harder during an incident?

Strong-answer traits:

- Names extra object layers and possible config drift.
- Mentions cluster or ingress failures that are not application bugs.
- Mentions resource pressure on a small VPS.
- Explains why small teams may prefer Dokku when orchestration is not paying
  for itself.

## Team Fit

### How would you defend staying on Dokku for production?

Strong-answer traits:

- Starts from workload, team size, and operational evidence.
- Says simpler operation can be the professional choice.
- Names what would be monitored or practiced on Dokku.
- States what evidence would change the recommendation.

### Give a two-minute answer comparing Dokku and k3s for OpsLedger.

Strong-answer traits:

- Dokku first for small-system deploy discipline.
- k3s later for orchestration concepts and multi-process lifecycle practice.
- Postgres and Redis placement is a separate stateful decision.
- Rollback, secrets, metrics exposure, and resource pressure are handled
  explicitly.
- Ends with a decision rule, not a platform slogan.
