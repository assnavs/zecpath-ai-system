import re
from typing import Any, Dict, List, Optional

class TechnicalSkillScoringEngine:
    """Explainable rule-based technical answer scoring baseline."""
    WEIGHTS = {
        "coding": {"accuracy": .40, "depth": .20, "logical_reasoning": .20, "real_world_applicability": .20},
        "debugging": {"accuracy": .30, "depth": .20, "logical_reasoning": .30, "real_world_applicability": .20},
        "conceptual": {"accuracy": .35, "depth": .30, "logical_reasoning": .20, "real_world_applicability": .15},
        "scenario": {"accuracy": .25, "depth": .25, "logical_reasoning": .25, "real_world_applicability": .25},
        "system_design": {"accuracy": .25, "depth": .25, "logical_reasoning": .20, "real_world_applicability": .30},
    }
    DIFFICULTY_REFERENCE = {"basic": 60.0, "intermediate": 65.0, "advanced": 70.0}
    MARKERS = {
        "depth": ("trade-off", "tradeoff", "because", "for example", "production", "edge case", "complexity", "scalability", "testing", "monitoring", "alternative"),
        "logical_reasoning": ("first", "then", "therefore", "because", "compare", "evaluate", "identify", "if", "otherwise"),
        "real_world_applicability": ("production", "user", "customer", "deployment", "monitor", "test", "security", "performance", "database", "api"),
    }

    def score_answer(self, answer: str, question_type: str = "conceptual", difficulty: str = "basic",
                     expected_concepts: Optional[List[str]] = None,
                     rubric_scores: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        if not isinstance(answer, str):
            raise TypeError("Answer must be a string.")
        qtype, level = question_type.lower(), difficulty.lower()
        if qtype not in self.WEIGHTS:
            raise ValueError(f"Unsupported question type: {question_type}")
        if level not in self.DIFFICULTY_REFERENCE:
            raise ValueError(f"Unsupported difficulty: {difficulty}")
        dims = ("accuracy", "depth", "logical_reasoning", "real_world_applicability")
        if rubric_scores is not None:
            if set(rubric_scores) != set(dims):
                raise ValueError("rubric_scores must contain all four dimensions.")
            scores = {k: float(v) for k, v in rubric_scores.items()}
            if any(v < 0 or v > 100 for v in scores.values()):
                raise ValueError("Rubric scores must be between 0 and 100.")
            evidence = {k: "reviewer_supplied_rubric" for k in dims}
        elif not answer.strip():
            scores = {k: 0.0 for k in dims}
            evidence = {k: "empty_answer" for k in dims}
        else:
            tokens = set(re.findall(r"[a-zA-Z0-9+#.-]+", answer.lower()))
            concepts = [str(x).lower().strip() for x in (expected_concepts or []) if str(x).strip()]
            accuracy = 70.0 if not concepts else 100 * sum(1 for c in concepts if c in tokens or c in answer.lower()) / len(concepts)
            scores = {"accuracy": round(accuracy, 2)}
            for key, markers in self.MARKERS.items():
                count = sum(1 for m in markers if m in answer.lower())
                base, step = (25, 12.5) if key == "depth" else ((25, 10) if key == "logical_reasoning" else (20, 10))
                scores[key] = round(min(100, base + count * step), 2)
            if len(tokens) < 8:
                scores["depth"] = min(scores["depth"], 35.0)
            evidence = {"accuracy": "expected_concept_coverage" if concepts else "not_assessed_without_expected_concepts",
                        "depth": "length_and_depth_markers", "logical_reasoning": "reasoning_markers",
                        "real_world_applicability": "application_markers"}
        weights = self.WEIGHTS[qtype]
        raw = round(sum(scores[k] * weights[k] for k in dims), 2)
        reference = self.DIFFICULTY_REFERENCE[level]
        normalized = round(min(100.0, raw / reference * 60.0), 2)
        depth_label = "shallow" if scores["depth"] < 40 else ("developing" if scores["depth"] < 70 else "deep")
        return {"question_type": qtype, "difficulty": level, "dimension_scores": scores,
                "weights": dict(weights), "raw_score": raw, "normalized_score": normalized,
                "difficulty_reference_score": reference, "answer_depth": depth_label,
                "evidence": evidence, "explanations": {k: f"{scores[k]:.1f}/100; weight {weights[k]:.0%}; {evidence[k]}" for k in dims},
                "scoring_method": "transparent_rule_based_baseline", "requires_human_review": True}

    def score_interview(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not isinstance(responses, list):
            raise TypeError("Responses must be a list.")
        results, skills = [], {}
        for item in responses:
            if not isinstance(item, dict) or "answer" not in item:
                raise ValueError("Each response must contain answer.")
            r = self.score_answer(item["answer"], item.get("question_type", "conceptual"),
                                  item.get("difficulty", "basic"), item.get("expected_concepts"),
                                  item.get("rubric_scores"))
            results.append(r)
            skills.setdefault(str(item.get("skill", "unspecified")), []).append(r["normalized_score"])
        return {"response_count": len(results),
                "technical_score": round(sum(r["normalized_score"] for r in results) / len(results), 2) if results else 0.0,
                "response_results": results,
                "skill_breakdown": {k: round(sum(v)/len(v), 2) for k, v in skills.items()},
                "human_review_required": True}

    def generate_evaluation_report(self, responses):
        return {"technical_evaluation_report": self.score_interview(responses)}
