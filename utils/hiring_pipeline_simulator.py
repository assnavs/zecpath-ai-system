"""Deterministic end-to-end hiring workflow simulator; not a production API."""
from scoring.ats_scoring_engine import ATSScoringEngine
from scoring.screening_scoring_engine import ScreeningScoringEngine
from scoring.hr_interview_scoring_engine import HRInterviewScoringEngine
from scoring.technical_skill_scoring_engine import TechnicalSkillScoringEngine
from interview_ai.machine_test_engine import MachineTestEngine
from scoring.cross_round_aggregation_engine import CrossRoundAggregationEngine
from interview_ai.final_recommendation_engine import FinalRecommendationEngine

class HiringPipelineSimulator:
    REQUIRED = ("candidate", "resume_text", "ats_inputs", "screening_responses",
                "hr_answers", "technical_responses", "machine_submissions")
    def __init__(self):
        self.ats = ATSScoringEngine()
        self.screening = ScreeningScoringEngine()
        self.hr = HRInterviewScoringEngine()
        self.technical = TechnicalSkillScoringEngine()
        self.machine = MachineTestEngine()
        self.aggregate = CrossRoundAggregationEngine()
        self.recommend = FinalRecommendationEngine()

    @staticmethod
    def _score(result, *keys):
        for key in keys:
            value = result.get(key)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return float(value)
        raise ValueError(f"Scoring result did not contain any of: {keys}")

    def run(self, payload, human_judgment=None):
        if not isinstance(payload, dict):
            raise TypeError("payload must be a dictionary")
        missing = [key for key in self.REQUIRED if key not in payload]
        if missing:
            raise ValueError(f"Missing simulation inputs: {', '.join(missing)}")
        candidate = payload["candidate"]
        if not isinstance(candidate, dict) or not candidate.get("candidate_id") or not candidate.get("role"):
            raise ValueError("candidate requires candidate_id and role")
        if not isinstance(payload["resume_text"], str) or not payload["resume_text"].strip():
            raise ValueError("resume_text must be a non-empty string")
        role = candidate["role"]
        stages = [{"stage":"resume_upload","status":"simulated_input_received",
                   "resume_character_count":len(payload["resume_text"])}]
        ats_result = self.ats.calculate_score(role, **payload["ats_inputs"])
        stages.append({"stage":"ats_scoring","status":"completed","score":ats_result["overall_score"]})
        screening_result = self.screening.score_screening(payload["screening_responses"])
        screening_score = self._score(screening_result, "final_screening_score")
        stages.append({"stage":"screening","status":"completed","score":screening_score})
        hr_result = self.hr.score_interview(payload["hr_answers"])
        hr_score = self._score(hr_result, "interview_score")
        stages.append({"stage":"hr_interview","status":"completed","score":hr_score})
        technical_result = self.technical.score_interview(payload["technical_responses"])
        technical_score = self._score(technical_result, "technical_score")
        stages.append({"stage":"technical_interview","status":"completed","score":technical_score})
        machine_result = self.machine.evaluate_session(payload["machine_submissions"])
        machine_score = self._score(machine_result, "overall_score")
        stages.append({"stage":"machine_test","status":"completed","score":machine_score})
        round_scores = {"ats":ats_result["overall_score"],"screening":screening_score,
                        "hr_interview":hr_score,"technical_interview":technical_score,
                        "machine_test":machine_score}
        aggregate = self.aggregate.aggregate(role, round_scores, candidate["candidate_id"])
        recommendation = self.recommend.recommend(aggregate)
        stages.append({"stage":"final_decision","status":"recommendation_generated",
                       "recommendation":recommendation["recommendation"]})
        comparison = None
        if human_judgment is not None:
            if not isinstance(human_judgment, dict) or human_judgment.get("recommendation") not in {
                "Selected","Hold / Review","Rejected"}:
                raise ValueError("human_judgment must contain a supported recommendation")
            comparison = {"ai_recommendation":recommendation["recommendation"],
                          "human_recommendation":human_judgment["recommendation"],
                          "agreement":recommendation["recommendation"] == human_judgment["recommendation"],
                          "note":"One simulated comparison is not a validated measure of model accuracy."}
        return {"candidate":candidate,"stages":stages,"round_scores":round_scores,
                "aggregation":aggregate,"recommendation":recommendation,
                "human_comparison":comparison,
                "simulation_scope":"Deterministic test workflow using supplied structured inputs; resume extraction/upload transport is not exercised.",
                "human_review_required":True}
