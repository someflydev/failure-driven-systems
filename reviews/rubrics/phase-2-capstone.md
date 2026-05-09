# Phase 2 Capstone Rubric

Score each category from 1 to 4. A passing capstone should have no category
below 3 unless the learner documents a real environment blocker and still
demonstrates the reasoning with local tests or written evidence.

## Scenario Execution

1. Scenario notes are missing or only describe intended commands.
2. One scenario is attempted, but evidence is thin or cleanup is unclear.
3. At least two Phase 2 scenarios are run with status responses, logs or test
   output, and cleanup notes.
4. Scenario evidence clearly distinguishes worker unavailable, queue
   unavailable, retry failure, duplicate execution, delayed completion, or side
   effect failure.

## Async State Reasoning

1. The learner confuses enqueue acceptance, execution, completion, and result
   availability.
2. The learner names statuses but cannot connect them to user-visible behavior.
3. The learner explains `queued`, `running`, `succeeded`, `failed`, `202
   Accepted`, and `report_result_unavailable` accurately.
4. The learner also identifies misleading UI or API language and proposes a
   precise correction.

## Retry And Idempotency Design

1. The learner treats retries as automatically safe.
2. The learner mentions idempotency but does not separate duplicate boundaries.
3. The learner explains bounded retries, attempt evidence, request
   idempotency, completed-output protection, and notification attempt
   idempotency.
4. The learner can defend remaining gaps and describe what a new side effect
   would need before retries are safe.

## Redis And Postgres Ownership

1. The learner treats Redis as durable user-facing truth.
2. The learner knows both systems exist but blurs their responsibilities.
3. The learner explains Postgres as durable source of truth and Redis as queue
   coordination.
4. The learner uses Redis-unavailable or worker-unavailable evidence to
   explain what the app can and cannot do.

## Fix Or Explanation Quality

1. No issue is fixed or explained.
2. The learner changes code or docs without tying the change to scenario
   evidence.
3. The learner fixes one small issue or writes a concrete explanation of one
   observed issue, with verification.
4. The learner shows the tradeoff behind the fix or explains why no code change
   was the correct outcome.

## Scope Control

1. The capstone adds unrelated infrastructure or architecture.
2. The learner avoids extra tools but cannot explain why they are out of scope.
3. The learner keeps the work within Phase 2 boundaries: no service extraction,
   Kubernetes, caching, or broad observability stack.
4. The learner states what future evidence would justify revisiting each
   deferred option.
