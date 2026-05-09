# Phase 2 Quiz

Answer in short paragraphs or bullets. A strong answer should connect the
concept to OpsLedger behavior and name the evidence you would inspect.

## Async Work

1. What pain does the synchronous report route create before the queue is
   introduced?
2. What does `202 Accepted` promise, and what does it deliberately not promise?
3. Why does the result endpoint return `409 report_result_unavailable` before
   `result_json` exists?
4. What status fields help a user or operator tell whether a report is queued,
   running, succeeded, or failed?
5. Why is a stopped worker different from a failed enqueue?

## Retries

1. Why must report retries be bounded?
2. What does `attempt_count` prove, and what does it not prove?
3. Why should the worker persist failure evidence before re-raising the
   exception to RQ?
4. What is risky about saying "just retry it" for code that may perform side
   effects?
5. How would you explain the default retry policy in terms of original attempt,
   retry count, and delay intervals?

## Idempotency And Duplicates

1. What duplicate does the `Idempotency-Key` header prevent?
2. Why is the database unique constraint more important than the application
   existence check?
3. Why should requests without an idempotency key still create new jobs?
4. What duplicate does the completed-output worker guard prevent?
5. Why does notification delivery need a separate idempotency key?

## Redis Versus Postgres

1. Which report job facts belong in Postgres?
2. Which queue coordination facts belong in Redis?
3. If Redis is unavailable, what can the API still do if Postgres is healthy?
4. Why should callers not treat an RQ job id as the durable status handle?
5. What evidence would prove a queue failure versus a worker failure?

## Side Effects And Eventual Consistency

1. Why can a report be succeeded while its notification attempt failed?
2. What crash window remains before a full outbox dispatcher exists?
3. What would a real provider add that the local notification adapter avoids?
4. What should the UI or caller say while a report is accepted but not ready?
5. What scenario evidence would you bring to a review of Phase 2 async work?
