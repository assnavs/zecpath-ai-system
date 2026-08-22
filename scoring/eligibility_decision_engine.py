"""
Day 21 - Eligibility Decision Engine

Determines whether a candidate is:
    ELIGIBLE
    REVIEW
    REJECTED

The engine uses:
- ATS score
- Mandatory skills
- Experience range
- Location constraints
- Availability constraints

Rules are loaded from:
data/eligibility_rules.json
"""

import json
from pathlib import Path


class EligibilityDecisionEngine:
    """
    Rule-based + score-based candidate eligibility engine.
    """

    def __init__(self, config_path=None):

        if config_path is None:
            config_path = (
                Path(__file__).resolve().parent.parent
                / "data"
                / "eligibility_rules.json"
            )

        self.config_path = Path(config_path)

        with open(
            self.config_path,
            "r",
            encoding="utf-8-sig"
        ) as file:
            self.rules = json.load(file)

    # --------------------------------------------
    # Utility methods
    # --------------------------------------------

    @staticmethod
    def _normalize(value):
        if value is None:
            return ""

        return str(value).strip().lower()

    @classmethod
    def _normalize_skills(cls, skills):
        if not skills:
            return set()

        return {
            cls._normalize(skill)
            for skill in skills
            if skill
        }

    # --------------------------------------------
    # Mandatory skill validation
    # --------------------------------------------

    def _check_mandatory_skills(
        self,
        candidate_skills,
        mandatory_skills
    ):

        candidate_set = self._normalize_skills(
            candidate_skills
        )

        required_set = self._normalize_skills(
            mandatory_skills
        )

        matched = candidate_set.intersection(
            required_set
        )

        missing = required_set - candidate_set

        return {
            "passed": len(missing) == 0,
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing)
        }

    # --------------------------------------------
    # Experience validation
    # --------------------------------------------

    def _check_experience(
        self,
        experience_years,
        experience_range
    ):

        minimum = experience_range.get(
            "minimum_years",
            0
        )

        maximum = experience_range.get(
            "maximum_years",
            float("inf")
        )

        try:
            years = float(
                experience_years
                if experience_years is not None
                else 0
            )
        except (TypeError, ValueError):
            years = 0

        passed = (
            minimum <= years <= maximum
        )

        return {
            "passed": passed,
            "candidate_years": years,
            "minimum_years": minimum,
            "maximum_years": (
                None
                if maximum == float("inf")
                else maximum
            )
        }

    # --------------------------------------------
    # Location validation
    # --------------------------------------------

    def _check_location(
        self,
        candidate_location,
        allowed_locations
    ):

        # Empty configuration means no restriction
        if not allowed_locations:
            return {
                "passed": True,
                "candidate_location": candidate_location,
                "allowed_locations": []
            }

        candidate = self._normalize(
            candidate_location
        )

        allowed = {
            self._normalize(location)
            for location in allowed_locations
        }

        return {
            "passed": candidate in allowed,
            "candidate_location": candidate_location,
            "allowed_locations": sorted(allowed)
        }

    # --------------------------------------------
    # Availability validation
    # --------------------------------------------

    def _check_availability(
        self,
        candidate_availability,
        allowed_availability
    ):

        # Empty configuration means no restriction
        if not allowed_availability:
            return {
                "passed": True,
                "candidate_availability": (
                    candidate_availability
                ),
                "allowed_availability": []
            }

        candidate = self._normalize(
            candidate_availability
        )

        allowed = {
            self._normalize(value)
            for value in allowed_availability
        }

        return {
            "passed": candidate in allowed,
            "candidate_availability": (
                candidate_availability
            ),
            "allowed_availability": sorted(allowed)
        }

    # --------------------------------------------
    # Main decision method
    # --------------------------------------------

    def evaluate_candidate(
        self,
        job_role,
        ats_result,
        candidate_data=None
    ):

        candidate_data = candidate_data or {}

        if job_role not in self.rules:
            raise ValueError(
                f"Unsupported job role: {job_role}"
            )

        if not isinstance(ats_result, dict):
            raise TypeError(
                "ats_result must be a dictionary"
            )

        rules = self.rules[job_role]

        # ----------------------------------------
        # Extract ATS score
        # ----------------------------------------

        ats_score = ats_result.get(
            "overall_score"
        )

        if ats_score is None:

            # Also support nested ATS API response
            data = ats_result.get(
                "data",
                {}
            )

            if isinstance(data, dict):
                ats_score = data.get(
                    "overall_score"
                )

        try:
            ats_score = float(
                ats_score
                if ats_score is not None
                else 0
            )
        except (TypeError, ValueError):
            ats_score = 0.0

        # ----------------------------------------
        # Validate individual rules
        # ----------------------------------------

        skill_result = (
            self._check_mandatory_skills(
                candidate_data.get("skills", []),
                rules.get(
                    "mandatory_skills",
                    []
                )
            )
        )

        experience_result = (
            self._check_experience(
                candidate_data.get(
                    "experience_years",
                    0
                ),
                rules.get(
                    "experience_range",
                    {}
                )
            )
        )

        location_result = (
            self._check_location(
                candidate_data.get(
                    "location"
                ),
                rules.get(
                    "location_constraints",
                    []
                )
            )
        )

        availability_result = (
            self._check_availability(
                candidate_data.get(
                    "availability"
                ),
                rules.get(
                    "availability_constraints",
                    []
                )
            )
        )

        # ----------------------------------------
        # Rule evaluation
        # ----------------------------------------

        minimum_score = float(
            rules.get(
                "minimum_ats_score",
                70
            )
        )

        review_score = float(
            rules.get(
                "review_minimum_score",
                55
            )
        )

        all_rules_pass = all(
            [
                skill_result["passed"],
                experience_result["passed"],
                location_result["passed"],
                availability_result["passed"]
            ]
        )

        # ----------------------------------------
        # Final decision
        # ----------------------------------------

        if (
            ats_score >= minimum_score
            and all_rules_pass
        ):
            decision = "ELIGIBLE"

        elif ats_score >= review_score:
            decision = "REVIEW"

        else:
            decision = "REJECTED"

        # ----------------------------------------
        # Result structure
        # ----------------------------------------

        result = {
            "success": True,
            "job_role": job_role,
            "candidate_id": candidate_data.get(
                "candidate_id"
            ),
            "candidate_name": candidate_data.get(
                "name"
            ),
            "eligibility": decision,
            "ats_score": round(
                ats_score,
                2
            ),
            "rules": {
                "minimum_ats_score": minimum_score,
                "review_minimum_score": review_score,
                "mandatory_skills": rules.get(
                    "mandatory_skills",
                    []
                )
            },
            "rule_results": {
                "mandatory_skills": skill_result,
                "experience": experience_result,
                "location": location_result,
                "availability": availability_result
            }
        }

        return result
