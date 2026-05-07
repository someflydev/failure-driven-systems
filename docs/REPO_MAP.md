# Repository Map

This repository begins with doctrine, navigation, and the initial OpsLedger API
scaffold. Directories should be created or populated only when later prompts
justify them. Planned directories below define the intended shape, not current
implementation.

## Current Foundation

- `README.md`: public positioning, audience, differentiators, and phase
  sequence, plus the current local development workflow.
- `AGENT.md`: routing instructions for future coding-assistant sessions.
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
- `docs/TECH_STACK.md`: current stack choices, Python tooling, and deferred
  technology decisions.
- `docs/data-models/phase-1.md`: implemented Phase 1 customer and work request
  tables, relational choices, deferred entities, and source-of-truth
  constraints.
- `curriculum/README.md`: phase sequence and concept timing boundaries.
- `curriculum/PHASE_PLAN.md`: OpsLedger capability plan for each curriculum
  phase.
- `reviews/llm/README.md`: reusable LLM reviewer prompt patterns.
- `reviews/llm/TEMPLATE_review_my_work.md`: learner-facing critique request
  template.
- `reviews/llm/TEMPLATE_interview_me.md`: learner-facing mock interview
  template.
- `services/api/opledger_api/`: FastAPI package with app creation,
  configuration, database engine/session setup, dependency-free liveness,
  database-backed readiness, Phase 1 SQLAlchemy models, and Pydantic schemas.
- `services/api/alembic.ini`: Alembic entry point for API database migrations.
- `services/api/migrations/`: Alembic migration environment and deterministic
  Phase 1 migration for customers and work requests.
- `services/api/tests/`: API scaffold, model, and schema tests.
- `docs/runbooks/DB_CONNECTIVITY.md`: local and future Dokku troubleshooting
  guide for database readiness failures.
- `scripts/verify.sh`: repo-root verification gate run through `uv`.

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
- `deploy/`: deployment configuration when a prompt introduces real deployment
  artifacts. Dokku should appear before k3s.
- `ops/`: runbooks, incident response notes, operational checks, and maintenance
  guidance when those materials become concrete.
- `scripts/`: small automation scripts that support verified workflows. The
  current verification entry point is `scripts/verify.sh`.
- `tests/`: repository or application tests once there is behavior to verify.
- `data/`: sample data, fixtures, or generated learner outputs when required by
  exercises.

## Population Rules

- Do not create empty implementation directories just to match the map.
- Do not add Docker, databases, Redis, queues, k3s manifests, or app code before
  the curriculum creates a concrete need.
- Keep planned material clearly labeled as planned.
- Keep current-state claims accurate.
- Prefer narrow, durable documents over broad placeholders.
- Update this map when a later prompt creates a new layer or changes ownership.
