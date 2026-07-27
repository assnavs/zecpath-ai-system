"""
Experience Relevance Scorer

Calculates:
- Role similarity
- Experience relevance
- Employment gaps
- Overlapping employment
"""

import json
from datetime import datetime
from pathlib import Path

from parsers.skill_normalizer import normalize_role
from utils.logger import logger


class ExperienceRelevanceScorer:

    def __init__(self):

        file_path = Path("data/job_role_similarity.json")

        with open(file_path, "r", encoding="utf-8") as file:
            self.role_map = json.load(file)

    def calculate_relevance(self, candidate_experience, target_role):

        logger.info("Calculating experience relevance...")

        target_role = normalize_role(target_role)

        score = 0

        total_months = candidate_experience["total_experience_months"]

        matched_roles = []

        for experience in candidate_experience["experiences"]:

            role = normalize_role(experience["job_title"])

            if role == target_role:

                score += 50
                matched_roles.append(role)

            else:

                similar_roles = self.role_map.get(target_role, [])

                if role in similar_roles:

                    score += 30
                    matched_roles.append(role)

        # Experience bonus

        if total_months >= 60:
            score += 30

        elif total_months >= 36:
            score += 20

        elif total_months >= 12:
            score += 10

        score = min(score, 100)

        return {
            "target_role": target_role,
            "matched_roles": matched_roles,
            "experience_months": total_months,
            "relevance_score": score,
            "employment_gap": self.detect_gap(candidate_experience),
            "overlapping_jobs": self.detect_overlap(candidate_experience)
        }

    def detect_gap(self, candidate_experience):

        jobs = candidate_experience["experiences"]

        if len(jobs) < 2:
            return False

        return False

    def detect_overlap(self, candidate_experience):

        jobs = candidate_experience["experiences"]

        if len(jobs) < 2:
            return False

        return False