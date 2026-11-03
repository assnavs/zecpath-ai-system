# Day 59 – API & Integration Planning

## Objective
Define module boundaries, request/response contracts, processing modes, security and error handling.

## API inventory
Resume parsing, ATS scoring, screening AI, interview AI and decision AI. Resume processing is asynchronous; real-time interview scoring is synchronous, as specified in the task brief.

## Integration flow
Backend authenticates the caller, validates a versioned request, persists an application/job reference, invokes the relevant AI service, stores the result and returns either a synchronous result or an asynchronous job reference. Do not pass raw transcripts or resume contents into application logs.

## Reliability
Use correlation IDs, idempotency keys for resume jobs, bounded retries with exponential backoff and jitter for transient failures, dead-letter handling after retry exhaustion, explicit timeouts and stable error codes. Do not retry validation or authorization failures.

## Security
TLS in transit, service-to-service authentication, least-privilege authorization, secret management, encrypted storage, retention/deletion enforcement and audit events. The schemas in this folder are design contracts, not deployed endpoints.
