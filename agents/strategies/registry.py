from typing import Dict, Type, Optional
from .base_strategy import BaseStrategy
from .flow_intent import FlowIntentStrategy
from .tool_happy_path import ToolHappyPathStrategy
from .memory_carry import MemoryCarryStrategy
from .tool_error import ToolErrorStrategy
from .dynamic_ai_strategy import DynamicAIStrategy
from .dynamic_financial_strategy import DynamicFinancialStrategy
from .dynamic_customer_service_strategy import DynamicCustomerServiceStrategy
from .dynamic_strategy_factory import DynamicStrategyFactory

class StrategyRegistry:
    """
    Registry for managing all available tester strategies.
    """
    
    def __init__(self):
        self._strategies: Dict[str, Type[BaseStrategy]] = {}
        self._register_default_strategies()
        
    def _register_default_strategies(self):
        """Register the default strategies."""
        # Traditional strategies
        self.register("FlowIntent", FlowIntentStrategy)
        self.register("ToolHappyPath", ToolHappyPathStrategy)
        self.register("MemoryCarry", MemoryCarryStrategy)
        self.register("ToolError", ToolErrorStrategy)
        
        # Dynamic AI-powered strategies
        self.register("DynamicAI", DynamicAIStrategy)
        self.register("DynamicFinancial", DynamicFinancialStrategy)
        self.register("DynamicCustomerService", DynamicCustomerServiceStrategy)
        
        # TODO: Register other strategies as they're implemented
        # self.register("Disturbance", DisturbanceStrategy)
        # self.register("Planner", PlannerStrategy)
        # self.register("Persona", PersonaStrategy)
        # self.register("PIIProbe", PIIProbeStrategy)
        # self.register("Interruption", InterruptionStrategy)
        # self.register("RepeatProbe", RepeatProbeStrategy)
        
    def register(self, name: str, strategy_class: Type[BaseStrategy]):
        """Register a new strategy."""
        self._strategies[name] = strategy_class
        
    def get(self, name: str) -> Optional[BaseStrategy]:
        """Get a strategy instance by name."""
        if name not in self._strategies:
            return None
        return self._strategies[name]()
        
    def list_available(self) -> list[str]:
        """List all available strategy names."""
        return list(self._strategies.keys())
        
    def get_default(self) -> BaseStrategy:
        """Get the default strategy (FlowIntent)."""
        return self.get("FlowIntent")
        
    def validate_strategy(self, strategy_name: str) -> bool:
        """Check if a strategy name is valid."""
        return strategy_name in self._strategies
        
    def create_dynamic_strategy(self, agent_url: str, scenario: Dict, agent_name: str = None) -> BaseStrategy:
        """Create a dynamic strategy using the factory."""
        factory = DynamicStrategyFactory()
        return factory.create_strategy(agent_url, scenario, agent_name)
        
    def get_dynamic_strategies(self) -> list[str]:
        """Get list of dynamic AI-powered strategies."""
        dynamic_strategies = [
            "DynamicAI",
            "DynamicFinancial", 
            "DynamicCustomerService"
        ]
        return [s for s in dynamic_strategies if s in self._strategies]
