# Queues And Streams

## Problem This Paradigm Solves

Queues and streams move work off the request path, buffer producers from
consumers, support retries, and provide a record of asynchronous activity. A
queue usually models work to be processed. A stream usually models an ordered
event log that multiple consumers may read.

## What OpsLedger Would Gain

OpsLedger already gains asynchronous report generation through Redis/RQ. The
API can accept report work quickly while the worker performs slow rendering,
records attempts, and updates durable state in Postgres.

A stronger queue or stream platform could add durable broker-level retention,
consumer groups, replay, fan-out, and operational tooling. That might matter if
OpsLedger had multiple independent consumers for work request events, high
throughput ingestion, or strict replay requirements.

For the current system, Postgres-backed report job state plus Redis/RQ is
enough to teach async reliability without adding Kafka, cloud queues, or an
event streaming platform.

## What OpsLedger Would Pay Operationally

OpsLedger would add broker deployment, partitions or queue topology, consumer
offsets, retention policy, dead-letter handling, replay rules, schema
compatibility, monitoring, and incident response. A small team would also need
to decide what lives in Postgres versus the stream and how to repair
disagreement.

## Failure Modes

- Producer succeeds in Postgres but fails to publish, or publishes before the
  transaction commits.
- Consumer handles a message twice and creates duplicate side effects.
- Poison message blocks progress or loops through retries.
- Consumer lag hides user-visible delay.
- Replay re-runs old business effects that were not designed to be idempotent.
- Stream is mistaken for the source of truth without a clear event ownership
  model.

## Interview Explanation Prompts

- Why did OpsLedger start with Redis/RQ instead of Kafka?
- What durable state makes a queued report inspectable after queue failure?
- How would an outbox change the publish-after-commit problem?
- When does a stream become justified over a simple background job queue?
- What would OpsLedger need before replay was safe?
