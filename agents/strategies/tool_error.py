from typing import Dict, Any, Optional, List
from .base_strategy import BaseStrategy

class ToolErrorStrategy(BaseStrategy):
    """
    ToolError strategy: Tests error handling and recovery in tool execution.
    
    - Sends tool requests that will fail
    - Tests error handling and recovery flows
    - Validates fallback mechanisms
    - Ensures proper error messaging
    """
    
    def __init__(self):
        super().__init__(
            name="ToolError",
            description="Tests error handling and recovery in tool execution"
        )
        
    def first_message(self, scenario: Dict[str, Any]) -> str:
        """Send the scenario's initial user message."""
        return scenario["conversation"]["initial_user_msg"]
        
    def next_message(self, last_agent_response: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[str]:
        """Generate next message based on agent response."""
        structured = last_agent_response.get("structured", {})
        text = last_agent_response.get("text", "").lower()
        
        # If agent reports tool error, test recovery
        if self._tool_failed(structured, text):
            return self._provide_recovery_input(scenario)
            
        # If agent asks for retry, provide different input
        if self._needs_retry(text):
            return self._provide_retry_input(scenario)
            
        # If agent asks for clarification after error, provide it
        if self._needs_error_clarification(text):
            return self._provide_error_clarification(scenario)
            
        return None
        
    def should_continue(self, conversation: List[Dict[str, str]], scenario: Dict[str, Any]) -> bool:
        """Continue until error handling is complete or max turns reached."""
        max_turns = scenario["conversation"].get("max_turns", 5)
        if len(conversation) >= max_turns:
            return False
            
        # Check if error handling test is complete
        if len(conversation) >= 4:  # Need at least 4 turns for error test
            return False
                
        return True
        
    def _tool_failed(self, structured: Dict[str, Any], text: str) -> bool:
        """Check if tool execution failed."""
        error_indicators = [
            "error", "failed", "unable to", "cannot", "invalid", 
            "not found", "permission denied", "timeout"
        ]
        
        # Check structured data for error indicators
        if structured.get("outcome") == "error":
            return True
            
        # Check text for error indicators
        return any(indicator in text for indicator in error_indicators)
        
    def _needs_retry(self, text: str) -> bool:
        """Check if agent is asking for retry."""
        retry_indicators = [
            "try again", "retry", "please try", "attempt again",
            "would you like to", "shall we try"
        ]
        return any(indicator in text for indicator in retry_indicators)
        
    def _needs_error_clarification(self, text: str) -> bool:
        """Check if agent needs clarification after error."""
        clarification_indicators = [
            "can you clarify", "what do you mean", "please specify",
            "which one", "what would you like", "i don't understand"
        ]
        return any(indicator in text for indicator in clarification_indicators)
        
    def _provide_recovery_input(self, scenario: Dict[str, Any]) -> str:
        """Provide input for error recovery."""
        goal = scenario.get("goal", {}).get("user_goal", "")
        
        if "create account" in goal.lower():
            return "Let me try with a different email: jane.doe@example.com"
        elif "make payment" in goal.lower():
            return "Can I try with a different payment method? I have a debit card."
        elif "schedule appointment" in goal.lower():
            return "How about next Wednesday at 3 PM instead?"
        else:
            return "Let me try a different approach. Can you help me with an alternative?"
            
    def _provide_retry_input(self, scenario: Dict[str, Any]) -> str:
        """Provide input for retry attempt."""
        goal = scenario.get("goal", {}).get("user_goal", "")
        
        if "create account" in goal.lower():
            return "Yes, let me try again with: John Smith, john.smith@email.com, 555-0199"
        elif "make payment" in goal.lower():
            return "Sure, let me try: $50 payment using my bank account ending in 5678"
        elif "schedule appointment" in goal.lower():
            return "Yes, let me try: Friday at 10 AM"
        else:
            return "Yes, let me try again with the correct information."
            
    def _provide_error_clarification(self, scenario: Dict[str, Any]) -> str:
        """Provide clarification after error."""
        goal = scenario.get("goal", {}).get("user_goal", "")
        
        if "create account" in goal.lower():
            return "I want to create a personal checking account with no monthly fees."
        elif "make payment" in goal.lower():
            return "I want to make a payment of $75 to my credit card balance."
        elif "schedule appointment" in goal.lower():
            return "I need to schedule a 30-minute consultation appointment."
        else:
            return "I need help with the specific task we were working on."