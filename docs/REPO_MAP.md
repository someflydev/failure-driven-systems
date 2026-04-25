# Repository Map

This repository begins with doctrine and navigation. Directories should be
created or populated only when later prompts justify them. Planned directories
below define the intended shape, not current implementation.

## Current Foundation

- `README.md`: public positioning, audience, differentiators, and phase
  sequence.
- `AGENT.md`: routing instructions for future coding-assistant sessions.
- `docs/DOCTRINE.md`: durable learning doctrine.
- `docs/CONSTRAINTS.md`: infrastructure and budget assumptions.
- `docs/REPO_MAP.md`: intended repository layers and directory responsibilities.
- `curriculum/README.md`: phase sequence and concept timing boundaries.

## Intended Layers

- `services/`: application services when implementation begins. Start with a
  single service and keep module boundaries explicit before extracting anything.
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
- `scripts/`: small automation scripts that support verified workflows.
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
