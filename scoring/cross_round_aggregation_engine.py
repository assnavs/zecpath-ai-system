from typing import Any, Dict, Optional

class CrossRoundAggregationEngine:
    """Role-weighted, explainable aggregation of supplied hiring-round scores."""
    ROUNDS = ("ats", "screening", "hr_interview", "technical_interview", "machine_test")
    DEFAULT_WEIGHTS = {
        "Data Scientist": dict(ats=.20, screening=.10, hr_interview=.15, technical_interview=.30, machine_test=.25),
        "Frontend Developer": dict(ats=.20, screening=.10, hr_interview=.15, technical_interview=.30, machine_test=.25),
        "Backend Developer": dict(ats=.20, screening=.10, hr_interview=.15, technical_interview=.30, machine_test=.25),
        "Business Analyst": dict(ats=.25, screening=.15, hr_interview=.25, technical_interview=.20, machine_test=.15),
        "MERN Developer": dict(ats=.20, screening=.10, hr_interview=.15, technical_interview=.30, machine_test=.25),
        "Java Developer": dict(ats=.20, screening=.10, hr_interview=.15, technical_interview=.30, machine_test=.25),
        "DevOps Engineer": dict(ats=.20, screening=.10, hr_interview=.15, technical_interview=.30, machine_test=.25),
    }

    def __init__(self, role_weights=None):
        self.role_weights = {k: dict(v) for k, v in (role_weights or self.DEFAULT_WEIGHTS).items()}
        for role, weights in self.role_weights.items():
            if set(weights) != set(self.ROUNDS) or any(isinstance(v, bool) or not isinstance(v, (int,float)) or v < 0 for v in weights.values()) or sum(weights.values()) <= 0:
                raise ValueError(f"Invalid weights for {role}")

    def aggregate(self, role: str, round_scores: Dict[str, Any], candidate_id: Optional[str] = None):
        if role not in self.role_weights:
            raise ValueError(f"Unsupported role: {role}")
        if not isinstance(round_scores, dict) or set(round_scores) - set(self.ROUNDS):
            raise ValueError("round_scores must contain supported round names.")
        for k, v in round_scores.items():
            if v is not None and (isinstance(v,bool) or not isinstance(v,(int,float)) or not 0 <= v <= 100):
                raise ValueError(f"{k} score must be between 0 and 100.")
        scores = {k: float(v) for k,v in round_scores.items() if v is not None}
        weights = self.role_weights[role]
        active = sum(weights[k] for k in scores)
        fit = round(sum(scores[k]*weights[k] for k in scores)/active, 2) if active else None
        missing = [k for k in self.ROUNDS if k not in scores]
        return {"candidate_id":candidate_id,"role":role,"hiring_fit_score":fit,"score_scale":"0-100 percent",
                "round_breakdown":{k:{"score":scores.get(k),"configured_weight":weights[k],
                "effective_weight":round(weights[k]/active,4) if k in scores and active else 0.0} for k in self.ROUNDS},
                "included_rounds":list(scores),"missing_rounds":missing,
                "coverage_percent":round(100*len(scores)/len(self.ROUNDS),2),
                "normalization":"weighted average over available rounds; weights renormalized",
                "requires_human_review":True}
