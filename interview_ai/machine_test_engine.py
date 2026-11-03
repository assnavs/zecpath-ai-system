from typing import Any, Dict, List

class MachineTestEngine:
    """Evaluates supplied test outputs and rubric scores; does not run submitted code."""
    TASK_TYPES = {"coding", "debugging", "file_based", "mini_system_design"}
    WEIGHTS = {
        "coding": {"correctness": .50, "efficiency": .15, "code_quality": .20, "problem_solving_approach": .15},
        "debugging": {"correctness": .40, "efficiency": .15, "code_quality": .20, "problem_solving_approach": .25},
        "file_based": {"correctness": .45, "efficiency": .15, "code_quality": .20, "problem_solving_approach": .20},
        "mini_system_design": {"correctness": .25, "efficiency": .10, "code_quality": .25, "problem_solving_approach": .40},
    }

    @staticmethod
    def _score(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 100:
            raise ValueError(f"{name} must be between 0 and 100.")
        return float(value)

    def evaluate_submission(self, task: Dict[str, Any], submission: Dict[str, Any]):
        if not isinstance(task, dict) or not isinstance(submission, dict):
            raise TypeError("task and submission must be dictionaries.")
        kind = task.get("task_type")
        if kind not in self.TASK_TYPES:
            raise ValueError(f"Unsupported task type: {kind}")
        limit, used = task.get("time_limit_seconds"), submission.get("time_used_seconds")
        if isinstance(limit, bool) or not isinstance(limit, (int, float)) or limit <= 0:
            raise ValueError("time_limit_seconds must be positive.")
        if isinstance(used, bool) or not isinstance(used, (int, float)) or used < 0:
            raise ValueError("time_used_seconds must be non-negative.")
        passed, total = submission.get("tests_passed", 0), submission.get("tests_total", 0)
        if any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in (passed, total)) or passed > total:
            raise ValueError("Test counts must be non-negative integers and passed cannot exceed total.")
        correctness = round(100 * passed / total, 2) if total else self._score(submission.get("correctness_score", 0), "correctness_score")
        ratio = used / limit
        efficiency = 100.0 if ratio <= .5 else (max(0.0, 100 * (1 - (ratio - .5) / 1.5)) if ratio < 2 else 0.0)
        dims = {"correctness": correctness, "efficiency": round(efficiency, 2),
                "code_quality": self._score(submission.get("code_quality_score", 0), "code_quality_score"),
                "problem_solving_approach": self._score(submission.get("problem_solving_approach_score", 0), "problem_solving_approach_score")}
        weights = self.WEIGHTS[kind]
        return {"task_id": task.get("task_id"), "task_type": kind, "dimension_scores": dims, "weights": dict(weights),
                "final_score": round(sum(dims[k] * weights[k] for k in weights), 2),
                "tests_passed": passed, "tests_total": total, "time_used_seconds": float(used),
                "time_limit_seconds": float(limit), "within_time_limit": used <= limit,
                "code_snapshots": list(submission.get("code_snapshots", [])),
                "execution_results": list(submission.get("execution_results", [])),
                "execution_performed_by_engine": False,
                "evaluation_note": "Execution results are externally supplied; submitted code was not executed.",
                "human_review_required": True}

    def evaluate_session(self, submissions: List[Dict[str, Any]]):
        if not isinstance(submissions, list):
            raise TypeError("submissions must be a list.")
        results = [self.evaluate_submission(x["task"], x["submission"]) for x in submissions]
        return {"task_count": len(results), "overall_score": round(sum(x["final_score"] for x in results)/len(results), 2) if results else 0.0,
                "task_results": results, "human_review_required": True}
