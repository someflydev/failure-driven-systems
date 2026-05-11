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
- `deploy/k3s/README.md`: later Phase 6 orchestration learning path for
  running the API, worker, and stateless reporting service on k3s without
  making Kubernetes the default starting deployment.
- `deploy/k3s/checklist.md`: k3s preflight, deploy, health, logs, rollout,
  rollback, and resource checklist for a constrained VPS.
- `deploy/k3s/manifests/`: plain Kubernetes starter manifests for the
  OpsLedger namespace, config, secret placeholders, API Deployment/Service,
  worker Deployment, reporting Deployment/Service, and API ingress placeholder.
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
  later worker-backed, boundary-aware, observable, measured, and
  architecture-defense operation.
- `docs/architecture/current-system.md`: Phase 6 snapshot of the actual
  current system shape across API, Postgres, Redis, worker, reporting service,
  logs, metrics, local Compose, and documented Dokku deployment mode.
- `docs/architecture/modular-monolith.md`: Phase 3 modular monolith guide
  naming current internal module ownership, why service boundaries are
  expensive, and why report rendering is studied before extraction.
- `docs/deployment/dokku-vs-k3s.md`: Phase 6 deployment-platform comparison
  explaining where Dokku remains simpler and where k3s teaches orchestration.
- `docs/adr/TEMPLATE.md`: Phase 6 ADR template requiring context, decision,
  alternatives, consequences, failure modes, operational cost, rollback, and
  interview defense.
- `docs/adr/0001-report-rendering-boundary.md`: accepted-for-learning ADR
  explaining the narrow stateless report-rendering service extraction and why
  the same extraction may be unjustified in a small production system.
- `docs/adr/0002-fastapi-python-primary-stack.md`: ADR defending FastAPI and
  Python as the primary stack for the current workload and team constraints.
- `docs/adr/0003-postgres-source-of-truth.md`: ADR defending Postgres as the
  durable source of truth for OpsLedger facts and derived-state rebuilds.
- `docs/adr/0004-redis-queue-cache-postgres-durability.md`: ADR defining Redis
  as queue/cache coordination while Postgres remains durable.
- `docs/adr/0005-dokku-first-deployment.md`: ADR defending Dokku as the first
  deployment strategy and naming what it does not solve.
- `docs/adr/0006-k3s-later-orchestration-learning-path.md`: ADR accepting k3s
  as a later orchestration learning path while keeping Dokku as the default
  first deployment recommendation.
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
- `docs/performance/baselines.md`: Phase 5 guide to the lightweight baseline
  runner, safe local defaults, VPS limits, result recording, and the
  measurement-before-optimization rule.
- `docs/performance/query-inspection.md`: Phase 5 guide to inspecting the
  filtered work request list query with `EXPLAIN`, interpreting plan shape, and
  documenting the write/storage cost of the narrow composite index.
- `docs/performance/read-models.md`: Phase 5 guide to the
  `customer_work_request_stats` derived dashboard projection, explicit rebuilds,
  visible staleness, source-of-truth ownership, and why read models differ from
  cache.
- `docs/performance/caching.md`: Phase 5 guide to the one Redis cached
  dashboard endpoint, stable keys, TTL, bypass, invalidation, stale-cache risk,
  Redis outage fallback, and why Redis is not authoritative.
- `docs/storage/README.md`: Phase 6 storage decision guide tying datastore
  choices to actual OpsLedger ownership, workloads, operational cost, and the
  discipline of not adding another store without evidence.
- `docs/storage/relational-postgres.md`: Phase 6 comparison note explaining why
  relational Postgres fits OpsLedger source-of-truth facts and what it costs.
- `docs/storage/document-stores.md`: Phase 6 comparison note for flexible
  document-shaped data and why current work request state remains relational.
- `docs/storage/key-value-and-cache.md`: Phase 6 comparison note for Redis,
  key-value lookups, queue coordination, cache speed, and disposable state.
- `docs/storage/queues-and-streams.md`: Phase 6 comparison note for queues,
  streams, replay, consumer failure, and why Redis/RQ is enough today.
- `docs/storage/search-indexes.md`: Phase 6 comparison note for search as
  derived state, including staleness, rebuild, relevance, and authorization
  risks.
- `docs/storage/analytical-stores.md`: Phase 6 comparison note for analytical
  stores, long-range aggregation, freshness gaps, and why the current dashboard
  read model is enough.
