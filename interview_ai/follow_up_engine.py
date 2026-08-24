from typing import Any, Dict, Optional
import re


class DynamicFollowUpEngine:
    """
    Day 34 dynamic follow-up and adaptive questioning engine.

    Responsibilities:
    - Detect incomplete or vague responses
    - Trigger clarification questions
    - Trigger deeper probes
    - Trigger example-based prompts
    - Adapt questioning difficulty
    - Avoid repetitive follow-up questions
    - Track follow-up conversation state
    """

    MAX_FOLLOW_UPS = 2

    VAGUE_RESPONSES = {
        "yes",
        "no",
        "okay",
        "fine",
        "good",
        "maybe",
        "not sure",
        "i don't know",
        "dont know",
        "nothing",
        "everything",
        "sometimes",
    }

    CONFIDENT_MARKERS = {
        "led",
        "developed",
        "implemented",
        "designed",
        "managed",
        "built",
        "optimized",
        "delivered",
        "deployed",
        "improved",
    }

    def __init__(self):
        self.state = {
            "follow_up_count": 0,
            "follow_up_eligible": False,
            "last_trigger": None,
            "asked_follow_ups": [],
        }

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", text.strip().lower())

    def analyze_response(
        self,
        response: str,
        question_id: Optional[str] = None,
    ) -> Dict[str, Any]:

        if not isinstance(response, str):
            raise TypeError(
                "Candidate response must be a string."
            )

        cleaned = self._normalize(response)

        if not cleaned:
            return self._build_decision(
                trigger="clarification",
                eligible=True,
                reason="empty_response",
                question_id=question_id,
            )

        words = cleaned.split()

        if cleaned in self.VAGUE_RESPONSES:
            return self._build_decision(
                trigger="clarification",
                eligible=True,
                reason="vague_response",
                question_id=question_id,
            )

        if len(words) <= 2:
            return self._build_decision(
                trigger="clarification",
                eligible=True,
                reason="very_short_response",
                question_id=question_id,
            )

        if len(words) <= 5:
            return self._build_decision(
                trigger="deepening",
                eligible=True,
                reason="short_response",
                question_id=question_id,
            )

        if self._contains_confident_marker(cleaned):
            return self._build_decision(
                trigger="scenario",
                eligible=True,
                reason="confident_response",
                question_id=question_id,
            )

        if len(words) >= 15:
            return self._build_decision(
                trigger="example",
                eligible=True,
                reason="detailed_response",
                question_id=question_id,
            )

        return self._build_decision(
            trigger=None,
            eligible=False,
            reason="sufficient_response",
            question_id=question_id,
        )

    def _contains_confident_marker(
        self,
        response: str,
    ) -> bool:
        return any(
            re.search(
                rf"\b{re.escape(marker)}\b",
                response,
            )
            for marker in self.CONFIDENT_MARKERS
        )

    def _build_decision(
        self,
        trigger: Optional[str],
        eligible: bool,
        reason: str,
        question_id: Optional[str],
    ) -> Dict[str, Any]:

        if (
            eligible
            and trigger is not None
            and self.state["follow_up_count"]
            >= self.MAX_FOLLOW_UPS
        ):
            trigger = None
            eligible = False
            reason = "maximum_follow_ups_reached"

        follow_up = self._create_follow_up(
            trigger,
            question_id,
        )

        if eligible and follow_up:
            self.state["follow_up_count"] += 1
            self.state["asked_follow_ups"].append(
                follow_up["text"]
            )

        self.state["follow_up_eligible"] = eligible
        self.state["last_trigger"] = trigger

        return {
            "follow_up_eligible": eligible,
            "trigger": trigger,
            "reason": reason,
            "follow_up": follow_up,
            "state": dict(self.state),
        }

    def _create_follow_up(
        self,
        trigger: Optional[str],
        question_id: Optional[str],
    ) -> Optional[Dict[str, Any]]:

        if trigger is None:
            return None

        prompts = {
            "clarification": (
                "Could you please provide a little more detail?"
            ),
            "deepening": (
                "Could you explain that in a little more detail?"
            ),
            "example": (
                "Could you give me a specific example from "
                "your experience?"
            ),
            "scenario": (
                "Can you describe how you would handle a "
                "real-world situation related to that?"
            ),
        }

        text = prompts[trigger]

        if text in self.state["asked_follow_ups"]:
            return None

        return {
            "type": trigger,
            "question_id": question_id,
            "text": text,
        }

    def should_continue(
        self,
        response: str,
        question_id: Optional[str] = None,
    ) -> bool:
        decision = self.analyze_response(
            response,
            question_id,
        )

        return not decision["follow_up_eligible"]

    def get_state(self) -> Dict[str, Any]:
        return dict(self.state)

    def reset(self) -> None:
        self.state = {
            "follow_up_count": 0,
            "follow_up_eligible": False,
            "last_trigger": None,
            "asked_follow_ups": [],
        }