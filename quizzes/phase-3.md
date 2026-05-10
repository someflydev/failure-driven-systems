# Phase 3 Quiz

Answer in short paragraphs or bullets. A strong answer should connect the
concept to OpsLedger behavior and name the evidence you would inspect.

## Modular Monolith Boundaries

1. What is the difference between an internal module boundary and a deployable
   service boundary in OpsLedger?
2. Which module owns customer identity, and why should reporting not decide
   customer uniqueness?
3. Which module owns work request lifecycle state and status history?
4. Why can report rendering be treated as derived computation?
5. What coupling is acceptable inside one deployable service but risky across
   an HTTP boundary?

## Service Extraction

1. Why was report rendering selected as the one Phase 3 extraction candidate?
2. What costs did the extraction add to local development and operations?
3. Why does "stateless" not mean the service is free to operate?
4. What production evidence would support keeping the reporting service
   extracted?
5. What production evidence would support folding it back into the monolith?

## Contracts And Compatibility

1. What does `contract_version: report-rendering.v1` protect during deploys?
2. Why is adding optional `requested_by` metadata backward-compatible?
3. Why is making an optional field required a breaking change?
4. How should an old worker handle additive response metadata from a newer
   renderer?
5. Which contract change would require a v2 or coordinated migration plan?

## Timeouts And Partial Failure

1. What failure mode appears when rendering changes from a function call to an
   HTTP call?
2. Which timeout bounds the worker's call to the reporting service?
3. Why should timeout, non-2xx response, malformed JSON, and invalid contract
   response be distinguishable?
4. What should the result endpoint return when a report job has not produced
   valid output?
5. Why are broad automatic retries not automatically safe across this boundary?

## Defense

1. Why is "microservices are better" the wrong lesson for Phase 3?
2. How would you explain the extraction decision to an operator who now has one
   more process to monitor?
3. What evidence from Phase 2 shows that async work solved a problem without
   requiring service extraction?
4. What would you include in a short decision memo about whether the extraction
   should stay?
5. How can an LLM help review your boundary decision without writing the
   decision for you?
