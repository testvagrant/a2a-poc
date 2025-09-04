import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class PolicyLoader:
    """
    Dynamic policy loader that supports different compliance profiles.
    """
    
    def __init__(self, fixtures_dir: str):
        self.fixtures_dir = Path(fixtures_dir)
        self._policies_cache = {}
        
    def load_profile(self, profile_name: str = "default") -> Dict[str, Any]:
        """Load a specific policy profile."""
        if profile_name in self._policies_cache:
            return self._policies_cache[profile_name]
            
        # Load base policies
        with open(self.fixtures_dir / "policies.yaml", "r", encoding="utf-8") as f:
            base_policies = yaml.safe_load(f)
            
        # Load profile-specific overrides
        profile_file = self.fixtures_dir / f"policies_{profile_name}.yaml"
        profile_overrides = {}
        if profile_file.exists():
            with open(profile_file, "r", encoding="utf-8") as f:
                profile_overrides = yaml.safe_load(f)
                
        # Merge base policies with profile overrides
        merged_policies = self._merge_policies(base_policies, profile_overrides)
        
        # Cache the result
        self._policies_cache[profile_name] = merged_policies
        return merged_policies
        
    def _merge_policies(self, base: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge policies with overrides taking precedence."""
        result = base.copy()
        
        for key, value in overrides.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_policies(result[key], value)
            else:
                result[key] = value
                
        return result
        
    def get_policy_value(self, profile_name: str, key_path: str, default: Any = None) -> Any:
        """Get a specific policy value using dot notation (e.g., 'mandatory_disclosures.0')."""
        policies = self.load_profile(profile_name)
        
        keys = key_path.split('.')
        current = policies
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
                
        return current
