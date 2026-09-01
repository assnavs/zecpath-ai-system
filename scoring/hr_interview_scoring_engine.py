import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from scoring.communication_scoring_engine import (
    CommunicationScoringEngine,
)
from scoring.confidence_sentiment_engine import (
    ConfidenceSentimentEngine,
)


class HRInterviewScoringEngine:
    """
    Day 37 HR Interview Scoring Engine.

    Combines:
    - Answer relevance
    - Communication score
    - Confidence score
    - Answer consistency

    The final score is normalized by averaging individual
    answer scores, allowing fair comparison across interviews
    with different numbers of answers.
    """

    CONFIG_PATH = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "hr_interview_scoring_configuration.json"
    )

    def __init__(self):
        self.config = self._load_configuration()

        self.communication_engine = (
            CommunicationScoringEngine()
        )

        self.confidence_engine = (
            ConfidenceSentimentEngine()
        )

    def _load_configuration(self) -> Dict[str, Any]:
        with open(
            self.CONFIG_PATH,
            "r",
            encoding="utf-8-sig",
        ) as file:
            return json.load(file)

    @staticmethod
    def _normalize_text(text: str) -> str:
        return re.sub(
            r"\s+",
            " ",
            text.strip().lower(),
        )

    @staticmethod
    def _extract_keywords(text: str) -> set:
        words = re.findall(
            r"\b[a-zA-Z]{3,}\b",
            text.lower(),
        )

        stop_words = {
            "the",
            "and",
            "for",
            "with",
            "that",
            "this",
            "have",
            "has",
            "had",
            "from",
            "your",
            "you",
            "are",
            "was",
            "were",
            "but",
            "not",
            "can",
            "will",
            "about",
            "into",
            "been",
            "being",
        }

        return {
            word
            for word in words
            if word not in stop_words
        }

    def calculate_relevance(
        self,
        answer: str,
        expected_keywords: Optional[List[str]] = None,
    ) -> float:
        """
        Calculate answer relevance using keyword overlap.
        """

        if not answer or not answer.strip():
            return 0.0

        if not expected_keywords:
            return 100.0

        answer_keywords = self._extract_keywords(answer)

        expected = {
            self._normalize_text(keyword)
            for keyword in expected_keywords
            if keyword.strip()
        }

        if not expected:
            return 100.0

        matches = sum(
            1
            for keyword in expected
            if keyword in answer_keywords
        )

        score = (
            matches / len(expected)
        ) * 100

        return round(
            max(0.0, min(100.0, score)),
            2,
        )

    def calculate_consistency(
        self,
        answer: str,
        previous_answer: Optional[str] = None,
    ) -> float:
        """
        Calculate consistency using keyword overlap between
        the current and previous answers.
        """

        if not previous_answer:
            return 100.0

        current_keywords = self._extract_keywords(answer)
        previous_keywords = self._extract_keywords(
            previous_answer
        )

        if not current_keywords:
            return 0.0

        if not previous_keywords:
            return 100.0

        overlap = (
            current_keywords.intersection(
                previous_keywords
            )
        )

        union = (
            current_keywords.union(
                previous_keywords
            )
        )

        if not union:
            return 100.0

        score = (
            len(overlap) / len(union)
        ) * 100

        return round(
            max(0.0, min(100.0, score)),
            2,
        )

    def score_answer(
        self,
        answer: str,
        expected_keywords: Optional[List[str]] = None,
        previous_answer: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Score a single interview answer.
        """

        if not isinstance(answer, str):
            raise TypeError(
                "Interview answer must be a string."
            )

        communication_result = (
            self.communication_engine.analyze_response(
                answer
            )
        )

        confidence_result = (
            self.confidence_engine.analyze_response(
                answer,
                previous_answer=previous_answer,
            )
        )

        relevance_score = self.calculate_relevance(
            answer,
            expected_keywords,
        )

        consistency_score = self.calculate_consistency(
            answer,
            previous_answer,
        )

        communication_score = float(
            communication_result[
                "communication_score"
            ]
        )

        confidence_score = float(
            confidence_result[
                "confidence_score"
            ]
        )

        weights = self.config["weights"]

        weighted_score = (
            relevance_score
            * weights["answer_relevance"]
            + communication_score
            * weights["communication"]
            + confidence_score
            * weights["confidence"]
            + consistency_score
            * weights["consistency"]
        )

        final_score = round(
            max(0.0, min(100.0, weighted_score)),
            2,
        )

        return {
            "answer": answer,
            "scores": {
                "answer_relevance": relevance_score,
                "communication": communication_score,
                "confidence": confidence_score,
                "consistency": consistency_score,
            },
            "weighted_score": final_score,
            "communication_details": (
                communication_result
            ),
            "confidence_details": (
                confidence_result
            ),
        }

    def score_interview(
        self,
        answers: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Score an entire interview.

        Each item should contain:
        {
            "answer": "...",
            "expected_keywords": [...]
        }
        """

        if not isinstance(answers, list):
            raise TypeError(
                "Answers must be provided as a list."
            )

        if not answers:
            return {
                "interview_score": 0.0,
                "interview_level": (
                    "needs_improvement"
                ),
                "answer_count": 0,
                "answer_results": [],
                "score_breakdown": {
                    "answer_relevance": 0.0,
                    "communication": 0.0,
                    "confidence": 0.0,
                    "consistency": 0.0,
                },
            }

        answer_results = []
        previous_answer = None

        for item in answers:

            if not isinstance(item, dict):
                raise TypeError(
                    "Each interview answer must be "
                    "a dictionary."
                )

            if "answer" not in item:
                raise ValueError(
                    "Each answer item must contain "
                    "an 'answer' field."
                )

            result = self.score_answer(
                answer=item["answer"],
                expected_keywords=item.get(
                    "expected_keywords"
                ),
                previous_answer=previous_answer,
            )

            answer_results.append(result)

            previous_answer = item["answer"]

        score_breakdown = {}

        for metric in [
            "answer_relevance",
            "communication",
            "confidence",
            "consistency",
        ]:
            values = [
                result["scores"][metric]
                for result in answer_results
            ]

            score_breakdown[metric] = round(
                sum(values) / len(values),
                2,
            )

        interview_score = round(
            sum(
                result["weighted_score"]
                for result in answer_results
            )
            / len(answer_results),
            2,
        )

        return {
            "interview_score": interview_score,
            "interview_level": (
                self._classify_score(
                    interview_score
                )
            ),
            "answer_count": len(answer_results),
            "answer_results": answer_results,
            "score_breakdown": score_breakdown,
        }

    def _classify_score(
        self,
        score: float,
    ) -> str:

        thresholds = self.config["thresholds"]

        if score >= thresholds["excellent"]:
            return "excellent"

        if score >= thresholds["good"]:
            return "good"

        if score >= thresholds["moderate"]:
            return "moderate"

        return "needs_improvement"

    def generate_candidate_report(
        self,
        answers: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate a structured candidate HR interview report.
        """

        interview_result = self.score_interview(
            answers
        )

        return {
            "candidate_hr_report": {
                "interview_score": (
                    interview_result[
                        "interview_score"
                    ]
                ),
                "interview_level": (
                    interview_result[
                        "interview_level"
                    ]
                ),
                "answer_count": (
                    interview_result[
                        "answer_count"
                    ]
                ),
                "score_breakdown": (
                    interview_result[
                        "score_breakdown"
                    ]
                ),
                "normalization_method": (
                    "average_per_answer"
                ),
            }
        }
