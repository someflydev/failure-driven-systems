# Repository Map

This repository begins with doctrine, navigation, and the initial OpsLedger API
scaffold. Directories should be created or populated only when later prompts
justify them. Planned directories below define the intended shape, not current
implementation.

## Current Foundation

- `README.md`: public positioning, audience, differentiators, and phase
  sequence, plus the current local development workflow.
- `AGENT.md`: routing instructions for future coding-assistant sessions.
- `Dockerfile`: production-flavored local image definition for the FastAPI API
  service and stateless reporting service using repo-root `uv` tooling and
  Python 3.12.
- `.dockerignore`: Docker build-context exclusions for local env files,
  virtualenvs, caches, and generated artifacts.
- `docker-compose.yml`: local development stack with API, Postgres, Redis, a
  worker process, the stateless reporting service used by the worker, and
  disabled-by-default local reporting-service failure injection settings.
- `deploy/dokku/README.md`: Phase 1 Dokku deployment path for the single
  Dockerfile-based API service, including app creation, Postgres linking,
  config, deploy, migrations, health checks, logs, and rollback basics.
- `deploy/dokku/checklist.md`: concise Dokku deployment preflight and
  post-deploy checklist.
- `.env.example`: local placeholder environment values for Compose, Redis,
  reporting service ports and timeouts, and health tuning, plus
  disabled-by-default report retry, worker failure injection, and reporting
  service failure injection settings; real `.env` files must remain
  uncommitted.
- `pyproject.toml`: repo-root Python 3.12 project metadata, dependencies, and
  quality-tool configuration for the `uv` workflow.
- `docs/DOCTRINE.md`: durable learning doctrine.
- `docs/ASSISTANT_WORKFLOW.md`: staged LLM collaboration rules for learners
  and coding assistants.
- `docs/COMMIT_DISCIPLINE.md`: prompt-numbered multi-line commit message
  guidance and examples.
- `docs/CONSTRAINTS.md`: infrastructure and budget assumptions.
- `docs/DOMAIN.md`: OpsLedger domain boundaries, conceptual entities, and the
  pointer to the implemented Phase 1 relational model.
- `docs/REPO_MAP.md`: intended repository layers and directory responsibilities.
- `docs/SYSTEM_EVOLUTION.md`: planned OpsLedger evolution from one service to
  later worker-backed, boundary-aware, observable operation.
- `docs/architecture/modular-monolith.md`: Phase 3 modular monolith guide
  naming current internal module ownership, why service boundaries are
  expensive, and why report rendering is studied before extraction.
- `docs/adr/0001-report-rendering-boundary.md`: accepted-for-learning ADR
  explaining the narrow stateless report-rendering service extraction and why
  the same extraction may be unjustified in a small production system.
- `docs/contracts/report-rendering-v1.md`: Phase 3 report rendering request and
  response contract, HTTP endpoint, compatibility rules, versioning approach,
  and stateless ownership boundary.
- `docs/contracts/compatibility-playbook.md`: Phase 3 playbook for safe and
  unsafe report contract changes, consumer-driven compatibility thinking, and
  versioned contract debugging.
- `docs/observability/logging-and-correlation.md`: Phase 4 guide to structured
  JSON logs, request IDs, correlation IDs, report job propagation, secret-safe
  log fields, and what remains out of scope before metrics or tracing.
- `docs/observability/metrics.md`: Phase 4 guide to the lightweight
  Prometheus-compatible `/metrics` surfaces, metric names, operational
  questions, label safety rules, worker exposure limitation, and internal-only
  access expectations.
- `docs/TESTING_STRATEGY.md`: current Phase 1 test layers, local verification
  entrypoint, fixture discipline, and deferred testing layers.
- `docs/TECH_STACK.md`: current stack choices, Python tooling, and deferred
  technology decisions.
- `docs/async/phase-2-job-lifecycle.md`: Phase 2 async report job lifecycle,
  durable Postgres ownership, ephemeral Redis queue ownership, bounded retry
  behavior, local/test report failure injection, and safe user-facing
  assumptions for status and result endpoints.
