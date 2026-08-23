import json
import re
from pathlib import Path
from typing import Any, Dict, List


class AnswerIntentEngine:
    """Classify and structure candidate screening answers."""

    def __init__(self, pattern_file: str = "data/answer_intent_patterns.json"):
        self.pattern_file = Path(pattern_file)

        with self.pattern_file.open("r", encoding="utf-8-sig") as file:
            self.patterns = json.load(file)

        self.intents = self.patterns.get("intents", {})
        self.off_topic_keywords = self.patterns.get("off_topic_keywords", [])

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize answer text for matching."""
        if not isinstance(text, str):
            return ""

        return re.sub(r"\s+", " ", text.strip().lower())

    def _keyword_score(self, text: str, keywords: List[str]) -> int:
        """Count matching intent keywords."""
        score = 0

        for keyword in keywords:
            if keyword.lower() in text:
                score += 1

        return score

    def classify_intent(self, answer: str) -> Dict[str, Any]:
        """Classify the primary intent of a candidate answer."""

        normalized = self._normalize_text(answer)

        if not normalized:
            return {
                "intent": "unknown",
                "confidence": 0.0
            }

        scores = {
            intent: self._keyword_score(normalized, keywords)
            for intent, keywords in self.intents.items()
        }

        best_intent = max(scores, key=scores.get)
        best_score = scores[best_intent]

        if best_score == 0:
            return {
                "intent": "unknown",
                "confidence": 0.0
            }

        confidence = min(0.95, 0.55 + (best_score * 0.10))

        return {
            "intent": best_intent,
            "confidence": round(confidence, 2)
        }

    def detect_off_topic(self, answer: str) -> bool:
        """Detect clearly off-topic responses."""
        normalized = self._normalize_text(answer)

        if not normalized:
            return False

        return any(
            keyword.lower() in normalized
            for keyword in self.off_topic_keywords
        )

    def detect_missing_or_vague(self, answer: str) -> bool:
        """Detect empty, extremely short, or vague responses."""

        normalized = self._normalize_text(answer)

        if not normalized:
            return True

        vague_answers = {
            "yes",
            "no",
            "maybe",
            "not sure",
            "i don't know",
            "dont know",
            "none",
            "nothing",
            "some",
            "okay",
            "fine"
        }

        if normalized in vague_answers:
            return True

        meaningful_words = normalized.split()

        return len(meaningful_words) < 2

    def extract_information(
        self,
        answer: str,
        intent: str
    ) -> Dict[str, Any]:
        """Extract basic semantic information according to intent."""

        normalized = self._normalize_text(answer)

        result: Dict[str, Any] = {
            "raw_text": answer,
            "normalized_text": normalized
        }

        if intent == "skills":
            result["skills"] = self._extract_skills(normalized)

        elif intent == "experience":
            result["experience_details"] = self._extract_experience(normalized)

        elif intent == "availability":
            result["availability"] = normalized

        elif intent == "salary_expectation":
            result["salary_expectation"] = self._extract_salary(normalized)

        return result

    def _extract_skills(self, text: str) -> List[str]:
        known_skills = [
            "python",
            "sql",
            "java",
            "javascript",
            "typescript",
            "c++",
            "c#",
            "html",
            "css",
            "excel",
            "power bi",
            "tableau",
            "machine learning",
            "deep learning",
            "pandas",
            "numpy",
            "scikit-learn",
            "docker",
            "kubernetes"
        ]

        return [
            skill
            for skill in known_skills
            if skill in text
        ]

    @staticmethod
    def _extract_experience(text: str) -> Dict[str, Any]:
        year_matches = re.findall(
            r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
            text
        )

        return {
            "years": [
                float(value) if "." in value else int(value)
                for value in year_matches
            ],
            "details": text
        }

    @staticmethod
    def _extract_salary(text: str) -> Dict[str, Any]:
        salary_matches = re.findall(
            r"(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*(?:lpa|lakhs?|lakh)?",
            text,
            flags=re.IGNORECASE
        )

        return {
            "values": [
                float(value) if "." in value else int(value)
                for value in salary_matches
            ],
            "details": text
        }

    def understand(self, answer: str) -> Dict[str, Any]:
        """Create a structured semantic object for a candidate answer."""

        normalized = self._normalize_text(answer)
        off_topic = self.detect_off_topic(answer)
        vague = self.detect_missing_or_vague(answer)

        intent_result = self.classify_intent(answer)
        intent = intent_result["intent"]

        if off_topic:
            response_status = "off_topic"
        elif vague:
            response_status = "missing_or_vague"
        elif intent == "unknown":
            response_status = "unknown"
        else:
            response_status = "understood"

        return {
            "raw_text": answer,
            "normalized_text": normalized,
            "intent": intent,
            "confidence": intent_result["confidence"],
            "off_topic": off_topic,
            "missing_or_vague": vague,
            "response_status": response_status,
            "semantic_data": self.extract_information(answer, intent)
        }


class AnswerUnderstandingEngine(AnswerIntentEngine):
    """Alias representing the answer understanding engine."""

    pass

