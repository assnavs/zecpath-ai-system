# Day 43 ? AI Ethics Documentation

## Purpose and scope
ZecPath AI supports resume screening and HR interview evaluation. Its scores are decision-support signals, not proof of candidate quality and not an automatic hiring decision.

## Candidate consent and notice
Before collecting or processing candidate data, the organization operating the system should provide a clear notice that explains:
- What resume, interview, transcript, and other candidate information is collected.
- Why each category of information is needed and how it is evaluated.
- Which scoring components may be automated and how results affect human review.
- Who can access the information, whether it is shared with third parties, and how long it is retained.
- How candidates can ask questions, request correction or deletion where applicable, and contact the responsible organization.
- The lawful basis or other applicable authorization for processing, including any consent that is required.

Consent must not be described as implemented by this repository: no explicit consent-capture workflow was identified in the inspected source files. The product owner must determine applicable legal requirements and implement appropriate notices, records, and withdrawal handling where required.

## Fairness and minimization
The fairness configuration masks specified personal attributes during structured resume normalization. The Day 43 update expands that list to include additional demographic and personal attributes. Masking applies to matching input keys; it does not guarantee removal of indirect identifiers, information embedded in free text, or proxies in other fields.

Use job-related, validated criteria. Review whether education, employment history, communication, confidence, keyword matching, or other signals could disadvantage candidates for reasons unrelated to the role. Do not infer protected traits or use them as proxies for suitability.

## Explainability
Candidate-facing or reviewer-facing explanations should identify the score components, configured weights or caps where relevant, missing data, limitations, and reasons a human review is needed. The ATS engine exposes a score breakdown and recommendation; the unified scoring engine includes a note that scores support human review rather than automatic hiring decisions.

A score breakdown improves transparency but does not, by itself, establish that a score is valid, accurate, or fair.

## Human oversight and contestability
A qualified reviewer should verify evidence, examine missing or inconsistent information, and be able to question or override an automated recommendation. High-impact decisions should not rely solely on a numeric score without a documented, job-related review process.

## Monitoring
Periodically evaluate false-positive and false-negative outcomes, selection rates, and score distributions using an appropriately governed and representative evaluation dataset. Any demographic analysis must have a lawful purpose, suitable safeguards, and restricted access. Document limitations when sample sizes or labels are inadequate.

## Current implementation status
- Implemented: configured structured-field masking and rule-based fairness indicators.
- Implemented: keyword score cap in the fairness-oriented evaluation output.
- Implemented: score breakdowns in relevant scoring outputs.
- Not identified in inspected code: explicit candidate consent capture and consent withdrawal workflow.
- Not identified in inspected code: a defined retention schedule and automated deletion process.
- Not demonstrated: measured fairness parity or absence of disparate impact across demographic groups.

## Review owner
The project owner and qualified privacy/legal reviewer should confirm operational requirements before production use.
