# Vector Storage

## Problem This Paradigm Solves

Vector storage solves similarity search over embeddings: finding semantically
similar text, tickets, documents, images, or knowledge chunks. It helps when
exact filters and keyword search cannot express the retrieval task.

## What OpsLedger Would Gain

OpsLedger could eventually use vector search for support-style retrieval such
as finding similar incidents, related work request descriptions, or relevant
postmortem fragments. That would be a retrieval feature, not a replacement for
the source-of-truth database.

Today, OpsLedger has no implemented embedding pipeline, retrieval workflow,
model evaluation, privacy policy, or user-facing similarity feature. Adding a
vector database now would create architecture before evidence.

## What OpsLedger Would Pay Operationally

OpsLedger would need embedding generation, chunking rules, model versioning,
index rebuilds, metadata filters, access control, evaluation data, drift
monitoring, and fallback behavior when retrieval is poor or unavailable. The
team would also need to protect sensitive customer and work request text before
sending it to any embedding model.

## Failure Modes

- Stale embeddings: updated work request text is not reflected in retrieval.
- Bad matches: plausible but irrelevant records are returned.
- Missing authorization filter: retrieval exposes text a caller should not see.
- Model drift: new embeddings are incompatible with old indexed vectors.
- Silent dependency: a workflow starts relying on approximate retrieval for
  correctness.
- Cost and latency surprise: embedding and search calls exceed the value of the
  feature.

## Interview Explanation Prompts

- What OpsLedger feature would vector search actually support?
- Why is vector storage not a source of truth?
- How would you evaluate whether similar-work-request retrieval is good enough?
- What metadata filters are required before retrieval is safe?
- When would Postgres plus ordinary search be enough?
