import json
from pathlib import Path
from typing import Any, Dict, List


class AIScreeningReportGenerator:
    """
    AI Screening Report Generator

    Combines existing AI evaluation outputs into a
    recruiter-friendly screening report.

    The report can summarize:
    - Candidate information
    - Key answers
    - Strengths
    - Risks
    - Missing data
    - Salary expectation
    - Availability
    - Skill confirmations
    - ATS evaluation
    - Screening evaluation
    - Communication signals
    - Final recommendation
    """

    def __init__(self):
        pass

    @staticmethod
    def _get_value(
        data: Dict[str, Any],
        *keys: str,
        default: Any = None
    ) -> Any:
        """
        Safely retrieve a value from a dictionary.
        """

        current = data

        for key in keys:
            if not isinstance(current, dict):
                return default

            current = current.get(key)

            if current is None:
                return default

        return current

    def extract_key_answers(
        self,
        answers: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Extract recruiter-friendly key answer information.
        """

        key_answers = []

        for answer in answers or []:
            key_answers.append({
                "question_id": answer.get(
                    "question_id"
                ),
                "question": answer.get(
                    "question"
                ),
                "answer": answer.get(
                    "answer",
                    ""
                ),
                "intent": answer.get(
                    "intent"
                )
            })

        return key_answers

    def identify_strengths(
        self,
        report_data: Dict[str, Any]
    ) -> List[str]:
        """
        Identify positive candidate indicators.
        """

        strengths = []

        ats_evaluation = report_data.get(
            "ats_evaluation",
            {}
        )

        ats_score = ats_evaluation.get(
            "overall_score"
        )

        if isinstance(ats_score, (int, float)):
            if ats_score >= 80:
                strengths.append(
                    "Strong ATS evaluation score"
                )
            elif ats_score >= 70:
                strengths.append(
                    "Good ATS evaluation score"
                )

        confidence_evaluation = report_data.get(
            "confidence_evaluation",
            {}
        )

        confidence_score = confidence_evaluation.get(
            "confidence_score"
        )

        if isinstance(confidence_score, (int, float)):
            if confidence_score >= 75:
                strengths.append(
                    "Strong observable communication signals"
                )
            elif confidence_score >= 50:
                strengths.append(
                    "Moderate observable communication signals"
                )

        skill_confirmations = report_data.get(
            "skill_confirmations",
            []
        )

        if skill_confirmations:
            strengths.append(
                "Relevant skills confirmed during screening"
            )

        availability = report_data.get(
            "availability"
        )

        if availability:
            strengths.append(
                "Candidate availability information provided"
            )

        return strengths

    def identify_risks(
        self,
        report_data: Dict[str, Any]
    ) -> List[str]:
        """
        Identify observable screening risks.
        """

        risks = []

        ats_evaluation = report_data.get(
            "ats_evaluation",
            {}
        )

        ats_score = ats_evaluation.get(
            "overall_score"
        )

        if isinstance(ats_score, (int, float)):
            if ats_score < 60:
                risks.append(
                    "Low ATS evaluation score"
                )
            elif ats_score < 70:
                risks.append(
                    "ATS evaluation requires review"
                )

        confidence_evaluation = report_data.get(
            "confidence_evaluation",
            {}
        )

        confidence_score = confidence_evaluation.get(
            "confidence_score"
        )

        if isinstance(confidence_score, (int, float)):
            if confidence_score < 50:
                risks.append(
                    "Communication signals require improvement"
                )

        communication_signals = confidence_evaluation.get(
            "signals",
            {}
        )

        hesitation = communication_signals.get(
            "hesitation",
            {}
        )

        if hesitation.get(
            "hesitation_count",
            0
        ) > 0:
            risks.append(
                "Hesitation indicators detected"
            )

        uncertainty = communication_signals.get(
            "uncertainty",
            {}
        )

        if uncertainty.get(
            "uncertainty_count",
            0
        ) > 0:
            risks.append(
                "Uncertainty indicators detected"
            )

        return risks

    def identify_missing_data(
        self,
        report_data: Dict[str, Any]
    ) -> List[str]:
        """
        Identify important screening information
        that has not been provided.
        """

        missing_data = []

        if not report_data.get(
            "candidate_name"
        ):
            missing_data.append(
                "Candidate name"
            )

        if not report_data.get(
            "job_role"
        ):
            missing_data.append(
                "Job role"
            )

        if not report_data.get(
            "salary_expectation"
        ):
            missing_data.append(
                "Salary expectation"
            )

        if not report_data.get(
            "availability"
        ):
            missing_data.append(
                "Availability"
            )

        if not report_data.get(
            "skill_confirmations"
        ):
            missing_data.append(
                "Skill confirmations"
            )

        return missing_data

    def determine_recommendation(
        self,
        report_data: Dict[str, Any]
    ) -> str:
        """
        Determine a recruiter-friendly recommendation
        from available screening decisions.
        """

        shortlisting = report_data.get(
            "shortlisting",
            {}
        )

        decision = shortlisting.get(
            "decision"
        )

        if decision:
            return decision

        ats_evaluation = report_data.get(
            "ats_evaluation",
            {}
        )

        ats_score = ats_evaluation.get(
            "overall_score"
        )

        if isinstance(ats_score, (int, float)):
            if ats_score >= 80:
                return "Shortlisted"

            if ats_score >= 60:
                return "Review"

            return "Rejected"

        return "Review"

    def generate_report(
        self,
        report_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate the complete recruiter-friendly
        screening report.
        """

        answers = report_data.get(
            "answers",
            []
        )

        report = {
            "report_type": "AI Screening Report",
            "candidate": {
                "name": report_data.get(
                    "candidate_name"
                ),
                "job_role": report_data.get(
                    "job_role"
                )
            },
            "summary": {
                "key_answers": self.extract_key_answers(
                    answers
                ),
                "strengths": self.identify_strengths(
                    report_data
                ),
                "risks": self.identify_risks(
                    report_data
                ),
                "missing_data": self.identify_missing_data(
                    report_data
                )
            },
            "highlights": {
                "salary_expectation": report_data.get(
                    "salary_expectation"
                ),
                "availability": report_data.get(
                    "availability"
                ),
                "skill_confirmations": report_data.get(
                    "skill_confirmations",
                    []
                )
            },
            "evaluations": {
                "ats": report_data.get(
                    "ats_evaluation",
                    {}
                ),
                "screening": report_data.get(
                    "screening_evaluation",
                    {}
                ),
                "confidence": report_data.get(
                    "confidence_evaluation",
                    {}
                )
            },
            "shortlisting": report_data.get(
                "shortlisting",
                {}
            ),
            "recommendation": self.determine_recommendation(
                report_data
            )
        }

        return report

    def export_json(
        self,
        report: Dict[str, Any],
        output_path: str
    ) -> str:
        """
        Export the generated report as JSON.
        """

        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with path.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False
            )

        return str(path)

    def generate_text_report(
        self,
        report: Dict[str, Any]
    ) -> str:
        """
        Generate an exportable plain-text
        recruiter-friendly report.
        """

        candidate = report.get(
            "candidate",
            {}
        )

        summary = report.get(
            "summary",
            {}
        )

        highlights = report.get(
            "highlights",
            {}
        )

        lines = [
            "AI SCREENING REPORT",
            "=" * 60,
            "",
            f"Candidate: {candidate.get('name')}",
            f"Job Role: {candidate.get('job_role')}",
            "",
            "SUMMARY",
            "-" * 60,
            "",
            "Key Answers:"
        ]

        for answer in summary.get(
            "key_answers",
            []
        ):
            lines.append(
                f"- {answer.get('question_id')}: "
                f"{answer.get('answer')}"
            )

        lines.extend([
            "",
            "Strengths:"
        ])

        for strength in summary.get(
            "strengths",
            []
        ):
            lines.append(
                f"- {strength}"
            )

        lines.extend([
            "",
            "Risks:"
        ])

        for risk in summary.get(
            "risks",
            []
        ):
            lines.append(
                f"- {risk}"
            )

        lines.extend([
            "",
            "Missing Data:"
        ])

        for item in summary.get(
            "missing_data",
            []
        ):
            lines.append(
                f"- {item}"
            )

        lines.extend([
            "",
            "HIGHLIGHTS",
            "-" * 60,
            f"Salary Expectation: "
            f"{highlights.get('salary_expectation')}",
            f"Availability: "
            f"{highlights.get('availability')}",
            f"Skills: "
            f"{', '.join(highlights.get('skill_confirmations', []))}",
            "",
            "RECOMMENDATION",
            "-" * 60,
            str(
                report.get(
                    "recommendation"
                )
            )
        ])

        return "\n".join(lines)
