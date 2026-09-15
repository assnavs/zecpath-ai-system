import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional


class InterviewSummaryGenerator:
    """
    Day 39 Interview Summary Generator.

    Converts interview evaluation outputs into a
    recruiter-ready structured summary.

    The generator can summarize:
    - Overall HR interview performance
    - Candidate strengths
    - Candidate weaknesses
    - Cultural-fit indicators
    - Risk flags
    - Inconsistencies
    - Natural-language interview insights
    """

    CONFIG_PATH = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "interview_summary_configuration.json"
    )

    TEMPLATE_PATH = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "interview_summary_template.json"
    )

    def __init__(self):
        self.config = self._load_json(
            self.CONFIG_PATH
        )

        self.template = self._load_json(
            self.TEMPLATE_PATH
        )

    @staticmethod
    def _load_json(path: Path) -> Dict[str, Any]:
        with open(
            path,
            "r",
            encoding="utf-8-sig",
        ) as file:
            return json.load(file)

    @staticmethod
    def _normalize_text(text: Any) -> str:
        if not isinstance(text, str):
            return ""

        return re.sub(
            r"\s+",
            " ",
            text.strip().lower(),
        )

    @staticmethod
    def _extract_score(
        evaluation: Dict[str, Any],
        key: str,
        default: float = 0.0,
    ) -> float:
        value = evaluation.get(key, default)

        try:
            return round(
                float(value),
                2,
            )
        except (TypeError, ValueError):
            return default

    def identify_strengths(
        self,
        interview_evaluation: Dict[str, Any],
        aptitude_evaluation: Optional[
            Dict[str, Any]
        ] = None,
    ) -> List[str]:
        """
        Identify strong areas from interview and aptitude
        evaluation scores.
        """

        strengths = []

        score_breakdown = interview_evaluation.get(
            "score_breakdown",
            {},
        )

        if (
            self._extract_score(
                interview_evaluation,
                "interview_score",
            )
            >= self.config["strength_thresholds"][
                "strong_score"
            ]
        ):
            strengths.append(
                "Strong overall HR interview performance"
            )

        if (
            self._extract_score(
                score_breakdown,
                "answer_relevance",
            )
            >= self.config["strength_thresholds"][
                "strong_score"
            ]
        ):
            strengths.append(
                "Strong answer relevance"
            )

        if (
            self._extract_score(
                score_breakdown,
                "communication",
            )
            >= self.config["strength_thresholds"][
                "strong_score"
            ]
        ):
            strengths.append(
                "Strong communication skills"
            )

        if (
            self._extract_score(
                score_breakdown,
                "confidence",
            )
            >= self.config["strength_thresholds"][
                "strong_score"
            ]
        ):
            strengths.append(
                "Strong confidence indicators"
            )

        if aptitude_evaluation:
            aptitude_score = self._extract_score(
                aptitude_evaluation,
                "aptitude_score",
            )

            if (
                aptitude_score
                >= self.config["strength_thresholds"][
                    "strong_score"
                ]
            ):
                strengths.append(
                    "Strong logical and problem-solving ability"
                )

        return strengths

    def identify_weaknesses(
        self,
        interview_evaluation: Dict[str, Any],
        aptitude_evaluation: Optional[
            Dict[str, Any]
        ] = None,
    ) -> List[str]:
        """
        Identify areas where evaluation scores indicate
        potential improvement.
        """

        weaknesses = []

        score_breakdown = interview_evaluation.get(
            "score_breakdown",
            {},
        )

        strong_threshold = self.config[
            "strength_thresholds"
        ]["strong_score"]

        metrics = {
            "answer_relevance": "Answer relevance",
            "communication": "Communication",
            "confidence": "Confidence",
            "consistency": "Consistency",
        }

        for metric, label in metrics.items():
            score = self._extract_score(
                score_breakdown,
                metric,
            )

            if 0 < score < strong_threshold:
                weaknesses.append(
                    f"{label} could be improved"
                )

        if aptitude_evaluation:
            aptitude_score = self._extract_score(
                aptitude_evaluation,
                "aptitude_score",
            )

            if 0 < aptitude_score < strong_threshold:
                weaknesses.append(
                    "Logical reasoning and problem-solving "
                    "could be improved"
                )

        return weaknesses

    def identify_cultural_fit_indicators(
        self,
        answers: List[Dict[str, Any]],
    ) -> List[str]:
        """
        Detect observable workplace collaboration and
        adaptability indicators from candidate responses.
        """

        combined_text = " ".join(
            str(item.get("answer", ""))
            for item in answers
            if isinstance(item, dict)
        )

        normalized = self._normalize_text(
            combined_text
        )

        detected = []

        for indicator in self.config[
            "cultural_fit_indicators"
        ]:
            if re.search(
                rf"\b{re.escape(indicator)}\b",
                normalized,
            ):
                detected.append(indicator)

        return detected

    def identify_risk_flags(
        self,
        interview_evaluation: Dict[str, Any],
        answers: List[Dict[str, Any]],
        aptitude_evaluation: Optional[
            Dict[str, Any]
        ] = None,
    ) -> List[str]:
        """
        Identify observable interview risk indicators.
        """

        risks = []

        score_breakdown = interview_evaluation.get(
            "score_breakdown",
            {},
        )

        if (
            self._extract_score(
                score_breakdown,
                "confidence",
            )
            < self.config["risk_thresholds"][
                "low_confidence"
            ]
        ):
            risks.append(
                "Low confidence indicators"
            )

        if (
            self._extract_score(
                score_breakdown,
                "communication",
            )
            < self.config["risk_thresholds"][
                "low_communication"
            ]
        ):
            risks.append(
                "Communication signals require improvement"
            )

        if (
            aptitude_evaluation
            and self._extract_score(
                aptitude_evaluation,
                "aptitude_score",
            )
            < self.config["risk_thresholds"][
                "low_aptitude"
            ]
        ):
            risks.append(
                "Low aptitude and problem-solving indicators"
            )

        combined_text = " ".join(
            str(item.get("answer", ""))
            for item in answers
            if isinstance(item, dict)
        )

        normalized = self._normalize_text(
            combined_text
        )

        for indicator in self.config[
            "risk_indicators"
        ]:
            if re.search(
                rf"\b{re.escape(indicator)}\b",
                normalized,
            ):
                risks.append(
                    f"Potential risk indicator: {indicator}"
                )

        return list(dict.fromkeys(risks))

    def identify_inconsistencies(
        self,
        interview_evaluation: Dict[str, Any],
    ) -> List[str]:
        """
        Identify potential consistency concerns from
        interview score breakdown.
        """

        inconsistencies = []

        score_breakdown = interview_evaluation.get(
            "score_breakdown",
            {},
        )

        consistency_score = self._extract_score(
            score_breakdown,
            "consistency",
        )

        threshold = self.config["risk_thresholds"][
            "high_inconsistency"
        ]

        if consistency_score < threshold:
            inconsistencies.append(
                "Significant inconsistency detected "
                "between interview responses"
            )

        return inconsistencies

    def summarize_overall_performance(
        self,
        interview_evaluation: Dict[str, Any],
        aptitude_evaluation: Optional[
            Dict[str, Any]
        ] = None,
    ) -> str:
        """
        Produce a concise overall HR performance statement.
        """

        interview_score = self._extract_score(
            interview_evaluation,
            "interview_score",
        )

        if aptitude_evaluation:
            aptitude_score = self._extract_score(
                aptitude_evaluation,
                "aptitude_score",
            )

            combined_score = round(
                (interview_score + aptitude_score)
                / 2,
                2,
            )
        else:
            combined_score = interview_score

        if combined_score >= 80:
            return "Excellent overall HR performance"

        if combined_score >= 65:
            return "Good overall HR performance"

        if combined_score >= 50:
            return "Moderate overall HR performance"

        return "Overall HR performance needs improvement"

    def generate_natural_language_summary(
        self,
        candidate_name: str,
        interview_evaluation: Dict[str, Any],
        strengths: List[str],
        weaknesses: List[str],
        risks: List[str],
        aptitude_evaluation: Optional[
            Dict[str, Any]
        ] = None,
    ) -> str:
        """
        Generate a recruiter-readable natural-language
        interview summary.
        """

        interview_score = self._extract_score(
            interview_evaluation,
            "interview_score",
        )

        interview_level = interview_evaluation.get(
            "interview_level",
            "needs_improvement",
        )

        summary = (
            f"{candidate_name} achieved an HR interview "
            f"score of {interview_score:.2f}, classified as "
            f"{interview_level.replace('_', ' ')}."
        )

        if aptitude_evaluation:
            aptitude_score = self._extract_score(
                aptitude_evaluation,
                "aptitude_score",
            )

            summary += (
                f" The aptitude evaluation score was "
                f"{aptitude_score:.2f}."
            )

        if strengths:
            summary += (
                " Key strengths include "
                + ", ".join(strengths[:3])
                + "."
            )

        if weaknesses:
            summary += (
                " Areas for improvement include "
                + ", ".join(weaknesses[:3])
                + "."
            )

        if risks:
            summary += (
                " Recruiters should review the following "
                "risk indicators: "
                + ", ".join(risks[:3])
                + "."
            )
        else:
            summary += (
                " No major observable risk indicators "
                "were identified."
            )

        return summary

    def determine_recommendation(
        self,
        interview_evaluation: Dict[str, Any],
        aptitude_evaluation: Optional[
            Dict[str, Any]
        ] = None,
    ) -> str:
        """
        Generate a recruiter-oriented recommendation.
        """

        interview_score = self._extract_score(
            interview_evaluation,
            "interview_score",
        )

        if aptitude_evaluation:
            aptitude_score = self._extract_score(
                aptitude_evaluation,
                "aptitude_score",
            )

            overall_score = (
                interview_score + aptitude_score
            ) / 2
        else:
            overall_score = interview_score

        if overall_score >= 80:
            return "Strongly Recommended"

        if overall_score >= 65:
            return "Recommended"

        if overall_score >= 50:
            return "Consider with Review"

        return "Not Recommended"

    def generate_report(
        self,
        candidate_name: str,
        job_role: str,
        answers: List[Dict[str, Any]],
        interview_evaluation: Dict[str, Any],
        aptitude_evaluation: Optional[
            Dict[str, Any]
        ] = None,
    ) -> Dict[str, Any]:
        """
        Generate the complete structured interview summary.
        """

        if not isinstance(answers, list):
            raise TypeError(
                "Answers must be provided as a list."
            )

        if not isinstance(
            interview_evaluation,
            dict,
        ):
            raise TypeError(
                "Interview evaluation must be a dictionary."
            )

        strengths = self.identify_strengths(
            interview_evaluation,
            aptitude_evaluation,
        )

        weaknesses = self.identify_weaknesses(
            interview_evaluation,
            aptitude_evaluation,
        )

        cultural_fit = (
            self.identify_cultural_fit_indicators(
                answers
            )
        )

        risks = self.identify_risk_flags(
            interview_evaluation,
            answers,
            aptitude_evaluation,
        )

        inconsistencies = (
            self.identify_inconsistencies(
                interview_evaluation
            )
        )

        overall_performance = (
            self.summarize_overall_performance(
                interview_evaluation,
                aptitude_evaluation,
            )
        )

        natural_language_summary = (
            self.generate_natural_language_summary(
                candidate_name,
                interview_evaluation,
                strengths,
                weaknesses,
                risks,
                aptitude_evaluation,
            )
        )

        interview_breakdown = (
            interview_evaluation.get(
                "score_breakdown",
                {},
            )
        )

        evaluation = {
            "interview_score": self._extract_score(
                interview_evaluation,
                "interview_score",
            ),
            "interview_level": interview_evaluation.get(
                "interview_level",
                "needs_improvement",
            ),
            "aptitude_score": (
                self._extract_score(
                    aptitude_evaluation or {},
                    "aptitude_score",
                )
            ),
            "aptitude_level": (
                (aptitude_evaluation or {}).get(
                    "aptitude_level",
                    "not_evaluated",
                )
            ),
            "communication_score": (
                self._extract_score(
                    interview_breakdown,
                    "communication",
                )
            ),
            "confidence_score": (
                self._extract_score(
                    interview_breakdown,
                    "confidence",
                )
            ),
            "consistency_score": (
                self._extract_score(
                    interview_breakdown,
                    "consistency",
                )
            ),
        }

        return {
            "report_type": (
                "AI Interview Summary Report"
            ),
            "candidate": {
                "name": candidate_name,
                "role": job_role,
            },
            "summary": {
                "overall_performance": (
                    overall_performance
                ),
                "natural_language_summary": (
                    natural_language_summary
                ),
            },
            "evaluation": evaluation,
            "insights": {
                "strengths": strengths,
                "weaknesses": weaknesses,
                "cultural_fit_indicators": cultural_fit,
                "risk_flags": risks,
                "inconsistencies": inconsistencies,
            },
            "recommendation": (
                self.determine_recommendation(
                    interview_evaluation,
                    aptitude_evaluation,
                )
            ),
        }

    @staticmethod
    def generate_text_report(
        report: Dict[str, Any],
    ) -> str:
        """
        Convert the structured report into a recruiter-readable
        text report.
        """

        candidate = report.get(
            "candidate",
            {},
        )

        summary = report.get(
            "summary",
            {},
        )

        evaluation = report.get(
            "evaluation",
            {},
        )

        insights = report.get(
            "insights",
            {},
        )

        lines = [
            "AI INTERVIEW SUMMARY REPORT",
            "=" * 32,
            "",
            f"Candidate: {candidate.get('name', '')}",
            f"Role: {candidate.get('role', '')}",
            "",
            "OVERALL PERFORMANCE",
            summary.get(
                "overall_performance",
                "",
            ),
            "",
            "EVALUATION",
            f"Interview Score: {evaluation.get('interview_score', 0.0)}",
            f"Interview Level: {evaluation.get('interview_level', '')}",
            f"Aptitude Score: {evaluation.get('aptitude_score', 0.0)}",
            f"Aptitude Level: {evaluation.get('aptitude_level', '')}",
            f"Communication Score: {evaluation.get('communication_score', 0.0)}",
            f"Confidence Score: {evaluation.get('confidence_score', 0.0)}",
            f"Consistency Score: {evaluation.get('consistency_score', 0.0)}",
            "",
            "STRENGTHS",
        ]

        lines.extend(
            f"- {item}"
            for item in insights.get(
                "strengths",
                [],
            )
        )

        lines.append("")
        lines.append("WEAKNESSES")

        lines.extend(
            f"- {item}"
            for item in insights.get(
                "weaknesses",
                [],
            )
        )

        lines.append("")
        lines.append("CULTURAL FIT INDICATORS")

        lines.extend(
            f"- {item}"
            for item in insights.get(
                "cultural_fit_indicators",
                [],
            )
        )

        lines.append("")
        lines.append("RISK FLAGS")

        lines.extend(
            f"- {item}"
            for item in insights.get(
                "risk_flags",
                [],
            )
        )

        lines.append("")
        lines.append("INCONSISTENCIES")

        lines.extend(
            f"- {item}"
            for item in insights.get(
                "inconsistencies",
                [],
            )
        )

        lines.extend(
            [
                "",
                "RECOMMENDATION",
                report.get(
                    "recommendation",
                    "",
                ),
                "",
                "NATURAL-LANGUAGE SUMMARY",
                summary.get(
                    "natural_language_summary",
                    "",
                ),
            ]
        )

        return "\n".join(lines)
