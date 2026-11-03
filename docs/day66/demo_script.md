# Day 66 — Final AI System Demonstration Script

**Target duration:** 10–12 minutes  
**Audience:** Internship guide, technical reviewer, recruiter/stakeholder  
**Dataset:** `data/demo/day63_hiring_pipeline_demo.json` (synthetic records only)

## 1. Opening (45 seconds)
"Good morning. I will demonstrate the Zecpath AI System, a modular recruitment decision-support prototype. It organizes resume evaluation, screening, interview assessments, technical tasks and a consolidated recruiter-facing recommendation. The system supports human review; it does not autonomously hire or reject candidates."

## 2. Problem statement (1 minute)
Recruitment workflows can involve repeated manual review, inconsistent evaluation formats and fragmented information across stages. This prototype explores a structured workflow with traceable stage scores and a consolidated view. Do not claim measured time savings or improved hiring accuracy; no production outcome study is included.

## 3. Architecture (2 minutes)
Walk through `hiring_pipeline_flow.mmd` and `ai_modules_flow.mmd`.
- Parsing modules normalize resume and job-description content.
- ATS scoring evaluates configured resume/job fit inputs.
- Screening, HR interview, technical interview and machine-test modules return rubric/rule-based scores.
- Cross-round aggregation applies role-specific weights and renormalizes available rounds.
- Recommendation logic uses score thresholds, coverage and supplied risk flags.
- Recruiter formatter presents the outputs without changing scores.
- Observability utilities provide in-process events/metrics/audit metadata only.

## 4. Live synthetic demo (3–4 minutes)
Run from repository root:
```powershell
python scripts/run_final_demo.py
```
Explain that the simulator receives structured stage inputs. It does not perform a live resume upload, invoke a speech model, execute candidate-submitted code or prove model accuracy. Compare all three synthetic candidate summaries and explain why "Hold / Review" is not a final hiring decision.

## 5. Scoring explanation (1 minute)
Describe the configured role-weighted average, missing-round coverage and the recommendation thresholds. State that the confidence field is a coverage-based heuristic, not a probability. Do not alter weights or thresholds during the demo.

## 6. Business impact (1 minute)
Potential value: a consistent evidence summary, clearer hand-offs, easier review of stage coverage and more explainable recruiter discussions. These are intended workflow benefits, not measured business results.

## 7. Close and handover (1 minute)
Show README setup instructions, tests, docs and roadmap. Invite questions. Reiterate that authorized human reviewers own the final decision and should consider source evidence, accommodations and context.
