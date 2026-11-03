# Day 56 – Full System Simulation

## Objective
Exercise the hiring workflow from structured resume input through ATS, screening, HR interview, technical interview, machine test, aggregation and recommendation.

## Implementation
The simulator uses existing scoring modules and deterministic structured fixtures. It records each stage, the five round scores, the unified recommendation and an optional comparison with a supplied human recommendation.

## Scope boundary
The resume text is accepted as a simulated upload input. This test does not exercise a real file-upload transport, OCR or document extraction. Human comparison is descriptive; one fixture cannot establish model accuracy or replace expert review.
