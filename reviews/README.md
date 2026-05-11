# Reviews

Reviews are the quality gate after a learner has attempted the work. They are
not answer keys and should not be used to skip implementation, debugging, or
decision writing.

Use this directory in this order:

1. Finish the exercise, incident drill, decision memo, or capstone attempt.
2. Gather evidence: changed files, commands, logs, metrics, database
   observations, scenario notes, and the learner's own reasoning.
3. Pick the narrowest relevant checklist or rubric.
4. Mark findings as concrete gaps, not vague preferences.
5. Write the next action the learner should take before asking for more help.

## Checklists

Use `reviews/checklists/` for focused pass/fail review of a completed attempt.
Checklists are best for implementation reviews, incident timelines, service
boundary critiques, performance work, and architecture proposals.

Good checklist use:

- cites the learner's files, commands, and observations;
- separates correctness gaps from explanation gaps;
- names missing evidence the learner must collect;
- avoids replacing the learner's design with a canned solution.

## Rubrics

Use `reviews/rubrics/` after capstones or larger phase work. Rubrics help the
learner self-score across correctness, reasoning, operational evidence,
communication, and scope control.

Rubric scores should be justified with evidence from the learner's attempt. A
low score should point to a concrete next revision or drill.

## LLM Templates

Use `reviews/llm/` only after the learner can provide:

- the prompt, exercise, incident, or decision being reviewed;
- relevant files or focused excerpts;
- commands and important output;
- failures or confusing behavior;
- the learner's own reasoning and rejected alternatives.

LLMs may act as reviewers, skeptics, incident commanders, or interviewers. They
should ask for evidence, challenge unsupported claims, and critique attempted
answers. They should not write the first solution, invent missing evidence, or
provide memorized interview answers.

## System-Wide Reviews

Use `reviews/checklists/system-wide-review.md` near phase boundaries, before a
public portfolio review, or before a mock interview panel. It checks whether
the learner can connect work across phases: source of truth, async behavior,
service boundaries, observability, performance, deployment, and architecture
defense.
