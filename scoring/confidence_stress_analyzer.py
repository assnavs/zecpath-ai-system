from typing import Any, Dict, List
import re

from scoring.confidence_sentiment_engine import (
    ConfidenceSentimentEngine,
)


class ConfidenceStressAnalyzer:
    """
    Day 36 confidence and stress indicator analyzer.

    Evaluates observable response signals including:
    - Long pause patterns
    - Repeated words
    - Uncertainty language
    - Hesitation patterns
    - Stress-related language
    - Sentiment
    - Behavioral confidence

    The output represents observable communication
    indicators and is not a psychological assessment.
    """

    STRESS_TERMS = {
        "stressed",
        "stress",
        "nervous",
        "anxious",
        "worried",
        "overwhelmed",
        "pressure",
        "panic",
        "afraid",
        "fear",
        "frustrated",
        "confused",
    }

    def __init__(self):
        self.confidence_engine = (
            ConfidenceSentimentEngine()
        )

    @staticmethod
    def _normalize_text(text: str) -> str:
        if not isinstance(text, str):
            return ""

        return re.sub(
            r"\s+",
            " ",
            text.strip().lower(),
        )

    def analyze_long_pauses(
        self,
        answer: str,
    ) -> Dict[str, Any]:
        """
        Detect textual pause indicators such as
        ellipses and repeated dash sequences.
        """

        if not isinstance(answer, str):
            answer = ""

        ellipsis_count = len(
            re.findall(r"\.{3,}", answer)
        )

        dash_pause_count = len(
            re.findall(r"(?:--|—)", answer)
        )

        pause_count = (
            ellipsis_count + dash_pause_count
        )

        score = max(
            0.0,
            100.0 - (pause_count * 20),
        )

        return {
            "pause_count": pause_count,
            "ellipsis_count": ellipsis_count,
            "dash_pause_count": dash_pause_count,
            "pause_score": round(score, 2),
        }

    def analyze_repeated_words(
        self,
        answer: str,
    ) -> Dict[str, Any]:
        """
        Detect immediately repeated words such as
        'I I' or 'the the'.
        """

        normalized = self._normalize_text(answer)

        words = re.findall(
            r"\b[\w']+\b",
            normalized,
        )

        repeated_words: List[str] = []

        for index in range(
            1,
            len(words),
        ):
            if words[index] == words[index - 1]:
                repeated_words.append(
                    words[index]
                )

        repetition_count = len(repeated_words)

        score = max(
            0.0,
            100.0 - (repetition_count * 15),
        )

        return {
            "repetition_count": repetition_count,
            "repeated_words": repeated_words,
            "repetition_score": round(score, 2),
        }

    def analyze_stress(
        self,
        answer: str,
    ) -> Dict[str, Any]:
        """
        Detect stress-related terms in the response.
        """

        normalized = self._normalize_text(answer)

        detected_terms = [
            term
            for term in self.STRESS_TERMS
            if re.search(
                rf"\b{re.escape(term)}\b",
                normalized,
            )
        ]

        stress_count = len(detected_terms)

        stress_score = max(
            0.0,
            100.0 - (stress_count * 15),
        )

        if stress_count == 0:
            stress_level = "low"
        elif stress_count <= 2:
            stress_level = "moderate"
        else:
            stress_level = "high"

        return {
            "stress_count": stress_count,
            "detected_terms": detected_terms,
            "stress_score": round(
                stress_score,
                2,
            ),
            "stress_level": stress_level,
        }

    def calculate_behavioral_confidence(
        self,
        confidence_score: float,
        pause_score: float,
        repetition_score: float,
        stress_score: float,
    ) -> float:
        """
        Calculate an observable behavioral confidence
        score from communication signals.
        """

        score = (
            confidence_score * 0.50
            + pause_score * 0.15
            + repetition_score * 0.15
            + stress_score * 0.20
        )

        return round(
            max(
                0.0,
                min(100.0, score),
            ),
            2,
        )

    @staticmethod
    def classify_behavioral_confidence(
        score: float,
    ) -> str:
        if score >= 75:
            return "strong"

        if score >= 50:
            return "moderate"

        return "needs_improvement"

    def analyze_response(
        self,
        answer: str,
        duration_seconds: float = None,
        previous_answer: str = None,
    ) -> Dict[str, Any]:
        """
        Run the complete Day 36 confidence and stress
        indicator analysis.
        """

        confidence_analysis = (
            self.confidence_engine.analyze_response(
                answer,
                duration_seconds=duration_seconds,
                previous_answer=previous_answer,
            )
        )

        pauses = self.analyze_long_pauses(answer)

        repetitions = self.analyze_repeated_words(
            answer
        )

        stress = self.analyze_stress(answer)

        behavioral_confidence_score = (
            self.calculate_behavioral_confidence(
                confidence_score=confidence_analysis[
                    "confidence_score"
                ],
                pause_score=pauses["pause_score"],
                repetition_score=repetitions[
                    "repetition_score"
                ],
                stress_score=stress["stress_score"],
            )
        )

        return {
            "raw_text": answer,
            "behavioral_confidence_score": (
                behavioral_confidence_score
            ),
            "behavioral_confidence_level": (
                self.classify_behavioral_confidence(
                    behavioral_confidence_score
                )
            ),
            "stress_level": stress["stress_level"],
            "signals": {
                "confidence": confidence_analysis,
                "long_pauses": pauses,
                "repeated_words": repetitions,
                "stress": stress,
            },
        }
