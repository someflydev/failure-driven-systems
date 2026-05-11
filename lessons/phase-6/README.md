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
5. Read `docs/storage/README.md` and the storage comparison docs in
   `docs/storage/` to compare Postgres, Redis, and rejected datastore options
   against actual OpsLedger workloads.
6. Read `docs/languages/README.md` and the runtime comparison docs in
   `docs/languages/` to compare Python, Go, TypeScript/Node, JVM, Rust, BEAM,
   and polyglot tradeoffs against actual OpsLedger components.
7. Read `docs/deployment/dokku-vs-k3s.md`, `deploy/dokku/`, and
   `deploy/k3s/` to compare the early Dokku path with later orchestration
   practice.
8. Read `reviews/README.md`, `quizzes/README.md`,
   `interviews/README.md`, and `interviews/mock-panels/README.md` so review,
   quiz, and interview materials are used after learner attempts.
9. Complete `exercises/phase-6/01-decision-memo-defense.md`.
10. Complete `exercises/phase-6/02-datastore-tradeoff-defense.md`.
11. Complete `exercises/phase-6/03-runtime-selection-defense.md`.
12. Complete `exercises/phase-6/04-dokku-vs-k3s-defense.md`.
13. Review the memo with `reviews/checklists/architecture-review.md` and, for
    cross-phase readiness, `reviews/checklists/system-wide-review.md`.
14. Practice defending the decision as an interview answer: state the context,
   decision, tradeoffs, failure modes, rollback plan, and evidence that would
   change your mind.
15. Use `interviews/phase-6-storage-systems.md`,
    `interviews/phase-6-language-runtime.md`, and
    `interviews/phase-6-deployment-platforms.md` to practice follow-up
    questions.
16. Complete `exercises/phase-6/05-mock-interview-panel.md` with one guide
    from `interviews/mock-panels/` and record weak areas for follow-up.

## Phase 6 Focus

Learners should be able to explain:

- What currently runs in the API, worker, reporting service, Postgres, and
  Redis.
- Why Postgres remains the source of truth even with queues, cache, and read
  models.
- Why the reporting service is a narrow stateless extraction, not a general
  endorsement of service sprawl.
- Why Dokku fits the early deployment target and what it does not solve.
- Why k3s is introduced later for orchestration learning and is not the
  default starting deployment.
- How measured performance and incident evidence constrain architecture
  proposals.
- How to compare document stores, key-value systems, queues/streams, search
  indexes, analytical stores, and vector storage without implying OpsLedger
  needs all of them.
- When not to add another datastore because Postgres, Redis, indexes, read
  models, cache, or an outbox are enough for the current evidence.
- How to compare Python, Go, TypeScript/Node, JVM, Rust, and BEAM/Elixir
  without ranking languages outside component, team, and operational context.
- Why a polyglot report-rendering extension can be useful practice without
  fragmenting the main OpsLedger path.
- What each decision costs a one-person or small-team operator.
- How to reverse or revise a decision when the evidence changes.

Optional extension work may use `extensions/polyglot-report-renderer/README.md`
to practice a contract-compatible Go or TypeScript report renderer outside the
main path. k3s work should stay scoped to the later deployment learning path.
Future Phase 6 work may add proposal critique drills and capstone architecture
reviews. It should not add new runtime datastores or new main-path runtime
features until a later prompt creates that need.
