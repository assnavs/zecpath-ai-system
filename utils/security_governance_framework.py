from datetime import datetime, timedelta, timezone

class SecurityGovernanceFramework:
    """In-memory reference framework for consent, audit metadata, retention and access roles."""
    ROLE_PERMISSIONS={
        "admin":{"read_candidate","write_candidate","read_report","write_report","read_audit","manage_policy"},
        "recruiter":{"read_candidate","write_candidate","read_report","write_report"},
        "reviewer":{"read_candidate","read_report","write_report"},
        "auditor":{"read_audit","read_report"}}
    def __init__(self,retention_days=365):
        if isinstance(retention_days,bool) or not isinstance(retention_days,int) or retention_days<1:
            raise ValueError("retention_days must be a positive integer.")
        self.retention_days=retention_days; self._consents={}; self._audit=[]
    def record_consent(self,subject_id,purpose,granted):
        if not subject_id or not purpose or not isinstance(granted,bool): raise ValueError("Valid subject, purpose and boolean consent required.")
        item={"granted":granted,"recorded_at":datetime.now(timezone.utc).isoformat()}
        self._consents[(subject_id,purpose)]=item
        self._audit.append({"event":"consent_recorded","subject_id":subject_id,"purpose":purpose,"granted":granted,"timestamp":item["recorded_at"]})
        return dict(item)
    def has_consent(self,subject_id,purpose): return bool(self._consents.get((subject_id,purpose),{}).get("granted",False))
    def authorize(self,role,permission): return permission in self.ROLE_PERMISSIONS.get(role,set())
    def record_audit_event(self,actor_id,action,subject_id=None,metadata=None):
        if not actor_id or not action: raise ValueError("actor_id and action are required.")
        safe={k:v for k,v in (metadata or {}).items() if k not in {"transcript","raw_transcript","password","token","secret"}}
        event={"actor_id":actor_id,"action":action,"subject_id":subject_id,"metadata":safe,"timestamp":datetime.now(timezone.utc).isoformat()}
        self._audit.append(event); return dict(event)
    def audit_trail(self): return [dict(x) for x in self._audit]
    def retention_status(self,created_at,now=None):
        if not isinstance(created_at,datetime): raise TypeError("created_at must be datetime.")
        now=now or datetime.now(timezone.utc)
        if created_at.tzinfo is None or now.tzinfo is None: raise ValueError("Timezone-aware datetimes are required.")
        expiry=created_at+timedelta(days=self.retention_days)
        return {"retention_days":self.retention_days,"expires_at":expiry.isoformat(),"eligible_for_deletion":now>=expiry,
                "policy_note":"Metadata only; actual deletion must be enforced by the storage layer."}
    def governance_summary(self):
        return {"retention_days":self.retention_days,"consent_records":len(self._consents),"audit_event_count":len(self._audit),
                "roles":{k:sorted(v) for k,v in self.ROLE_PERMISSIONS.items()},
                "storage_security_required":["encryption at rest","TLS in transit","secret management","least privilege","verified deletion"],
                "implementation_scope":"in-memory reference framework; persistent storage and cryptographic tamper evidence are not implemented"}
