"""Privacy-aware, dependency-free observability helpers for Zecpath.

This module provides structured event records and in-process metrics. It is not
a durable log store, distributed metrics backend, or production alert manager.
"""
from __future__ import annotations
from collections import defaultdict, deque
from datetime import datetime, timezone
import json
import logging
import math
import threading
import time
import uuid

SENSITIVE_KEYS = {
    "resume", "resume_text", "raw_resume", "transcript", "raw_transcript",
    "answer", "answers", "candidate_name", "email", "phone", "password",
    "token", "secret", "authorization", "access_token",
}

def _safe_value(value, key=""):
    if key.lower() in SENSITIVE_KEYS:
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(k): _safe_value(v, str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_safe_value(v, key) for v in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        if isinstance(value, float) and not math.isfinite(value):
            return str(value)
        return value
    return str(value)

class StructuredEventLogger:
    """Emit JSON event records; payload fields are redacted before logging."""
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger("zecpath.observability")

    def emit(self, event_type, *, service, status="info", correlation_id=None,
             candidate_ref=None, duration_ms=None, details=None):
        if not isinstance(event_type, str) or not event_type.strip():
            raise ValueError("event_type is required")
        if not isinstance(service, str) or not service.strip():
            raise ValueError("service is required")
        if duration_ms is not None and (
            isinstance(duration_ms, bool) or not isinstance(duration_ms, (int, float))
            or not math.isfinite(duration_ms) or duration_ms < 0
        ):
            raise ValueError("duration_ms must be a finite non-negative number")
        record = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "service": service,
            "status": status,
            "correlation_id": correlation_id,
            "candidate_ref": candidate_ref,
            "duration_ms": duration_ms,
            "details": _safe_value(details or {}),
        }
        self.logger.info(json.dumps(record, sort_keys=True))
        return record

class InMemoryMetrics:
    """Thread-safe process-local counters and latency samples for demos/tests."""
    def __init__(self, max_samples=1000):
        if isinstance(max_samples, bool) or not isinstance(max_samples, int) or max_samples < 1:
            raise ValueError("max_samples must be a positive integer")
        self._lock = threading.RLock()
        self._counters = defaultdict(int)
        self._latencies = defaultdict(lambda: deque(maxlen=max_samples))

    def increment(self, name, amount=1):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("metric name is required")
        if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:
            raise ValueError("amount must be a non-negative integer")
        with self._lock:
            self._counters[name] += amount
            return self._counters[name]

    def observe_latency(self, service, duration_ms):
        if (not isinstance(service, str) or not service.strip()
            or isinstance(duration_ms, bool) or not isinstance(duration_ms, (int, float))
            or not math.isfinite(duration_ms) or duration_ms < 0):
            raise ValueError("service and finite non-negative duration_ms are required")
        with self._lock:
            self._latencies[service].append(float(duration_ms))

    def snapshot(self):
        with self._lock:
            latencies = {}
            for service, values in self._latencies.items():
                ordered = sorted(values)
                if not ordered:
                    continue
                idx = min(len(ordered)-1, int(.95 * (len(ordered)-1)))
                latencies[service] = {
                    "sample_count": len(ordered),
                    "mean_ms": round(sum(ordered)/len(ordered), 3),
                    "p95_ms": round(ordered[idx], 3),
                    "max_ms": round(ordered[-1], 3),
                }
            return {"counters": dict(self._counters), "latencies": latencies,
                    "scope": "in-process metrics; reset on restart and not shared across workers"}

class AlertRuleEvaluator:
    """Evaluate explicit thresholds against a supplied metrics snapshot."""
    DEFAULT_RULES = {
        "failure_rate_pct": {"operator": "gt", "threshold": 5.0, "severity": "critical"},
        "p95_latency_ms": {"operator": "gt", "threshold": 2000.0, "severity": "warning"},
        "api_error_count": {"operator": "gt", "threshold": 20, "severity": "warning"},
    }

    def __init__(self, rules=None):
        self.rules = dict(rules or self.DEFAULT_RULES)

    def evaluate(self, values):
        if not isinstance(values, dict):
            raise TypeError("values must be a dictionary")
        alerts = []
        for name, rule in self.rules.items():
            if name not in values:
                continue
            value = values[name]
            threshold = rule["threshold"]
            if (isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value)):
                raise ValueError(f"{name} must be a finite number")
            triggered = value > threshold if rule.get("operator", "gt") == "gt" else value < threshold
            if triggered:
                alerts.append({"metric": name, "observed": value, "threshold": threshold,
                               "severity": rule.get("severity", "warning"),
                               "message": f"{name} crossed configured threshold"})
        return alerts

class DecisionAuditTrail:
    """In-memory metadata-only audit trail; persistence/tamper evidence are external."""
    def __init__(self):
        self._events = []
        self._lock = threading.RLock()

    def record(self, *, actor_ref, action, candidate_ref, recommendation=None,
               score=None, rationale_codes=None, model_version="unspecified"):
        if not actor_ref or not action or not candidate_ref:
            raise ValueError("actor_ref, action and candidate_ref are required")
        if score is not None and (
            isinstance(score, bool) or not isinstance(score, (int, float))
            or not math.isfinite(score) or not 0 <= score <= 100
        ):
            raise ValueError("score must be between 0 and 100")
        event = {
            "audit_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "actor_ref": str(actor_ref),
            "action": str(action),
            "candidate_ref": str(candidate_ref),
            "recommendation": recommendation,
            "score": score,
            "rationale_codes": list(rationale_codes or []),
            "model_version": str(model_version),
            "human_review_required": True,
        }
        with self._lock:
            self._events.append(event)
        return dict(event)

    def list_events(self):
        with self._lock:
            return [dict(event) for event in self._events]
