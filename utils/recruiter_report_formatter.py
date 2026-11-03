"""Presentation-only recruiter report formatter; does not alter scores or decisions."""
from datetime import datetime, timezone

class RecruiterReportFormatter:
    REQUIRED_ROUNDS = ("ats", "screening", "hr_interview", "technical_interview", "machine_test")

    @staticmethod
    def _valid_score(value, field):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 100:
            raise ValueError(f"{field} must be between 0 and 100")
        return round(float(value), 2)

    def format(self, pipeline_result):
        if not isinstance(pipeline_result, dict):
            raise TypeError("pipeline_result must be a dictionary")
        candidate = pipeline_result.get("candidate")
        if not isinstance(candidate, dict) or not candidate.get("candidate_id") or not candidate.get("role"):
            raise ValueError("candidate_id and role are required")
        scores = pipeline_result.get("round_scores")
        if not isinstance(scores, dict):
            raise ValueError("round_scores must be a dictionary")
        missing = [name for name in self.REQUIRED_ROUNDS if name not in scores]
        if missing:
            raise ValueError(f"Missing round scores: {', '.join(missing)}")
        clean_scores = {name: self._valid_score(scores[name], name) for name in self.REQUIRED_ROUNDS}
        recommendation = pipeline_result.get("recommendation")
        if not isinstance(recommendation, dict) or not recommendation.get("recommendation"):
            raise ValueError("recommendation details are required")
        return {
            "report_version": "1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "candidate": {"candidate_id": str(candidate["candidate_id"]), "role": str(candidate["role"])},
            "round_scores": clean_scores,
            "hiring_fit_score": self._valid_score(
                pipeline_result.get("aggregation", {}).get("hiring_fit_score"), "hiring_fit_score"
            ),
            "recommendation": recommendation["recommendation"],
            "explanation": list(recommendation.get("explanation", [])),
            "coverage_percent": self._valid_score(
                pipeline_result.get("aggregation", {}).get("coverage_percent"), "coverage_percent"
            ),
            "limitations": [
                "Scores are rule-based or rubric-based indicators, not objective measures of candidate worth.",
                "This report is decision support only; an authorized human reviewer must make the hiring decision.",
                "Review source evidence and accommodations before interpreting automated scores."
            ],
            "human_review_required": True,
        }
