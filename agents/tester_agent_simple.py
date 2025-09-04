from typing import Dict, Any, Optional

class TesterAgentSimple:
    """
    A tiny tester-agent that plays the user.
    For the mock POC, we keep it minimal and deterministic:
    - Sends the scenario's initial message
    - If the product asks to confirm a promise, it confirms once.
    """
    def __init__(self) -> None:
        pass

    def first_message(self, scenario: Dict[str, Any]) -> str:
        return scenario["conversation"]["initial_user_msg"]

    def next_message(self, last_agent_response: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[str]:
        s = last_agent_response.get("structured", {})
        if s.get("promise_to_pay") and s.get("outcome") == "success":
            ptp = s["promise_to_pay"]
            return f"Yes, I confirm the promise to pay ₹{ptp['amount']} by {ptp['date']}."
        return None
