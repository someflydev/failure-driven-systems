# Phase 3 Lesson Path

Phase 3 teaches careful boundaries inside the existing OpsLedger service. The
default architecture remains a modular monolith because extraction is not
automatically good, and service boundaries are expensive.

## Path

1. Start with `docs/architecture/modular-monolith.md`.
2. Complete `exercises/phase-3/01-modular-monolith-boundaries.md`.
3. Review `docs/adr/0001-report-rendering-boundary.md` as an exploratory ADR,
   not as approval to create another service.
4. Revisit the Phase 2 capstone evidence and identify which pain was solved by
   async work rather than service extraction.

## Boundary Focus

Learners should be able to explain:

- Why customer identity, work request lifecycle state, report jobs, report
  rendering, and notification attempts have different ownership.
- Why report rendering is the safest first candidate boundary to study.
- Why moving a module into another process creates failure modes that do not
  exist for in-process calls.
- Why a clean internal contract is useful even when no service is extracted.

Future Phase 3 lessons may add contract reviews, dependency direction checks,
and extraction criteria. They should not start by adding another deployable
service.
