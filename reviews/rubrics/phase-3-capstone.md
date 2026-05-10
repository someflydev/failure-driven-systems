# Phase 3 Capstone Rubric

Score each category from 1 to 4. A passing capstone should have no category
below 3 unless the learner documents a real environment blocker and still
demonstrates the reasoning with focused tests or written evidence.

## Backward-Compatible Contract Change

1. The learner changes the contract in a breaking or unclear way.
2. The change is described as optional, but tests or behavior require all
   callers to send it.
3. The learner adds one backward-compatible request or response change with
   updated docs and tests proving old behavior still works.
4. The learner also explains old caller, old provider, persisted-result, and
   mixed-version implications.

## Failure Scenario Evidence

1. Scenario evidence is missing or only lists intended commands.
2. One Phase 3 scenario is attempted, but job status, logs, or cleanup are
   incomplete.
3. At least one reporting timeout, bad-response, or mixed-version scenario is
   run with durable job evidence, relevant logs, result endpoint behavior, and
   cleanup notes.
4. The evidence clearly distinguishes timeout, non-2xx, malformed JSON, and
   invalid contract behavior where relevant.

## Boundary Reasoning

1. The learner treats the reporting service as better because it is a service.
2. The learner names costs but does not connect them to OpsLedger behavior.
3. The learner explains ownership, contract stability, timeout behavior,
   retries, deployment cost, debugging, and rollback.
4. The learner compares keeping the service with folding it back into the
   monolith using concrete evidence.

## Decision Memo

1. No clear recommendation is made.
2. The recommendation is generic and not tied to scenario evidence.
3. The memo defends whether the extraction should stay, names benefits and
   costs, and explains what evidence would change the decision.
4. The memo is concise, operator-aware, and honest about uncertainty and
   tradeoffs.

## Technical Verification

1. Verification is missing.
2. Verification runs only broad tests or only manual checks.
3. The learner runs `./scripts/verify.sh` and focused contract or client tests
   relevant to the change.
4. The learner also records the scenario command, inspected endpoints or logs,
   and any environment blocker precisely.

## LLM Senior-Review Use

1. The learner lets an LLM write the memo or decision.
2. The learner asks for broad approval without providing evidence.
3. The learner writes the memo first, then asks an LLM for senior-review
   critique of hidden costs, weak evidence, rollback, and contract risk.
4. The learner revises the memo based on critique while keeping their own
   recommendation and reasoning accountable.

## Scope Control

1. The capstone adds unrelated infrastructure, caching, k3s, or another
   service.
2. The learner avoids extra tools but cannot explain why they are out of
   scope.
3. The learner stays within Phase 3 boundaries: one reporting service, current
   logs/status evidence, no cache, no k3s, and no new deployable service.
4. The learner states what later evidence would justify each deferred option.