- `docs/storage/vector-storage.md`: Phase 6 comparison note for vector
  retrieval, embeddings, evaluation, privacy, and why it is not source of
  truth.
- `docs/storage/when-not-to-add-a-datastore.md`: Phase 6 guide to refusing
  extra datastores when current OpsLedger evidence does not justify the
  operational burden.
- `docs/languages/README.md`: Phase 6 runtime decision guide tying language
  choices to actual OpsLedger components, team constraints, operability, and
  rollback rather than generic language rankings.
- `docs/languages/python.md`: Phase 6 comparison note for Python/FastAPI as
  the current API, worker, reporting, test, and tooling baseline.
- `docs/languages/go.md`: Phase 6 comparison note for Go as a possible fit for
  small operational services, CLIs, or a narrow stateless report renderer.
- `docs/languages/typescript-node.md`: Phase 6 comparison note for
  TypeScript/Node as a possible fit for full-stack teams, schema-sharing, and
  I/O-heavy product surfaces.
- `docs/languages/jvm.md`: Phase 6 comparison note for JVM languages where
  enterprise integration, mature service platforms, or organizational
  standards justify the runtime cost.
- `docs/languages/rust.md`: Phase 6 comparison note for Rust where measured
  performance, memory safety, or systems-level constraints justify the team
  and tooling cost.
- `docs/languages/beam-elixir.md`: Phase 6 comparison note for BEAM/Elixir
  where supervision, realtime messaging, or highly concurrent workflow
  pressure exists.
- `docs/languages/polyglot-systems.md`: Phase 6 guide to justified polyglot
  systems, contract boundaries, and why OpsLedger's main path stays
  Python/FastAPI.
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
- `lessons/phase-5/README.md`: complete Phase 5 lesson path for safe baseline
  measurement, query inspection, indexes, read models, Redis caching,
  staleness scenarios, review checklist, quiz, interview practice, and
  capstone.
- `lessons/phase-6/README.md`: Phase 6 path for current-architecture review,
  ADR reading, storage tradeoff comparison, decision memo defense,
  architecture review, and interview practice.
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
- `exercises/phase-4/04-phase-4-capstone.md`: Phase 4 capstone requiring
  scenario evidence, bounded logs and metrics, durable status, status updates,
  hypotheses, learner-written postmortem, and LLM critique without outsourcing
  conclusions.
- `exercises/phase-5/01-measure-before-optimizing.md`: first Phase 5 exercise
  requiring baseline latency and error evidence, dataset notes, metrics
  snippets, and one suspected bottleneck before changing code.
- `exercises/phase-5/02-pagination-and-indexes.md`: Phase 5 exercise requiring
  learners to validate bounded pagination, stable ordering, filtered query
  behavior, and before/after query-plan reasoning for a narrowly justified
  work request index.
- `exercises/phase-5/03-derived-read-models.md`: Phase 5 exercise requiring
  learners to rebuild the customer work request stats projection, simulate
  stale dashboard output, verify source-of-truth endpoints remain correct, and
  explain user impact.
- `exercises/phase-5/04-caching-and-staleness.md`: Phase 5 exercise requiring
  learners to inspect the cached dashboard endpoint, collect hit/miss/bypass
  metrics, demonstrate stale cache behavior, and confirm Redis outage fallback.
- `exercises/phase-5/05-phase-5-capstone.md`: Phase 5 capstone requiring
  baseline evidence, query and index reasoning, read-model staleness, cache
  behavior, Redis outage evidence, a decision memo, quiz/interview practice,
  and review against the checklist and rubric.
- `exercises/phase-6/01-decision-memo-defense.md`: first Phase 6 exercise
  requiring a small architecture decision memo grounded in current workload,
  team, evidence, alternatives, consequences, failure modes, operational cost,
  rollback, and interview defense.
- `exercises/phase-6/02-datastore-tradeoff-defense.md`: Phase 6 exercise for
  defending whether OpsLedger should add, reject, or remove a datastore based
  on workload evidence, source-of-truth ownership, failure modes, and small-team
  operational cost.
- `exercises/phase-6/03-runtime-selection-defense.md`: Phase 6 exercise for
  defending Python, Go, TypeScript/Node, JVM, Rust, BEAM/Elixir, or a rejected
  polyglot move against actual OpsLedger components and operational cost.
