class FinalRecommendationEngine:
    """Explainable recommendation logic; never makes an autonomous hiring decision."""
    def __init__(self, selected_threshold=80, review_threshold=60, minimum_coverage=60):
        if not 0 <= review_threshold <= selected_threshold <= 100 or not 0 <= minimum_coverage <= 100:
            raise ValueError("Invalid recommendation thresholds.")
        self.selected_threshold=float(selected_threshold); self.review_threshold=float(review_threshold)
        self.minimum_coverage=float(minimum_coverage)

    def recommend(self, aggregate, risk_factors=None):
        if not isinstance(aggregate,dict): raise TypeError("aggregate must be a dictionary.")
        score=aggregate.get("hiring_fit_score"); coverage=aggregate.get("coverage_percent",0)
        if score is not None and (isinstance(score,bool) or not isinstance(score,(int,float)) or not 0 <= score <= 100):
            raise ValueError("hiring_fit_score must be 0-100 or None.")
        if isinstance(coverage,bool) or not isinstance(coverage,(int,float)) or not 0 <= coverage <= 100:
            raise ValueError("coverage_percent must be 0-100.")
        risks=risk_factors or []
        if not isinstance(risks,list): raise TypeError("risk_factors must be a list.")
        for r in risks:
            if not isinstance(r,dict) or r.get("severity") not in {"low","medium","high","unverified"}:
                raise ValueError("Each risk factor needs a supported severity.")
        reasons=[]
        if score is None: category="Hold / Review"; reasons.append("No evaluation score is available.")
        elif coverage < self.minimum_coverage: category="Hold / Review"; reasons.append("Evaluation coverage is below minimum.")
        elif any(r["severity"] in {"high","unverified"} for r in risks):
            category="Hold / Review"; reasons.append("A high-severity or unverified risk needs human investigation.")
        elif score >= self.selected_threshold: category="Selected"; reasons.append("Score meets selection threshold.")
        elif score >= self.review_threshold: category="Hold / Review"; reasons.append("Score is within the review band.")
        else: category="Rejected"; reasons.append("Score is below the review threshold.")
        if risks: reasons.append("Risk flags are contextual review inputs, not proof of misconduct.")
        confidence=0.0 if score is None else round(coverage*(1-min(.5,.08*len(risks))),2)
        return {"recommendation":category,"confidence_score":confidence,
                "confidence_basis":"coverage-based heuristic, not statistical probability",
                "hiring_fit_score":score,"coverage_percent":coverage,"risk_factors":risks,
                "explanation":reasons,"decision_status":"recommendation_for_human_review",
                "automated_hiring_decision":False,"human_review_required":True}
