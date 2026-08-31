import re
from typing import Any, Dict, List


class CommunicationScoringEngine:
    """
    Day 35 Communication Skill Evaluation Engine.

    Evaluates observable communication characteristics:
    - Fluency
    - Grammar
    - Vocabulary range
    - Clarity
    - Filler words
    - Answer structure

    The final score is normalized to a 0-100 range.
    """

    MINIMUM_SCORE = 0
    MAXIMUM_SCORE = 100

    FILLER_WORDS = {
        "um",
        "uh",
        "er",
        "ah",
        "hmm",
        "like",
        "basically",
        "actually",
        "you know",
        "i mean",
    }

    def _normalize_text(
        self,
        text: str,
    ) -> str:
        """Normalize whitespace in candidate text."""

        if not isinstance(text, str):
            return ""

        return re.sub(
            r"\s+",
            " ",
            text.strip(),
        )

    def _get_words(
        self,
        text: str,
    ) -> List[str]:
        """Extract alphabetic words."""

        normalized = self._normalize_text(text)

        return re.findall(
            r"\b[a-zA-Z]+\b",
            normalized.lower(),
        )

    def analyze_fluency(
        self,
        answer: str,
    ) -> Dict[str, Any]:
        """
        Estimate fluency using sentence continuity
        and response completeness.
        """

        normalized = self._normalize_text(answer)

        if not normalized:
            return {
                "sentence_count": 0,
                "average_sentence_length": 0.0,
                "fluency_score": 0.0,
            }

        sentences = [
            sentence.strip()
            for sentence in re.split(
                r"[.!?]+",
                normalized,
            )
            if sentence.strip()
        ]

        words = self._get_words(normalized)

        sentence_count = len(sentences)
        word_count = len(words)

        average_sentence_length = (
            word_count / sentence_count
            if sentence_count
            else 0
        )

        if word_count < 3:
            score = 30
        elif average_sentence_length < 3:
            score = 50
        elif 5 <= average_sentence_length <= 25:
            score = 100
        elif average_sentence_length <= 35:
            score = 80
        else:
            score = 65

        return {
            "sentence_count": sentence_count,
            "average_sentence_length": round(
                average_sentence_length,
                2,
            ),
            "fluency_score": float(score),
        }

    def analyze_grammar(
        self,
        answer: str,
    ) -> Dict[str, Any]:
        """
        Apply lightweight grammar heuristics.

        This is not a full grammar checker.
        """

        normalized = self._normalize_text(answer)

        if not normalized:
            return {
                "grammar_issues": 1,
                "grammar_score": 0.0,
            }

        issues = 0

        if normalized and normalized[0].islower():
            issues += 1

        if normalized and normalized[-1] not in ".!?":
            issues += 1

        if re.search(r"\b(i)\b", normalized):
            issues += len(
                re.findall(
                    r"\bi\b",
                    normalized,
                )
            )

        if re.search(r"\s{2,}", answer):
            issues += 1

        score = max(
            self.MINIMUM_SCORE,
            self.MAXIMUM_SCORE - (issues * 15),
        )

        return {
            "grammar_issues": issues,
            "grammar_score": float(score),
        }

    def analyze_vocabulary(
        self,
        answer: str,
    ) -> Dict[str, Any]:
        """Measure vocabulary diversity."""

        words = self._get_words(answer)

        if not words:
            return {
                "word_count": 0,
                "unique_word_count": 0,
                "vocabulary_ratio": 0.0,
                "vocabulary_score": 0.0,
            }

        unique_words = set(words)

        ratio = len(unique_words) / len(words)

        score = ratio * 100

        if len(words) < 5:
            score = min(score, 60)

        return {
            "word_count": len(words),
            "unique_word_count": len(unique_words),
            "vocabulary_ratio": round(
                ratio,
                2,
            ),
            "vocabulary_score": round(
                min(
                    self.MAXIMUM_SCORE,
                    score,
                ),
                2,
            ),
        }

    def analyze_clarity(
        self,
        answer: str,
    ) -> Dict[str, Any]:
        """
        Estimate clarity from response length
        and sentence complexity.
        """

        words = self._get_words(answer)

        if not words:
            return {
                "word_count": 0,
                "clarity_score": 0.0,
            }

        word_count = len(words)

        if word_count < 3:
            score = 40
        elif word_count < 8:
            score = 65
        elif word_count <= 80:
            score = 100
        elif word_count <= 120:
            score = 80
        else:
            score = 65

        return {
            "word_count": word_count,
            "clarity_score": float(score),
        }

    def analyze_filler_words(
        self,
        answer: str,
    ) -> Dict[str, Any]:
        """Detect common filler words."""

        normalized = self._normalize_text(
            answer,
        ).lower()

        detected = []

        for filler in self.FILLER_WORDS:
            pattern = (
                rf"\b{re.escape(filler)}\b"
            )

            if re.search(pattern, normalized):
                detected.append(filler)

        filler_count = sum(
            len(
                re.findall(
                    rf"\b{re.escape(filler)}\b",
                    normalized,
                )
            )
            for filler in self.FILLER_WORDS
        )

        score = max(
            self.MINIMUM_SCORE,
            self.MAXIMUM_SCORE - (
                filler_count * 12
            ),
        )

        return {
            "filler_count": filler_count,
            "detected_fillers": detected,
            "filler_score": float(score),
        }

    def analyze_answer_structure(
        self,
        answer: str,
    ) -> Dict[str, Any]:
        """
        Estimate whether an answer contains
        a reasonably structured explanation.
        """

        normalized = self._normalize_text(answer)

        if not normalized:
            return {
                "sentence_count": 0,
                "structure_score": 0.0,
            }

        sentences = [
            sentence.strip()
            for sentence in re.split(
                r"[.!?]+",
                normalized,
            )
            if sentence.strip()
        ]

        sentence_count = len(sentences)
        word_count = len(
            self._get_words(normalized)
        )

        if word_count < 5:
            score = 40
        elif sentence_count >= 2:
            score = 100
        elif word_count >= 10:
            score = 80
        else:
            score = 60

        return {
            "sentence_count": sentence_count,
            "structure_score": float(score),
        }

    def calculate_communication_score(
        self,
        fluency_score: float,
        grammar_score: float,
        vocabulary_score: float,
        clarity_score: float,
        filler_score: float,
        structure_score: float,
    ) -> float:
        """Calculate normalized communication score."""

        weighted_score = (
            fluency_score * 0.20
            + grammar_score * 0.15
            + vocabulary_score * 0.15
            + clarity_score * 0.20
            + filler_score * 0.15
            + structure_score * 0.15
        )

        return round(
            max(
                self.MINIMUM_SCORE,
                min(
                    self.MAXIMUM_SCORE,
                    weighted_score,
                ),
            ),
            2,
        )

    def classify_communication(
        self,
        score: float,
    ) -> str:
        """Classify communication performance."""

        if score >= 80:
            return "excellent"

        if score >= 60:
            return "good"

        if score >= 40:
            return "moderate"

        return "needs_improvement"

    def analyze_response(
        self,
        answer: str,
    ) -> Dict[str, Any]:
        """Run complete communication analysis."""

        if not isinstance(answer, str):
            raise TypeError(
                "Candidate response must be a string."
            )

        normalized = self._normalize_text(answer)

        fluency = self.analyze_fluency(answer)
        grammar = self.analyze_grammar(answer)
        vocabulary = self.analyze_vocabulary(answer)
        clarity = self.analyze_clarity(answer)
        fillers = self.analyze_filler_words(answer)
        structure = self.analyze_answer_structure(answer)

        final_score = (
            self.calculate_communication_score(
                fluency_score=fluency[
                    "fluency_score"
                ],
                grammar_score=grammar[
                    "grammar_score"
                ],
                vocabulary_score=vocabulary[
                    "vocabulary_score"
                ],
                clarity_score=clarity[
                    "clarity_score"
                ],
                filler_score=fillers[
                    "filler_score"
                ],
                structure_score=structure[
                    "structure_score"
                ],
            )
        )

        return {
            "raw_text": answer,
            "normalized_text": normalized,
            "communication_score": final_score,
            "communication_level": (
                self.classify_communication(
                    final_score
                )
            ),
            "metrics": {
                "fluency": fluency,
                "grammar": grammar,
                "vocabulary": vocabulary,
                "clarity": clarity,
                "fillers": fillers,
                "structure": structure,
            },
        }