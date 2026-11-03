import pytest
from scoring.behavioral_signal_framework import BehavioralSignalFramework

def test_consent_required():
    assert not BehavioralSignalFramework().analyze_signals({})["analysis_performed"]

def test_gaze_head_face_not_scored():
    m = BehavioralSignalFramework().get_signal_mapping()
    for k in ("gaze_stability", "head_movement", "facial_engagement", "nervous_gestures"):
        assert not m[k]["eligible_for_scoring"]

def test_focus_events_context_only():
    r = BehavioralSignalFramework().analyze_signals({"focus_loss_count": 2, "focus_loss_duration_seconds": 4}, True)
    assert r["candidate_score"] is None and len(r["observations"]) == 2

def test_invalid_focus_count():
    with pytest.raises(ValueError): BehavioralSignalFramework().analyze_signals({"focus_loss_count": -1}, True)