- `docs/async/idempotency.md`: Phase 2 report job idempotency guide separating
  request idempotency, job idempotency, side-effect idempotency, and the
  Postgres uniqueness constraint that prevents duplicate enqueue records.
- `docs/async/side-effects-and-outbox.md`: Phase 2 side-effect guide for local
  report completion notifications, durable notification attempt identity,
  visible failed attempts, and the remaining gap before a full outbox
  dispatcher.
- `docs/data-models/phase-1.md`: implemented Phase 1 customer, work request,
  and work request status event tables, relational choices, deferred entities,
  transaction reasoning, and source-of-truth constraints.
- `curriculum/README.md`: phase sequence and concept timing boundaries.
- `curriculum/PHASE_PLAN.md`: OpsLedger capability plan for each curriculum
  phase.
- `lessons/phase-1/README.md`: Phase 1 lesson index linking app features,
  exercises, scenarios, runbooks, deployment docs, review gates, quiz,
  interview practice, and capstone in order.
- `lessons/phase-2/README.md`: complete Phase 2 lesson path linking
  synchronous report pain, Redis/RQ worker flow, durable job status, retries,
  idempotency, safe side effects, scenario drills, review checklist, quiz,
  interview practice, capstone exercise, and capstone rubric.
- `lessons/phase-3/README.md`: complete Phase 3 lesson path for modular
  monolith boundaries, report rendering as a candidate boundary, contract
  compatibility, the stateless reporting-service extraction, failure
  scenarios, review checklist, quiz, interview practice, and capstone defense.
- `lessons/phase-4/README.md`: Phase 4 lesson path for structured logging,
  metrics, request/correlation IDs, incident scenarios, status updates,
  runbooks, postmortems, and evidence-first review.
- `exercises/TEMPLATE.md`: canonical structure for later learner exercises.
- `exercises/phase-1/01-basic-crud.md`: first Phase 1 CRUD exercise for
  customers and work requests.
- `exercises/phase-1/02-transactions-and-history.md`: Phase 1 transaction and
  status history exercise for work request status changes.
- `exercises/phase-1/03-test-matrix-and-edge-cases.md`: Phase 1 exercise for
  designing a test matrix before using an LLM to review edge cases.
- `exercises/phase-1/04-db-down-debugging.md`: Phase 1 exercise for debugging
  database unavailability from logs and health endpoints before changing code.
- `exercises/phase-1/05-local-container-workflow.md`: Phase 1 exercise for
  bringing up the Docker Compose stack, running migrations, checking health,
  breaking database connectivity, and explaining the symptoms.
- `exercises/phase-1/06-dokku-first-deploy.md`: Phase 1 exercise for deploying
  the API to Dokku, linking Postgres, running migrations, checking health,
  inspecting logs, and reflecting on rollback risk.
- `exercises/phase-1/07-phase-1-capstone.md`: Phase 1 capstone requiring one
  small CRUD improvement, tests, deployment evidence or blocker notes, database
  unavailable simulation, tradeoff explanation, and delayed LLM critique.
- `exercises/phase-2/01-synchronous-report-pain.md`: first Phase 2 exercise
  requiring synchronous report measurement, controlled local delay, blocked
  caller observation, and before/after expectations before asynchronous work.
- `exercises/phase-2/02-background-report-worker.md`: Phase 2 exercise for
  enqueueing report generation, running the worker, inspecting durable
  `report_jobs` state, and comparing queued behavior with the synchronous
  report path.
- `exercises/phase-2/03-job-status-and-eventual-consistency.md`: Phase 2
  exercise for explaining `202 Accepted`, polling durable report job status,
  fetching completed output only when available, and designing user-visible
  eventual consistency language.
- `exercises/phase-2/04-retries-before-idempotency.md`: Phase 2 exercise for
  observing controlled report worker failure, bounded retries, persisted
  attempt evidence, and duplicate side-effect risks before implementing
  idempotency.
- `exercises/phase-2/05-idempotent-report-jobs.md`: Phase 2 exercise for
  database-backed report enqueue idempotency, duplicate worker execution
  safety, and reflection on remaining side-effect risks.
- `exercises/phase-2/06-safe-side-effects.md`: Phase 2 exercise for local
  report completion notifications, duplicate side-effect prevention, failed
  attempt visibility, and reasoning about what changes with a real provider.
