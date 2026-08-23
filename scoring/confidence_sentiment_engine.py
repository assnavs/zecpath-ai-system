import json
import re
from pathlib import Path
from typing import Any, Dict, List


class ConfidenceSentimentEngine:
    """
    Analyzes observable communication signals from candidate responses.

    The engine evaluates:
    - Hesitation patterns
    - Response length
    - Response pace
    - Sentiment
    - Uncertainty
    - Consistency indicators

    The resulting confidence score represents observable
    communication strength, not a psychological assessment.
    """

    def __init__(
        self,
        config_path: str = "data/confidence_sentiment_configuration.json"
    ):
        self.config_path = Path(config_path)

        with self.config_path.open(
            "r",
            encoding="utf-8-sig"
        ) as file:
            self.configuration = json.load(file)

        self.weights = self.configuration["weights"]
        self.thresholds = self.configuration["thresholds"]

        self.hesitation_terms = self.configuration["hesitation_terms"]
        self.uncertainty_terms = self.configuration["uncertainty_terms"]
        self.positive_terms = self.configuration["positive_terms"]
        self.negative_terms = self.configuration["negative_terms"]

        self.minimum_score = self.configuration[
            "score_range"
        ]["minimum"]

        self.maximum_score = self.configuration[
            "score_range"
        ]["maximum"]

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize response text for signal detection."""

        if not isinstance(text, str):
            return ""

        return re.sub(
            r"\s+",
            " ",
            text.strip().lower()
        )

    @staticmethod
    def _count_terms(
        text: str,
        terms: List[str]
    ) -> int:
        """Count occurrences of configured terms."""

        count = 0

        for term in terms:
            pattern = rf"\b{re.escape(term.lower())}\b"
            count += len(
                re.findall(pattern, text)
            )

        return count

    def analyze_hesitation(
        self,
        answer: str
    ) -> Dict[str, Any]:
        """Detect hesitation patterns in a response."""

        normalized = self._normalize_text(answer)

        count = self._count_terms(
            normalized,
            self.hesitation_terms
        )

        score = max(
            self.minimum_score,
            self.maximum_score - (count * 15)
        )

        return {
            "hesitation_count": count,
            "hesitation_score": round(score, 2),
            "detected_terms": [
                term
                for term in self.hesitation_terms
                if re.search(
                    rf"\b{re.escape(term.lower())}\b",
                    normalized
                )
            ]
        }

    def analyze_response_length(
        self,
        answer: str
    ) -> Dict[str, Any]:
        """Measure response length."""

        normalized = self._normalize_text(answer)
        word_count = len(normalized.split()) if normalized else 0

        if word_count == 0:
            score = 0
        elif word_count < 5:
            score = 40
        elif word_count < 10:
            score = 60
        elif word_count < 30:
            score = 80
        else:
            score = 100

        return {
            "word_count": word_count,
            "length_score": float(score)
        }

    def analyze_pace(
        self,
        answer: str,
        duration_seconds: float = None
    ) -> Dict[str, Any]:
        """Measure response pace when duration is available."""

        normalized = self._normalize_text(answer)
        word_count = len(normalized.split()) if normalized else 0

        if not duration_seconds or duration_seconds <= 0:
            return {
                "duration_seconds": duration_seconds,
                "words_per_second": None,
                "pace_score": 0.0,
                "pace_available": False
            }

        words_per_second = (
            word_count / float(duration_seconds)
        )

        if 1.5 <= words_per_second <= 3.0:
            score = 100
        elif 1.0 <= words_per_second < 1.5:
            score = 80
        elif 3.0 < words_per_second <= 4.0:
            score = 80
        elif 0.5 <= words_per_second < 1.0:
            score = 60
        else:
            score = 40

        return {
            "duration_seconds": float(duration_seconds),
            "words_per_second": round(
                words_per_second,
                2
            ),
            "pace_score": float(score),
            "pace_available": True
        }

    def analyze_sentiment(
        self,
        answer: str
    ) -> Dict[str, Any]:
        """Estimate lexical sentiment from configured terms."""

        normalized = self._normalize_text(answer)

        positive_count = self._count_terms(
            normalized,
            self.positive_terms
        )

        negative_count = self._count_terms(
            normalized,
            self.negative_terms
        )

        if positive_count > negative_count:
            sentiment = "positive"
            score = 100
        elif negative_count > positive_count:
            sentiment = "negative"
            score = 40
        else:
            sentiment = "neutral"
            score = 70

        return {
            "sentiment": sentiment,
            "positive_count": positive_count,
            "negative_count": negative_count,
            "sentiment_score": float(score)
        }

    def analyze_uncertainty(
        self,
        answer: str
    ) -> Dict[str, Any]:
        """Detect uncertainty-related language."""

        normalized = self._normalize_text(answer)

        count = self._count_terms(
            normalized,
            self.uncertainty_terms
        )

        score = max(
            self.minimum_score,
            self.maximum_score - (count * 15)
        )

        return {
            "uncertainty_count": count,
            "uncertainty_score": round(score, 2),
            "detected_terms": [
                term
                for term in self.uncertainty_terms
                if re.search(
                    rf"\b{re.escape(term.lower())}\b",
                    normalized
                )
            ]
        }

    def analyze_consistency(
        self,
        answer: str,
        previous_answer: str = None
    ) -> Dict[str, Any]:
        """
        Detect basic lexical consistency between responses.

        This is a lightweight signal and does not claim
        full semantic contradiction detection.
        """

        if not previous_answer:
            return {
                "consistency_score": 100.0,
                "comparison_available": False
            }

        current_words = set(
            self._normalize_text(answer).split()
        )

        previous_words = set(
            self._normalize_text(previous_answer).split()
        )

        if not current_words or not previous_words:
            return {
                "consistency_score": 0.0,
                "comparison_available": True
            }

        overlap = len(
            current_words.intersection(previous_words)
        )

        total = len(
            current_words.union(previous_words)
        )

        similarity = overlap / total if total else 0

        return {
            "consistency_score": round(
                similarity * 100,
                2
            ),
            "comparison_available": True
        }

    def calculate_confidence_score(
        self,
        hesitation_score: float,
        response_length_score: float,
        pace_score: float,
        sentiment_score: float,
        uncertainty_score: float,
        consistency_score: float
    ) -> float:
        """Calculate weighted communication-strength score."""

        weighted_score = (
            hesitation_score * self.weights["hesitation"]
            + response_length_score * self.weights["response_length"]
            + pace_score * self.weights["pace"]
            + sentiment_score * self.weights["sentiment"]
            + uncertainty_score * self.weights["uncertainty"]
            + consistency_score * self.weights["consistency"]
        )

        return round(
            max(
                self.minimum_score,
                min(
                    self.maximum_score,
                    weighted_score
                )
            ),
            2
        )

    def classify_strength(
        self,
        score: float
    ) -> str:
        """Classify observable communication strength."""

        if score >= self.thresholds["strong"]:
            return "strong"

        if score >= self.thresholds["moderate"]:
            return "moderate"

        return "needs_improvement"

    def analyze_response(
        self,
        answer: str,
        duration_seconds: float = None,
        previous_answer: str = None
    ) -> Dict[str, Any]:
        """Run the complete communication signal analysis."""

        normalized = self._normalize_text(answer)

        hesitation = self.analyze_hesitation(answer)
        response_length = self.analyze_response_length(answer)
        pace = self.analyze_pace(
            answer,
            duration_seconds
        )
        sentiment = self.analyze_sentiment(answer)
        uncertainty = self.analyze_uncertainty(answer)
        consistency = self.analyze_consistency(
            answer,
            previous_answer
        )

        final_score = self.calculate_confidence_score(
            hesitation_score=hesitation["hesitation_score"],
            response_length_score=response_length["length_score"],
            pace_score=pace["pace_score"],
            sentiment_score=sentiment["sentiment_score"],
            uncertainty_score=uncertainty["uncertainty_score"],
            consistency_score=consistency["consistency_score"]
        )

        return {
            "raw_text": answer,
            "normalized_text": normalized,
            "confidence_score": final_score,
            "communication_strength": self.classify_strength(
                final_score
            ),
            "signals": {
                "hesitation": hesitation,
                "response_length": response_length,
                "pace": pace,
                "sentiment": sentiment,
                "uncertainty": uncertainty,
                "consistency": consistency
            }
        }
