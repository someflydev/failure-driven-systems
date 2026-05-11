# Portfolio Guide

This repo is strongest as a portfolio when the learner presents evidence from
working, broken, repaired, and defended OpsLedger states. Do not present it as
a finished product template or a list of technologies.

## Evidence To Capture

For each phase, keep short notes or screenshots that show:

- the command or request you ran;
- the observed behavior before and after the change;
- the database, log, metric, or test evidence that proves the claim;
- the failure mode you reproduced;
- what you deliberately did not add.

Useful artifacts include pytest output, API request examples, migration notes,
health endpoint checks, worker logs, correlation IDs, metric samples, baseline
measurements, incident timelines, and review checklist results.

## Decision Memos

Write brief memos for decisions that would matter in an interview:

- why OpsLedger begins as one service;
- why Postgres owns durable facts;
- why Redis is limited to queue and cache coordination;
- why report rendering is the only studied service boundary;
- why Dokku is the first deploy target;
- when k3s would be worth the added operating cost;
- when a cache, read model, index, or extra datastore should be rejected.

Good memos name alternatives, consequences, rollback, failure modes, and what
new evidence would change the decision.

## Incident Writeups

Use `ops/incidents/TEMPLATE_postmortem.md` and
`ops/incidents/TEMPLATE_incident_status_update.md` for scenario work. A useful
incident writeup includes:

- user-visible impact;
- timeline of evidence, not guesses;
- logs, metrics, health checks, or database facts;
- immediate mitigation;
- root cause or best current explanation;
- one or two corrective actions that fit the current phase.

Avoid claiming broad production readiness from a local drill. The value is the
quality of the reasoning and the operational discipline.

## Deployment Notes

For Dokku or k3s work, capture:

- environment assumptions and VPS limits;
- config values without secrets;
- migration command and result;
- health checks before and after deploy;
- rollback plan;
- what metrics or debug-style endpoints remain internal-only.

Dokku evidence belongs early. k3s evidence belongs later, after the learner can
explain what orchestration adds and what it does not solve.

## Interview Narratives

Prepare concise stories around real repository artifacts:

- "A synchronous report path became painful, so I moved work behind a durable
  job record and Redis/RQ worker."
- "A reporting boundary was studied because the work was stateless derived
  computation, not source-of-truth ownership."
- "The dashboard cache improved one read path, but Postgres and the read model
  remained authoritative."
- "A database outage drill taught me to inspect readiness, logs, and config
  before changing code."
- "The k3s path is useful for orchestration learning, but Dokku remains simpler
  for the first constrained VPS deploy."

Each story should include the failure, the evidence, the tradeoff, the
verification, and the limitation.

## Public Readability

When sharing the repo:

- link to `README.md`, `docs/NAVIGATION.md`, and the relevant role path;
- keep private notes, secrets, real hostnames, and customer-like data out;
- avoid claiming scale, reliability, or production maturity that the evidence
  does not support;
- show review results and remaining gaps plainly.
