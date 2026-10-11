# Day 43 ? Fairness Review Notes

## Scope
Review of `scoring/fair_scoring_engine.py`, `parsers/resume_normalizer.py`, `data/fairness_configuration.json`, the ATS scoring output, and the unified scoring output.

## Existing controls
- Resume normalization standardizes text and collections.
- Configured personal attributes are replaced with `[MASKED]` when their normalized top-level keys match the configuration.
- Keyword-based score contribution is capped at 85 by the existing fairness configuration.
- Rule-based indicators can flag high keyword dependency, low semantic contribution, and unmasked configured attributes.
- ATS output includes component score breakdowns.
- Unified scoring output warns that the score supports candidate review and is not an automatic hiring decision.

## Day 43 configuration update
The masking list was extended with `race`, `ethnicity`, `age`, `disability`, `sexual_orientation`, `gender_identity`, `pronouns`, `place_of_birth`, and `postal_code`. Existing attributes and scoring settings were retained.

## Limitations and risks
1. Masking is key-based and primarily applies to structured resume fields. It does not detect every spelling, alias, nested field, or sensitive detail in free text.
2. The normalizer's configured masking check does not establish that every upstream or downstream component uses the normalized resume.
3. Keyword caps and semantic-weight thresholds are heuristic controls, not empirical evidence of fairness.
4. The current rule-based `requires_review` flag checks a limited set of conditions; no flag does not mean no bias exists.
5. Communication and confidence signals may be affected by language proficiency, disability, accent, recording quality, or cultural differences. Their job-related validity needs evaluation.
6. No labeled, representative demographic evaluation dataset or disparate-impact analysis was provided for this review.

## Recommended validation
- Test all configured masking keys with varied casing and whitespace.
- Test nested and free-text cases to identify masking limitations.
- Confirm that downstream scoring receives the intended normalized representation.
- Compare relevant error rates and selection outcomes across appropriately governed groups when lawful and statistically meaningful.
- Have qualified reviewers assess whether each feature is necessary for the job and whether less discriminatory alternatives exist.
- Record dataset provenance, evaluation dates, sample sizes, confidence intervals, and known limitations.

## Conclusion
The repository contains useful preliminary fairness controls. They reduce some identifiable risks but do not prove that hiring outcomes are unbiased. Production readiness requires end-to-end data-flow verification and empirical evaluation.
