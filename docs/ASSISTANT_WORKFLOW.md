# Assistant Workflow

LLMs are part of the Failure-Driven Systems learning environment, but they are
not hidden solution engines. Learners should use assistants to sharpen
judgment, expose weak assumptions, and practice defending decisions after doing
their own work first.

The default order is:

1. Struggle first.
2. Ask for critique second.
3. Ask for explanation third.
4. Compare with possible solutions only after a serious attempt.

## Learner Responsibilities

Before asking an assistant for help, learners should provide the relevant
artifact context:

- The prompt, exercise, or incident scenario being attempted.
- The files, commands, logs, or database observations involved.
- The failure or uncertainty they observed.
- Their own reasoning about what they think is happening.
- The specific kind of critique they want.

Learners should not ask for a full answer before they can explain what they
tried, what failed, and what decision they are currently considering.

## Assistant Responsibilities

Coding assistants and LLM reviewers should act as critics, reviewers,
interviewers, and scenario generators. They should ask for evidence, test
reasoning, identify missing cases, and challenge unsupported claims.

Assistants should avoid producing answer-key style learner solutions unless the
active repository prompt explicitly asks for implementation. When learners are
still practicing, the assistant should prefer questions, review notes,
counterexamples, and small targeted explanations over complete code.

## Phase 1: Critique After Completion

In Phase 1, learners should finish their own implementation attempt before
using an assistant for critique. The assistant may review completed work for
correctness, missing validation, transaction mistakes, weak logs, unclear status
changes, and source-of-truth confusion.

Good assistant use:

- "Review this completed endpoint and migration for correctness."
- "Tell me what assumptions in my status-change handling are weak."
- "Ask me questions until I can defend where truth lives."

Bad assistant use:

- "Write the endpoint and schema for me."
- "Give me the complete Phase 1 solution."

## Phase 2: Edge Cases And Failure Analysis

In Phase 2, learners may use assistants to explore edge cases around slow work,
retries, idempotency, duplicate side effects, stuck jobs, and partial failure.
The assistant should help build a test matrix and ask what can be retried
safely.

Appropriate prompts include:

- "Find missed edge cases in this retry design."
- "Critique my idempotency key choice."
- "Suggest a failure matrix for this background job."

## Phase 3: Design Review And Contract Critique

In Phase 3, assistants should review module boundaries, ownership, dependency
direction, transaction boundaries, and internal contracts. The goal is not to
invent a distributed architecture. The goal is to make one deployable service
easier to reason about.

Appropriate prompts include:

- "Challenge this module boundary before I implement it."
- "Review whether this contract leaks workflow ownership."
- "Ask what failure would justify extraction later."

## Phase 4: Incident Analysis And Debugging Drills

In Phase 4, assistants should act like incident commanders or debugging
coaches. They should push learners to build timelines from evidence, separate
symptoms from causes, and identify the smallest corrective change.

Appropriate prompts include:

- "Run an incident review from these logs and commands."
- "Interview me on what users experienced and how I know."
- "Give me one new failure variation based on this outage."

## Phase 5: Performance And Tradeoff Questioning

In Phase 5, assistants should challenge performance work with evidence. They
should ask for baselines, query plans, read/write tradeoffs, rebuild strategy,
source-of-truth clarity, and accepted failure modes.

Appropriate prompts include:

- "Question this index choice using the observed query plan."
- "Critique whether this cache is justified."
- "Ask me to defend staleness, invalidation, and rebuild behavior."

## Phase 6: Architecture Proposals And Defense

In Phase 6, assistants may help generate architecture proposals, mock
interviews, and decision-defense drills. The learner remains accountable for
evidence. Strong answers should refer back to actual OpsLedger failures,
constraints, and tradeoffs rather than memorized diagrams.

Appropriate prompts include:

- "Act as a skeptical architecture reviewer."
- "Mock interview me on the evolution from one service to async work."
- "Challenge whether this boundary should become a separate service."
