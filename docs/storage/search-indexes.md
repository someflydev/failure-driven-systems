# Search Indexes

## Problem This Paradigm Solves

Search indexes solve relevance-ranked text search, tokenization, stemming,
faceting, filtering, highlighting, and typo tolerance across large or
text-heavy datasets. They are derived stores optimized for search access
patterns, not general systems of record.

## What OpsLedger Would Gain

OpsLedger could gain better search across work request titles, descriptions,
customer names, status history reasons, or report outputs if users needed
full-text discovery beyond simple filters. A search index could support
operator workflows such as "find all requests mentioning a failed integration"
when Postgres filters or full-text indexes are not enough.

Current OpsLedger does not yet show that pressure. It has bounded lists,
status filters, detail pages, and dashboard summaries. Postgres indexes and
query inspection are the first response.

## What OpsLedger Would Pay Operationally

OpsLedger would add an indexing pipeline, reindexing procedure, schema mapping,
security rules, monitoring, backup or rebuild strategy, and tooling for search
quality. The team would also need to explain why search results can lag
Postgres and which screen must still read source-of-truth rows.

## Failure Modes

- Stale index: search misses a newly created or updated work request.
- Partial indexing: some rows never reach the search store.
- Mapping drift: fields are indexed differently than code expects.
- Relevance regressions: users see plausible but wrong ordering.
- Authorization leak: indexed data is returned to a caller who could not read
  the source row.
- Accidental authority: operators update search results instead of fixing
  Postgres facts.

## Interview Explanation Prompts

- What user workflow would justify search beyond Postgres filters?
- Why is a search index derived state in OpsLedger?
- How would you prove search staleness is acceptable or unacceptable?
- What rebuild path would you require before adding Elasticsearch or a similar
  service?
- When is Postgres full-text search a better first step?