- `exercises/phase-6/04-dokku-vs-k3s-defense.md`: Phase 6 exercise requiring
  a deployment-platform defense that compares Dokku and k3s against OpsLedger
  workload, team, resource, secrets, networking, rollout, and rollback costs.
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
- `scenarios/phase-5/stale-cache.md`: guided local scenario for proving the
  dashboard cache and read model can be stale while source-of-truth work
  request endpoints remain current.
- `scenarios/phase-5/redis-cache-unavailable.md`: guided local scenario for
  stopping Redis, confirming dashboard fallback to the Postgres-backed read
  model, and verifying source-of-truth data is not corrupted.
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
- `reviews/checklists/phase-5-performance-review.md`: Phase 5 checklist for
  reviewing baseline evidence, query/index reasoning, read-model ownership,
  cache behavior, staleness, Redis outage handling, and scope control.
- `reviews/checklists/architecture-review.md`: Phase 6 checklist for reviewing
  ADRs, decision memos, system design answers, and architecture proposals
  against workload, team, data ownership, operational cost, failure modes,
  rollback, and interview defense.
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
- `reviews/rubrics/phase-4-capstone.md`: scoring rubric for the Phase 4
  capstone covering scenario evidence, timelines, metrics and durable state,
  incident communication, postmortem quality, LLM-assisted debugging
  discipline, secret safety, and scope control.
- `reviews/rubrics/phase-5-capstone.md`: scoring rubric for the Phase 5
  capstone covering measurement evidence, query/index reasoning, read-model
  ownership, cache behavior, staleness, Redis outage reasoning, and
  communication quality.
- `reviews/llm/README.md`: reusable LLM reviewer prompt patterns.
- `reviews/llm/TEMPLATE_review_my_work.md`: learner-facing critique request
  template.
- `reviews/llm/TEMPLATE_interview_me.md`: learner-facing mock interview
  template.
- `reviews/llm/TEMPLATE_incident_commander.md`: Phase 4 incident commander
  prompt requiring facts, assumptions, learner hypothesis, and a clear next
  check.
- `reviews/llm/TEMPLATE_log_analysis_helper.md`: Phase 4 bounded log analysis
  prompt requiring scenario context, metrics or durable status, and the
  learner's hypothesis before analysis.
- `reviews/llm/TEMPLATE_postmortem_critique.md`: Phase 4 postmortem critique
  prompt for reviewing unsupported claims, weak evidence, action items, and
  secret-handling risk after the learner writes a draft.
- `quizzes/phase-1.md`: Phase 1 short-answer quiz for HTTP basics, relational
  modeling, transactions, migrations, health checks, logs, deployment, database
  failure, and scope control.
- `quizzes/phase-2.md`: Phase 2 short-answer quiz for async work, retries,
  idempotency, duplicates, Redis versus Postgres, side effects, and eventual
  consistency.
- `quizzes/phase-3.md`: Phase 3 short-answer quiz for modular monoliths,
  service extraction, contracts, compatibility, timeouts, partial failure, and
  extraction defense.
- `quizzes/phase-4.md`: Phase 4 short-answer quiz for logs, metrics,
  correlation IDs, health checks, incident response, and postmortem quality.
- `quizzes/phase-5.md`: Phase 5 short-answer quiz for measurement, pagination,
  indexes, read models, Redis cache, staleness, failure, and review judgment.
- `interviews/phase-1-backend.md`: Phase 1 backend mock interview prompts with
  strong-answer traits instead of canned answers.
- `interviews/phase-2-backend-distributed.md`: Phase 2 backend and distributed
  systems mock interview prompts with strong-answer traits for async jobs,
  queue coordination, retries, idempotency, side effects, and scope control.
- `interviews/phase-3-distributed-boundaries.md`: Phase 3 distributed-boundary
  mock interview prompts with strong-answer traits for ownership, extraction
  decisions, contracts, failure debugging, operations, and scope control.
- `interviews/phase-4-operational-debugging.md`: Phase 4 operational debugging
  mock interview prompts with strong-answer traits for timelines, logs,
  metrics, health checks, durable state, incident response, postmortems, and
  LLM-assisted debugging discipline.
- `interviews/phase-5-performance-scaling.md`: Phase 5 performance and scaling
  mock interview prompts with strong-answer traits for baselines, query shape,
  read models, Redis cache, staleness, outage fallback, and tradeoff defense.
