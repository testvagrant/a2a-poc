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
        self._turn_count = 0
        
    def first_message(self, scenario: Dict[str, Any]) -> str:
        """Send the scenario's initial user message with context."""
        return scenario["conversation"]["initial_user_msg"]
        
    def next_message(self, last_agent_response: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[str]:
        """Generate next message that references earlier context."""
        conversation_context = self._extract_conversation_context(scenario)
        self._turn_count += 1
        
        # Turn 2: Reference account number to test memory
        if self._turn_count == 1:
            if "account_number" in conversation_context:
                return f"Can you confirm that my account number {conversation_context['account_number']} is correct in your system?"
            else:
                return "Can you confirm my account details are correct in your system?"
        
        # Turn 3: Reference payment issue to test context carry
        elif self._turn_count == 2:
            if "payment_issue" in conversation_context:
                return f"About the payment issue I mentioned earlier, what are my options to resolve it?"
            else:
                return "What are my options to resolve the issue we discussed?"
        
        # Turn 4: Final memory test - ask agent to summarize what was discussed
        elif self._turn_count == 3:
            return "Can you summarize what we've discussed so far to make sure we're on the same page?"
        
        return None
            
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
        
        # Extract account number from initial message
        initial_msg = scenario.get("conversation", {}).get("initial_user_msg", "")
        if "12345" in initial_msg:
            context["account_number"] = "12345"
            
        # Extract account type
        if "checking account" in initial_msg.lower():
            context["account_type"] = "checking"
            
        # Extract payment issue context
        if "payment issue" in initial_msg.lower():
            context["payment_issue"] = "payment issue"
            
        return context
        
