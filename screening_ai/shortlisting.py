"""
Candidate Shortlisting Automation Module

Automatically classifies candidates into:
- Shortlisted
- Review
- Rejected

The thresholds are loaded from a configurable JSON file.
"""

import json
from pathlib import Path

from scoring.candidate_ranking_engine import CandidateRankingEngine
from utils.logger import logger


class CandidateShortlistingEngine:
    """
    Automates candidate filtering and shortlisting.
    """

    def __init__(self):

        logger.info("Initializing Candidate Shortlisting Engine...")

        config_path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "shortlisting_thresholds.json"
        )

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.shortlist_threshold = self.config.get(
            "shortlist_threshold",
            80
        )

        self.review_threshold = self.config.get(
            "review_threshold",
            60
        )

        self.top_candidate_limit = self.config.get(
            "top_candidate_limit",
            5
        )

        if self.review_threshold > self.shortlist_threshold:
            raise ValueError(
                "review_threshold cannot be greater than "
                "shortlist_threshold."
            )

        self.ranking_engine = CandidateRankingEngine()

    def get_decision(self, score):
        """
        Determine candidate status based on ATS score.
        """

        if score >= self.shortlist_threshold:
            return "Shortlisted"

        if score >= self.review_threshold:
            return "Review"

        return "Rejected"

    def shortlist_candidates(self, candidates):
        """
        Rank candidates and assign shortlisting decisions.
        """

        logger.info("Starting candidate shortlisting...")

        ranking_result = self.ranking_engine.rank_candidates(
            candidates
        )

        ranked_candidates = ranking_result["ranked_candidates"]

        processed_candidates = []

        shortlisted = []
        review = []
        rejected = []

        for candidate in ranked_candidates:

            candidate_result = candidate.copy()

            decision = self.get_decision(
                candidate_result["score"]
            )

            candidate_result["decision"] = decision

            processed_candidates.append(candidate_result)

            if decision == "Shortlisted":
                shortlisted.append(candidate_result)

            elif decision == "Review":
                review.append(candidate_result)

            else:
                rejected.append(candidate_result)

        top_candidates = processed_candidates[
            :self.top_candidate_limit
        ]

        result = {
            "total_candidates": len(processed_candidates),
            "shortlisted_count": len(shortlisted),
            "review_count": len(review),
            "rejected_count": len(rejected),
            "thresholds": {
                "shortlist_threshold": self.shortlist_threshold,
                "review_threshold": self.review_threshold
            },
            "ranked_candidates": processed_candidates,
            "top_candidates": top_candidates
        }

        logger.info(
            "Candidate shortlisting completed. "
            "Shortlisted: %s, Review: %s, Rejected: %s",
            len(shortlisted),
            len(review),
            len(rejected)
        )

        return result