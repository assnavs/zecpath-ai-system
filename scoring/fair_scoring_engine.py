"""
Fair Scoring Engine

Provides fairness-oriented controls for candidate scoring.

Features:
- Score normalization
- Keyword dependency control
- Personal attribute masking
- Bias indicator evaluation
- Explainable structured output
"""

import json
from pathlib import Path

from parsers.resume_normalizer import ResumeNormalizer
from utils.logger import logger


class FairScoringEngine:
    """
    Applies normalization and fairness-oriented controls
    before candidate scores are used for ranking.
    """

    def __init__(self):

        logger.info("Initializing Fair Scoring Engine...")

        config_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "fairness_configuration.json"
        )

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

        score_range = self.config.get("score_range", {})

        self.minimum_score = score_range.get(
            "minimum",
            0
        )

        self.maximum_score = score_range.get(
            "maximum",
            100
        )

        self.keyword_score_cap = self.config.get(
            "keyword_score_cap",
            85
        )

        bias_thresholds = self.config.get(
            "bias_thresholds",
            {}
        )

        self.high_keyword_dependency = bias_thresholds.get(
            "high_keyword_dependency",
            0.60
        )

        self.low_semantic_contribution = bias_thresholds.get(
            "low_semantic_contribution",
            0.15
        )

        self.resume_normalizer = ResumeNormalizer(
            self.config.get(
                "personal_attributes_to_mask",
                []
            )
        )

    def normalize_score(
        self,
        score,
        source_min=0,
        source_max=100
    ):
        """
        Normalize a score to the configured ATS range.

        Uses min-max normalization.
        """

        if score is None:
            score = 0

        try:
            score = float(score)
            source_min = float(source_min)
            source_max = float(source_max)

        except (TypeError, ValueError):

            logger.warning(
                "Invalid score supplied. Using 0."
            )

            score = 0
            source_min = 0
            source_max = 100

        if source_max <= source_min:
            raise ValueError(
                "source_max must be greater than source_min."
            )

        score = max(
            source_min,
            min(score, source_max)
        )

        normalized = (
            (score - source_min)
            / (source_max - source_min)
        )

        normalized = (
            self.minimum_score
            + normalized
            * (self.maximum_score - self.minimum_score)
        )

        return round(float(normalized), 2)

    def limit_keyword_dependency(self, keyword_score):
        """
        Prevent keyword matching from dominating evaluation.

        A configurable cap is applied to the keyword-based
        component while other contextual evaluation signals
        remain available to the scoring system.
        """

        keyword_score = self.normalize_score(
            keyword_score
        )

        adjusted_score = min(
            keyword_score,
            self.keyword_score_cap
        )

        return round(float(adjusted_score), 2)

    def evaluate_bias_indicators(
        self,
        scoring_weights,
        personal_attributes_masked
    ):
        """
        Evaluate transparent rule-based bias indicators.

        These indicators do not claim to prove that the
        system is bias-free. They identify configurations
        that may deserve additional review.
        """

        scoring_weights = scoring_weights or {}

        keyword_weight = float(
            scoring_weights.get(
                "keyword_match",
                scoring_weights.get(
                    "skill_match",
                    0
                )
            )
        )

        semantic_weight = float(
            scoring_weights.get(
                "semantic_similarity",
                0
            )
        )

        flags = []

        if keyword_weight > self.high_keyword_dependency:

            flags.append(
                "High keyword dependency detected."
            )

        if semantic_weight < self.low_semantic_contribution:

            flags.append(
                "Low semantic contribution detected."
            )

        if not personal_attributes_masked:

            flags.append(
                "Personal attributes are not fully masked."
            )

        return {
            "personal_attributes_masked":
                personal_attributes_masked,

            "keyword_dependency_reduced":
                keyword_weight
                <= self.high_keyword_dependency,

            "semantic_contribution_sufficient":
                semantic_weight
                >= self.low_semantic_contribution,

            "bias_flags": flags,

            "requires_review": len(flags) > 0
        }

    def evaluate_candidate(
        self,
        resume,
        scores,
        scoring_weights=None
    ):
        """
        Normalize resume information and candidate scores,
        then generate fairness indicators.
        """

        logger.info(
            "Starting fairness-oriented candidate evaluation..."
        )

        normalized_resume = (
            self.resume_normalizer.normalize_resume(
                resume
            )
        )

        scores = scores or {}

        keyword_score = scores.get(
            "keyword_match",
            scores.get(
                "skill_match",
                0
            )
        )

        experience_score = scores.get(
            "experience_relevance",
            0
        )

        education_score = scores.get(
            "education_alignment",
            0
        )

        semantic_score = scores.get(
            "semantic_similarity",
            0
        )

        normalized_scores = {
            "keyword_match":
                self.limit_keyword_dependency(
                    keyword_score
                ),

            "experience_relevance":
                self.normalize_score(
                    experience_score
                ),

            "education_alignment":
                self.normalize_score(
                    education_score
                ),

            "semantic_similarity":
                self.normalize_score(
                    semantic_score
                )
        }

        masked_attributes = (
            self.config.get(
                "personal_attributes_to_mask",
                []
            )
        )

        personal_attributes_masked = all(
            normalized_resume.get(attribute)
            in (None, self.resume_normalizer.MASK_VALUE)
            for attribute in masked_attributes
        )

        bias_indicators = (
            self.evaluate_bias_indicators(
                scoring_weights or {},
                personal_attributes_masked
            )
        )

        logger.info(
            "Fairness-oriented candidate evaluation completed."
        )

        return {
            "normalized_resume": normalized_resume,
            "normalized_scores": normalized_scores,
            "fairness_controls": {
                "score_normalized": True,
                "keyword_score_cap":
                    self.keyword_score_cap,
                "personal_attributes_masked":
                    personal_attributes_masked
            },
            "bias_indicators": bias_indicators
        }