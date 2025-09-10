"""
Reasoning and logic capabilities for universal testing.
Tests logical reasoning, causal reasoning, analogical reasoning, etc.
"""

from typing import Dict, Any, List, Optional


class ReasoningLogicTests:
    """Test methods for reasoning and logic capabilities."""
    
    def __init__(self, turn_count: int):
        self._turn_count = turn_count
    
    def test_logical_reasoning(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test logical reasoning capabilities."""
        logic_tests = [
            "If A implies B, and B implies C, what can we say about A and C?",
            "All birds can fly. Penguins are birds. Can penguins fly?",
            "If it's raining, then the ground is wet. The ground is wet. Is it raining?",
            "Some cats are black. Some black things are scary. Are some cats scary?"
        ]
        return logic_tests[self._turn_count % len(logic_tests)]
    
    def test_causal_reasoning(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test causal reasoning capabilities."""
        causal_tests = [
            "What causes rain?",
            "Why did the car stop working?",
            "What would happen if I didn't water the plants?",
            "Why is the sky blue?"
        ]
        return causal_tests[self._turn_count % len(causal_tests)]
    
    def test_analogical_reasoning(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test analogical reasoning capabilities."""
        analogy_tests = [
            "A heart is to a body as a pump is to what?",
            "How is a library like a database?",
            "What's similar between a computer and a brain?",
            "How is learning like building a house?"
        ]
        return analogy_tests[self._turn_count % len(analogy_tests)]
    
    def test_deductive_reasoning(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test deductive reasoning capabilities."""
        deductive_tests = [
            "All mammals are warm-blooded. Whales are mammals. Therefore?",
            "If it's a weekday, then I work. Today is Tuesday. Therefore?",
            "All roses are flowers. This is a rose. Therefore?",
            "If it's snowing, then it's cold. It's snowing. Therefore?"
        ]
        return deductive_tests[self._turn_count % len(deductive_tests)]
    
    def test_inductive_reasoning(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test inductive reasoning capabilities."""
        inductive_tests = [
            "Every swan I've seen is white. What can I conclude?",
            "The sun has risen every day. What can I predict?",
            "All the apples I've eaten are sweet. What's likely?",
            "Every time I press this button, a light turns on. What should happen next?"
        ]
        return inductive_tests[self._turn_count % len(inductive_tests)]
    
    def test_critical_thinking(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test critical thinking capabilities."""
        critical_tests = [
            "What are the assumptions in this argument?",
            "What evidence supports this claim?",
            "What are the weaknesses in this reasoning?",
            "How reliable is this source?"
        ]
        return critical_tests[self._turn_count % len(critical_tests)]
    
    def test_problem_solving(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test problem solving capabilities."""
        problem_tests = [
            "How would you solve this problem?",
            "What steps would you take?",
            "What are the possible solutions?",
            "How would you approach this challenge?"
        ]
        return problem_tests[self._turn_count % len(problem_tests)]
    
    def test_pattern_recognition(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test pattern recognition capabilities."""
        pattern_tests = [
            "What pattern do you see in this sequence: 2, 4, 8, 16, ?",
            "What's the next number: 1, 1, 2, 3, 5, 8, ?",
            "What's the pattern in these shapes?",
            "What comes next in this series?"
        ]
        return pattern_tests[self._turn_count % len(pattern_tests)]
