# Phase 2 Capstone

## Phase

Phase 2: Async After Synchronous Pain. This capstone belongs here because the
learner now has enough working system behavior to defend asynchronous report
jobs, bounded retries, idempotency, side effects, and user-visible consistency
from evidence.

## Concepts

- Async job acceptance versus completion.
- Durable status and result ownership.
- Redis queue coordination.
- Bounded retries and failure evidence.
- Request, job, and side-effect idempotency.
- Partial failure and eventual consistency.
- Scenario-driven review.

## Prerequisites

- `exercises/phase-2/01-synchronous-report-pain.md`
- `exercises/phase-2/02-background-report-worker.md`
- `exercises/phase-2/03-job-status-and-eventual-consistency.md`
- `exercises/phase-2/04-retries-before-idempotency.md`
- `exercises/phase-2/05-idempotent-report-jobs.md`
- `exercises/phase-2/06-safe-side-effects.md`
- `docs/async/phase-2-job-lifecycle.md`
- `docs/async/idempotency.md`
- `docs/async/side-effects-and-outbox.md`
- At least two scenario docs under `scenarios/phase-2/`.

## Build/Change Task

Run at least two Phase 2 failure scenarios. For each scenario, capture the
commands you ran, the status or test output that proves what happened, and the
cleanup step that restored the local environment.

Then choose one observed issue. Either make a small code or documentation fix,
or write a concrete explanation of why the behavior is acceptable for Phase 2
and what future work would be needed. The issue can be a confusing status,
missing note, weak test, unclear user-facing explanation, or a real bug.

Finish by writing a short defense of the retry and idempotency design. The
defense must distinguish request idempotency, duplicate worker execution after
success, notification attempt idempotency, and the remaining outbox gap.

## Constraints

- Do not add extracted services.
- Do not add Kubernetes, k3s manifests, or cluster tooling.
- Do not add caching or performance optimization.
- Do not add a broad observability stack.
- Do not use a real notification provider.
- Keep fixes small and tied to scenario evidence.
- Do not hide failed background work behind successful API responses.

## Failure Modes

- Treating `202 Accepted` as completed work.
- Treating Redis as durable user-visible status.
- Adding retries without proving duplicate safety.
- Confusing request idempotency with side-effect idempotency.
- Marking report success as failed because notification delivery failed.
- Running a scenario but failing to capture status, logs, or cleanup evidence.
- Solving a Phase 2 learning issue with Phase 4 or Phase 5 infrastructure.

## Expected Reasoning

After the capstone, explain what the user can know after enqueueing a report,
what an operator can inspect when work stalls, and why completed output and
notification attempts need separate duplicate guards.

You should be able to defend the current limits: Redis can be unavailable,
workers can be stopped, retries can repeat work, and a crash can still occur
between report success and notification attempt creation.

## Verification

- Run `./scripts/verify.sh`.
- Run at least two scenario drills from `scenarios/phase-2/`.
- Inspect `GET /reports/jobs/{id}` for each report job involved.
- Inspect `GET /reports/jobs/{id}/result` when a scenario expects completion.
- Inspect `GET /notification-attempts?target_type=report_job&target_id={id}`
  for side-effect scenarios.
- If you changed code, add or update focused tests.
- Confirm every Phase 2 exercise still follows `exercises/TEMPLATE.md`.

## Reflection Questions

- Which scenario produced the clearest evidence of partial failure?
- What changed your understanding of `202 Accepted`?
- Which duplicate boundary is easiest to explain, and which is easiest to get
  wrong?
- What would break if Redis were treated as the source of truth?
- What future Phase 4 or Phase 5 work is tempting but still out of scope?

## LLM Usage

Use an LLM only after you have scenario notes and your own design defense. Ask
it to review your evidence for missing failure modes, unclear idempotency
boundaries, and unsupported claims. Do not ask it to invent scenario results or
write the defense before you have run the drills.

## Path-Specific Extensions

Backend: add one focused regression test for the issue you fixed or explained.

Operations: turn one scenario into a short incident note with impact, evidence,
cause, recovery, and follow-up.

Architecture: write a one-page argument for why Phase 2 still does not justify
service extraction.

Interview: answer the prompts in
`interviews/phase-2-backend-distributed.md` from your own scenario evidence.

## Deployment/Debugging Actions If Relevant

Use local Compose logs, status endpoints, result endpoints, notification
attempts, and test output as evidence. Deployment to Dokku is not required for
this capstone unless your instructor explicitly asks for it.
