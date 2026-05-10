# Phase 4 Capstone Rubric

Score each category from 1 to 4. A passing capstone should have no category
below 3 unless the learner documents a real environment blocker and still
demonstrates the reasoning with sanitized evidence from tests, logs, metrics,
or written incident notes.

## Scenario Evidence

1. Scenario notes are missing or only list intended commands.
2. One incident scenario is attempted, but evidence is thin, unbounded, or not
   tied to specific IDs.
3. At least two Phase 4 scenarios are run or one scenario is run deeply with
   logs, metrics, durable status, status updates, and cleanup notes.
4. Evidence clearly distinguishes worker stall, reporting latency, ambiguous
   correlation, and noisy notification failure where relevant.

## Timeline And Correlation

1. The learner gives a narrative without timestamps or evidence sources.
2. The learner includes timestamps but mixes facts, assumptions, and guesses.
3. The learner builds an evidence-backed timeline using correlation IDs, job
   IDs, services, and durable status.
4. The learner also names ambiguity and shows how a next check reduced it.

## Metrics, Health, And Durable State Reasoning

1. The learner treats one green health check or one metric as complete truth.
2. The learner names logs, metrics, and durable state but blurs their roles.
3. The learner explains what each surface proves and cannot prove.
4. The learner uses scenario evidence to defend the order of checks during an
   incident.

## Incident Communication

1. Status updates are missing or read like internal debugging notes.
2. Updates mention components but omit impact, next action, or next update time.
3. Updates name impact, evidence, hypothesis, action now, and next update time.
4. Updates evolve as evidence changes and avoid premature root cause or
   resolution claims.

## Postmortem And Follow-Up Quality

1. The postmortem is missing or mostly a blame-free feature summary.
2. The postmortem names a cause but has weak evidence or broad action items.
3. The postmortem separates impact, timeline, detection, root cause,
   contributing factors, and small evidence-tied actions.
4. The learner rejects unjustified platform work and explains what future
   evidence would change the follow-up.

## LLM-Assisted Debugging Discipline

1. The learner asks an LLM for the incident answer before collecting evidence.
2. The learner provides evidence but no hypothesis or asks for broad diagnosis.
3. The learner provides bounded evidence, their own hypothesis, uncertainty,
   and asks for critique or next-check guidance.
4. The learner uses LLM critique to strengthen evidence and communication while
   retaining ownership of the conclusion.

## Secret Safety And Scope Control

1. Notes or prompts include secrets, full connection strings, raw customer
   data, request bodies, or full environment dumps.
2. Sensitive data is avoided, but pasted evidence is excessive or unfocused.
3. Evidence is sanitized, bounded by time window, service, ID, and question.
4. The learner also explains why no new runtime feature, dashboard, tracing
   stack, or infrastructure was added for this capstone.
