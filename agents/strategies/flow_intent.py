from typing import Dict, Any, Optional, List
from .dynamic_base_strategy import DynamicBaseStrategy

class FlowIntentStrategy(DynamicBaseStrategy):
    """
    FlowIntent strategy: Simple flow testing with optional clarification.
    Now uses AI-powered dynamic conversation generation.
    
    - Sends initial message
    - Asks one clarifier if ambiguous
    - Confirms when appropriate
    - Stops when goal achieved
    """
    
    def __init__(self):
        super().__init__(
            name="FlowIntent",
            description="Simple flow testing with optional clarification and confirmation",
            domain="conversation_flow"
        )
        
    def _extract_scenario_goals(self, scenario: Dict[str, Any]) -> List[str]:
        """Extract flow-specific goals from the scenario."""
        goals = super()._extract_scenario_goals(scenario)
        
        # Add flow-specific goals
        goals.extend([
            "Test basic conversation flow and intent understanding",
            "Verify agent can handle clarification requests",
            "Check if agent provides appropriate confirmations",
            "Test natural conversation progression"
        ])
        
        return goals