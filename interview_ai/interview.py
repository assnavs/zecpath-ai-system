import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class InterviewAI:
    """
    Foundational AI HR Interview Engine.

    Day 33 responsibilities:
    - HR interview categories
    - Role-based question generation
    - Fresher / experienced handling
    - Technical / non-technical role classification
    - Interview state management
    - Response capture
    - Follow-up eligibility
    - Conversation phases
    """

    DATASET_PATH = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "hr_screening_dataset.json"
    )

    HR_CATEGORIES = [
        "Self-introduction",
        "Career journey",
        "Strengths & weaknesses",
        "Teamwork & culture fit",
        "Career goals",
        "Availability & commitment",
    ]

    CONVERSATION_PHASES = [
        "introduction",
        "core_hr_questions",
        "role_based_evaluation",
        "closing",
    ]

    TECHNICAL_ROLES = {
        "Data Scientist",
        "Data Analyst",
        "Software Engineer",
        "ML Engineer",
        "AI Engineer",
        "Backend Developer",
        "Frontend Developer",
        "Full Stack Developer",
    }

    def __init__(
        self,
        role: str,
        experience_level: str = "fresher",
    ):
        self.role = role
        self.experience_level = (
            experience_level.strip().lower()
        )

        if self.experience_level not in {
            "fresher",
            "experienced",
        }:
            raise ValueError(
                "experience_level must be "
                "'fresher' or 'experienced'."
            )

        self.dataset = self._load_dataset()

        if role not in self.dataset.get("roles", {}):
            raise ValueError(
                f"Unsupported interview role: {role}"
            )

        self.state = self._create_initial_state()

    def _load_dataset(self) -> Dict[str, Any]:
        with open(
            self.DATASET_PATH,
            "r",
            encoding="utf-8-sig",
        ) as file:
            return json.load(file)

    def _create_initial_state(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "experience_level": self.experience_level,
            "phase": "introduction",
            "question_id": None,
            "response": None,
            "response_received": False,
            "follow_up_eligible": False,
            "completed": False,
        }

    def get_role_type(self) -> str:
        """
        Identify whether the selected role is technical
        or non-technical.
        """

        if self.role in self.TECHNICAL_ROLES:
            return "technical"

        return "non_technical"

    def get_conversation_phases(self) -> List[str]:
        return list(self.CONVERSATION_PHASES)

    def get_hr_categories(self) -> List[str]:
        return list(self.HR_CATEGORIES)

    def generate_questions(self) -> List[Dict[str, Any]]:
        """
        Generate role-based interview questions using
        the existing HR screening dataset.
        """

        base_questions = self.dataset["roles"][self.role]

        questions = []

        for question in base_questions:

            question_copy = dict(question)

            question_copy["role"] = self.role
            question_copy["role_type"] = (
                self.get_role_type()
            )
            question_copy["experience_level"] = (
                self.experience_level
            )

            questions.append(question_copy)

        return questions

    def get_questions_for_phase(
        self,
        phase: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Return questions appropriate for the
        current interview phase.
        """

        current_phase = (
            phase or self.state["phase"]
        )

        questions = self.generate_questions()

        if current_phase == "introduction":
            return [
                question
                for question in questions
                if question["category"]
                == "Introduction"
            ]

        if current_phase == "core_hr_questions":
            return [
                question
                for question in questions
                if question["category"]
                in {
                    "Education",
                    "Experience",
                    "Location",
                    "Salary",
                    "Notice Period",
                }
            ]

        if current_phase == "role_based_evaluation":
            return [
                question
                for question in questions
                if question["category"]
                == "Skills"
            ]

        return []

    def start_interview(self) -> Dict[str, Any]:
        """
        Start the interview and return the first question.
        """

        self.state["phase"] = "introduction"

        questions = self.get_questions_for_phase(
            "introduction"
        )

        if questions:
            self.state["question_id"] = (
                questions[0]["question_id"]
            )

        return {
            "phase": self.state["phase"],
            "question": (
                questions[0]
                if questions
                else None
            ),
            "state": dict(self.state),
        }

    def capture_response(
        self,
        response: str,
    ) -> Dict[str, Any]:
        """
        Capture the candidate response and determine
        whether a follow-up may be appropriate.
        """

        if not isinstance(response, str):
            raise TypeError(
                "Candidate response must be a string."
            )

        cleaned_response = response.strip()

        self.state["response"] = cleaned_response
        self.state["response_received"] = bool(
            cleaned_response
        )

        self.state["follow_up_eligible"] = (
            len(cleaned_response.split()) < 5
        )

        return dict(self.state)

    def move_to_phase(
        self,
        phase: str,
    ) -> Dict[str, Any]:
        """
        Move the interview to a valid conversation phase.
        """

        if phase not in self.CONVERSATION_PHASES:
            raise ValueError(
                f"Unsupported interview phase: {phase}"
            )

        self.state["phase"] = phase
        self.state["question_id"] = None

        questions = self.get_questions_for_phase(
            phase
        )

        if questions:
            self.state["question_id"] = (
                questions[0]["question_id"]
            )

        if phase == "closing":
            self.state["completed"] = True

        return {
            "phase": phase,
            "question": (
                questions[0]
                if questions
                else None
            ),
            "completed": self.state["completed"],
            "state": dict(self.state),
        }

    def get_interview_state(self) -> Dict[str, Any]:
        return dict(self.state)
