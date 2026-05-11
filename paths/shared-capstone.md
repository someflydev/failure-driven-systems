# Shared Role-Path Capstone

The shared capstone is a final portfolio defense for any role path. It uses the
same OpsLedger system and asks the learner to bias the explanation toward a
target role without pretending they built a separate project.

## Evidence Package

Bring concise evidence from existing artifacts:

- implementation: at least one completed exercise from `exercises/phase-1/`,
  `exercises/phase-2/`, `exercises/phase-3/`, or `exercises/phase-5/`;
- debugging: at least one scenario from `scenarios/` with logs, metrics,
  database observations, or health checks;
- review: at least one completed checklist or rubric from `reviews/`;
- explanation: at least one mock interview or decision defense from
  `interviews/` or `exercises/phase-6/`;
- verification: latest output from `./scripts/verify.sh`.

## Defense Flow

1. Explain the current system using `docs/architecture/current-system.md`.
2. Name where durable truth lives and which parts are derived or disposable.
3. Walk through one implementation change and the tests or checks that prove
   it.
4. Walk through one failure, the evidence used, a discarded hypothesis, and the
   resolution or next action.
5. Defend one architecture decision, one rejected alternative, and rollback.
6. Bias the final answer toward the selected path:
   `paths/backend-python.md`, `paths/data-backend.md`,
   `paths/distributed-systems.md`, `paths/generalist-backend.md`, or
   `paths/architecture-decisions.md`.

## Required Milestones

Every completed capstone must include:

- one implementation milestone;
- one debugging milestone;
- one review milestone;
- one explanation milestone.

The milestones may come from different phases, but they must refer to real
OpsLedger files, scenarios, commands, or review artifacts.

## Final Review

Use `reviews/checklists/system-wide-review.md` first. Then use the matching
role-track interview guide in `interviews/role-tracks/`.

Do not add new runtime services, datastores, generated artifacts, or optional
extensions only to make the capstone look larger. The capstone is judged by
evidence quality, tradeoff clarity, and the ability to answer follow-up
questions from the built system.
