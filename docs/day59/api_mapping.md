# Day 59 – API Mapping

```mermaid
flowchart TD
  B[Backend / Auth Gateway] --> RP[Resume Parsing API]
  RP --> Q[(Async Job Queue)]
  Q --> ATS[ATS Scoring API]
  ATS --> DB[(Candidate / Evaluation Database)]
  B --> S[Screening AI API]
  B --> I[Interview AI API]
  I -->|Sync response| B
  S --> DB
  ATS --> DB
  DB --> D[Decision AI API]
  D --> B
  D --> DB
```

**Modes:** resume processing is asynchronous; real-time interview scoring is synchronous.

**Contracts:** see `schemas/resume_parse_request.schema.json`, `schemas/ats_score_request.schema.json`, and `schemas/decision_response.schema.json`.

**Security:** authenticate every service call; authorize by role and purpose; use correlation IDs; avoid logging raw resumes/transcripts; encrypt data in transit and at rest.
