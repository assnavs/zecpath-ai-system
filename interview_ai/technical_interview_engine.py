import json
from pathlib import Path
from typing import Any, Dict, List


class TechnicalInterviewEngine:
    """Role-based technical interview flow and question selection."""

    CONFIG_PATH = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "technical_interview_configuration.json"
    )

    def __init__(self, role: str, experience_years: float):
        if not isinstance(role, str) or not role.strip():
            raise ValueError("A valid technical role is required.")

        if isinstance(experience_years, bool) or not isinstance(
            experience_years, (int, float)
        ):
            raise TypeError("Experience years must be numeric.")

        if experience_years < 0:
            raise ValueError("Experience years cannot be negative.")

        with self.CONFIG_PATH.open("r", encoding="utf-8-sig") as file:
            self.config = json.load(file)

        self.role = role.strip()
        self.experience_years = experience_years

        if self.role not in self.config["roles"]:
            raise ValueError(f"Unsupported technical role: {self.role}")

        self.experience_level = self._resolve_experience_level()
        self.role_config = self.config["roles"][self.role]
        self.questions = self._build_question_list()
        self.current_state = self.config["flow"]["initial_state"]
        self.current_question_index = 0
        self.responses: List[Dict[str, Any]] = []

    def _resolve_experience_level(self) -> str:
        if self.experience_years <= 2:
            return "entry"
        if self.experience_years < 5:
            return "intermediate"
        return "advanced"

    def _build_question_list(self) -> List[Dict[str, Any]]:
        questions = []

        for level in self.config["experience_priority"]:
            if level != self.experience_level:
                continue

            questions.extend(
                self.role_config["questions"].get(level, [])
            )

        return [
            {
                **question,
                "role": self.role,
                "experience_level": self.experience_level
            }
            for question in questions
        ]

    def get_role_skills(self) -> List[str]:
        return list(self.role_config["skills"])

    def get_interview_structure(self) -> List[str]:
        return list(self.config["interview_sections"])

    def get_questions(self) -> List[Dict[str, Any]]:
        return [dict(question) for question in self.questions]

    def start_interview(self) -> Dict[str, Any]:
        self.current_state = "introduction"
        self.current_question_index = 0
        self.responses = []

        return {
            "role": self.role,
            "experience_years": self.experience_years,
            "experience_level": self.experience_level,
            "state": self.current_state,
            "question": self.get_current_question(),
            "question_count": len(self.questions)
        }

    def get_current_question(self):
        if self.current_question_index >= len(self.questions):
            return None

        return dict(self.questions[self.current_question_index])

    def submit_response(self, answer: str) -> Dict[str, Any]:
        if self.current_state in {"evaluation", "closing", "completed"}:
            raise RuntimeError("The question session is no longer active.")

        if not isinstance(answer, str):
            raise TypeError("Answer must be a string.")

        question = self.get_current_question()

        if question is None:
            raise RuntimeError("No questions are available.")

        self.responses.append({
            "question": question["question"],
            "skill": question["skill"],
            "difficulty": question["difficulty"],
            "answer": answer.strip()
        })

        self.current_question_index += 1

        return {
            "submitted": True,
            "response_count": len(self.responses),
            "next_question": self.get_current_question()
        }

    def advance_flow(self) -> Dict[str, Any]:
        transitions = self.config["flow"]["transitions"]

        if self.current_state not in transitions:
            raise ValueError(
                f"Unknown interview state: {self.current_state}"
            )

        if self.current_state == "scenario_based" and (
            self.current_question_index < len(self.questions)
        ):
            raise RuntimeError("Complete all questions before evaluation.")

        self.current_state = transitions[self.current_state]

        return self.get_interview_state()

    def get_interview_state(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "experience_level": self.experience_level,
            "state": self.current_state,
            "question_index": self.current_question_index,
            "total_questions": len(self.questions),
            "completed_responses": len(self.responses),
            "completed": self.current_state == "completed"
        }

    def generate_evaluation_input(self) -> Dict[str, Any]:
        return {
            "role": self.role,
            "experience_level": self.experience_level,
            "responses": [dict(item) for item in self.responses]
        }
