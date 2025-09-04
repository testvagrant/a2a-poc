from typing import Dict, Any, Optional, List
from .base_strategy import BaseStrategy

class ToolHappyPathStrategy(BaseStrategy):
    """
    ToolHappyPath strategy: Tests successful tool usage and execution.
    
    - Sends initial message requesting tool action
    - Provides necessary input for tool execution
    - Confirms tool results
    - Stops when tool side-effect is recorded
    """
    
    def __init__(self):
        super().__init__(
            name="ToolHappyPath",
            description="Tests successful tool usage and execution flow"
        )
        
    def first_message(self, scenario: Dict[str, Any]) -> str:
        """Send the scenario's initial user message."""
        return scenario["conversation"]["initial_user_msg"]
        
    def next_message(self, last_agent_response: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[str]:
        """Generate next message based on agent response."""
        structured = last_agent_response.get("structured", {})
        text = last_agent_response.get("text", "").lower()
        
        # If agent asks for input to execute tool, provide it
        if self._needs_tool_input(text):
            return self._provide_tool_input(scenario)
            
        # If agent asks for confirmation, confirm it
        if self._needs_confirmation(structured, text):
            return self._provide_confirmation(structured)
            
        # If agent reports tool success, acknowledge it
        if self._tool_succeeded(structured):
            return "Great! Thank you for completing that."
            
        return None
        
    def should_continue(self, conversation: List[Dict[str, str]], scenario: Dict[str, Any]) -> bool:
        """Continue until tool is executed or max turns reached."""
        max_turns = scenario["conversation"].get("max_turns", 5)
        if len(conversation) >= max_turns:
            return False
            
        # Check if tool was successfully executed
        last_response = conversation[-1] if conversation else {}
        if last_response.get("role") == "assistant":
            structured = last_response.get("structured", {})
            if self._tool_succeeded(structured):
                return False
                
        return True
        
    def _needs_tool_input(self, text: str) -> bool:
        """Check if agent needs input to execute tool."""
        input_indicators = [
            "please provide", "i need", "enter", "input", "fill in",
            "what is your", "can you tell me", "specify"
        ]
        return any(indicator in text for indicator in input_indicators)
        
    def _needs_confirmation(self, structured: Dict[str, Any], text: str) -> bool:
        """Check if agent needs confirmation."""
        confirmation_indicators = [
            "confirm", "proceed", "continue", "okay", "yes"
        ]
        return any(indicator in text for indicator in confirmation_indicators)
        
    def _tool_succeeded(self, structured: Dict[str, Any]) -> bool:
        """Check if tool was successfully executed."""
        return structured.get("outcome") == "success" and structured.get("intent") == "tool_execution"
        
    def _provide_tool_input(self, scenario: Dict[str, Any]) -> str:
        """Provide input needed for tool execution."""
        goal = scenario.get("goal", {}).get("user_goal", "")
        
        if "create account" in goal.lower():
            return "My name is John Doe, email is john@example.com, and I want a basic checking account."
        elif "make payment" in goal.lower():
            return "I want to pay $100 using my credit card ending in 1234."
        elif "schedule appointment" in goal.lower():
            return "I need an appointment next Tuesday at 2 PM."
        else:
            return "Here is the information you requested: John Doe, john@example.com, 555-0123."
            
    def _provide_confirmation(self, structured: Dict[str, Any]) -> str:
        """Provide confirmation for tool execution."""
        return "Yes, please proceed with that action."
