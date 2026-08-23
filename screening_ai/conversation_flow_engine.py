import json
from pathlib import Path
from typing import Any, Dict


class ConversationFlowEngine:
    """
    Controls the state flow of the AI screening conversation.

    The engine manages:
    - Conversation states
    - Response evaluation actions
    - Retry handling
    - Clarification handling
    - Continuation after maximum retries
    """

    def __init__(
        self,
        config_path: str = "data/conversation_flow_configuration.json"
    ):
        self.config_path = Path(config_path)

        with self.config_path.open(
            "r",
            encoding="utf-8-sig"
        ) as file:
            self.configuration = json.load(file)

        self.states = self.configuration["conversation_states"]
        self.response_rules = self.configuration["response_rules"]
        self.retry_policy = self.configuration["retry_policy"]

    def get_state(self, state: str) -> Dict[str, Any]:
        """Return information about a conversation state."""

        if state not in self.states:
            raise ValueError(f"Unknown conversation state: {state}")

        return self.states[state]

    def get_next_state(self, state: str) -> Any:
        """Return the configured next state."""

        return self.get_state(state)["next_state"]

    def evaluate_response(
        self,
        response_type: str
    ) -> Dict[str, Any]:
        """Return the action and message for a response type."""

        rule = self.response_rules.get(
            response_type,
            self.response_rules["unknown"]
        )

        return {
            "response_type": response_type,
            "action": rule["action"],
            "message": rule["message"]
        }

    def handle_retry(
        self,
        retry_count: int
    ) -> Dict[str, Any]:
        """Determine the action after the current retry count."""

        maximum_retries = self.retry_policy["maximum_retries"]

        if retry_count < maximum_retries:
            action_index = min(
                retry_count,
                len(self.retry_policy["retry_actions"]) - 1
            )

            return {
                "retry_count": retry_count,
                "maximum_retries": maximum_retries,
                "action": self.retry_policy["retry_actions"][action_index],
                "continue": True
            }

        return {
            "retry_count": retry_count,
            "maximum_retries": maximum_retries,
            "action": self.retry_policy["after_maximum_retries"],
            "continue": False
        }

    def transition(
        self,
        current_state: str,
        response_type: str = "understood",
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """Calculate the next conversation transition."""

        response_result = self.evaluate_response(response_type)

        if response_result["action"] == "retry":
            retry_result = self.handle_retry(retry_count)

            return {
                "current_state": current_state,
                "next_state": current_state,
                "response_type": response_type,
                "action": retry_result["action"],
                "message": response_result["message"],
                "retry_count": retry_result["retry_count"],
                "continue": retry_result["continue"]
            }

        if response_result["action"] in {
            "clarify",
            "redirect"
        }:
            return {
                "current_state": current_state,
                "next_state": current_state,
                "response_type": response_type,
                "action": response_result["action"],
                "message": response_result["message"],
                "retry_count": retry_count,
                "continue": True
            }

        next_state = self.get_next_state(current_state)

        return {
            "current_state": current_state,
            "next_state": next_state,
            "response_type": response_type,
            "action": response_result["action"],
            "message": response_result["message"],
            "retry_count": retry_count,
            "continue": next_state is not None
        }

    def get_flow(self) -> Dict[str, Any]:
        """Return the complete configured conversation flow."""

        return {
            "states": self.states,
            "response_rules": self.response_rules,
            "retry_policy": self.retry_policy
        }
