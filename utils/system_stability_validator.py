"""Small reusable validation helpers for score and API response contracts."""
import math

class SystemStabilityValidator:
    @staticmethod
    def validate_score(value, field="score"):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{field} must be a numeric score from 0 to 100")
        if not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError(f"{field} must be a finite score from 0 to 100")
        return float(value)

    @staticmethod
    def validate_success_envelope(payload):
        if not isinstance(payload, dict) or payload.get("success") is not True:
            raise ValueError("API response must use the success response envelope")
        if "data" not in payload:
            raise ValueError("Successful API response must include data")
        return payload["data"]

    @staticmethod
    def normalize_error(error, code="PROCESSING_ERROR"):
        if not isinstance(code, str) or not code.strip():
            raise ValueError("error code must be a non-empty string")
        return {"success":False,"error":{"code":code.strip(),
                "message":str(error) if error else "An unexpected error occurred."}}
