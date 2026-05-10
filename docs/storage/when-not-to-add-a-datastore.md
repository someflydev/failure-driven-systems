# When Not To Add A Datastore

## Problem This Paradigm Solves

This document solves a design discipline problem: teams often add datastores
because a technology sounds appropriate, not because the current system has a
measured workload that needs it. OpsLedger should teach refusal as an
architecture skill.

## What OpsLedger Would Gain

By not adding another datastore, OpsLedger keeps fact ownership clear,
deployment small, debugging teachable, failure modes bounded, and rollback
practical. A learner can still reason about document stores, search, analytics,
streams, and vector retrieval without pretending the current repo needs all of
them.

The system can often gain enough from simpler moves:

- a better Postgres query;
- a narrow index;
- a rebuildable read model;
- a short-lived Redis cache;
- an outbox pattern inside Postgres;
- clearer API contracts;
- better logs, metrics, or scenario drills;
- deleting a speculative optimization.

## What OpsLedger Would Pay Operationally

Saying no has a cost: some future feature may need revisiting, and Postgres may
carry work that a specialized store could eventually handle better. The team
must keep measuring instead of treating the initial refusal as permanent
doctrine.

That cost is lower than running a datastore with unclear ownership.

## Failure Modes

- Premature refusal: real search, analytics, queue, or retrieval pressure is
  ignored after evidence appears.
- Premature adoption: a new database adds stale copies and operational burden
  before the workload needs it.
- Ownership ambiguity: two stores claim the same OpsLedger fact.
- Hidden coupling: code cannot run locally or deploy because optional
  infrastructure became mandatory.
- Interview hand-waving: the answer says "scale" without naming dataset,
  access pattern, team, failure modes, and rollback.

## Interview Explanation Prompts

- What evidence would make you add a datastore to OpsLedger?
- What current problem can Postgres solve with less operational cost?
- Which facts become ambiguous if this store is added?
- How would a small team back up, monitor, and restore the new store?
- What is the rollback plan if the datastore is removed?
