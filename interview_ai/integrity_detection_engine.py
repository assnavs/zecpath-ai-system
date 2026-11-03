from collections import Counter
from typing import Any, Dict, List

class IntegrityDetectionEngine:
    """Threshold event flags for review; never makes a malpractice finding."""
    ALLOWED = {"tab_switch", "window_blur", "external_voice_indicator", "looking_away_indicator"}
    DEFAULT_THRESHOLDS = {"tab_switch": 3, "window_blur": 3, "external_voice_indicator": 2}

    def __init__(self, thresholds: Dict[str, int] = None):
        self.thresholds = dict(thresholds or self.DEFAULT_THRESHOLDS)
        if any(k not in self.ALLOWED or isinstance(v, bool) or not isinstance(v, int) or v < 1 for k, v in self.thresholds.items()):
            raise ValueError("Thresholds require supported event names and positive integers.")

    def evaluate_events(self, events: List[Dict[str, Any]], consent_confirmed: bool = False):
        if not isinstance(events, list):
            raise TypeError("events must be a list.")
        if not consent_confirmed:
            return {"analysis_performed": False, "reason": "explicit_consent_required", "event_count": 0,
                    "risk_tag": "not_assessed", "alerts": [], "human_review_required": True, "malpractice_conclusion": None}
        counts = Counter()
        for event in events:
            if not isinstance(event, dict) or event.get("type") not in self.ALLOWED:
                raise ValueError("Each event must contain a supported event type.")
            counts[event["type"]] += 1
        alerts = []
        for kind, threshold in self.thresholds.items():
            if counts[kind] >= threshold:
                alerts.append({"event_type": kind, "count": counts[kind], "threshold": threshold,
                               "tag": "review_required", "message": "Verify context with the candidate."})
        if counts["looking_away_indicator"]:
            alerts.append({"event_type": "looking_away_indicator", "count": counts["looking_away_indicator"],
                           "threshold": None, "tag": "not_scored",
                           "message": "Visual attention cues cannot establish malpractice."})
        flagged = any(a["tag"] == "review_required" for a in alerts)
        return {"analysis_performed": True, "event_count": sum(counts.values()), "event_counts": dict(counts),
                "alerts": alerts, "risk_tag": "review_required" if flagged else "no_threshold_flag",
                "human_review_required": True, "malpractice_conclusion": None, "automated_hiring_decision": False}
