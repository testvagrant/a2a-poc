from typing import Dict, Any, Optional, List
from .base_strategy import BaseStrategy

class FlowIntentStrategy(BaseStrategy):
    """
    FlowIntent strategy: Simple flow testing with optional clarification.
    
    - Sends initial message
    - Asks one clarifier if ambiguous
    - Confirms when appropriate
    - Stops when goal achieved
    """
    
    def __init__(self):
        super().__init__(
            name="FlowIntent",
            description="Simple flow testing with optional clarification and confirmation"
        )
        
    def first_message(self, scenario: Dict[str, Any]) -> str:
        """Send the scenario's initial user message."""
        return scenario["conversation"]["initial_user_msg"]
        
    def next_message(self, last_agent_response: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[str]:
        """Generate next message based on agent response."""
        structured = last_agent_response.get("structured", {})
        
        # If agent asks for clarification, provide it
        if self._needs_clarification(last_agent_response):
            return self._provide_clarification(scenario)
            
        # If agent proposes something to confirm, confirm it
        if self._needs_confirmation(structured):
            return self._provide_confirmation(structured)
            
        # If agent asks for input, provide it
        if self._needs_input(last_agent_response):
            return self._provide_input(scenario)
            
        return None
        
    def should_continue(self, conversation: List[Dict[str, str]], scenario: Dict[str, Any]) -> bool:
        """Continue until max turns or goal achieved."""
        max_turns = scenario["conversation"].get("max_turns", 5)
        return len(conversation) < max_turns
        
    def _needs_clarification(self, response: Dict[str, Any]) -> bool:
        """Check if agent is asking for clarification."""
        text = response.get("text", "").lower()
        clarification_indicators = [
            "can you clarify", "what do you mean", "please specify",
            "which one", "what would you like", "i don't understand"
        ]
        return any(indicator in text for indicator in clarification_indicators)
        
    def _needs_confirmation(self, structured: Dict[str, Any]) -> bool:
        """Check if agent is asking for confirmation."""
        return structured.get("outcome") == "pending_confirmation"
        
    def _needs_input(self, response: Dict[str, Any]) -> bool:
        """Check if agent is asking for input."""
        text = response.get("text", "").lower()
        input_indicators = [
            "please provide", "i need", "enter", "input", "fill in"
        ]
        return any(indicator in text for indicator in input_indicators)
        
    def _provide_clarification(self, scenario: Dict[str, Any]) -> str:
        """Provide clarification based on scenario goal."""
        goal = scenario.get("goal", {}).get("user_goal", "")
        if "account" in goal.lower():
            return "I want to check my account balance and recent transactions."
        elif "payment" in goal.lower():
            return "I want to make a payment of $100."
        elif "support" in goal.lower():
            return "I have a technical issue with the mobile app."
        else:
            return "I need help with my account."
            
    def _provide_confirmation(self, structured: Dict[str, Any]) -> str:
        """Provide confirmation for proposed actions."""
        if "promise_to_pay" in structured:
            ptp = structured["promise_to_pay"]
            return f"Yes, I confirm the promise to pay ${ptp.get('amount', '0')} by {ptp.get('date', '')}."
        elif "action" in structured:
            return f"Yes, please proceed with {structured['action']}."
        else:
            return "Yes, that's correct."
            
    def _provide_input(self, scenario: Dict[str, Any]) -> str:
        """Provide input based on scenario context."""
        goal = scenario.get("goal", {}).get("user_goal", "")
        if "payment" in goal.lower():
            return "My payment amount is $100 and I want to use my credit card."
        elif "account" in goal.lower():
            return "My account number is 123456789."
        else:
            return "Here is the information you requested."
