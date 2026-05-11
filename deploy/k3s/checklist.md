# k3s Deployment Checklist

Use this checklist only for the later k3s orchestration path. It is not
required for earlier phases, and it does not replace `deploy/dokku/checklist.md`.

## Preflight

- Confirm the learner has already completed the simpler Dokku deployment path
  or can explain why it is being skipped for this later exercise.
- Confirm k3s is installed and `kubectl` points at the intended VPS cluster.
- Confirm the node has enough headroom for a 4 GB RAM, 3 vCPU environment.
- Confirm the image tag is immutable and matches the Git commit being deployed.
- Replace every `ghcr.io/YOUR_ORG/opledger:TAG` placeholder.
- Replace `api.opledger.example.com` with the intended hostname.
- Decide where Postgres runs: VPS-managed, in-cluster for learning, or managed
  externally in a hypothetical cloud target.
- Decide where Redis runs: VPS-managed, in-cluster for learning, or managed
  externally in a hypothetical cloud target.
- Confirm `DATABASE_URL` and `OPLEDGER_REDIS_URL` are provided as secrets and
  are not committed with real values.
- Confirm `OPLEDGER_REPORT_RENDERING_SERVICE_URL` points to
  `http://opledger-reporting:8001`.
- Confirm reporting-service failure injection is disabled.
- Confirm metrics and debug-style endpoints are not exposed through ingress.
- Run `./scripts/verify.sh` locally before deploying.

## Deploy

- Apply the namespace.
- Apply config and secret placeholders after replacing values safely.
- Apply the reporting service first.
- Apply the API service.
- Apply the worker.
- Run Alembic migrations explicitly with the same image tag.
- Apply ingress only after API readiness succeeds internally.

## Health

- Check pods: `kubectl -n opledger get pods -o wide`.
- Check API rollout: `kubectl -n opledger rollout status deployment/opledger-api`.
- Check reporting rollout:
  `kubectl -n opledger rollout status deployment/opledger-reporting`.
- Port-forward the API service and call `/health/live`.
- Port-forward the API service and call `/health/ready`.
- Port-forward the reporting service and call `/health/live`.
- Confirm API readiness fails honestly if Postgres is unreachable.
- Confirm the worker has no public Service and is inspected through pod status,
  logs, and durable report job state.

## Logs

- Inspect API logs: `kubectl -n opledger logs deployment/opledger-api`.
- Inspect worker logs: `kubectl -n opledger logs deployment/opledger-worker`.
- Inspect reporting logs:
  `kubectl -n opledger logs deployment/opledger-reporting`.
- Look for request IDs, correlation IDs, report job events, readiness failures,
  reporting-service call failures, and startup errors.
- Do not paste full connection strings or secrets into notes, issues, commits,
  or chat.

## Rollout

- Confirm the old and new image tags before changing the deployment.
- Update one deployment at a time unless the change requires coordinated API,
  worker, and reporting-service behavior.
- Watch rollout status for the changed deployment.
- Confirm readiness before sending public traffic to the new version.
- Record sanitized evidence: commit, image tag, rollout time, health status,
  and relevant log event names.

## Rollback

- For bad config, restore the previous ConfigMap or Secret value and restart
  the affected deployment.
- For a bad image, run `kubectl -n opledger rollout undo deployment/NAME` only
  after confirming the previous ReplicaSet used a compatible schema.
- For a risky schema change, prefer a forward repair migration unless a down
  migration has been rehearsed and proven safe.
- After rollback, check API readiness, worker progress, reporting health, and
  durable report job status.

## Resource Checks

- Run `kubectl -n opledger top pods` if metrics-server is available.
- Run `kubectl top nodes` if metrics-server is available.
- Use `kubectl -n opledger describe pod POD_NAME` when pods are pending,
  evicted, OOMKilled, or restarting.
- Keep initial replicas at one for a 4 GB VPS unless you have measured headroom.
- Treat in-cluster Postgres or Redis as a deliberate stateful learning
  extension with backup and restore notes, not as the default.
