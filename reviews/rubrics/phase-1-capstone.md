# Phase 1 Capstone Rubric

Score each category from 1 to 4. A passing capstone should have no category
below 3 unless the learner documents a real environment blocker and still
demonstrates the reasoning with local evidence.

## Implementation Correctness

1. The change is incomplete, breaks existing CRUD behavior, or bypasses the
   current API shape.
2. The change works only on the happy path and has weak validation or error
   behavior.
3. The change is small, safe, consistent with existing routes, schemas, models,
   migrations, and tests.
4. The change is correct, minimal, well tested, and improves the API without
   making Phase 1 harder to understand.

## Relational Reasoning

1. The learner cannot explain where truth lives or which constraints matter.
2. The learner names tables but treats route validation as enough for data
   integrity.
3. The learner explains primary keys, foreign keys, uniqueness, status checks,
   and transaction boundaries relevant to the change.
4. The learner also identifies possible inconsistent states and shows how the
   chosen database design prevents or exposes them.

## Operational Debugging

1. The learner guesses from code or symptoms without collecting evidence.
2. The learner checks one endpoint or log line but confuses liveness,
   readiness, and database-backed behavior.
3. The learner uses health endpoints, logs, config, database reachability, and
   migration state in a sensible order.
4. The learner produces a clear sanitized incident note with timeline, impact,
   evidence, cause, recovery, and follow-up.

## Deployment Evidence

1. No deployment attempt or blocker is documented.
2. Deployment notes exist but omit commit, migration, health, logs, or config
   evidence.
3. The learner records the deploy commit, app/service names, migration result,
   liveness, readiness, logs, and one database-backed check, or documents a
   concrete blocker.
4. The learner also records rollback thinking tied to the exact code and schema
   state.

## Explanation Quality

1. The explanation is a feature summary with little reasoning.
2. The explanation names concepts but does not connect them to observed
   behavior.
3. The explanation connects the implementation, tests, deploy evidence,
   failure drill, and tradeoffs.
4. The explanation is interview-ready: concrete, concise, evidence-based, and
   honest about limits.

## Restraint Around Premature Complexity

1. The learner adds or proposes unrelated infrastructure or architecture.
2. The learner avoids adding it but cannot explain why it is out of scope.
3. The learner explains why Redis, queues, caching, service extraction, k3s, and
   Kubernetes are not Phase 1 fixes.
4. The learner can state what later evidence would justify revisiting each
   deferred option.
