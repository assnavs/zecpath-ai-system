from datetime import datetime,timedelta,timezone
import pytest
from utils.security_governance_framework import SecurityGovernanceFramework
def test_consent_can_be_revoked():
    g=SecurityGovernanceFramework(); g.record_consent("C1","recording",True)
    assert g.has_consent("C1","recording")
    g.record_consent("C1","recording",False); assert not g.has_consent("C1","recording")
def test_role_access():
    g=SecurityGovernanceFramework(); assert g.authorize("auditor","read_audit")
    assert not g.authorize("auditor","write_candidate")
def test_audit_redacts_sensitive_fields():
    e=SecurityGovernanceFramework().record_audit_event("U","view","C",{"transcript":"private","token":"secret","source":"portal"})
    assert "transcript" not in e["metadata"] and e["metadata"]["source"]=="portal"
def test_retention():
    g=SecurityGovernanceFramework(30); d=datetime(2026,1,1,tzinfo=timezone.utc)
    assert g.retention_status(d,d+timedelta(days=31))["eligible_for_deletion"]
def test_naive_datetime_rejected():
    with pytest.raises(ValueError): SecurityGovernanceFramework().retention_status(datetime(2026,1,1))
def test_scope_disclosed():
    assert "in-memory" in SecurityGovernanceFramework().governance_summary()["implementation_scope"]