- `interviews/phase-6-storage-systems.md`: Phase 6 storage systems mock
  interview prompts with strong-answer traits for source-of-truth ownership,
  Redis, document stores, queues/streams, search, analytics, vector storage,
  and refusing unjustified datastores.
- `interviews/phase-6-language-runtime.md`: Phase 6 language and runtime mock
  interview prompts with strong-answer traits for Python/FastAPI, Go,
  TypeScript/Node, JVM, Rust, BEAM/Elixir, and polyglot restraint.
- `interviews/phase-6-deployment-platforms.md`: Phase 6 deployment-platform
  mock interview prompts for defending Dokku, k3s, stateful dependency
  placement, rollouts, secrets, networking, observability, and team fit.
- `extensions/polyglot-report-renderer/README.md`: optional extension spec for
  reimplementing only the stateless report renderer in Go or TypeScript behind
  `report-rendering.v1`; not required for the main OpsLedger path.
- `services/api/opledger_api/`: FastAPI package with app creation,
  configuration, database engine/session setup, dependency-free liveness,
  database-backed readiness, Phase 1 SQLAlchemy models, Pydantic schemas,
  explicit internal modules for customers, work requests, versioned report
  rendering contracts, local report rendering, a bounded reporting-service
  client, async report job state, notification attempts, an explicit
  customer work request stats read-model rebuild and Redis cached dashboard
  read path, shared route dependencies, a worker entrypoint with bounded
  retries, completed-output duplicate execution protection, local/test failure
  injection, structured JSON logs, request ID handling, correlation ID
  propagation through report jobs, and lightweight in-process metrics for HTTP,
  report job, worker, reporting-boundary, notification, and cache signals.
- `services/reporting/reporting_service/`: stateless FastAPI report-rendering
  service that implements `report-rendering.v1` without database ownership and
  exposes disabled-by-default local/test failure modes for boundary drills,
  with the same structured request logging, correlation header handling, and
  `/metrics` surface as the API.
- `services/api/alembic.ini`: Alembic entry point for API database migrations.
- `services/api/migrations/`: Alembic migration environment and deterministic
  migrations for customers, work requests, status events, report jobs,
  notification attempts, the Phase 5 filtered work request list index, and the
  customer work request stats read model.
- `services/api/tests/`: API scaffold, CRUD route, status history, derived
  read-model and cache, report job endpoint and worker lifecycle, reporting
  client, model, and schema tests.
- `services/reporting/tests/`: reporting service contract tests.
- `docs/runbooks/DB_CONNECTIVITY.md`: local and future Dokku troubleshooting
  guide for database readiness failures, including Docker Compose checks.
- `scripts/verify.sh`: repo-root verification gate run through `uv`.
- `scripts/worker.sh`: host-local RQ worker entrypoint for report jobs.
- `scripts/dev-up.sh`: small wrapper around `docker compose up --build`.
- `scripts/dev-down.sh`: small wrapper around `docker compose down`.
- `scripts/migrate.sh`: explicit Alembic migration wrapper for host or Compose
  execution.
- `scripts/rebuild-read-models.sh`: explicit host-local command for rebuilding
  the customer work request stats read model from source-of-truth tables.
- `scripts/scenarios/phase2_worker_down.sh`: small helper for stopping,
  starting, or inspecting only the Compose worker during Phase 2 worker-down
  drills.
- `scripts/scenarios/phase2_redis_down.sh`: small helper for stopping,
  starting, or inspecting Redis and the worker during Phase 2 Redis-down
  drills.
- `scripts/perf/baseline.py`: dependency-free Phase 5 baseline runner for
  low-rate work request listing, dashboard stats reads, opt-in work request
  creation, report job polling, and a small deterministic local read fixture.

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
  first concrete path is Dokku for the single-service API. k3s now exists as a
  later orchestration learning path and should not be treated as the default
  starting deployment.
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
- Do not add new databases, service extraction, retries, or idempotency before
  the curriculum creates a concrete need. Keep the k3s manifests scoped to the
  later orchestration learning path.
- Keep planned material clearly labeled as planned.
- Keep current-state claims accurate.
- Prefer narrow, durable documents over broad placeholders.
- Update this map when a later prompt creates a new layer or changes ownership.
