"""
Day 22 - HR Screening Dataset Tests
"""

import json
from pathlib import Path


DATASET_PATH = Path("data/hr_screening_dataset.json")


def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def test_dataset_exists():
    assert DATASET_PATH.exists()


def test_required_categories():
    data = load_dataset()

    expected_categories = {
        "Introduction",
        "Education",
        "Experience",
        "Skills",
        "Location",
        "Salary",
        "Notice Period"
    }

    assert set(data["question_categories"]) == expected_categories


def test_multiple_roles():
    data = load_dataset()

    assert len(data["roles"]) >= 3
    assert "Data Scientist" in data["roles"]
    assert "Data Analyst" in data["roles"]
    assert "Software Engineer" in data["roles"]


def test_question_structure():
    data = load_dataset()

    required_fields = {
        "question_id",
        "category",
        "question",
        "expected_answer_type",
        "mandatory",
        "scoring_importance"
    }

    for role, questions in data["roles"].items():
        assert len(questions) == 7

        for question in questions:
            assert required_fields.issubset(question.keys())
            assert question["category"] in data["question_categories"]
            assert isinstance(question["mandatory"], bool)
            assert question["scoring_importance"] in {1, 2, 3}


def test_ai_ready_question_objects():
    data = load_dataset()

    for questions in data["roles"].values():
        for question in questions:
            assert question["question_id"]
            assert question["question"]
            assert question["expected_answer_type"] in {
                "text",
                "number",
                "multiple_choice"
            }


def test_day22_dataset():
    test_dataset_exists()
    test_required_categories()
    test_multiple_roles()
    test_question_structure()
    test_ai_ready_question_objects()

    print("Dataset existence: PASSED")
    print("Question categories: PASSED")
    print("Multiple roles: PASSED")
    print("Question structure: PASSED")
    print("AI-ready question objects: PASSED")
    print()
    print("All Day 22 HR Screening Dataset tests passed successfully!")


if __name__ == "__main__":
    test_day22_dataset()
