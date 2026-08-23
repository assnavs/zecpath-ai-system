from pathlib import Path
import json
from typing import Any, Dict, List


class ScreeningScoringEngine:
    """
    Evaluates candidate screening answers using:
    - Clarity
    - Relevance
    - Completeness
    - Consistency

    Scores are provided on a 0-10 scale and normalized
    into a 0-100 screening score.
    """

    def __init__(
        self,
        config_path: str = "data/screening_scoring_configuration.json"
    ):
        self.config_path = Path(config_path)

        with self.config_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            self.configuration = json.load(file)

        self.weights = self.configuration["criteria_weights"]

        self.minimum_score = self.configuration[
            "score_range"
        ]["minimum"]

        self.maximum_score = self.configuration[
            "score_range"
        ]["maximum"]

    def _normalize_score(self, score: float) -> float:
        """Normalize a 0-10 score into a 0-100 score."""

        score = max(
            self.minimum_score,
            min(self.maximum_score, float(score))
        )

        normalized = (
            (score - self.minimum_score)
            / (self.maximum_score - self.minimum_score)
        ) * 100

        return round(normalized, 2)

    def score_question(
        self,
        question_id: str,
        clarity: float,
        relevance: float,
        completeness: float,
        consistency: float
    ) -> Dict[str, Any]:
        """Calculate the score for one screening question."""

        criteria = {
            "clarity": self._normalize_score(clarity),
            "relevance": self._normalize_score(relevance),
            "completeness": self._normalize_score(completeness),
            "consistency": self._normalize_score(consistency)
        }

        weighted_score = (
            criteria["clarity"] * self.weights["clarity"]
            + criteria["relevance"] * self.weights["relevance"]
            + criteria["completeness"] * self.weights["completeness"]
            + criteria["consistency"] * self.weights["consistency"]
        )

        return {
            "question_id": question_id,
            "criteria_scores": criteria,
            "normalized_score": round(weighted_score, 2),
            "score_explanation": {
                "clarity_weight": self.weights["clarity"],
                "relevance_weight": self.weights["relevance"],
                "completeness_weight": self.weights["completeness"],
                "consistency_weight": self.weights["consistency"]
            }
        }

    def calculate_final_score(
        self,
        question_scores: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Aggregate per-question scores into a final screening score."""

        if not question_scores:
            return {
                "total_questions": 0,
                "final_screening_score": 0.0,
                "question_scores": [],
                "explanation": "No screening responses were provided."
            }

        scores = [
            item["normalized_score"]
            for item in question_scores
        ]

        final_score = round(
            sum(scores) / len(scores),
            2
        )

        return {
            "total_questions": len(question_scores),
            "final_screening_score": final_score,
            "question_scores": question_scores,
            "explanation": (
                "Final screening score is the average of "
                "the normalized per-question scores."
            )
        }

    def score_screening(
        self,
        responses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Score multiple screening responses."""

        question_scores = []

        for response in responses:
            result = self.score_question(
                question_id=response["question_id"],
                clarity=response["clarity"],
                relevance=response["relevance"],
                completeness=response["completeness"],
                consistency=response["consistency"]
            )

            question_scores.append(result)

        return self.calculate_final_score(question_scores)
