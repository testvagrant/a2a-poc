"""
Unified Judge Interface

This module provides a unified interface for both heuristic and LLM-based judging.
It allows the UTA to use either approach or both for comprehensive evaluation.
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

from .schema_judge import run_hard_assertions, heuristic_soft_metrics
from .llm_judge import LLMJudge, LLMJudgeConfig, JudgeResult

class JudgeMode(Enum):
    """Available judging modes."""
    HEURISTIC = "heuristic"
    LLM = "llm"
    HYBRID = "hybrid"

@dataclass
class UnifiedJudgeConfig:
    """Configuration for unified judge."""
    mode: JudgeMode = JudgeMode.HEURISTIC
    llm_config: Optional[LLMJudgeConfig] = None
    hybrid_weights: Dict[str, float] = None
    
    def __post_init__(self):
        if self.hybrid_weights is None:
            self.hybrid_weights = {
                'heuristic': 0.5,
                'llm': 0.5
            }

@dataclass
class UnifiedJudgeResult:
    """Result from unified judge evaluation."""
    hard_results: Dict[str, bool]
    soft_metrics: Dict[str, float]
    judge_mode: JudgeMode
    llm_result: Optional[JudgeResult] = None
    hybrid_breakdown: Optional[Dict[str, Dict[str, float]]] = None

class UnifiedJudge:
    """
    Unified judge that can use heuristic, LLM, or hybrid evaluation.
    
    This judge provides a consistent interface while supporting multiple
    evaluation approaches for comprehensive AI agent assessment.
    """
    
    def __init__(self, config: UnifiedJudgeConfig):
        """
        Initialize unified judge with configuration.
        
        Args:
            config: Unified judge configuration
        """
        self.config = config
        self.llm_judge = None
        
        if config.mode in [JudgeMode.LLM, JudgeMode.HYBRID]:
            if config.llm_config is None:
                raise ValueError("LLM config required for LLM or hybrid mode")
            self.llm_judge = LLMJudge(config.llm_config)
    
    def evaluate(self, scenario: Dict[str, Any], 
                 messages: List[Dict[str, str]], 
                 agent_structured: Dict[str, Any]) -> UnifiedJudgeResult:
        """
        Evaluate AI agent response using the configured judging mode.
        
        Args:
            scenario: Scenario configuration
            messages: Conversation messages
            agent_structured: Structured response from agent
            
        Returns:
            UnifiedJudgeResult with evaluation results
        """
        # Always run hard assertions (they're deterministic)
        hard_results = run_hard_assertions(
            scenario.get('oracle', {}), 
            messages, 
            agent_structured
        )
        
        if self.config.mode == JudgeMode.HEURISTIC:
            return self._evaluate_heuristic(scenario, messages, agent_structured, hard_results)
        elif self.config.mode == JudgeMode.LLM:
            return self._evaluate_llm(scenario, messages, agent_structured, hard_results)
        elif self.config.mode == JudgeMode.HYBRID:
            return self._evaluate_hybrid(scenario, messages, agent_structured, hard_results)
        else:
            raise ValueError(f"Unsupported judge mode: {self.config.mode}")
    
    def _evaluate_heuristic(self, scenario: Dict[str, Any], 
                           messages: List[Dict[str, str]], 
                           agent_structured: Dict[str, Any],
                           hard_results: Dict[str, bool]) -> UnifiedJudgeResult:
        """Evaluate using heuristic approach."""
        soft_metrics = heuristic_soft_metrics(scenario, messages, agent_structured)
        
        return UnifiedJudgeResult(
            hard_results=hard_results,
            soft_metrics=soft_metrics,
            judge_mode=JudgeMode.HEURISTIC
        )
    
    def _evaluate_llm(self, scenario: Dict[str, Any], 
                     messages: List[Dict[str, str]], 
                     agent_structured: Dict[str, Any],
                     hard_results: Dict[str, bool]) -> UnifiedJudgeResult:
        """Evaluate using LLM approach."""
        llm_result = self.llm_judge.evaluate_response(scenario, messages, agent_structured)
        
        soft_metrics = {
            'relevance': llm_result.relevance,
            'completeness': llm_result.completeness,
            'groundedness': llm_result.groundedness
        }
        
        return UnifiedJudgeResult(
            hard_results=hard_results,
            soft_metrics=soft_metrics,
            judge_mode=JudgeMode.LLM,
            llm_result=llm_result
        )
    
    def _evaluate_hybrid(self, scenario: Dict[str, Any], 
                        messages: List[Dict[str, str]], 
                        agent_structured: Dict[str, Any],
                        hard_results: Dict[str, bool]) -> UnifiedJudgeResult:
        """Evaluate using hybrid approach (both heuristic and LLM)."""
        # Get heuristic evaluation
        heuristic_metrics = heuristic_soft_metrics(scenario, messages, agent_structured)
        
        # Get LLM evaluation
        llm_result = self.llm_judge.evaluate_response(scenario, messages, agent_structured)
        llm_metrics = {
            'relevance': llm_result.relevance,
            'completeness': llm_result.completeness,
            'groundedness': llm_result.groundedness
        }
        
        # Combine metrics using weights
        weights = self.config.hybrid_weights
        combined_metrics = {}
        for metric in ['relevance', 'completeness', 'groundedness']:
            heuristic_val = heuristic_metrics.get(metric, 0.0)
            llm_val = llm_metrics.get(metric, 0.0)
            combined_val = (heuristic_val * weights['heuristic'] + 
                           llm_val * weights['llm'])
            combined_metrics[metric] = combined_val
        
        # Create breakdown for transparency
        hybrid_breakdown = {
            'heuristic': heuristic_metrics,
            'llm': llm_metrics,
            'combined': combined_metrics
        }
        
        return UnifiedJudgeResult(
            hard_results=hard_results,
            soft_metrics=combined_metrics,
            judge_mode=JudgeMode.HYBRID,
            llm_result=llm_result,
            hybrid_breakdown=hybrid_breakdown
        )
    
    def get_judge_info(self) -> Dict[str, Any]:
        """Get information about the judge configuration."""
        info = {
            'mode': self.config.mode.value,
            'has_llm_judge': self.llm_judge is not None
        }
        
        if self.llm_judge:
            info['llm_model'] = self.config.llm_config.model_name
            info['llm_type'] = self.config.llm_config.judge_type.value
        
        if self.config.mode == JudgeMode.HYBRID:
            info['hybrid_weights'] = self.config.hybrid_weights
        
        return info

class UnifiedJudgeFactory:
    """Factory for creating unified judges with different configurations."""
    
    @staticmethod
    def create_heuristic_judge() -> UnifiedJudge:
        """Create heuristic-only judge."""
        config = UnifiedJudgeConfig(mode=JudgeMode.HEURISTIC)
        return UnifiedJudge(config)
    
    @staticmethod
    def create_llm_judge(llm_config: LLMJudgeConfig) -> UnifiedJudge:
        """Create LLM-only judge."""
        config = UnifiedJudgeConfig(mode=JudgeMode.LLM, llm_config=llm_config)
        return UnifiedJudge(config)
    
    @staticmethod
    def create_hybrid_judge(llm_config: LLMJudgeConfig, 
                           weights: Optional[Dict[str, float]] = None) -> UnifiedJudge:
        """Create hybrid judge (heuristic + LLM)."""
        config = UnifiedJudgeConfig(
            mode=JudgeMode.HYBRID, 
            llm_config=llm_config,
            hybrid_weights=weights
        )
        return UnifiedJudge(config)
    
    @staticmethod
    def create_from_config(config_dict: Dict[str, Any]) -> UnifiedJudge:
        """Create judge from configuration dictionary."""
        mode = JudgeMode(config_dict.get('mode', 'heuristic'))
        
        llm_config = None
        if mode in [JudgeMode.LLM, JudgeMode.HYBRID]:
            llm_config_dict = config_dict.get('llm_config', {})
            llm_config = LLMJudgeConfig(**llm_config_dict)
        
        weights = config_dict.get('hybrid_weights')
        
        config = UnifiedJudgeConfig(
            mode=mode,
            llm_config=llm_config,
            hybrid_weights=weights
        )
        
        return UnifiedJudge(config)

# Example usage and testing
if __name__ == "__main__":
    print("Testing Unified Judge...")
    
    # Test heuristic judge
    heuristic_judge = UnifiedJudgeFactory.create_heuristic_judge()
    print(f"Heuristic judge info: {heuristic_judge.get_judge_info()}")
    
    # Test LLM judge (requires API key)
    try:
        from .llm_judge import LLMJudgeConfig, JudgeType
        
        llm_config = LLMJudgeConfig(
            judge_type=JudgeType.OPENAI,
            model_name="gpt-3.5-turbo",
            api_key="your-api-key-here"
        )
        
        llm_judge = UnifiedJudgeFactory.create_llm_judge(llm_config)
        print(f"LLM judge info: {llm_judge.get_judge_info()}")
        
    except Exception as e:
        print(f"LLM judge test skipped: {e}")
    
    # Test hybrid judge
    try:
        hybrid_judge = UnifiedJudgeFactory.create_hybrid_judge(
            llm_config, 
            weights={'heuristic': 0.3, 'llm': 0.7}
        )
        print(f"Hybrid judge info: {hybrid_judge.get_judge_info()}")
        
    except Exception as e:
        print(f"Hybrid judge test skipped: {e}")
    
    print("Unified Judge test completed!")
