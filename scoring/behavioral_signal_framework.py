from typing import Any, Dict

class BehavioralSignalFramework:
    """Consent-based contextual observations; no biometric/emotion scoring."""
    NON_SCORABLE = {
        "gaze_stability": "Not scored: gaze varies by disability, culture and individual preference.",
        "head_movement": "Not scored: movement is not a reliable proxy for attention or competence.",
        "facial_engagement": "Not scored: facial expression is not a reliable emotion or suitability measure.",
        "nervous_gestures": "Not scored: may reflect disability, neurodiversity, culture or ordinary stress.",
    }

    def get_signal_mapping(self):
        result = {k: {"eligible_for_scoring": False, "output": "not_scored", "reason": v} for k, v in self.NON_SCORABLE.items()}
        result["attention_patterns"] = {"eligible_for_scoring": False, "output": "contextual_observation_only",
            "reason": "Window focus events may reflect notifications, assistive technology or technical issues."}
        return result

    def analyze_signals(self, signals: Dict[str, Any], consent_confirmed: bool = False):
        if not isinstance(signals, dict):
            raise TypeError("signals must be a dictionary.")
        if not consent_confirmed:
            return {"analysis_performed": False, "reason": "explicit_consent_required", "observations": [],
                    "non_scorable_signals": dict(self.NON_SCORABLE), "candidate_score": None, "human_review_required": True}
        observations = []
        count = signals.get("focus_loss_count")
        duration = signals.get("focus_loss_duration_seconds")
        if count is not None:
            if isinstance(count, bool) or not isinstance(count, int) or count < 0:
                raise ValueError("focus_loss_count must be a non-negative integer.")
            observations.append({"signal": "window_focus_events", "value": count, "interpretation": "contextual_event_only",
                                 "note": "Do not infer misconduct or low attention."})
        if duration is not None:
            if isinstance(duration, bool) or not isinstance(duration, (int, float)) or duration < 0:
                raise ValueError("focus_loss_duration_seconds must be non-negative.")
            observations.append({"signal": "window_focus_duration", "value": float(duration),
                                 "interpretation": "contextual_event_only",
                                 "note": "Consider technical interruptions and accessibility needs."})
        return {"analysis_performed": True, "observations": observations,
                "non_scorable_signals": dict(self.NON_SCORABLE), "candidate_score": None,
                "recommendation": "Ask a neutral clarification only if relevant.",
                "human_review_required": True, "automated_hiring_decision": False}
