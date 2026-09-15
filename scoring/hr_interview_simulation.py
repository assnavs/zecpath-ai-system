import json
from pathlib import Path
from typing import Any, Dict, List

from interview_ai.interview import InterviewAI
from interview_ai.follow_up_engine import DynamicFollowUpEngine
from scoring.hr_interview_scoring_engine import (
    HRInterviewScoringEngine,
)
from scoring.aptitude_logic_engine import (
    AptitudeLogicEngine,
)
from scoring.interview_summary_generator import (
    InterviewSummaryGenerator,
)


class HRInterviewSimulationEngine:
    """
    Day 40 end-to-end HR interview simulation engine.

    Simulates multiple candidate types through the existing
    interview, follow-up, scoring, aptitude, and summary
    components.

    Candidate profiles:
    - Confident
    - Hesitant
    - Inexperienced
    - Overqualified

    The manual evaluation values are benchmark/reference
    values used only for simulation comparison. They are
    not ground-truth psychological or hiring labels.
    """

    REPORT_PATH = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "hr_interview_simulation_report.json"
    )

    CANDIDATES = [
        {
            "candidate_name": "Ananya Menon",
            "candidate_type": "confident",
            "role": "Data Analyst",
            "experience_level": "experienced",
            "manual_evaluation": {
                "interview_score": 90.0,
                "aptitude_score": 88.0,
                "performance_level": "excellent",
            },
            "answers": [
                {
                    "question": (
                        "Tell me about your experience with "
                        "data analysis."
                    ),
                    "answer": (
                        "I have successfully worked on data analysis "
                        "projects using Python and SQL. I clearly "
                        "explained my approach and communicated "
                        "results with my team."
                    ),
                    "expected_keywords": [
                        "data",
                        "analysis",
                        "python",
                        "sql",
                    ],
                    "aptitude_keywords": [
                        "data",
                        "analysis",
                    ],
                    "aptitude_actions": [
                        "analyze",
                        "communicate",
                    ],
                },
                {
                    "question": (
                        "How would you handle an unexpected "
                        "data quality problem?"
                    ),
                    "answer": (
                        "First I identify the cause, then analyze "
                        "the affected data and compare possible "
                        "solutions. I communicate the issue to "
                        "the team and verify the final result."
                    ),
                    "expected_keywords": [
                        "data",
                        "problem",
                        "solution",
                    ],
                    "aptitude_keywords": [
                        "cause",
                        "data",
                        "solution",
                    ],
                    "aptitude_actions": [
                        "analyze",
                        "communicate",
                        "verify",
                    ],
                },
                {
                    "question": (
                        "How do you work with feedback from a team?"
                    ),
                    "answer": (
                        "I consider feedback carefully, communicate "
                        "with the team, adapt my approach, and improve "
                        "the final result."
                    ),
                    "expected_keywords": [
                        "feedback",
                        "team",
                        "communicate",
                    ],
                    "aptitude_keywords": [
                        "feedback",
                        "team",
                    ],
                    "aptitude_actions": [
                        "communicate",
                        "improve",
                    ],
                },
            ],
        },
        {
            "candidate_name": "Rahul Nair",
            "candidate_type": "hesitant",
            "role": "Data Analyst",
            "experience_level": "fresher",
            "manual_evaluation": {
                "interview_score": 55.0,
                "aptitude_score": 52.0,
                "performance_level": "moderate",
            },
            "answers": [
                {
                    "question": (
                        "Tell me about your experience with "
                        "data analysis."
                    ),
                    "answer": (
                        "I think I have maybe worked on some "
                        "Python projects, but I am not sure "
                        "how to explain everything."
                    ),
                    "expected_keywords": [
                        "data",
                        "analysis",
                        "python",
                    ],
                    "aptitude_keywords": [
                        "data",
                        "analysis",
                    ],
                    "aptitude_actions": [
                        "analyze",
                    ],
                },
                {
                    "question": (
                        "How would you handle an unexpected "
                        "data quality problem?"
                    ),
                    "answer": (
                        "Maybe I would check the problem first, "
                        "then I think I would try to find a solution."
                    ),
                    "expected_keywords": [
                        "problem",
                        "solution",
                    ],
                    "aptitude_keywords": [
                        "problem",
                        "solution",
                    ],
                    "aptitude_actions": [
                        "check",
                        "solve",
                    ],
                },
                {
                    "question": (
                        "How do you work with feedback from a team?"
                    ),
                    "answer": (
                        "I guess feedback is useful and I would "
                        "probably try to improve."
                    ),
                    "expected_keywords": [
                        "feedback",
                        "improve",
                    ],
                    "aptitude_keywords": [
                        "feedback",
                        "improve",
                    ],
                    "aptitude_actions": [
                        "improve",
                    ],
                },
            ],
        },
        {
            "candidate_name": "Arjun Kumar",
            "candidate_type": "inexperienced",
            "role": "Data Analyst",
            "experience_level": "fresher",
            "manual_evaluation": {
                "interview_score": 50.0,
                "aptitude_score": 48.0,
                "performance_level": "moderate",
            },
            "answers": [
                {
                    "question": (
                        "Tell me about your experience with "
                        "data analysis."
                    ),
                    "answer": (
                        "I completed a college project using "
                        "Python and learned basic data analysis."
                    ),
                    "expected_keywords": [
                        "python",
                        "data",
                        "analysis",
                    ],
                    "aptitude_keywords": [
                        "data",
                        "analysis",
                    ],
                    "aptitude_actions": [
                        "learn",
                    ],
                },
                {
                    "question": (
                        "How would you handle an unexpected "
                        "data quality problem?"
                    ),
                    "answer": (
                        "I would first understand the problem and "
                        "ask an experienced team member for guidance."
                    ),
                    "expected_keywords": [
                        "problem",
                        "guidance",
                    ],
                    "aptitude_keywords": [
                        "problem",
                    ],
                    "aptitude_actions": [
                        "understand",
                    ],
                },
                {
                    "question": (
                        "How do you work with feedback from a team?"
                    ),
                    "answer": (
                        "I listen to feedback and try to learn "
                        "from the team so I can improve."
                    ),
                    "expected_keywords": [
                        "feedback",
                        "team",
                        "learn",
                    ],
                    "aptitude_keywords": [
                        "feedback",
                        "learn",
                    ],
                    "aptitude_actions": [
                        "learn",
                        "improve",
                    ],
                },
            ],
        },
        {
            "candidate_name": "Meera Thomas",
            "candidate_type": "overqualified",
            "role": "Data Analyst",
            "experience_level": "experienced",
            "manual_evaluation": {
                "interview_score": 75.0,
                "aptitude_score": 82.0,
                "performance_level": "good",
            },
            "answers": [
                {
                    "question": (
                        "Tell me about your experience with "
                        "data analysis."
                    ),
                    "answer": (
                        "I have extensive experience in data analysis, "
                        "Python, SQL, reporting, and analytical projects. "
                        "I have also led several technical initiatives."
                    ),
                    "expected_keywords": [
                        "data",
                        "analysis",
                        "python",
                        "sql",
                    ],
                    "aptitude_keywords": [
                        "data",
                        "analysis",
                    ],
                    "aptitude_actions": [
                        "analyze",
                    ],
                },
                {
                    "question": (
                        "How would you handle an unexpected "
                        "data quality problem?"
                    ),
                    "answer": (
                        "I would identify the root cause, evaluate "
                        "alternative solutions, prioritize business "
                        "impact, communicate the risk, and verify "
                        "the corrected result."
                    ),
                    "expected_keywords": [
                        "problem",
                        "solutions",
                        "impact",
                        "communicate",
                    ],
                    "aptitude_keywords": [
                        "cause",
                        "solutions",
                        "impact",
                    ],
                    "aptitude_actions": [
                        "evaluate",
                        "prioritize",
                        "communicate",
                        "verify",
                    ],
                },
                {
                    "question": (
                        "How do you work with feedback from a team?"
                    ),
                    "answer": (
                        "I use feedback to improve processes, support "
                        "the team, and adapt when project requirements "
                        "change."
                    ),
                    "expected_keywords": [
                        "feedback",
                        "team",
                        "improve",
                    ],
                    "aptitude_keywords": [
                        "feedback",
                        "team",
                    ],
                    "aptitude_actions": [
                        "improve",
                        "adapt",
                    ],
                },
            ],
        },
    ]

    def __init__(self):
        self.interview_engine = HRInterviewScoringEngine()
        self.aptitude_engine = AptitudeLogicEngine()
        self.summary_generator = InterviewSummaryGenerator()

    @staticmethod
    def _classify_score(score: float) -> str:
        if score >= 80:
            return "excellent"

        if score >= 65:
            return "good"

        if score >= 50:
            return "moderate"

        return "needs_improvement"

    @staticmethod
    def _safe_number(
        value: Any,
        default: float = 0.0,
    ) -> float:
        try:
            return round(float(value), 2)
        except (TypeError, ValueError):
            return default

    def simulate_session(
        self,
        candidate: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Run one complete simulated interview session.
        """

        interview = InterviewAI(
            role=candidate["role"],
            experience_level=candidate[
                "experience_level"
            ],
        )

        interview_state = interview.start_interview()

        follow_up_engine = DynamicFollowUpEngine()

        responses = []
        follow_up_events = []

        for item in candidate["answers"]:
            response = item["answer"]

            interview.capture_response(response)

            follow_up_result = (
                follow_up_engine.analyze_response(
                    response
                )
            )

            follow_up_eligible = (
                follow_up_engine.should_continue(
                    response
                )
            )

            follow_up_events.append(
                {
                    "response": response,
                    "follow_up_eligible": (
                        follow_up_eligible
                    ),
                    "analysis": follow_up_result,
                }
            )

            responses.append(
                {
                    "answer": response,
                    "expected_keywords": item[
                        "expected_keywords"
                    ],
                }
            )

        interview_evaluation = (
            self.interview_engine.score_interview(
                responses
            )
        )

        aptitude_responses = [
            {
                "answer": item["answer"],
                "expected_keywords": item[
                    "aptitude_keywords"
                ],
                "expected_actions": item[
                    "aptitude_actions"
                ],
            }
            for item in candidate["answers"]
        ]

        aptitude_evaluation = (
            self.aptitude_engine.evaluate_interview(
                aptitude_responses
            )
        )

        summary = self.summary_generator.generate_report(
            candidate_name=candidate["candidate_name"],
            job_role=candidate["role"],
            answers=responses,
            interview_evaluation=interview_evaluation,
            aptitude_evaluation=aptitude_evaluation,
        )

        return {
            "candidate_name": candidate[
                "candidate_name"
            ],
            "candidate_type": candidate[
                "candidate_type"
            ],
            "role": candidate["role"],
            "experience_level": candidate[
                "experience_level"
            ],
            "interview_state": interview_state,
            "follow_up_events": follow_up_events,
            "interview_evaluation": interview_evaluation,
            "aptitude_evaluation": aptitude_evaluation,
            "summary": summary,
        }

    def compare_with_manual_evaluation(
        self,
        simulation: Dict[str, Any],
        manual: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Compare AI simulation output with reference/manual
        evaluation values.
        """

        ai_interview = self._safe_number(
            simulation["interview_evaluation"].get(
                "interview_score"
            )
        )

        ai_aptitude = self._safe_number(
            simulation["aptitude_evaluation"].get(
                "aptitude_score"
            )
        )

        manual_interview = self._safe_number(
            manual.get("interview_score")
        )

        manual_aptitude = self._safe_number(
            manual.get("aptitude_score")
        )

        interview_error = round(
            abs(ai_interview - manual_interview),
            2,
        )

        aptitude_error = round(
            abs(ai_aptitude - manual_aptitude),
            2,
        )

        ai_level = self._classify_score(
            ai_interview
        )

        manual_level = manual.get(
            "performance_level",
            "needs_improvement",
        )

        return {
            "ai_interview_score": ai_interview,
            "manual_interview_score": manual_interview,
            "interview_absolute_error": interview_error,
            "ai_aptitude_score": ai_aptitude,
            "manual_aptitude_score": manual_aptitude,
            "aptitude_absolute_error": aptitude_error,
            "ai_performance_level": ai_level,
            "manual_performance_level": manual_level,
            "classification_agreement": (
                ai_level == manual_level
            ),
        }

    def identify_scoring_inconsistencies(
        self,
        comparison: Dict[str, Any],
    ) -> List[str]:
        """
        Identify meaningful differences between AI and
        manual/reference scores.
        """

        inconsistencies = []

        if comparison[
            "interview_absolute_error"
        ] > 15:
            inconsistencies.append(
                "Interview score differs from manual "
                "evaluation by more than 15 points"
            )

        if comparison[
            "aptitude_absolute_error"
        ] > 15:
            inconsistencies.append(
                "Aptitude score differs from manual "
                "evaluation by more than 15 points"
            )

        if not comparison[
            "classification_agreement"
        ]:
            inconsistencies.append(
                "AI performance classification differs "
                "from the manual reference classification"
            )

        return inconsistencies

    def generate_improvement_recommendations(
        self,
        results: List[Dict[str, Any]],
    ) -> List[str]:
        """
        Generate system-level recommendations based on
        simulation results.
        """

        recommendations = []

        classification_matches = sum(
            1
            for result in results
            if result["comparison"][
                "classification_agreement"
            ]
        )

        total = len(results)

        if total and classification_matches < total:
            recommendations.append(
                "Review score thresholds and candidate "
                "classification boundaries using a larger "
                "manually evaluated benchmark set."
            )

        interview_errors = [
            result["comparison"][
                "interview_absolute_error"
            ]
            for result in results
        ]

        aptitude_errors = [
            result["comparison"][
                "aptitude_absolute_error"
            ]
            for result in results
        ]

        if interview_errors and max(interview_errors) > 10:
            recommendations.append(
                "Calibrate interview scoring weights against "
                "additional recruiter-reviewed interview samples."
            )

        if aptitude_errors and max(aptitude_errors) > 10:
            recommendations.append(
                "Expand aptitude reasoning indicators and "
                "scenario answer structures beyond keyword-based "
                "matching."
            )

        recommendations.append(
            "Use a larger and more diverse validation dataset "
            "before treating AI scores as production hiring signals."
        )

        recommendations.append(
            "Keep human recruiter review in the decision loop "
            "and use AI output as decision support rather than "
            "an automatic hiring decision."
        )

        return list(dict.fromkeys(recommendations))

    def run_all_simulations(self) -> Dict[str, Any]:
        """
        Run all defined candidate simulations and create the
        final Day 40 evaluation report.
        """

        results = []

        for candidate in self.CANDIDATES:
            simulation = self.simulate_session(
                candidate
            )

            comparison = (
                self.compare_with_manual_evaluation(
                    simulation,
                    candidate["manual_evaluation"],
                )
            )

            inconsistencies = (
                self.identify_scoring_inconsistencies(
                    comparison
                )
            )

            results.append(
                {
                    "candidate": {
                        "name": candidate[
                            "candidate_name"
                        ],
                        "type": candidate[
                            "candidate_type"
                        ],
                        "role": candidate["role"],
                        "experience_level": candidate[
                            "experience_level"
                        ],
                    },
                    "simulation": simulation,
                    "manual_evaluation": candidate[
                        "manual_evaluation"
                    ],
                    "comparison": comparison,
                    "scoring_inconsistencies": (
                        inconsistencies
                    ),
                }
            )

        total = len(results)

        agreement_count = sum(
            1
            for result in results
            if result["comparison"][
                "classification_agreement"
            ]
        )

        classification_accuracy = (
            round(
                (agreement_count / total) * 100,
                2,
            )
            if total
            else 0.0
        )

        interview_mae = round(
            sum(
                result["comparison"][
                    "interview_absolute_error"
                ]
                for result in results
            )
            / total,
            2,
        ) if total else 0.0

        aptitude_mae = round(
            sum(
                result["comparison"][
                    "aptitude_absolute_error"
                ]
                for result in results
            )
            / total,
            2,
        ) if total else 0.0

        report = {
            "report_type": (
                "HR Interview End-to-End Simulation Report"
            ),
            "simulation_count": total,
            "candidate_types": [
                candidate["candidate_type"]
                for candidate in self.CANDIDATES
            ],
            "results": results,
            "accuracy_evaluation": {
                "classification_accuracy": (
                    classification_accuracy
                ),
                "classification_matches": (
                    agreement_count
                ),
                "total_classifications": total,
                "interview_mean_absolute_error": (
                    interview_mae
                ),
                "aptitude_mean_absolute_error": (
                    aptitude_mae
                ),
            },
            "improvement_recommendations": (
                self.generate_improvement_recommendations(
                    results
                )
            ),
        }

        return report

    @staticmethod
    def generate_text_report(
        report: Dict[str, Any],
    ) -> str:
        """
        Convert the structured simulation report into a
        recruiter-readable text report.
        """

        lines = [
            "HR INTERVIEW END-TO-END SIMULATION REPORT",
            "=" * 45,
            "",
            f"Simulation Count: {report.get('simulation_count', 0)}",
            "",
            "CANDIDATE SIMULATIONS",
        ]

        for result in report.get(
            "results",
            [],
        ):
            candidate = result["candidate"]
            comparison = result["comparison"]

            lines.extend(
                [
                    "",
                    f"Candidate: {candidate['name']}",
                    f"Type: {candidate['type']}",
                    f"Role: {candidate['role']}",
                    f"Experience: {candidate['experience_level']}",
                    (
                        "AI Interview Score: "
                        f"{comparison['ai_interview_score']}"
                    ),
                    (
                        "Manual Interview Score: "
                        f"{comparison['manual_interview_score']}"
                    ),
                    (
                        "AI Aptitude Score: "
                        f"{comparison['ai_aptitude_score']}"
                    ),
                    (
                        "Manual Aptitude Score: "
                        f"{comparison['manual_aptitude_score']}"
                    ),
                    (
                        "Classification Agreement: "
                        f"{comparison['classification_agreement']}"
                    ),
                    "Scoring Inconsistencies:",
                ]
            )

            inconsistencies = result.get(
                "scoring_inconsistencies",
                [],
            )

            if inconsistencies:
                lines.extend(
                    f"- {item}"
                    for item in inconsistencies
                )
            else:
                lines.append(
                    "- None detected"
                )

        accuracy = report.get(
            "accuracy_evaluation",
            {},
        )

        lines.extend(
            [
                "",
                "ACCURACY EVALUATION",
                (
                    "Classification Accuracy: "
                    f"{accuracy.get('classification_accuracy', 0.0)}%"
                ),
                (
                    "Interview Mean Absolute Error: "
                    f"{accuracy.get('interview_mean_absolute_error', 0.0)}"
                ),
                (
                    "Aptitude Mean Absolute Error: "
                    f"{accuracy.get('aptitude_mean_absolute_error', 0.0)}"
                ),
                "",
                "IMPROVEMENT RECOMMENDATIONS",
            ]
        )

        recommendations = report.get(
            "improvement_recommendations",
            [],
        )

        lines.extend(
            f"- {item}"
            for item in recommendations
        )

        return "\n".join(lines)

