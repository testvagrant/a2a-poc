from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List

class BaseStrategy(ABC):
    """
    Base class for all tester agent strategies.
    Each strategy implements a specific testing approach.
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        
    @abstractmethod
    def first_message(self, scenario: Dict[str, Any]) -> str:
        """Generate the first user message for the scenario."""
        pass
        
    @abstractmethod
    def next_message(self, last_agent_response: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[str]:
        """Generate the next user message based on agent response."""
        pass
        
    @abstractmethod
    def should_continue(self, conversation: List[Dict[str, str]], scenario: Dict[str, Any]) -> bool:
        """Determine if the conversation should continue."""
        pass
        
    def get_strategy_info(self) -> Dict[str, str]:
        """Get strategy metadata."""
        return {
            "name": self.name,
            "description": self.description
        }
