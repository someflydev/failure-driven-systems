# Mock Interview Panel

## Phase

Phase 6: architecture defense, system design, and interview readiness.

This exercise belongs here because the learner has enough accumulated
implementation, debugging, incident, performance, deployment, and decision
evidence to defend the system under questioning.

## Concepts

- Evidence-based interview answers.
- Backend implementation defense.
- Distributed failure debugging.
- Operational incident communication.
- Architecture decision critique.
- Weak-area identification and follow-up practice.

## Prerequisites

Read these before starting:

- `interviews/README.md`
- `interviews/mock-panels/README.md`
- one mock panel guide in `interviews/mock-panels/`
- `reviews/checklists/system-wide-review.md`
- `reviews/llm/TEMPLATE_interview_me.md`
- `reviews/llm/TEMPLATE_adversarial_architecture_panel.md`
- at least one completed Phase 6 decision defense exercise

You should also have completed enough prior phase work to cite concrete
OpsLedger evidence from exercises, scenarios, tests, logs, metrics, or decision
memos.

## Build/Change Task

Run one mock interview panel and record the outcome.

Your panel record must include:

- the panel mode selected;
- the evidence package used;
- at least six questions asked;
- a short summary of your attempted answers;
- critique received from a human, peer, self-review, or LLM;
- at least three weak areas;
- one follow-up exercise, checklist, or scenario for each weak area;
- one revised two-minute answer after the panel.

You may use a human interviewer, self-recording, a peer group, or an LLM. If
using an LLM, paste your artifacts and reasoning first and require questions
before critique.

## Constraints

- Do not ask an LLM to produce polished answers before you attempt them.
- Do not include secrets, raw customer data, tokens, connection strings, or
  private deployment details.
- Do not claim experience with systems, incidents, metrics, alerts, or
  deployments not represented in your evidence.
- Do not treat role tracks as separate codebases.
- Do not add runtime code, services, infrastructure manifests, dependencies, or
  generated artifacts for this exercise.

## Failure Modes

- The panel becomes memorization instead of defense from evidence.
- Answers use generic scale language without naming OpsLedger behavior.
- The learner cannot distinguish Postgres truth from Redis queue/cache state.
- The learner jumps to root cause without logs, metrics, health checks, or
  durable status evidence.
- Architecture answers omit operational cost, rollback, or reversal criteria.
- The panel notes record only what went well and no weak areas.
- LLM use invents missing evidence or writes the learner's answers.

## Expected Reasoning

After completing the exercise, you should be able to explain OpsLedger's
evolution, defend one implementation choice, debug one distributed failure,
communicate one incident, and defend one architecture decision using concrete
artifacts instead of memorized answers.

## Verification

- Run `./scripts/verify.sh`.
- Confirm your panel record names the selected guide in
  `interviews/mock-panels/`.
- Confirm your evidence package cites at least five concrete repository
  artifacts or scenario observations.
- Confirm each weak area has a follow-up action.
- Confirm any LLM prompt included your artifacts and reasoning before critique.
- Confirm no secrets or private deployment details are included.

## Reflection Questions

- Which answer became weaker when the interviewer asked for evidence?
- Which failure mode can you explain clearly now, and which one still needs a
  rerun?
- Where did you overclaim beyond what OpsLedger currently implements?
- Which tradeoff are you most prepared to defend?
- What evidence would make you change one architecture recommendation?
- What question do you want to be asked again after follow-up practice?

## LLM Usage

Use an LLM only as an interviewer or critic after preparing your evidence
package and your own reasoning. Use `reviews/llm/TEMPLATE_interview_me.md` for
general practice or
`reviews/llm/TEMPLATE_adversarial_architecture_panel.md` for architecture
defense. Require one question at a time, answer before requesting critique, and
do not ask for model answers until after your attempt.

## Path-Specific Extensions

Backend path: run `interviews/mock-panels/backend-implementation-panel.md` and
focus on routes, transactions, migrations, tests, and async semantics.

Operations path: run `interviews/mock-panels/distributed-systems-debugging-panel.md`
and focus on an incident or failure scenario with logs, metrics, health checks,
and durable status evidence.

Architecture path: run `interviews/mock-panels/architecture-staff-engineer-panel.md`
and focus on a decision memo, datastore/runtime/platform choice, rollback, and
operational cost.

Interview path: run two different panel modes on separate days and compare the
weak areas that repeat.

## Deployment/Debugging Actions If Relevant

No deployment is required. If your selected panel uses an incident or debugging
scenario, record only sanitized evidence: command names, health response status,
log event names, metrics names, durable status fields, and timestamps. Do not
record secrets or private deployment values.
