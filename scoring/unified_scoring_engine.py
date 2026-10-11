import json
import math
from pathlib import Path
from typing import Any, Dict, Optional


class UnifiedScoringEngine:
    """Combine ATS, screening and HR interview scores."""

    CONFIG_PATH = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "unified_scoring_configuration.json"
    )

    ROUND_NAMES = ("ats", "screening", "hr_interview")

    def __init__(self, config_path: Optional[str] = None):
        path = Path(config_path) if config_path else self.CONFIG_PATH

        with path.open("r", encoding="utf-8-sig") as file:
            self.config = json.load(file)

        self._validate_configuration()

    def _validate_weights(self, weights: Dict[str, Any]) -> None:
        if not isinstance(weights, dict):
            raise ValueError("Weights must be a dictionary.")

        if set(weights) != set(self.ROUND_NAMES):
            raise ValueError(
                "Weights must define ats, screening and hr_interview."
            )

        values = list(weights.values())

        for value in values:
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or value <= 0
            ):
                raise ValueError(
                    "Weights must be finite, positive numbers."
                )

        if not math.isclose(sum(values), 1.0, abs_tol=1e-6):
            raise ValueError("Weights must sum to 1.0.")

    def _validate_configuration(self) -> None:
        score_range = self.config.get("score_range", {})
        minimum = score_range.get("minimum")
        maximum = score_range.get("maximum")

        if (
            isinstance(minimum, bool)
            or isinstance(maximum, bool)
            or not isinstance(minimum, (int, float))
            or not isinstance(maximum, (int, float))
            or not math.isfinite(minimum)
            or not math.isfinite(maximum)
            or minimum >= maximum
        ):
            raise ValueError("Invalid score range configuration.")

        self.minimum_score = float(minimum)
        self.maximum_score = float(maximum)

        if self.config.get("missing_score_policy") != (
            "renormalize_available_weights"
        ):
            raise ValueError("Unsupported missing score policy.")

        self._validate_weights(self.config.get("default_weights"))

        role_weights = self.config.get("role_weights")

        if not isinstance(role_weights, dict) or not role_weights:
            raise ValueError("Role weights must be a non-empty dictionary.")

        for weights in role_weights.values():
            self._validate_weights(weights)

        thresholds = self.config.get("thresholds", {})
        required = ("excellent", "good", "moderate")

        if any(key not in thresholds for key in required):
            raise ValueError("Missing classification thresholds.")

        values = [thresholds[key] for key in required]

        if (
            any(
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or not self.minimum_score <= value <= self.maximum_score
                for value in values
            )
            or not values[0] > values[1] > values[2]
        ):
            raise ValueError("Invalid classification thresholds.")

    def _validate_score(self, name: str, value: Any) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{name} score must be a number.")

        if not math.isfinite(value):
            raise ValueError(f"{name} score must be finite.")

        if not self.minimum_score <= value <= self.maximum_score:
            raise ValueError(
                f"{name} score must be between "
                f"{self.minimum_score} and {self.maximum_score}."
            )

        return float(value)

    def _classify(self, score: float) -> str:
        thresholds = self.config["thresholds"]

        if score >= thresholds["excellent"]:
            return "excellent"
        if score >= thresholds["good"]:
            return "good"
        if score >= thresholds["moderate"]:
            return "moderate"
        return "needs_improvement"

    def calculate_unified_score(
        self,
        candidate_id: str,
        job_role: str,
        ats_score: Optional[float] = None,
        screening_score: Optional[float] = None,
        hr_interview_score: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Calculate a unified score from available round scores."""

        if not isinstance(candidate_id, str) or not candidate_id.strip():
            raise ValueError("candidate_id must be a non-empty string.")

        if not isinstance(job_role, str) or not job_role.strip():
            raise ValueError("job_role must be a non-empty string.")

        role_weights = self.config["role_weights"].get(job_role)

        if role_weights is None:
            raise ValueError(f"Unsupported job role: {job_role}")

        supplied_scores = {
            "ats": ats_score,
            "screening": screening_score,
            "hr_interview": hr_interview_score,
        }

        scores = {}
        missing_rounds = []

        for round_name, value in supplied_scores.items():
            if value is None:
                missing_rounds.append(round_name)
            else:
                scores[round_name] = self._validate_score(
                    round_name, value
                )

        if not scores:
            raise ValueError("At least one round score is required.")

        available_weight = sum(
            role_weights[name] for name in scores
        )

        if available_weight <= 0:
            raise ValueError(
                "Available rounds must have a positive combined weight."
            )

        applied_weights = {
            name: round(role_weights[name] / available_weight, 6)
            for name in scores
        }

        # Calculate using unrounded weights to minimize rounding drift.
        unified_score = sum(
            scores[name] * role_weights[name] / available_weight
            for name in scores
        )

        unified_score = round(
            max(
                self.minimum_score,
                min(self.maximum_score, unified_score),
            ),
            2,
        )

        return {
            "candidate_id": candidate_id.strip(),
            "job_role": job_role.strip(),
            "round_scores": scores,
            "missing_rounds": missing_rounds,
            "configured_role_weights": dict(role_weights),
            "applied_weights": applied_weights,
            "unified_score": unified_score,
            "hiring_fit_percentage": unified_score,
            "classification": self._classify(unified_score),
            "score_range": {
                "minimum": self.minimum_score,
                "maximum": self.maximum_score,
            },
            "weighting_note": (
                "Available round weights are renormalized when a round "
                "score is missing. Review missing rounds before comparing "
                "candidates."
                if missing_rounds
                else "All configured evaluation rounds were included."
            ),
            "decision_note": (
                "This score supports candidate review; it is not an "
                "automatic hiring decision."
            ),
        }
