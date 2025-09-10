"""
Comprehensive Universal Strategy for domain-agnostic AI testing.
Tests fundamental capabilities that all AI agents should have using modular test components.
"""

from typing import Dict, Any, List, Optional
import random
import json
import requests
from agents.agent_analyzer import AgentAnalyzer

# Import all test modules
from agents.strategies.universal.core_conversation import CoreConversationTests
from agents.strategies.universal.language_understanding import LanguageUnderstandingTests
from agents.strategies.universal.response_quality import ResponseQualityTests
from agents.strategies.universal.error_handling import ErrorHandlingTests
from agents.strategies.universal.reasoning_logic import ReasoningLogicTests
from agents.strategies.universal.memory_learning import MemoryLearningTests
from agents.strategies.universal.safety_ethics import SafetyEthicsTests


class ComprehensiveUniversalStrategy:
    """Comprehensive universal strategy for testing fundamental AI capabilities."""
    
    def __init__(self, agent_config: Dict[str, Any], scenario: Dict[str, Any]):
        self.name = "ComprehensiveUniversal"
        self.agent_config = agent_config
        self.scenario = scenario
        self._turn_count = 0
        self._tested_capabilities = set()
        self._agent_analyzer = AgentAnalyzer()
        
        # Initialize test modules
        self._core_tests = CoreConversationTests(self._turn_count)
        self._language_tests = LanguageUnderstandingTests(self._turn_count)
        self._quality_tests = ResponseQualityTests(self._turn_count)
        self._error_tests = ErrorHandlingTests(self._turn_count)
        self._reasoning_tests = ReasoningLogicTests(self._turn_count)
        self._memory_tests = MemoryLearningTests(self._turn_count)
        self._safety_tests = SafetyEthicsTests(self._turn_count)
        
        # Mock agent capabilities for demo
        self._agent_capabilities = {
            'domain_expertise': ['general_assistance'],
            'conversation_style': 'helpful',
            'api_capabilities': {'text_generation': True},
            'limitations': []
        }
        
        # Get comprehensive capabilities to test
        self.fundamental_capabilities = self._get_comprehensive_capabilities()
    
    def first_message(self, scenario: Dict[str, Any]) -> str:
        """Send the scenario's initial user message."""
        self._turn_count = 0
        self._tested_capabilities = set()
        return scenario["conversation"]["initial_user_msg"]
    
    def next_message(self, last_agent_response: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[str]:
        """Generate next message to test comprehensive AI capabilities."""
        self._turn_count += 1
        
        # Update test modules with current turn count
        self._update_test_modules()
        
        # Check if we should continue
        if not self.should_continue(scenario):
            return None
        
        # Select next capability to test
        capability = self._select_next_capability()
        if not capability:
            return None
        
        # Generate test message for the capability
        message = self._generate_capability_test_message(capability, scenario, last_agent_response)
        
        # Mark capability as tested
        self._tested_capabilities.add(capability)
        
        return message
    
    def should_continue(self, scenario: Dict[str, Any]) -> bool:
        """Check if we should continue the conversation."""
        max_turns = scenario.get("conversation", {}).get("max_turns", 10)
        return self._turn_count < max_turns
    
    def _update_test_modules(self):
        """Update all test modules with current turn count."""
        self._core_tests._turn_count = self._turn_count
        self._language_tests._turn_count = self._turn_count
        self._quality_tests._turn_count = self._turn_count
        self._error_tests._turn_count = self._turn_count
        self._reasoning_tests._turn_count = self._turn_count
        self._memory_tests._turn_count = self._turn_count
        self._safety_tests._turn_count = self._turn_count
    
    def _get_comprehensive_capabilities(self) -> List[str]:
        """Get comprehensive list of fundamental AI capabilities to test."""
        return [
            # Core Conversation Capabilities
            'conversation_flow',
            'intent_understanding',
            'context_retention',
            'turn_taking',
            'conversation_repair',
            
            # Language Understanding
            'natural_language_processing',
            'ambiguity_resolution',
            'sarcasm_detection',
            'sentiment_analysis',
            'entity_recognition',
            'pronoun_resolution',
            'negation_handling',
            'question_understanding',
            
            # Response Quality
            'response_relevance',
            'response_completeness',
            'response_accuracy',
            'response_consistency',
            'response_helpfulness',
            'response_clarity',
            'response_appropriateness',
            'response_timeliness',
            
            # Error Handling
            'error_detection',
            'error_recovery',
            'graceful_degradation',
            'fallback_handling',
            'exception_management',
            'validation_errors',
            'timeout_handling',
            'retry_mechanisms',
            
            # Reasoning & Logic
            'logical_reasoning',
            'causal_reasoning',
            'analogical_reasoning',
            'deductive_reasoning',
            'inductive_reasoning',
            'critical_thinking',
            'problem_solving',
            'pattern_recognition',
            
            # Memory & Learning
            'short_term_memory',
            'long_term_memory',
            'episodic_memory',
            'semantic_memory',
            'learning_adaptation',
            'context_switching',
            'memory_consolidation',
            'forgetting_curves',
            
            # Safety & Ethics
            'bias_detection',
            'harmful_content_detection',
            'privacy_protection',
            'ethical_guidelines',
            'safety_guardrails',
            'consent_handling',
            'transparency',
            'accountability'
        ]
    
    def _select_next_capability(self) -> Optional[str]:
        """Select the next capability to test."""
        untested = [cap for cap in self.fundamental_capabilities if cap not in self._tested_capabilities]
        
        if untested:
            return untested[0]
        
        # If all tested, return the most important one
        return self.fundamental_capabilities[0]
    
    def _generate_capability_test_message(self, capability: str, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> Optional[str]:
        """Generate message to test a specific capability using appropriate test module."""
        
        # Map capabilities to test modules
        capability_mapping = {
            # Core Conversation
            'conversation_flow': self._core_tests.test_conversation_flow,
            'intent_understanding': self._core_tests.test_intent_understanding,
            'context_retention': self._core_tests.test_context_retention,
            'turn_taking': self._core_tests.test_turn_taking,
            'conversation_repair': self._core_tests.test_conversation_repair,
            
            # Language Understanding
            'natural_language_processing': self._language_tests.test_nlp,
            'ambiguity_resolution': self._language_tests.test_ambiguity_resolution,
            'sarcasm_detection': self._language_tests.test_sarcasm_detection,
            'sentiment_analysis': self._language_tests.test_sentiment_analysis,
            'entity_recognition': self._language_tests.test_entity_recognition,
            'pronoun_resolution': self._language_tests.test_pronoun_resolution,
            'negation_handling': self._language_tests.test_negation_handling,
            'question_understanding': self._language_tests.test_question_understanding,
            
            # Response Quality
            'response_relevance': self._quality_tests.test_response_relevance,
            'response_completeness': self._quality_tests.test_response_completeness,
            'response_accuracy': self._quality_tests.test_response_accuracy,
            'response_consistency': self._quality_tests.test_response_consistency,
            'response_helpfulness': self._quality_tests.test_response_helpfulness,
            'response_clarity': self._quality_tests.test_response_clarity,
            'response_appropriateness': self._quality_tests.test_response_appropriateness,
            'response_timeliness': self._quality_tests.test_response_timeliness,
            
            # Error Handling
            'error_detection': self._error_tests.test_error_detection,
            'error_recovery': self._error_tests.test_error_recovery,
            'graceful_degradation': self._error_tests.test_graceful_degradation,
            'fallback_handling': self._error_tests.test_fallback_handling,
            'exception_management': self._error_tests.test_exception_management,
            'validation_errors': self._error_tests.test_validation_errors,
            'timeout_handling': self._error_tests.test_timeout_handling,
            'retry_mechanisms': self._error_tests.test_retry_mechanisms,
            
            # Reasoning & Logic
            'logical_reasoning': self._reasoning_tests.test_logical_reasoning,
            'causal_reasoning': self._reasoning_tests.test_causal_reasoning,
            'analogical_reasoning': self._reasoning_tests.test_analogical_reasoning,
            'deductive_reasoning': self._reasoning_tests.test_deductive_reasoning,
            'inductive_reasoning': self._reasoning_tests.test_inductive_reasoning,
            'critical_thinking': self._reasoning_tests.test_critical_thinking,
            'problem_solving': self._reasoning_tests.test_problem_solving,
            'pattern_recognition': self._reasoning_tests.test_pattern_recognition,
            
            # Memory & Learning
            'short_term_memory': self._memory_tests.test_short_term_memory,
            'long_term_memory': self._memory_tests.test_long_term_memory,
            'episodic_memory': self._memory_tests.test_episodic_memory,
            'semantic_memory': self._memory_tests.test_semantic_memory,
            'learning_adaptation': self._memory_tests.test_learning_adaptation,
            'context_switching': self._memory_tests.test_context_switching,
            'memory_consolidation': self._memory_tests.test_memory_consolidation,
            'forgetting_curves': self._memory_tests.test_forgetting_curves,
            
            # Safety & Ethics
            'bias_detection': self._safety_tests.test_bias_detection,
            'harmful_content_detection': self._safety_tests.test_harmful_content_detection,
            'privacy_protection': self._safety_tests.test_privacy_protection,
            'ethical_guidelines': self._safety_tests.test_ethical_guidelines,
            'safety_guardrails': self._safety_tests.test_safety_guardrails,
            'consent_handling': self._safety_tests.test_consent_handling,
            'transparency': self._safety_tests.test_transparency,
            'accountability': self._safety_tests.test_accountability
        }
        
        test_function = capability_mapping.get(capability)
        if test_function:
            return test_function(scenario, last_response)
        
        # Fallback to basic conversation flow
        return self._core_tests.test_conversation_flow(scenario, last_response)
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """Get information about this strategy."""
        return {
            'name': self.name,
            'description': 'Comprehensive universal strategy for testing fundamental AI capabilities',
            'domain': 'universal',
            'capabilities_tested': len(self.fundamental_capabilities),
            'tested_so_far': len(self._tested_capabilities),
            'turn_count': self._turn_count
        }
