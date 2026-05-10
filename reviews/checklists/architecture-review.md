# Architecture Review Checklist

Use this checklist to review ADRs, decision memos, system design answers, and
architecture proposals for OpsLedger.

## Context

- Names the workload, dataset size, traffic shape, and latency or reliability
  concern.
- Names the team and operator assumption.
- Cites concrete repo artifacts, measurements, incidents, scenarios, docs, or
  code paths.
- States whether the target is local Compose, current Dokku docs, or a future
  deployment shape.

## Decision Quality

- States one clear decision and what is out of scope.
- Compares at least two realistic alternatives.
- Avoids presenting one architecture as universally best.
- Explains why the decision fits the current constraints: small VPS, Dokku,
  Postgres, Redis, worker, stateless reporting service, logs, metrics, and
  measured performance.

## Data Ownership

- Identifies the source of truth for every durable fact.
- Keeps Postgres authoritative unless explicitly justified otherwise.
- Explains what Redis, cache, read models, logs, and metrics can and cannot
  prove.
- Names any staleness, rebuild, idempotency, or consistency risk.

## Operational Cost

- Lists new processes, services, config, secrets, migrations, health checks,
  logs, metrics, alerts, runbooks, and deployment steps.
- Explains how a one-person or small-team operator would debug the change.
- Names local development cost and test coverage impact.
- States the likely cost on a 4 GB RAM, 3 vCPU VPS.

## Failure Modes

- Describes how the decision fails when Postgres, Redis, the worker, the
  reporting service, network calls, or migrations fail.
- Explains what user-visible behavior changes.
- Names the evidence an operator should inspect first.
- Avoids hiding partial failure behind success language.

## Rollback And Reversal

- Gives a realistic rollback or reversal path.
- Separates image/config rollback from database repair.
- Explains whether rollback is safe, lossy, partial, or requires forward
  migration.
- Names the evidence that would trigger reversal later.

## Interview Defense

- Can be defended in two minutes without a diagram.
- Includes tradeoffs without apologizing for constraints.
- Names what would change for a larger team, larger workload, managed cloud
  environment, or stricter reliability target.
- Answers follow-up questions with evidence from OpsLedger instead of generic
  architecture vocabulary.