- `exercises/phase-2/07-phase-2-capstone.md`: Phase 2 capstone requiring at
  least two failure scenarios, durable status and side-effect inspection, one
  small fix or concrete issue explanation, and a defense of retry/idempotency
  design.
- `exercises/phase-3/01-modular-monolith-boundaries.md`: first Phase 3
  exercise requiring learners to identify coupling, ownership of facts, and
  what would break if each module were extracted.
- `exercises/phase-3/02-contract-before-network.md`: Phase 3 exercise requiring
  learners to make a backward-compatible report rendering contract change
  before adding any HTTP or deployable service boundary.
- `exercises/phase-3/03-extract-reporting-service.md`: Phase 3 exercise for
  extracting the stateless report renderer, wiring bounded worker calls, and
  defending the educational value against small-system production cost.
- `exercises/phase-3/04-timeouts-and-contracts.md`: Phase 3 exercise for
  running reporting timeout and bad-contract scenarios, inspecting durable job
  evidence and logs, and explaining user-visible impact.
- `exercises/phase-3/05-phase-3-capstone.md`: Phase 3 capstone requiring one
  backward-compatible report contract change, one service-boundary failure
  scenario, technical verification, a short decision memo defending whether
  the extraction should stay, and delayed LLM senior-review critique.
- `exercises/phase-4/01-follow-a-request-through-logs.md`: first Phase 4
  exercise for tracing one report workflow through API, worker, reporting
  service, durable job status, and sanitized logs using a correlation ID.
- `exercises/phase-4/02-meaningful-metrics.md`: Phase 4 exercise for breaking a
  reporting dependency, observing request/job/reporting/notification metrics,
  checking durable job status, and explaining what changed without adding a
  heavy observability stack.
- `exercises/phase-4/03-incident-debugging-drill.md`: Phase 4 incident drill
  requiring a scenario run, two status updates, evidence across logs, metrics,
  durable status, one discarded hypothesis, and a learner-written postmortem
  before LLM critique.
- `scenarios/phase-1/db-unavailable.md`: guided local database outage scenario
  for observing live-but-not-ready behavior.
- `scenarios/phase-2/worker-unavailable.md`: guided local scenario for stopping
  the worker, enqueueing a report, inspecting queued status, restarting the
  worker, and explaining accepted-but-incomplete work.
- `scenarios/phase-2/duplicate-job-execution.md`: guided local scenario for
  triggering duplicate completed job execution and confirming completed output
  and notification attempts are not duplicated.
- `scenarios/phase-2/delayed-job-completion.md`: guided local scenario for
  delaying completion by holding the worker down and writing honest
  user-facing eventual-consistency language.
- `scenarios/phase-2/report-retry-failure.md`: guided local report worker
  failure scenario for triggering bounded retries, inspecting durable attempt
  state, and explaining duplicate side-effect risk.
- `scenarios/phase-2/failed-notification-side-effect.md`: guided scenario for
  forcing deterministic local notification failure and inspecting the durable
  failed attempt.
- `scenarios/phase-2/redis-unavailable.md`: guided local scenario for stopping
  Redis, observing enqueue failure, and stating what the app can and cannot do
  without queue coordination.
- `scenarios/phase-3/reporting-timeout.md`: guided local scenario for delaying
  the extracted reporting service past the worker timeout and inspecting
  durable failure evidence.
- `scenarios/phase-3/reporting-bad-response.md`: guided local scenario for
  malformed and incompatible reporting service responses.
- `scenarios/phase-3/mixed-version-contract.md`: guided contract scenario for
  additive v1 fields, incompatible contract drift, and consumer-driven tests.
- `scenarios/phase-4/reporting-service-latency-incident.md`: incident drill for
  slow reporting service behavior using health, logs, metrics, durable report
  job evidence, and status updates.
- `scenarios/phase-4/worker-stalled-incident.md`: incident drill for accepted
  report jobs that remain queued while the worker is stopped, then recover
  after worker restart.
- `scenarios/phase-4/noisy-nonfatal-errors.md`: incident drill for separating
  notification side-effect failures from successful report generation using
  notification attempts and metrics.
