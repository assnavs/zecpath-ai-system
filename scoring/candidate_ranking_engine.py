"""
Candidate Ranking Engine

Ranks candidates based on their ATS scores and generates
recruiter-friendly ranked candidate lists.

Features:
- Sort candidates by ATS score
- Assign ranking positions
- Generate top candidate lists
- Handle missing candidate scores
- Produce structured output
"""

from utils.logger import logger


class CandidateRankingEngine:
    """
    Automatically ranks candidates based on ATS score.
    """

    def __init__(self):
        logger.info("Candidate Ranking Engine initialized.")

    def rank_candidates(self, candidates):
        """
        Rank candidates from highest ATS score to lowest.

        Candidates with missing scores are treated as having score 0.
        """

        logger.info("Starting candidate ranking...")

        if not candidates:
            logger.warning("No candidates provided for ranking.")

            return {
                "total_candidates": 0,
                "ranked_candidates": []
            }

        normalized_candidates = []

        for candidate in candidates:

            candidate_copy = candidate.copy()

            score = candidate_copy.get("score")

            if score is None:
                score = 0

            try:
                score = float(score)
            except (TypeError, ValueError):
                score = 0

            # Keep scores within valid ATS range.
            score = max(0, min(score, 100))

            candidate_copy["score"] = round(score, 2)

            normalized_candidates.append(candidate_copy)

        ranked_candidates = sorted(
            normalized_candidates,
            key=lambda candidate: candidate["score"],
            reverse=True
        )

        for position, candidate in enumerate(
            ranked_candidates,
            start=1
        ):
            candidate["rank"] = position

        logger.info(
            "Candidate ranking completed for %s candidates.",
            len(ranked_candidates)
        )

        return {
            "total_candidates": len(ranked_candidates),
            "ranked_candidates": ranked_candidates
        }

    def get_top_candidates(self, candidates, limit=5):
        """
        Return the highest-ranked candidates.
        """

        ranked_result = self.rank_candidates(candidates)

        ranked_candidates = ranked_result["ranked_candidates"]

        try:
            limit = int(limit)
        except (TypeError, ValueError):
            limit = 5

        limit = max(limit, 0)

        top_candidates = ranked_candidates[:limit]

        return {
            "requested_limit": limit,
            "candidate_count": len(top_candidates),
            "top_candidates": top_candidates
        }