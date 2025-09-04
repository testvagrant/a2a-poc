from typing import Dict, Any, Optional, List
from .base_strategy import BaseStrategy

class MemoryCarryStrategy(BaseStrategy):
    """
    MemoryCarry strategy: Tests memory and context carry across conversation turns.
    
    - Sends initial message with context
    - References earlier information in follow-up messages
    - Checks if agent maintains context and memory
    - Tests slot filling and entity carry
    """
    
    def __init__(self):
        super().__init__(
            name="MemoryCarry",
            description="Tests memory and context carry across conversation turns"
        )
        
    def first_message(self, scenario: Dict[str, Any]) -> str:
        """Send the scenario's initial user message with context."""
        return scenario["conversation"]["initial_user_msg"]
        
    def next_message(self, last_agent_response: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[str]:
        """Generate next message that references earlier context."""
        conversation_context = self._extract_conversation_context(scenario)
        
        # Reference earlier information to test memory
        if "account" in conversation_context:
            return f"Thanks for helping with my {conversation_context['account']} account. Can you also check the balance?"
        elif "payment" in conversation_context:
            return f"About that {conversation_context['payment']} payment we discussed, when will it be processed?"
        elif "name" in conversation_context:
            return f"By the way, my name is {conversation_context['name']}. Can you update my profile?"
        else:
            return "Can you remind me what we were just talking about?"
            
    def should_continue(self, conversation: List[Dict[str, str]], scenario: Dict[str, Any]) -> bool:
        """Continue until memory test is complete or max turns reached."""
        max_turns = scenario["conversation"].get("max_turns", 5)
        if len(conversation) >= max_turns:
            return False
            
        # Check if memory test is complete
        if len(conversation) >= 3:  # Need at least 3 turns for memory test
            return False
                
        return True
        
    def _extract_conversation_context(self, scenario: Dict[str, Any]) -> Dict[str, str]:
        """Extract context information from the scenario."""
        context = {}
        
        # Extract account type if mentioned
        if "account" in scenario.get("goal", {}).get("user_goal", "").lower():
            context["account"] = "checking"
            
        # Extract payment info if mentioned
        if "payment" in scenario.get("goal", {}).get("user_goal", "").lower():
            context["payment"] = "$100"
            
        # Extract name if available
        context["name"] = "John Doe"
        
        return context