- `scenarios/phase-4/ambiguous-logs-before-correlation.md`: incident drill for
  comparing unfiltered logs with correlation-filtered timelines across API,
  worker, reporting service, and durable job state.
- `ops/runbooks/phase-1-first-response.md`: first-response runbook for health
  endpoints, logs, environment, database reachability, migrations, and rollback
  thinking.
- `ops/runbooks/dokku-api-incident.md`: Dokku API incident runbook for bad env
  vars, unavailable Postgres, failed migrations, boot failures, memory pressure,
  and unreadable logs.
- `ops/runbooks/report-jobs-stuck.md`: Phase 4 runbook for queued or running
  report jobs that are not progressing, using health checks, durable job
  status, logs, metrics, and worker/reporting-service evidence.
- `ops/runbooks/reporting-service-down.md`: Phase 4 runbook for reporting
  service boundary incidents covering health, worker failures, contract
  failures, latency, metrics, mitigations, and resolution checks.
- `ops/incidents/TEMPLATE_incident_status_update.md`: concise Phase 4 status
  update template for impact, evidence, hypothesis, current action, and next
  update time during an incident.
- `ops/incidents/TEMPLATE_postmortem.md`: Phase 4 postmortem template for
  learner-owned timelines, impact, detection, root cause, contributing factors,
  action items, and interview explanation.
- `ops/dashboards/README.md`: lightweight dashboard sketch and Prometheus query
  examples for API traffic, report jobs, reporting boundary failures, and
  notifications without requiring Grafana or a Prometheus container.
- `reviews/checklists/phase-1-api-review.md`: practical Phase 1 API review
  checklist covering validation, constraints, transactions, errors, health
  behavior, tests, and scope control.
- `reviews/checklists/phase-2-async-review.md`: practical Phase 2 async review
  checklist covering job API behavior, Redis/Postgres ownership, retries,
  idempotency, side effects, scenario evidence, and scope control.
- `reviews/checklists/phase-3-service-boundary-review.md`: Phase 3
  service-boundary review checklist covering ownership, contract stability,
  timeout behavior, retries, deployment cost, debugging, rollback, and scope
  control.
- `reviews/checklists/incident-review.md`: Phase 4 checklist for critiquing
  incident response quality, evidence use, correlation, status updates,
  postmortems, LLM use, and scope control.
- `reviews/rubrics/phase-1-capstone.md`: scoring rubric for the Phase 1
  capstone covering correctness, relational reasoning, operational debugging,
  deployment evidence, explanation quality, and restraint around premature
  complexity.
- `reviews/rubrics/phase-2-capstone.md`: scoring rubric for the Phase 2
  capstone covering scenario execution, async state reasoning,
  retry/idempotency design, Redis/Postgres ownership, fix or explanation
  quality, and scope control.
- `reviews/rubrics/phase-3-capstone.md`: scoring rubric for the Phase 3
  capstone covering backward-compatible contract change, failure scenario
  evidence, boundary reasoning, decision memo quality, verification, LLM
  senior-review use, and scope control.
- `reviews/llm/README.md`: reusable LLM reviewer prompt patterns.
- `reviews/llm/TEMPLATE_review_my_work.md`: learner-facing critique request
  template.
- `reviews/llm/TEMPLATE_interview_me.md`: learner-facing mock interview
  template.
- `quizzes/phase-1.md`: Phase 1 short-answer quiz for HTTP basics, relational
  modeling, transactions, migrations, health checks, logs, deployment, database
  failure, and scope control.
- `quizzes/phase-2.md`: Phase 2 short-answer quiz for async work, retries,
  idempotency, duplicates, Redis versus Postgres, side effects, and eventual
  consistency.
- `quizzes/phase-3.md`: Phase 3 short-answer quiz for modular monoliths,
  service extraction, contracts, compatibility, timeouts, partial failure, and
  extraction defense.
- `interviews/phase-1-backend.md`: Phase 1 backend mock interview prompts with
  strong-answer traits instead of canned answers.
