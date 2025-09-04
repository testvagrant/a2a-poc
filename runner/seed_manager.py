"""
Seed Manager for Deterministic Test Runs

This module provides deterministic seeding capabilities to ensure
reproducible test runs across different environments and executions.
"""

import random
import hashlib
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

@dataclass
class SeedConfig:
    """Configuration for seeding."""
    seed: Optional[int] = None
    auto_seed: bool = True
    seed_source: str = "timestamp"  # "timestamp", "scenario_id", "custom"
    custom_seed: Optional[str] = None

class SeedManager:
    """
    Manages deterministic seeding for reproducible test runs.
    
    This class ensures that random number generation, scenario ordering,
    and other non-deterministic operations are reproducible when a seed is provided.
    """
    
    def __init__(self, config: SeedConfig):
        """
        Initialize seed manager with configuration.
        
        Args:
            config: Seed configuration
        """
        self.config = config
        self.original_seed = None
        self.current_seed = None
        self.seed_history: List[int] = []
        
        # Set initial seed
        self._set_initial_seed()
    
    def _set_initial_seed(self):
        """Set the initial seed based on configuration."""
        if self.config.seed is not None:
            # Use provided seed
            self.current_seed = self.config.seed
            self.original_seed = self.config.seed
        elif self.config.auto_seed:
            # Generate seed automatically
            if self.config.seed_source == "timestamp":
                self.current_seed = int(time.time() * 1000) % (2**32)
            elif self.config.seed_source == "custom" and self.config.custom_seed:
                # Generate seed from custom string
                self.current_seed = self._hash_to_seed(self.config.custom_seed)
            else:
                # Default to timestamp
                self.current_seed = int(time.time() * 1000) % (2**32)
        else:
            # No seeding
            self.current_seed = None
        
        if self.current_seed is not None:
            random.seed(self.current_seed)
            self.seed_history.append(self.current_seed)
    
    def _hash_to_seed(self, text: str) -> int:
        """Convert text to a deterministic seed."""
        hash_obj = hashlib.md5(text.encode())
        return int(hash_obj.hexdigest()[:8], 16)
    
    def get_scenario_seed(self, scenario_id: str) -> int:
        """
        Get a deterministic seed for a specific scenario.
        
        Args:
            scenario_id: Unique scenario identifier
            
        Returns:
            Deterministic seed for the scenario
        """
        if self.current_seed is None:
            return random.randint(0, 2**32 - 1)
        
        # Combine base seed with scenario ID for scenario-specific seeding
        scenario_seed = self._hash_to_seed(f"{self.current_seed}_{scenario_id}")
        return scenario_seed
    
    def set_scenario_seed(self, scenario_id: str):
        """
        Set the random seed for a specific scenario.
        
        Args:
            scenario_id: Unique scenario identifier
        """
        scenario_seed = self.get_scenario_seed(scenario_id)
        random.seed(scenario_seed)
        self.seed_history.append(scenario_seed)
    
    def reset_to_base_seed(self):
        """Reset random number generator to the base seed."""
        if self.current_seed is not None:
            random.seed(self.current_seed)
    
    def get_random_choice(self, choices: List[Any]) -> Any:
        """
        Get a deterministic random choice from a list.
        
        Args:
            choices: List of choices
            
        Returns:
            Deterministically selected choice
        """
        if not choices:
            return None
        return random.choice(choices)
    
    def get_random_int(self, min_val: int, max_val: int) -> int:
        """
        Get a deterministic random integer.
        
        Args:
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)
            
        Returns:
            Deterministic random integer
        """
        return random.randint(min_val, max_val)
    
    def get_random_float(self, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """
        Get a deterministic random float.
        
        Args:
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)
            
        Returns:
            Deterministic random float
        """
        return random.uniform(min_val, max_val)
    
    def shuffle_list(self, items: List[Any]) -> List[Any]:
        """
        Shuffle a list deterministically.
        
        Args:
            items: List to shuffle
            
        Returns:
            Deterministically shuffled list
        """
        shuffled = items.copy()
        random.shuffle(shuffled)
        return shuffled
    
    def get_seed_info(self) -> Dict[str, Any]:
        """
        Get information about current seeding state.
        
        Returns:
            Dictionary with seed information
        """
        return {
            'original_seed': self.original_seed,
            'current_seed': self.current_seed,
            'seed_history': self.seed_history.copy(),
            'auto_seed': self.config.auto_seed,
            'seed_source': self.config.seed_source,
            'is_deterministic': self.current_seed is not None
        }
    
    def create_scenario_seed_manager(self, scenario_id: str) -> 'ScenarioSeedManager':
        """
        Create a scenario-specific seed manager.
        
        Args:
            scenario_id: Unique scenario identifier
            
        Returns:
            Scenario-specific seed manager
        """
        return ScenarioSeedManager(self, scenario_id)

class ScenarioSeedManager:
    """
    Scenario-specific seed manager for fine-grained control.
    """
    
    def __init__(self, parent_manager: SeedManager, scenario_id: str):
        """
        Initialize scenario seed manager.
        
        Args:
            parent_manager: Parent seed manager
            scenario_id: Scenario identifier
        """
        self.parent_manager = parent_manager
        self.scenario_id = scenario_id
        self.scenario_seed = parent_manager.get_scenario_seed(scenario_id)
        self.local_seed = self.scenario_seed
    
    def set_local_seed(self, seed: int):
        """Set a local seed for this scenario."""
        self.local_seed = seed
        random.seed(seed)
    
    def reset_to_scenario_seed(self):
        """Reset to the scenario's base seed."""
        random.seed(self.scenario_seed)
        self.local_seed = self.scenario_seed
    
    def get_random_choice(self, choices: List[Any]) -> Any:
        """Get a deterministic random choice for this scenario."""
        if not choices:
            return None
        return random.choice(choices)
    
    def get_random_int(self, min_val: int, max_val: int) -> int:
        """Get a deterministic random integer for this scenario."""
        return random.randint(min_val, max_val)
    
    def get_random_float(self, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Get a deterministic random float for this scenario."""
        return random.uniform(min_val, max_val)

# Global seed manager instance
_global_seed_manager: Optional[SeedManager] = None

def initialize_seed_manager(config: SeedConfig) -> SeedManager:
    """
    Initialize the global seed manager.
    
    Args:
        config: Seed configuration
        
    Returns:
        Initialized seed manager
    """
    global _global_seed_manager
    _global_seed_manager = SeedManager(config)
    return _global_seed_manager

def get_seed_manager() -> Optional[SeedManager]:
    """
    Get the global seed manager.
    
    Returns:
        Global seed manager or None if not initialized
    """
    return _global_seed_manager

def get_scenario_seed_manager(scenario_id: str) -> Optional[ScenarioSeedManager]:
    """
    Get a scenario-specific seed manager.
    
    Args:
        scenario_id: Scenario identifier
        
    Returns:
        Scenario seed manager or None if global manager not initialized
    """
    global_manager = get_seed_manager()
    if global_manager:
        return global_manager.create_scenario_seed_manager(scenario_id)
    return None

# Example usage and testing
if __name__ == "__main__":
    # Test deterministic seeding
    print("Testing Seed Manager...")
    
    # Test with fixed seed
    config = SeedConfig(seed=12345)
    manager = SeedManager(config)
    
    print(f"Seed info: {manager.get_seed_info()}")
    
    # Test deterministic random generation
    numbers1 = [manager.get_random_int(1, 100) for _ in range(5)]
    print(f"Random numbers (first run): {numbers1}")
    
    # Reset and generate again
    manager.reset_to_base_seed()
    numbers2 = [manager.get_random_int(1, 100) for _ in range(5)]
    print(f"Random numbers (second run): {numbers2}")
    
    # Should be identical
    print(f"Numbers are identical: {numbers1 == numbers2}")
    
    # Test scenario-specific seeding
    scenario_manager = manager.create_scenario_seed_manager("TEST_SCENARIO")
    scenario_numbers = [scenario_manager.get_random_int(1, 100) for _ in range(3)]
    print(f"Scenario-specific numbers: {scenario_numbers}")
    
    print("Seed Manager test completed!")
