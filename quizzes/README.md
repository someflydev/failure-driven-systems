# Quizzes

Quizzes are short-answer checks for whether a learner can explain the phase in
their own words. They are not trivia and do not have answer keys in this repo.

## Format

Each quiz is organized by topic. Answer with short paragraphs or bullets. A
strong answer should:

- connect the concept to OpsLedger behavior;
- name the files, commands, logs, metrics, scenarios, or database records that
  support the claim;
- identify tradeoffs and failure modes;
- avoid generic system-design phrases that are not tied to the current system.

## How To Self-Grade

For each answer, mark it as:

- `Strong`: cites concrete OpsLedger evidence, names tradeoffs, and says what
  would change the decision.
- `Partial`: explains the concept but lacks evidence, misses a failure mode, or
  uses vague terms.
- `Weak`: gives a memorized definition, overclaims, or cannot name how the
  behavior appears in the repository.

After grading, choose the weakest topic and revisit the matching lesson,
exercise, checklist, or interview prompt. Do not use an LLM to generate quiz
answers before attempting them. After an attempt, an LLM can critique whether
the answer is supported by evidence.

## Phase Coverage

- `phase-1.md`: single-service backend fundamentals.
- `phase-2.md`: async work, retries, idempotency, and Redis/Postgres ownership.
- `phase-3.md`: boundaries, contracts, service extraction, and partial failure.
- `phase-4.md`: logs, metrics, correlation, incidents, and postmortems.
- `phase-5.md`: measurement, indexes, read models, cache, and staleness.

Phase 6 uses decision memos, architecture checklists, and mock interviews
instead of a quiz because the work is primarily defense and critique.
