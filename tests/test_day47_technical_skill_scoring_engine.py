import pytest
from scoring.technical_skill_scoring_engine import TechnicalSkillScoringEngine

def test_empty_answer():
    assert TechnicalSkillScoringEngine().score_answer("")["raw_score"] == 0

def test_expected_concept_coverage():
    r = TechnicalSkillScoringEngine().score_answer("Python uses lists and dictionaries", expected_concepts=["Python", "lists", "SQL"])
    assert r["dimension_scores"]["accuracy"] == pytest.approx(66.67, abs=.01)

def test_depth_and_explanation():
    r = TechnicalSkillScoringEngine().score_answer("First compare trade-offs, test edge case, monitor production performance.")
    assert r["answer_depth"] in {"developing", "deep"}
    assert r["explanations"]["depth"]

def test_difficulty_reference():
    e = TechnicalSkillScoringEngine()
    assert e.score_answer("Detailed answer for testing production.", difficulty="advanced")["difficulty_reference_score"] == 70

def test_rubric_override():
    d = {"accuracy": 80, "depth": 70, "logical_reasoning": 60, "real_world_applicability": 50}
    assert TechnicalSkillScoringEngine().score_answer("x", rubric_scores=d)["dimension_scores"] == d

def test_bad_question_type():
    with pytest.raises(ValueError): TechnicalSkillScoringEngine().score_answer("x", question_type="essay")

def test_interview_breakdown():
    r = TechnicalSkillScoringEngine().score_interview([{"answer": "Python list and dictionary", "skill": "Python", "expected_concepts": ["Python"]}])
    assert r["response_count"] == 1 and "Python" in r["skill_breakdown"]
