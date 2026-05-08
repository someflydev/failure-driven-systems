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
  service using repo-root `uv` tooling and Python 3.12.
- `.dockerignore`: Docker build-context exclusions for local env files,
  virtualenvs, caches, and generated artifacts.
- `docker-compose.yml`: local development stack with API, Postgres, Redis, and
  a worker process for Phase 2 background report generation.
- `deploy/dokku/README.md`: Phase 1 Dokku deployment path for the single
  Dockerfile-based API service, including app creation, Postgres linking,
  config, deploy, migrations, health checks, logs, and rollback basics.
- `deploy/dokku/checklist.md`: concise Dokku deployment preflight and
  post-deploy checklist.
- `.env.example`: local placeholder environment values for Compose, Redis, and
  health tuning; real `.env` files must remain uncommitted.
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
- `docs/TESTING_STRATEGY.md`: current Phase 1 test layers, local verification
  entrypoint, fixture discipline, and deferred testing layers.
- `docs/TECH_STACK.md`: current stack choices, Python tooling, and deferred
  technology decisions.
- `docs/async/phase-2-job-lifecycle.md`: Phase 2 async report job lifecycle,
  durable Postgres ownership, ephemeral Redis queue ownership, and safe
  user-facing assumptions for status and result endpoints.
- `docs/data-models/phase-1.md`: implemented Phase 1 customer, work request,
  and work request status event tables, relational choices, deferred entities,
  transaction reasoning, and source-of-truth constraints.
- `curriculum/README.md`: phase sequence and concept timing boundaries.
- `curriculum/PHASE_PLAN.md`: OpsLedger capability plan for each curriculum
  phase.
- `lessons/phase-1/README.md`: Phase 1 lesson index linking app features,
  exercises, scenarios, runbooks, deployment docs, review gates, quiz,
  interview practice, and capstone in order.
- `lessons/phase-2/README.md`: Phase 2 starter lesson index with only the
  synchronous report pain exercise linked and an explicit warning to observe
  request-path pain before adding a queue.
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
- `scenarios/phase-1/db-unavailable.md`: guided local database outage scenario
  for observing live-but-not-ready behavior.
- `ops/runbooks/phase-1-first-response.md`: first-response runbook for health
  endpoints, logs, environment, database reachability, migrations, and rollback
  thinking.
- `ops/runbooks/dokku-api-incident.md`: Dokku API incident runbook for bad env
  vars, unavailable Postgres, failed migrations, boot failures, memory pressure,
  and unreadable logs.
- `reviews/checklists/phase-1-api-review.md`: practical Phase 1 API review
  checklist covering validation, constraints, transactions, errors, health
  behavior, tests, and scope control.
- `reviews/rubrics/phase-1-capstone.md`: scoring rubric for the Phase 1
  capstone covering correctness, relational reasoning, operational debugging,
  deployment evidence, explanation quality, and restraint around premature
  complexity.
- `reviews/llm/README.md`: reusable LLM reviewer prompt patterns.
- `reviews/llm/TEMPLATE_review_my_work.md`: learner-facing critique request
  template.
- `reviews/llm/TEMPLATE_interview_me.md`: learner-facing mock interview
  template.
- `quizzes/phase-1.md`: Phase 1 short-answer quiz for HTTP basics, relational
  modeling, transactions, migrations, health checks, logs, deployment, database
  failure, and scope control.
- `interviews/phase-1-backend.md`: Phase 1 backend mock interview prompts with
  strong-answer traits instead of canned answers.
- `services/api/opledger_api/`: FastAPI package with app creation,
  configuration, database engine/session setup, dependency-free liveness,
  database-backed readiness, Phase 1 SQLAlchemy models, Pydantic schemas,
  synchronous customer/work-request CRUD, status history routes, synchronous
  work request summary reporting helpers with opt-in local route delay,
  Redis/RQ-backed report job enqueueing, recent job listing, durable job status
  and result endpoints, a worker entrypoint, durable report job state, and
  simple request/readiness logging.
- `services/api/alembic.ini`: Alembic entry point for API database migrations.
- `services/api/migrations/`: Alembic migration environment and deterministic
  Phase 1 migrations for customers, work requests, and status events.
- `services/api/tests/`: API scaffold, CRUD route, status history, report job
  endpoint and worker lifecycle, model, and schema tests.
- `docs/runbooks/DB_CONNECTIVITY.md`: local and future Dokku troubleshooting
  guide for database readiness failures, including Docker Compose checks.
- `scripts/verify.sh`: repo-root verification gate run through `uv`.
- `scripts/worker.sh`: host-local RQ worker entrypoint for report jobs.
- `scripts/dev-up.sh`: small wrapper around `docker compose up --build`.
- `scripts/dev-down.sh`: small wrapper around `docker compose down`.
- `scripts/migrate.sh`: explicit Alembic migration wrapper for host or Compose
  execution.

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
