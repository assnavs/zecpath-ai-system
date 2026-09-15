import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class AptitudeLogicEngine:
    """
    Day 38 Aptitude and Logic Evaluation Engine.

    Evaluates reasoning-based and situational interview
    responses using observable answer characteristics.

    The engine focuses on:
    - Problem understanding
    - Logical reasoning
    - Decision quality
    - Problem-solving clarity

    The evaluation is intended as an interview aptitude
    indicator and is not a psychological assessment.
    """

    CONFIG_PATH = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "aptitude_logic_configuration.json"
    )

    def __init__(self):
        self.config = self._load_configuration()

    def _load_configuration(self) -> Dict[str, Any]:
        with open(
            self.CONFIG_PATH,
            "r",
            encoding="utf-8-sig",
        ) as file:
            return json.load(file)

    @staticmethod
    def _normalize_text(text: str) -> str:
        if not isinstance(text, str):
            return ""

        return re.sub(
            r"\s+",
            " ",
            text.strip().lower(),
        )

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        normalized = AptitudeLogicEngine._normalize_text(
            text
        )

        return re.findall(
            r"\b[a-zA-Z]{3,}\b",
            normalized,
        )

    def _count_indicators(
        self,
        answer: str,
        indicators: List[str],
    ) -> int:
        normalized = self._normalize_text(answer)

        count = 0

        for indicator in indicators:
            if re.search(
                rf"\b{re.escape(indicator.lower())}\b",
                normalized,
            ):
                count += 1

        return count

    def calculate_problem_understanding(
        self,
        answer: str,
        expected_keywords: Optional[List[str]] = None,
    ) -> float:
        """
        Estimate how well the response addresses the
        core problem using expected concept coverage.
        """

        if not isinstance(answer, str) or not answer.strip():
            return 0.0

        if not expected_keywords:
            return 100.0

        answer_tokens = set(self._tokenize(answer))

        expected_tokens = {
            self._normalize_text(keyword)
            for keyword in expected_keywords
            if isinstance(keyword, str)
            and keyword.strip()
        }

        if not expected_tokens:
            return 100.0

        matches = sum(
            1
            for keyword in expected_tokens
            if keyword in answer_tokens
        )

        score = (
            matches / len(expected_tokens)
        ) * 100

        return round(
            max(0.0, min(100.0, score)),
            2,
        )

    def calculate_logical_reasoning(
        self,
        answer: str,
    ) -> float:
        """
        Evaluate observable reasoning structure.

        More distinct reasoning indicators and a structured
        multi-step response produce a stronger score.
        """

        if not isinstance(answer, str) or not answer.strip():
            return 0.0

        tokens = self._tokenize(answer)

        if not tokens:
            return 0.0

        indicator_count = self._count_indicators(
            answer,
            self.config["reasoning_indicators"],
        )

        score = min(
            100.0,
            40.0
            + min(indicator_count, 6) * 8.0
            + min(len(tokens), 60) * 0.20,
        )

        return round(score, 2)

    def calculate_decision_quality(
        self,
        answer: str,
        expected_actions: Optional[List[str]] = None,
    ) -> float:
        """
        Evaluate whether the candidate identifies useful
        actions or decisions for the problem.
        """

        if not isinstance(answer, str) or not answer.strip():
            return 0.0

        normalized = self._normalize_text(answer)

        if expected_actions:
            actions = {
                self._normalize_text(action)
                for action in expected_actions
                if isinstance(action, str)
                and action.strip()
            }

            if actions:
                matches = sum(
                    1
                    for action in actions
                    if action in normalized
                )

                return round(
                    max(
                        0.0,
                        min(
                            100.0,
                            (matches / len(actions))
                            * 100,
                        ),
                    ),
                    2,
                )

        action_count = self._count_indicators(
            answer,
            self.config["problem_solving_indicators"],
        )

        score = min(
            100.0,
            40.0 + min(action_count, 6) * 10.0,
        )

        return round(score, 2)

    def calculate_problem_solving_clarity(
        self,
        answer: str,
    ) -> float:
        """
        Evaluate how clearly the candidate describes a
        problem-solving approach.
        """

        if not isinstance(answer, str) or not answer.strip():
            return 0.0

        tokens = self._tokenize(answer)

        if not tokens:
            return 0.0

        action_count = self._count_indicators(
            answer,
            self.config["problem_solving_indicators"],
        )

        reasoning_count = self._count_indicators(
            answer,
            self.config["reasoning_indicators"],
        )

        structure_score = min(
            35.0,
            len(tokens) * 0.50,
        )

        action_score = min(
            35.0,
            action_count * 7.0,
        )

        reasoning_score = min(
            30.0,
            reasoning_count * 6.0,
        )

        score = (
            structure_score
            + action_score
            + reasoning_score
        )

        return round(
            max(0.0, min(100.0, score)),
            2,
        )

    def evaluate_reasoning(
        self,
        answer: str,
        expected_keywords: Optional[List[str]] = None,
        expected_actions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate a reasoning-based answer.
        """

        if not isinstance(answer, str):
            raise TypeError(
                "Aptitude answer must be a string."
            )

        scores = {
            "problem_understanding": (
                self.calculate_problem_understanding(
                    answer,
                    expected_keywords,
                )
            ),
            "logical_reasoning": (
                self.calculate_logical_reasoning(
                    answer
                )
            ),
            "decision_quality": (
                self.calculate_decision_quality(
                    answer,
                    expected_actions,
                )
            ),
            "problem_solving_clarity": (
                self.calculate_problem_solving_clarity(
                    answer
                )
            ),
        }

        weights = self.config["weights"]

        final_score = (
            scores["problem_understanding"]
            * weights["problem_understanding"]
            + scores["logical_reasoning"]
            * weights["logical_reasoning"]
            + scores["decision_quality"]
            * weights["decision_quality"]
            + scores["problem_solving_clarity"]
            * weights["problem_solving_clarity"]
        )

        final_score = round(
            max(0.0, min(100.0, final_score)),
            2,
        )

        return {
            "answer": answer,
            "scores": scores,
            "aptitude_score": final_score,
            "aptitude_level": self.classify_score(
                final_score
            ),
        }

    def evaluate_scenario(
        self,
        scenario: Dict[str, Any],
        answer: str,
    ) -> Dict[str, Any]:
        """
        Evaluate a situational scenario response.

        A scenario may contain:
        {
            "scenario": "...",
            "expected_keywords": [...],
            "expected_actions": [...]
        }
        """

        if not isinstance(scenario, dict):
            raise TypeError(
                "Scenario must be provided as a dictionary."
            )

        if "scenario" not in scenario:
            raise ValueError(
                "Scenario must contain a 'scenario' field."
            )

        result = self.evaluate_reasoning(
            answer=answer,
            expected_keywords=scenario.get(
                "expected_keywords"
            ),
            expected_actions=scenario.get(
                "expected_actions"
            ),
        )

        return {
            "scenario": scenario["scenario"],
            "evaluation": result,
        }

    def evaluate_interview(
        self,
        responses: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Evaluate multiple aptitude/reasoning responses.

        Each response should contain:
        {
            "answer": "...",
            "expected_keywords": [...],
            "expected_actions": [...]
        }
        """

        if not isinstance(responses, list):
            raise TypeError(
                "Responses must be provided as a list."
            )

        if not responses:
            return {
                "aptitude_score": 0.0,
                "aptitude_level": "needs_improvement",
                "response_count": 0,
                "response_results": [],
                "score_breakdown": {
                    "problem_understanding": 0.0,
                    "logical_reasoning": 0.0,
                    "decision_quality": 0.0,
                    "problem_solving_clarity": 0.0,
                },
            }

        results = []

        for item in responses:
            if not isinstance(item, dict):
                raise TypeError(
                    "Each response must be a dictionary."
                )

            if "answer" not in item:
                raise ValueError(
                    "Each response must contain an 'answer' field."
                )

            results.append(
                self.evaluate_reasoning(
                    answer=item["answer"],
                    expected_keywords=item.get(
                        "expected_keywords"
                    ),
                    expected_actions=item.get(
                        "expected_actions"
                    ),
                )
            )

        metrics = [
            "problem_understanding",
            "logical_reasoning",
            "decision_quality",
            "problem_solving_clarity",
        ]

        score_breakdown = {}

        for metric in metrics:
            values = [
                result["scores"][metric]
                for result in results
            ]

            score_breakdown[metric] = round(
                sum(values) / len(values),
                2,
            )

        aptitude_score = round(
            sum(
                result["aptitude_score"]
                for result in results
            )
            / len(results),
            2,
        )

        return {
            "aptitude_score": aptitude_score,
            "aptitude_level": self.classify_score(
                aptitude_score
            ),
            "response_count": len(results),
            "response_results": results,
            "score_breakdown": score_breakdown,
        }

    @staticmethod
    def classify_score(score: float) -> str:
        """
        Classify an aptitude score using configured thresholds.
        """

        thresholds = {
            "excellent": 80,
            "good": 65,
            "moderate": 50,
        }

        if score >= thresholds["excellent"]:
            return "excellent"

        if score >= thresholds["good"]:
            return "good"

        if score >= thresholds["moderate"]:
            return "moderate"

        return "needs_improvement"

    def generate_aptitude_report(
        self,
        responses: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate a structured aptitude evaluation report.
        """

        result = self.evaluate_interview(responses)

        return {
            "candidate_aptitude_report": {
                "aptitude_score": result[
                    "aptitude_score"
                ],
                "aptitude_level": result[
                    "aptitude_level"
                ],
                "response_count": result[
                    "response_count"
                ],
                "score_breakdown": result[
                    "score_breakdown"
                ],
                "response_results": result[
                    "response_results"
                ],
            }
        }
