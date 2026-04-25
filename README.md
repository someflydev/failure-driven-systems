# Failure-Driven Systems

Failure-Driven Systems is a learning platform for building practical backend,
data/backend, distributed systems, platform, and architecture judgment through
constrained, observable practice.

This repository is not a toy tutorial collection and not an application scaffold
yet. It is the doctrine, curriculum frame, and navigable skeleton for a public
learning project where concepts are earned through experience: learners hit
friction, name the failure, recognize the pattern, vary the situation, explain
the tradeoff, and defend the decision under questioning.

## Who It Is For

This project is for engineers who want stronger production judgment, especially:

- Backend engineers moving beyond endpoint implementation.
- Data/backend engineers who need source-of-truth, ingestion, and reliability
  instincts.
- Generalist platform engineers practicing deployment, operations, and incident
  response on modest infrastructure.
- Interview candidates who need to explain architecture decisions from concrete
  experience instead of memorized diagrams.

## What Makes It Different

The platform starts from a deliberately constrained environment: one Linux VPS
with 4 GB RAM, 3 vCPUs, Dokku installed, Docker available, and k3s available
later. The constraint is part of the curriculum. Learners must make small,
defensible choices before reaching for distributed machinery.

The doctrine favors:

- Failure before abstraction.
- Friction before naming.
- A modular monolith before service sprawl.
- Postgres as the source of truth.
- Redis only after a later failure creates the need.
- Dokku before k3s.
- LLMs as reviewers, interviewers, and critics, not ghostwriters.

## System Domain

All later lessons build one evolving system: OpsLedger, a small internal
operations workflow platform for tracking customer work requests, status
changes, operational notes, generated reports, and later notifications.

OpsLedger is deliberately ordinary. It supports concrete CRUD early, then
naturally creates pressure for transactions, background jobs, side effects,
module boundaries, observability, read models, caching, and architecture
defense. See `docs/DOMAIN.md` for the domain boundaries and conceptual
entities.

## Phase Sequence

The curriculum progresses through six phases:

1. Single service fundamentals.
2. Async work after synchronous pain appears.
3. Careful boundaries before service extraction.
4. Observability, operations, and incidents.
5. Performance, caching, and read models when justified by measured pressure.
6. Architecture defense, system design, and interview readiness.

Directories and application code should appear only when later prompts justify
them. This repository should remain easy to navigate, honest about what exists,
and strict about teaching judgment before tooling.
