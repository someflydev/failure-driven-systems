# Dokku vs k3s

Dokku is the first OpsLedger deployment path. k3s is a later orchestration
learning path. The comparison matters because both can run containers on a VPS,
but they teach different operating models and impose different costs.

OpsLedger should not start on Kubernetes by default. Use k3s only after the
learner can explain what Dokku already covers and what orchestration would add
for the API, worker, reporting service, Postgres, Redis, logs, metrics, and
rollback practice.

## Simplicity

Dokku is simpler for the early system: create one app, attach Postgres, set
config, push Git, run migrations, check health, inspect logs, and plan
rollback. That is enough to teach real deployment discipline without requiring
cluster concepts.

k3s adds Kubernetes objects: Deployments, Services, ingress, ConfigMaps,
Secrets, probes, replica sets, node pressure, and rollout history. Those are
valuable concepts, but they are extra concepts.

## Operational Cost

Dokku cost is one VPS, Dokku, Docker, plugins, app config, proxy settings,
logs, image tags, migrations, backups, and updates.

k3s cost includes the VPS plus cluster operation: Kubernetes API availability,
manifests, controller behavior, ingress controller behavior, pod scheduling,
resource requests, image pull behavior, object drift, and cluster debugging.
On a 4 GB RAM, 3 vCPU VPS, that overhead is visible.

## Scaling

Dokku fits one or a few small processes. It can run the API well and can be
extended for more processes, but the current Dokku docs are intentionally
API-first and should not claim a full multi-service production topology.

k3s makes multiple stateless processes and replicas more explicit. API and
reporting-service replicas are natural Kubernetes teaching examples. Worker
replicas are more dangerous because queue semantics, idempotency, Postgres
state, Redis behavior, and duplicate side-effect protection must already be
understood.

## Rollback

Dokku rollback can be a config restore, known-good image tag deploy, or Git
revert plus redeploy. Schema rollback remains a data decision, not merely a
platform command.

k3s provides rollout history and `kubectl rollout undo`, but that does not make
database compatibility automatic. If an image change and migration are coupled,
the same forward-repair discipline applies.

## Secrets

Dokku exposes app config through Dokku commands and linked service
environment. Operators must avoid copying connection strings into notes,
issues, commits, or chat.

k3s uses Secrets as Kubernetes objects. Plain Secret manifests are only
base64-encoded, not a complete secret-management solution. The teaching
manifests include `secret.example.yaml` only as a placeholder. Real secret
handling needs a deliberate process such as external secret injection, sealed
secrets, SOPS, or a host-local operational procedure that keeps real values out
of Git.

## Networking

Dokku gives app proxying and a straightforward public HTTP route to the app
container port.

k3s introduces ClusterIP Services for internal stable addresses and ingress for
public routing. This helps the worker call `http://opledger-reporting:8001`,
but it also creates more network surfaces to secure and debug.

Do not expose `/metrics` or debug-style endpoints publicly by default. Use
internal access such as `kubectl port-forward`, a private network, or an
authenticated metrics stack.

## Observability

Dokku logs are direct and enough for early deploy and health failures.

k3s logs require object awareness: deployment, replica set, pod, container, and
rollout state. Kubernetes events can explain scheduling, image pull, OOMKill,
probe, and restart failures that app logs do not show.

OpsLedger's structured logs and lightweight metrics still matter in both
paths. k3s changes how operators reach them; it does not replace application
observability.

## Team Fit

Dokku fits a small team or solo learner operating a modest system where
clarity, low ceremony, and direct VPS ownership are the priority.

k3s fits a learner or team that needs orchestration practice or has real
pressure from process count, stateless replicas, release coordination,
scheduling, isolation, or platform consistency. It is a worse fit if the team
cannot yet debug the simpler deployment path.

## Decision Rule

Choose Dokku when:

- the system is small;
- one VPS and one operator are enough;
- the main lesson is deploy, config, migrations, logs, health, and rollback;
- orchestration would add vocabulary without solving a real problem.

Study k3s when:

- the learner has already operated the simpler path;
- multiple long-running processes need explicit lifecycle practice;
- rolling updates, Services, ingress, replicas, probes, and resource limits
  are the lesson;
- the team can accept the cluster debugging cost.

k3s is worth learning. It is not the default starting recommendation for
OpsLedger.
