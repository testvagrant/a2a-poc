"""
Budget Enforcement Module

Handles enforcement of budget constraints during test execution:
- Turn limits (max_turns)
- Latency tracking (max_latency_ms_avg)
- Cost monitoring (max_cost_usd_per_session)
"""

import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class BudgetMetrics:
    """Tracks budget metrics during test execution."""
    turns_used: int = 0
    total_latency_ms: float = 0.0
    estimated_cost_usd: float = 0.0
    start_time: float = 0.0
    
    def __post_init__(self):
        if self.start_time == 0.0:
            self.start_time = time.time()
    
    def add_turn(self, latency_ms: float, estimated_cost: float = 0.0):
        """Add a turn with its latency and cost."""
        self.turns_used += 1
        self.total_latency_ms += latency_ms
        self.estimated_cost_usd += estimated_cost
    
    def get_average_latency_ms(self) -> float:
        """Get average latency per turn."""
        if self.turns_used == 0:
            return 0.0
        return self.total_latency_ms / self.turns_used
    
    def get_elapsed_time_ms(self) -> float:
        """Get total elapsed time in milliseconds."""
        return (time.time() - self.start_time) * 1000

class BudgetEnforcer:
    """
    Enforces budget constraints during test execution.
    """
    
    def __init__(self, budget_config: Dict[str, Any]):
        """
        Initialize budget enforcer with configuration.
        
        Args:
            budget_config: Budget configuration from scenario
                - max_turns: Maximum number of turns allowed
                - max_latency_ms_avg: Maximum average latency per turn
                - max_cost_usd_per_session: Maximum cost per session
        """
        self.max_turns = budget_config.get('max_turns', 10)
        self.max_latency_ms_avg = budget_config.get('max_latency_ms_avg', 5000.0)
        self.max_cost_usd_per_session = budget_config.get('max_cost_usd_per_session', 0.10)
        
        self.metrics = BudgetMetrics()
        self.violations: List[str] = []
    
    def check_turn_limit(self) -> bool:
        """Check if turn limit has been exceeded."""
        if self.metrics.turns_used >= self.max_turns:
            self.violations.append(f"Turn limit exceeded: {self.metrics.turns_used}/{self.max_turns}")
            return False
        return True
    
    def check_latency_limit(self) -> bool:
        """Check if latency limit has been exceeded."""
        avg_latency = self.metrics.get_average_latency_ms()
        if avg_latency > self.max_latency_ms_avg:
            self.violations.append(f"Latency limit exceeded: {avg_latency:.2f}ms > {self.max_latency_ms_avg}ms")
            return False
        return True
    
    def check_cost_limit(self) -> bool:
        """Check if cost limit has been exceeded."""
        if self.metrics.estimated_cost_usd > self.max_cost_usd_per_session:
            self.violations.append(f"Cost limit exceeded: ${self.metrics.estimated_cost_usd:.4f} > ${self.max_cost_usd_per_session:.4f}")
            return False
        return True
    
    def record_turn(self, latency_ms: float, estimated_cost: float = 0.0) -> bool:
        """
        Record a turn and check all budget constraints.
        
        Args:
            latency_ms: Latency for this turn in milliseconds
            estimated_cost: Estimated cost for this turn in USD
            
        Returns:
            True if budget constraints are satisfied, False otherwise
        """
        self.metrics.add_turn(latency_ms, estimated_cost)
        
        # Check all constraints
        turn_ok = self.check_turn_limit()
        latency_ok = self.check_latency_limit()
        cost_ok = self.check_cost_limit()
        
        return turn_ok and latency_ok and cost_ok
    
    def get_status(self) -> Dict[str, Any]:
        """Get current budget status."""
        return {
            'turns_used': self.metrics.turns_used,
            'max_turns': self.max_turns,
            'turns_remaining': max(0, self.max_turns - self.metrics.turns_used),
            'average_latency_ms': self.metrics.get_average_latency_ms(),
            'max_latency_ms_avg': self.max_latency_ms_avg,
            'total_cost_usd': self.metrics.estimated_cost_usd,
            'max_cost_usd_per_session': self.max_cost_usd_per_session,
            'elapsed_time_ms': self.metrics.get_elapsed_time_ms(),
            'violations': self.violations.copy(),
            'within_budget': len(self.violations) == 0
        }
    
    def estimate_turn_cost(self, message_length: int, response_length: int) -> float:
        """
        Estimate cost for a turn based on message and response lengths.
        
        This is a simplified cost estimation model. In production, this would
        be based on actual LLM pricing and usage patterns.
        
        Args:
            message_length: Length of user message
            response_length: Length of agent response
            
        Returns:
            Estimated cost in USD
        """
        # Simplified cost model: $0.001 per 1000 characters
        total_chars = message_length + response_length
        return (total_chars / 1000.0) * 0.001
    
    def should_continue(self) -> bool:
        """Check if execution should continue based on budget constraints."""
        return len(self.violations) == 0 and self.metrics.turns_used < self.max_turns

class BudgetViolationError(Exception):
    """Raised when budget constraints are violated."""
    
    def __init__(self, violations: List[str], metrics: BudgetMetrics):
        self.violations = violations
        self.metrics = metrics
        super().__init__(f"Budget violations: {', '.join(violations)}")
