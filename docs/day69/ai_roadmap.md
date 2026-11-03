# Zecpath AI System — AI Roadmap

## Current prototype baseline
- Modular resume parsing and normalization components.
- ATS scoring, screening, HR interview, technical interview and machine-test evaluation components.
- Role-weighted cross-round aggregation and explainable recommendation logic.
- Recruiter report formatting, in-process observability/audit utilities and synthetic end-to-end demo.
- Human review required; no autonomous hiring decision.

## Roadmap

### Phase 1 — Reliability and integration
- Define versioned contracts between each module.
- Replace in-memory API stores with a durable database and managed job queue.
- Add authentication, role-based authorization, secure upload validation, malware scanning and retention controls.
- Add integration tests against a deployed staging environment.

### Phase 2 — Evaluation and evidence
- Create a consented, representative, privacy-reviewed evaluation dataset.
- Define task-specific metrics and baselines for parsing, matching and scoring.
- Measure calibration, error rates, subgroup performance and inter-rater agreement.
- Add reviewer override capture and auditability with access controls.
- Keep automated outputs advisory and provide contestability.

### Phase 3 — Responsible AI and monitoring
- Conduct privacy, security, accessibility and legal reviews before pilot use.
- Monitor drift, missing data, latency, failure rates and score distributions.
- Add model/version lineage, alert routing and retention/deletion workflows.
- Validate accommodations and prevent protected attributes or proxies from improperly influencing ranking.

### Phase 4 — Controlled pilot
- Pilot with trained recruiters in shadow mode before any workflow reliance.
- Compare system outputs with independently reviewed evidence.
- Gather stakeholder feedback and document acceptance criteria.
- Expand only after governance approval and measured benefit.

## Proposed future capabilities (not implemented)
- Video interview analytics, emotion inference and candidate coaching are proposals only. Any future behavioral/video feature requires explicit consent, necessity assessment, bias validation, accessibility safeguards and legal review. Do not infer personality, honesty or job suitability from facial expression or gaze.
- Candidate-facing feedback and analytics dashboards require separate product and privacy design.
- Production-grade distributed observability, persistence and asynchronous processing remain future work.
