# Phase 3 Lesson Path

Phase 3 teaches careful boundaries inside OpsLedger before and during one
narrow service extraction. The default posture remains skeptical because
extraction is not automatically good, and service boundaries are expensive.

## Path

1. Start with `docs/architecture/modular-monolith.md`.
2. Complete `exercises/phase-3/01-modular-monolith-boundaries.md`.
3. Review `docs/adr/0001-report-rendering-boundary.md` as the accepted
   learning decision for the one narrow extraction.
4. Review `docs/contracts/report-rendering-v1.md` and complete
   `exercises/phase-3/02-contract-before-network.md` to practice compatibility
   before adding a network boundary.
5. Complete `exercises/phase-3/03-extract-reporting-service.md` to wire the
   stateless service with explicit timeout and failure behavior.
6. Review `docs/contracts/compatibility-playbook.md`, then complete
   `exercises/phase-3/04-timeouts-and-contracts.md` using the reporting
   timeout, bad-response, and mixed-version scenarios.
7. Revisit the Phase 2 capstone evidence and identify which pain was solved by
   async work rather than service extraction.

## Boundary Focus

Learners should be able to explain:

- Why customer identity, work request lifecycle state, report jobs, report
  rendering, and notification attempts have different ownership.
- Why report rendering is the safest first candidate boundary to study.
- Why moving a module into another process creates failure modes that do not
  exist for in-process calls.
- Why a clean internal contract is useful before a service is extracted.
- Why additive contract fields are different from missing fields, wrong
  versions, malformed responses, and slow downstream services.

Future Phase 3 lessons may add contract reviews, dependency direction checks,
and extraction criteria. They should not add more deployable services without a
new concrete failure or teaching moment.
