from datetime import datetime, timezone

class HiringIntelligenceReportGenerator:
    """Builds a recruiter-friendly report from supplied evaluation results only."""
    SECTIONS=("ats","screening","hr_interview","technical_interview","machine_test","behavioral","integrity")
    def generate(self,candidate,aggregate,recommendation,evaluation_details=None):
        if not all(isinstance(x,dict) for x in (candidate,aggregate,recommendation)):
            raise TypeError("candidate, aggregate and recommendation must be dictionaries.")
        details=evaluation_details or {}
        if not isinstance(details,dict): raise TypeError("evaluation_details must be a dictionary.")
        strengths=[]; weaknesses=[]; risks=[]
        for section in self.SECTIONS:
            value=details.get(section)
            if isinstance(value,dict):
                score=value.get("score")
                if isinstance(score,(int,float)) and not isinstance(score,bool):
                    if score>=75: strengths.append(f"{section}: strong supplied score ({score:.1f}/100)")
                    elif score<50: weaknesses.append(f"{section}: low supplied score ({score:.1f}/100)")
                flags=value.get("risk_flags",[])
                if isinstance(flags,list): risks.extend(flags)
        risks.extend(x.get("description","Unspecified risk") for x in recommendation.get("risk_factors",[]))
        return {"report_type":"candidate_hiring_intelligence","generated_at_utc":datetime.now(timezone.utc).isoformat(),
                "candidate":{k:candidate[k] for k in ("candidate_id","name","role","application_reference") if k in candidate},
                "ats_summary":details.get("ats"),"screening_results":details.get("screening"),
                "hr_insights":details.get("hr_interview"),"technical_performance":details.get("technical_interview"),
                "machine_test_performance":details.get("machine_test"),"behavioral_observations":details.get("behavioral"),
                "integrity_review":details.get("integrity"),"unified_score":aggregate,"strengths":strengths,
                "weaknesses":weaknesses,"risk_indicators":risks,"final_recommendation":recommendation,
                "limitations":["Only supplied data is included; absent rounds are not inferred.",
                "Behavioral and integrity flags require contextual human review.",
                "This report is decision support, not an autonomous hiring decision."]}
