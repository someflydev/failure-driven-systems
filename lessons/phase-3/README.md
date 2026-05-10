# Phase 3 Lesson Path

Phase 3 teaches careful boundaries inside OpsLedger before and during one
narrow service extraction. The default posture remains skeptical: service
boundaries are expensive, and extracting a service is only defensible when the
costs solve a concrete failure, ownership problem, or learning objective.

## Ordered Path

1. Review `docs/architecture/modular-monolith.md` to name current module
   ownership and why the monolith remains the default deployment shape.
2. Complete `exercises/phase-3/01-modular-monolith-boundaries.md` to identify
   facts, readers, dependency direction, and coupling before proposing any
   service boundary.
3. Read `docs/adr/0001-report-rendering-boundary.md` as the accepted
   learning decision for exactly one narrow extraction, including the arguments
   against keeping that service in a small production system.
4. Review `docs/contracts/report-rendering-v1.md` and complete
   `exercises/phase-3/02-contract-before-network.md` to practice a
   backward-compatible contract change before adding HTTP, deployment, or
   network failure.
5. Complete `exercises/phase-3/03-extract-reporting-service.md` to wire the
   stateless renderer as a second process with explicit configuration,
   bounded timeouts, and visible failure mapping.
6. Review `docs/contracts/compatibility-playbook.md`, then complete
   `exercises/phase-3/04-timeouts-and-contracts.md` using the reporting
   timeout, bad-response, and mixed-version scenarios.
7. Use `reviews/checklists/phase-3-service-boundary-review.md` to critique the
   reporting boundary for ownership, contract stability, timeout behavior,
   retries, deployment cost, debugging, and rollback.
8. Take `quizzes/phase-3.md`, then use
   `interviews/phase-3-distributed-boundaries.md` for mock defense practice.
9. Complete `exercises/phase-3/05-phase-3-capstone.md` and score it with
   `reviews/rubrics/phase-3-capstone.md`.
10. Revisit the Phase 2 capstone evidence and identify which pain was solved by
    async work rather than service extraction.

## Boundary Focus

Learners should be able to explain:

- Why customer identity, work request lifecycle state, report jobs, report
  rendering, and notification attempts have different ownership.
- Why report rendering is the safest first candidate boundary to study, and why
  that does not make every module a service candidate.
- Why moving a module into another process creates timeout, versioning,
  deployment, debugging, rollback, and partial-failure costs.
- Why a clean internal contract is useful even if the service is never
  extracted.
- Why additive contract fields are different from missing fields, wrong
  versions, malformed responses, and slow downstream services.
- Why a capstone decision memo may defensibly recommend folding the renderer
  back into the monolith if the observed benefits do not outweigh the cost.

Future Phase 3 lessons may add contract reviews, dependency direction checks,
and extraction criteria. They should not add more deployable services without a
new concrete failure or teaching moment.
