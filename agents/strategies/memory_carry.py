from typing import Dict, Any, Optional, List
from .dynamic_base_strategy import DynamicBaseStrategy

class MemoryCarryStrategy(DynamicBaseStrategy):
    """
    MemoryCarry strategy: Tests memory and context carry across conversation turns.
    Now uses AI-powered dynamic conversation generation.
    
    - Sends initial message with context
    - References earlier information in follow-up messages
    - Checks if agent maintains context and memory
    - Tests slot filling and entity carry
    """
    
    def __init__(self):
        super().__init__(
            name="MemoryCarry",
            description="Tests memory and context carry across conversation turns",
            domain="memory"
        )
        
    def _extract_scenario_goals(self, scenario: Dict[str, Any]) -> List[str]:
        """Extract memory-specific goals from the scenario."""
        goals = super()._extract_scenario_goals(scenario)
        
        # Add memory-specific goals
        goals.extend([
            "Test agent's ability to retain context across turns",
            "Verify memory of account details and previous discussions",
            "Check if agent can reference earlier information",
            "Test slot filling and entity carry capabilities"
        ])
        
        return goals