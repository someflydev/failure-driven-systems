# Phase 4 Quiz

Answer in short paragraphs or bullets. A strong answer should connect the
concept to OpsLedger behavior and name the evidence you would inspect.

## Logs And Correlation IDs

1. What is the difference between a request ID and a correlation ID in
   OpsLedger?
2. Why should a report job persist its `correlation_id`?
3. What claim is unsafe to make from unfiltered logs when several report jobs
   run close together?
4. Which log fields help connect API, worker, and reporting service behavior?
5. Which data should not be copied into logs, incident notes, or LLM prompts?

## Metrics

1. What question do metrics answer better than individual log lines?
2. Why are raw report job IDs, customer IDs, request IDs, or correlation IDs bad
   metric labels?
3. How can a report job fail while the original enqueue request still returns
   `202 Accepted`?
4. Which metric or status evidence would you inspect during a reporting latency
   incident?
5. What evidence survives a worker restart, and what evidence may reset?

## Health Checks And Durable State

1. Why can `/health/ready` stay green during a reporting timeout incident?
2. What does `/reports/jobs/{id}` prove that `/metrics` cannot prove?
3. Why does `queued` not prove a worker is healthy?
4. What should `/reports/jobs/{id}/result` return before report output exists?
5. How would you distinguish a stopped worker from a failed reporting service?

## Incident Response

1. What belongs in a first status update before root cause is confirmed?
2. Why should status updates name user impact instead of only component
   behavior?
3. What is one reasonable next check during the worker-stalled scenario?
4. What evidence should support a resolved status update?
5. Why should incident notes include one discarded hypothesis?

## Postmortem Quality

1. What makes a postmortem timeline evidence-based?
2. Why is "worker issue" usually too vague as a root cause?
3. How should action items connect to incident evidence?
4. What makes a dashboard or error counter misleading in the noisy nonfatal
   errors scenario?
5. How can an LLM critique a postmortem without writing the postmortem for the
   learner?
