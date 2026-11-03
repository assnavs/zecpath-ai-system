# Day 60 – Performance Tuning & Scalability

## Objective
Establish measurable performance practices and a horizontal scaling design.

## Included utilities
A bounded TTL cache, ordered batch processor and local callable benchmark helper. The benchmark reports mean, median, p95, minimum and maximum latency.

## Scaling strategy
Place stateless API workers behind a load balancer; move resume parsing to a durable queue and independently scale worker pools; keep real-time interview requests on a latency-monitored synchronous path; externalize cache and job state for multi-instance deployments; use object storage for documents and a database for metadata.

## Load-test plan
Measure p50/p95/p99 latency, throughput, error rate, queue wait, CPU, memory and cache hit rate at increasing concurrency. Test cold/warm cache, batch sizes, large resumes, dependency timeouts and retry storms.

## Limitation
No production traffic, model endpoint, distributed cache, queue or load environment was available in this batch. Do not present local microbenchmark numbers as production performance improvements.
