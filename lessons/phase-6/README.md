# Phase 6 Lesson Path

Phase 6 turns the built system into architecture judgment and interview
readiness. The goal is not to invent a bigger architecture; it is to defend
small, specific decisions from evidence, constraints, and operational cost.

## Initial Path

1. Read `docs/architecture/current-system.md` to name the actual runtime shape
   before proposing changes.
2. Read `docs/CONSTRAINTS.md` and `docs/SYSTEM_EVOLUTION.md` to keep VPS,
   Dokku, Postgres, Redis, worker, reporting service, observability, and
   measured performance constraints in view.
3. Read `docs/adr/TEMPLATE.md` and the current ADRs in `docs/adr/`.
4. Revisit `docs/performance/baselines.md`,
   `docs/performance/read-models.md`, `docs/performance/caching.md`, and
   `docs/observability/metrics.md` so decisions cite evidence instead of
   labels.
5. Complete `exercises/phase-6/01-decision-memo-defense.md`.
6. Review the memo with `reviews/checklists/architecture-review.md`.
7. Practice defending the decision as an interview answer: state the context,
   decision, tradeoffs, failure modes, rollback plan, and evidence that would
   change your mind.

## Phase 6 Focus

Learners should be able to explain:

- What currently runs in the API, worker, reporting service, Postgres, and
  Redis.
- Why Postgres remains the source of truth even with queues, cache, and read
  models.
- Why the reporting service is a narrow stateless extraction, not a general
  endorsement of service sprawl.
- Why Dokku fits the early deployment target and what it does not solve.
- How measured performance and incident evidence constrain architecture
  proposals.
- What each decision costs a one-person or small-team operator.
- How to reverse or revise a decision when the evidence changes.

Future Phase 6 work may add system-design interview prompts, proposal critique
drills, and capstone architecture reviews. It should not add k3s manifests or
new runtime features until a later prompt creates that need.
