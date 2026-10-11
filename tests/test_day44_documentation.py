from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "day44"


def test_day44_required_documents_exist_and_are_nonempty():
    expected = [
        "hr_ai_architecture.md",
        "api_specification.md",
        "developer_handbook.md",
    ]
    for name in expected:
        path = DOCS / name
        assert path.is_file(), f"Missing Day 44 document: {name}"
        assert path.stat().st_size > 500, f"Document is unexpectedly short: {name}"


def test_architecture_documents_actual_component_paths():
    content = (DOCS / "hr_ai_architecture.md").read_text(encoding="utf-8")
    for path in (
        "interview_ai/interview.py",
        "interview_ai/follow_up_engine.py",
        "scoring/hr_interview_scoring_engine.py",
        "ats_engine/api.py",
    ):
        assert path in content


def test_api_specification_lists_confirmed_routes():
    content = (DOCS / "api_specification.md").read_text(encoding="utf-8")
    for route in (
        "/api/v1/health",
        "/api/v1/resumes/upload",
        "/api/v1/resumes/parse",
        "/api/v1/scoring",
        "/api/v1/shortlisting",
        "/api/v1/jobs/{job_id}",
    ):
        assert route in content


def test_documentation_preserves_scoring_weights_and_limits():
    architecture = (DOCS / "hr_ai_architecture.md").read_text(encoding="utf-8")
    handbook = (DOCS / "developer_handbook.md").read_text(encoding="utf-8")
    assert "35%" in architecture and "25%" in architecture and "15%" in architecture
    assert "35%" in handbook and "25%" in handbook and "15%" in handbook
    assert "two" in architecture.lower()
    assert "human recruiter review" in architecture.lower()


def test_api_contract_json_is_valid_and_versioned():
    contract_path = ROOT / "data" / "api_contracts.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    assert contract["api_version"] == "v1"
    assert contract["base_path"] == "/api/v1"
    assert "health_check" in contract["endpoints"]
