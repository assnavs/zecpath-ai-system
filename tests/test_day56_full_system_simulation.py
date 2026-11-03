import pytest
from utils.hiring_pipeline_simulator import HiringPipelineSimulator

def sample():
    return {"candidate":{"candidate_id":"SIM-001","role":"Data Scientist"},
      "resume_text":"Python SQL machine learning experience",
      "ats_inputs":{"skill_match":85,"experience_relevance":80,"education_alignment":75,"semantic_similarity":82},
      "screening_responses":[{"question_id":"Q1","clarity":8,"relevance":8,"completeness":8,"consistency":8}],
      "hr_answers":[{"answer":"I used Python and SQL to build a data analysis project with clear communication and teamwork."}],
      "technical_responses":[{"answer":"First I would analyze the data, then validate the model with testing and compare trade-offs in production.","question_type":"conceptual","difficulty":"intermediate","expected_concepts":["data","model","testing"]}],
      "machine_submissions":[{"task":{"task_id":"T1","task_type":"coding","time_limit_seconds":600},
        "submission":{"time_used_seconds":300,"tests_passed":8,"tests_total":10,"code_quality_score":80,"problem_solving_approach_score":75}}]}

def test_end_to_end_pipeline_completes():
    result=HiringPipelineSimulator().run(sample(),{"recommendation":"Selected"})
    assert [x["stage"] for x in result["stages"]][-1]=="final_decision"
    assert set(result["round_scores"])=={"ats","screening","hr_interview","technical_interview","machine_test"}
    assert result["human_comparison"]["agreement"] in (True,False)
    assert result["human_review_required"] is True

def test_simulation_discloses_upload_boundary():
    assert "not exercised" in HiringPipelineSimulator().run(sample())["simulation_scope"]

def test_missing_stage_input_is_rejected():
    data=sample(); del data["resume_text"]
    with pytest.raises(ValueError,match="resume_text"):
        HiringPipelineSimulator().run(data)

def test_invalid_human_judgment_is_rejected():
    with pytest.raises(ValueError,match="human_judgment"):
        HiringPipelineSimulator().run(sample(),{"recommendation":"Maybe"})
