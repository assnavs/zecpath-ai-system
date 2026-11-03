import json
import logging
import pytest
from utils.ai_observability import StructuredEventLogger, InMemoryMetrics, AlertRuleEvaluator, DecisionAuditTrail

class Capture(logging.Handler):
    def __init__(self):
        super().__init__()
        self.messages=[]
    def emit(self, record):
        self.messages.append(record.getMessage())

def test_structured_event_is_json_and_redacts_sensitive_fields():
    logger=logging.getLogger("test.observability.capture")
    logger.handlers=[]; logger.setLevel(logging.INFO); logger.propagate=False
    handler=Capture(); logger.addHandler(handler)
    result=StructuredEventLogger(logger).emit(
        "score_generated", service="ats", candidate_ref="C-1",
        details={"resume_text":"private", "score":88, "nested":{"token":"secret"}}
    )
    assert json.loads(handler.messages[0])["details"]["resume_text"] == "[REDACTED]"
    assert result["details"]["nested"]["token"] == "[REDACTED]"
    logger.removeHandler(handler)

def test_event_duration_validation():
    with pytest.raises(ValueError):
        StructuredEventLogger().emit("x", service="ats", duration_ms=-1)

def test_metrics_snapshot():
    m=InMemoryMetrics(max_samples=3)
    m.increment("api_requests")
    m.observe_latency("ats", 100)
    m.observe_latency("ats", 200)
    snap=m.snapshot()
    assert snap["counters"]["api_requests"] == 1
    assert snap["latencies"]["ats"]["sample_count"] == 2

def test_metrics_reject_invalid_latency():
    with pytest.raises(ValueError):
        InMemoryMetrics().observe_latency("ats", float("nan"))

def test_alert_thresholds():
    alerts=AlertRuleEvaluator().evaluate({"failure_rate_pct":6,"p95_latency_ms":100})
    assert len(alerts)==1 and alerts[0]["severity"]=="critical"

def test_audit_trail_records_metadata_only():
    audit=DecisionAuditTrail()
    event=audit.record(actor_ref="R-1",action="reviewed",candidate_ref="C-1",
                       recommendation="Hold / Review",score=70,rationale_codes=["LOW_COVERAGE"])
    assert event["human_review_required"] is True
    assert audit.list_events()[0]["candidate_ref"]=="C-1"

def test_audit_rejects_invalid_score():
    with pytest.raises(ValueError):
        DecisionAuditTrail().record(actor_ref="R",action="review",candidate_ref="C",score=101)
