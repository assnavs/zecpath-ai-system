# Day 49 – Malpractice and Integrity Detection Design

## Objective
Generate threshold-based review flags from explicitly supplied session events.

## Implementation
- Module: `interview_ai/integrity_detection_engine.py`
- Events: tab switch, window blur, external-voice indicator and looking-away indicator.
- Default thresholds: 3 tab switches, 3 window-blur events and 2 external-voice indicators.
- Thresholds create review alerts only. Looking-away indicators are never scored.
- Consent is required; unknown event types are rejected.

## Limitations
The module does not monitor browsers, capture screens, record audio or establish malpractice. External-voice detection is not implemented; an indicator must come from a separately consented source. Technical interruptions and assistive technology can explain focus events. Human review is mandatory.
