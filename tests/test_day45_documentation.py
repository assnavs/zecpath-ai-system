from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "day45"


def test_day45_documents_exist_and_are_substantive():
    expected = (
        "hr_interview_demo.md",
        "feedback_and_improvements.md",
        "system_handover.md",
    )

    for name in expected:
        path = DOCS / name
        assert path.is_file(), f"Missing Day 45 document: {name}"
        assert path.stat().st_size > 1000


def test_demo_contains_all_candidates_and_benchmark_results():
    content = (DOCS / "hr_interview_demo.md").read_text(encoding="utf-8")

    for expected in (
        "Ananya Menon",
        "Rahul Nair",
        "Arjun Kumar",
        "Meera Thomas",
        "25%",
        "16.79",
        "15.35",
        "human recruiter review",
    ):
        assert expected.lower() in content.lower()


def test_documents_match_scoring_configuration():
    config = json.loads(
        (ROOT / "data" / "hr_interview_scoring_configuration.json")
        .read_text(encoding="utf-8-sig")
    )

    demo = (DOCS / "hr_interview_demo.md").read_text(encoding="utf-8")
    handover = (DOCS / "system_handover.md").read_text(encoding="utf-8")

    for key in (
        "answer_relevance",
        "communication",
        "confidence",
        "consistency",
    ):
        percentage = f"{round(config['weights'][key] * 100)}%"
        assert percentage in demo
        assert percentage in handover

    for label, value in config["thresholds"].items():
        assert str(value) in demo
        assert label.capitalize() in demo


def test_handover_contains_test_commands_and_safeguards():
    content = (DOCS / "system_handover.md").read_text(encoding="utf-8")

    assert "python -m pytest -q" in content
    assert "human recruiter" in content.lower()
    assert "25%" in content
    assert "production accuracy" in content.lower()


def test_improvement_plan_distinguishes_proposals_from_results():
    content = (
        DOCS / "feedback_and_improvements.md"
    ).read_text(encoding="utf-8")

    assert "Prioritized Improvement Plan" in content
    assert "held-out test data" in content
    assert "human review" in content.lower()
    assert "proposed goals, not achieved results" in content.lower()