# k3s Deployment Learning Path

k3s is a later OpsLedger learning path for orchestration. It is not the
default starting deployment route, and it does not replace the Phase 1 Dokku
path in `deploy/dokku/`. Use Dokku first when the lesson is release discipline,
configuration, migrations, logs, health checks, and rollback on one small VPS.

Use this k3s material after learners have operated the API, worker, Redis,
reporting service, Postgres, logs, metrics, and failure drills long enough to
understand what orchestration adds and what it costs.

## Learning Goal

The k3s path should teach Kubernetes concepts through the existing OpsLedger
shape:

- `Deployment` objects for the API, worker, and reporting service.
- `Service` objects for stable in-cluster API and reporting-service addresses.
- An ingress placeholder for public API traffic.
- Replica counts and rolling updates.
- Config and secret boundaries.
- Readiness and liveness probes.
- Logs, rollout status, rollback, and resource checks.
- The operational cost of a scheduler, ingress controller, manifests, image
  tags, and cluster state.

The goal is orchestration literacy, not making Kubernetes the baseline answer
for a small system.

## Prerequisites

- One Linux VPS with k3s already installed.
- `kubectl` configured for that cluster.
- Enough Dokku or local Compose experience to explain the simpler deployment
  model first.
- A built and pushed OpsLedger image that contains the repo-root `Dockerfile`
  output. Replace `ghcr.io/YOUR_ORG/opledger:TAG` in the manifests with a real
  immutable image tag.
- Postgres and Redis connection targets chosen before deploy.
- TLS, DNS, backups, and secret storage decisions made outside these teaching
  manifests.

## Resource Warning

The baseline target is a 4 GB RAM, 3 vCPU VPS. That is enough for a careful
learning cluster, but not much more.

Start with one replica for each OpsLedger process. Give the API, worker, and
reporting service small requests and conservative limits. Watch node pressure
with `kubectl top nodes` if metrics-server is available, and inspect pods with
`kubectl describe pod` when scheduling or restarts look suspicious.

Running Postgres and Redis inside the same small k3s cluster is possible for
learning, but it competes with the application for memory, CPU, disk I/O, and
operator attention. It also turns backup, restore, persistent volumes, and
stateful upgrade behavior into part of the lesson. Do that deliberately, not
as an accidental side effect of "moving to Kubernetes."

## How This Differs From Dokku

Dokku keeps the first deployment path intentionally small: one app, app config,
service attachment, logs, explicit migrations, health checks, and image or Git
rollback. It is still the better fit when the system is small, the team is
small, and the main lesson is operating a clear VPS deployment.

k3s adds a scheduler, pod lifecycle, Services, ingress, rollouts, resource
requests, probes, and more places where config can drift. It becomes worth the
cost when the learner needs to practice multiple long-running processes,
replicas, rolling updates, scheduling, internal service discovery, and
cluster-level debugging.

For OpsLedger, k3s should be introduced later as an orchestration comparison,
not as proof that a small production system must run Kubernetes.

## Stateful Dependencies

These manifests do not include Postgres or Redis by default.

Reasonable options:

- Keep VPS-managed services outside k3s. This preserves the existing
  source-of-truth and queue/cache decisions while using k3s for stateless app
  orchestration.
- Run Postgres and Redis in-cluster only as a learning extension. Document
  persistent volumes, backup/restore, resource limits, upgrades, and data loss
  risk before doing it.
- In a hypothetical cloud deployment, use managed Postgres and managed Redis.
  That lowers local operational burden but changes cost, networking, IAM,
  backup, and failure-mode ownership.

Postgres remains the durable source of truth. Redis remains queue/cache
coordination. k3s changes process placement and networking; it does not change
data ownership.

## Manifests

The starter manifests live in `deploy/k3s/manifests/`:

- `namespace.yaml`
- `configmap.yaml`
- `secret.example.yaml`
- `api.yaml`
- `worker.yaml`
- `reporting.yaml`
- `ingress.yaml`

Apply them only after replacing image names, hostnames, and placeholder secret
values:

```sh
kubectl apply -f deploy/k3s/manifests/namespace.yaml
kubectl apply -f deploy/k3s/manifests/configmap.yaml
kubectl apply -f deploy/k3s/manifests/secret.example.yaml
kubectl apply -f deploy/k3s/manifests/reporting.yaml
kubectl apply -f deploy/k3s/manifests/api.yaml
kubectl apply -f deploy/k3s/manifests/worker.yaml
kubectl apply -f deploy/k3s/manifests/ingress.yaml
```

`secret.example.yaml` is a template, not a real secret store. Do not commit
real `DATABASE_URL`, `OPLEDGER_REDIS_URL`, passwords, tokens, or generated
secret manifests.

## Migrations

These manifests do not run Alembic automatically. Keep migrations explicit so
learners can reason about image rollout separately from schema change:

```sh
kubectl -n opledger run opledger-migrate --rm -it --restart=Never \
  --image=ghcr.io/YOUR_ORG/opledger:TAG \
  --env-from=configmap/opledger-config \
  --env-from=secret/opledger-secrets \
  -- uv run --no-sync alembic -c services/api/alembic.ini upgrade head
```

Use the exact image tag you are deploying. If a migration is risky, write the
forward repair plan before changing production traffic.

## Health And Access

The API exposes:

- `/health/live`
- `/health/ready`
- `/metrics`

The reporting service exposes the same health surface plus `/metrics`.

The ingress placeholder routes only normal API HTTP traffic. Do not expose
internal metrics or debug endpoints through public ingress by default. Prefer
internal access such as:

```sh
kubectl -n opledger port-forward service/opledger-api 8000:8000
kubectl -n opledger port-forward service/opledger-reporting 8001:8001
```

Then inspect health or metrics from your local machine. If metrics are ever
published, require explicit authentication, network controls, and a review of
labels and response content.

## When k3s Is Worth It

k3s is worth studying when you need to explain or practice:

- independent API, worker, and reporting-service lifecycles;
- rolling updates and rollback evidence;
- more than one replica for stateless HTTP services;
- stable service discovery between worker and reporting service;
- scheduling, pod restart behavior, and resource limits;
- how Kubernetes changes incident debugging.

Dokku remains the better choice when one VPS, one small operator team, and a
few processes are easier to operate directly than a cluster.
