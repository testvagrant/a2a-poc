from typing import Dict, Type, Optional
from .base_strategy import BaseStrategy
from .flow_intent import FlowIntentStrategy
from .tool_happy_path import ToolHappyPathStrategy
from .memory_carry import MemoryCarryStrategy
from .tool_error import ToolErrorStrategy

class StrategyRegistry:
    """
    Registry for managing all available tester strategies.
    """
    
    def __init__(self):
        self._strategies: Dict[str, Type[BaseStrategy]] = {}
        self._register_default_strategies()
        
    def _register_default_strategies(self):
        """Register the default strategies."""
        self.register("FlowIntent", FlowIntentStrategy)
        self.register("ToolHappyPath", ToolHappyPathStrategy)
        self.register("MemoryCarry", MemoryCarryStrategy)
        self.register("ToolError", ToolErrorStrategy)
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