- `interviews/phase-2-backend-distributed.md`: Phase 2 backend and distributed
  systems mock interview prompts with strong-answer traits for async jobs,
  queue coordination, retries, idempotency, side effects, and scope control.
- `interviews/phase-3-distributed-boundaries.md`: Phase 3 distributed-boundary
  mock interview prompts with strong-answer traits for ownership, extraction
  decisions, contracts, failure debugging, operations, and scope control.
- `services/api/opledger_api/`: FastAPI package with app creation,
  configuration, database engine/session setup, dependency-free liveness,
  database-backed readiness, Phase 1 SQLAlchemy models, Pydantic schemas,
  explicit internal modules for customers, work requests, versioned report
  rendering contracts, local report rendering, a bounded reporting-service
  client, async report job state, notification attempts, shared route
  dependencies, a worker entrypoint with bounded retries, completed-output
  duplicate execution protection, local/test failure injection, structured
  JSON logs, request ID handling, correlation ID propagation through report
  jobs, and lightweight in-process metrics for HTTP, report job, worker,
  reporting-boundary, and notification signals.
- `services/reporting/reporting_service/`: stateless FastAPI report-rendering
  service that implements `report-rendering.v1` without database ownership and
  exposes disabled-by-default local/test failure modes for boundary drills,
  with the same structured request logging, correlation header handling, and
  `/metrics` surface as the API.
- `services/api/alembic.ini`: Alembic entry point for API database migrations.
- `services/api/migrations/`: Alembic migration environment and deterministic
  migrations for customers, work requests, status events, report jobs, and
  notification attempts.
- `services/api/tests/`: API scaffold, CRUD route, status history, report job
  endpoint and worker lifecycle, reporting client, model, and schema tests.
- `services/reporting/tests/`: reporting service contract tests.
- `docs/runbooks/DB_CONNECTIVITY.md`: local and future Dokku troubleshooting
  guide for database readiness failures, including Docker Compose checks.
- `scripts/verify.sh`: repo-root verification gate run through `uv`.
- `scripts/worker.sh`: host-local RQ worker entrypoint for report jobs.
- `scripts/dev-up.sh`: small wrapper around `docker compose up --build`.
- `scripts/dev-down.sh`: small wrapper around `docker compose down`.
- `scripts/migrate.sh`: explicit Alembic migration wrapper for host or Compose
  execution.
- `scripts/scenarios/phase2_worker_down.sh`: small helper for stopping,
  starting, or inspecting only the Compose worker during Phase 2 worker-down
  drills.
- `scripts/scenarios/phase2_redis_down.sh`: small helper for stopping,
  starting, or inspecting Redis and the worker during Phase 2 Redis-down
  drills.

## Intended Layers

- `services/`: OpsLedger application services. The current implementation starts
  with one minimal FastAPI service under `services/api/`; keep module boundaries
  explicit before extracting anything.
- `curriculum/`: phase-level learning structure, concept timing, and progression
  rules.
- `lessons/`: individual lesson plans once the curriculum needs concrete
  learner-facing units.
- `exercises/`: hands-on tasks, failure drills, and implementation assignments.
- `scenarios/`: incident narratives, system pressure cases, and variation
  prompts.
- `reviews/`: review rubrics, critique prompts, and expected reasoning checks.
- `interviews/`: architecture defense and interview simulation materials.
- `deploy/`: deployment configuration and operator-facing deployment docs. The
  current concrete path is Dokku for the single-service API; k3s remains
  deferred.
- `ops/`: runbooks, incident response notes, operational checks, and maintenance
  guidance when those materials become concrete.
- `scripts/`: small automation scripts that support verified workflows. The
  current entries cover verification, local Compose startup/shutdown, and
  explicit database migrations.
- `tests/`: repository or application tests once there is behavior to verify.
- `data/`: sample data, fixtures, or generated learner outputs when required by
  exercises.

## Population Rules

- Do not create empty implementation directories just to match the map.
- Do not add k3s manifests, new databases, service extraction, retries, or
  idempotency before the curriculum creates a concrete need.
- Keep planned material clearly labeled as planned.
- Keep current-state claims accurate.
- Prefer narrow, durable documents over broad placeholders.
- Update this map when a later prompt creates a new layer or changes ownership.
