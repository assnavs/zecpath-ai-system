import json
from pathlib import Path

from utils.logger import logger


class ATSScoringEngine:
    """
    ATS Scoring Engine

    Calculates an overall ATS score based on:
    - Skill Match
    - Experience Relevance
    - Education Alignment
    - Semantic Similarity

    Supports dynamic weight configuration based on job roles
    and provides an explainable score breakdown.
    """

    def __init__(self):
        logger.info("Initializing ATS Scoring Engine...")

        config_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "ats_weight_configuration.json"
        )

        with open(config_path, "r", encoding="utf-8") as file:
            self.role_weights = json.load(file)

    def calculate_score(
        self,
        job_role,
        skill_match=None,
        experience_relevance=None,
        education_alignment=None,
        semantic_similarity=None,
    ):
        """
        Calculate overall ATS score for a specific job role.

        Missing values are treated as zero.
        """

        skill_match = skill_match or 0
        experience_relevance = experience_relevance or 0
        education_alignment = education_alignment or 0
        semantic_similarity = semantic_similarity or 0

        weights = self.role_weights.get(job_role)

        if weights is None:
            raise ValueError(f"Unsupported job role: {job_role}")

        overall_score = (
            skill_match * weights["skill_match"]
            + experience_relevance * weights["experience_relevance"]
            + education_alignment * weights["education_alignment"]
            + semantic_similarity * weights["semantic_similarity"]
        )

        overall_score = round(float(overall_score), 2)

        result = {
            "job_role": job_role,
            "overall_score": overall_score,
            "recommendation": self.generate_recommendation(overall_score),
            "score_breakdown": {
                "skill_match": skill_match,
                "experience_relevance": experience_relevance,
                "education_alignment": education_alignment,
                "semantic_similarity": semantic_similarity,
            },
        }

        logger.info(
            f"ATS Score Generated for {job_role}: {overall_score}"
        )

        return result

    def generate_recommendation(self, score):
        """
        Generate recommendation based on ATS score.
        """

        if score >= 90:
            return "Excellent Candidate"

        if score >= 80:
            return "Strong Candidate"

        if score >= 70:
            return "Good Candidate"

        if score >= 60:
            return "Average Candidate"

        return "Needs Improvement"