"""
Response quality capabilities for universal testing.
Tests relevance, completeness, accuracy, consistency, etc.
"""

from typing import Dict, Any, List, Optional


class ResponseQualityTests:
    """Test methods for response quality capabilities."""
    
    def __init__(self, turn_count: int):
        self._turn_count = turn_count
    
    def test_response_relevance(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test response relevance."""
        relevance_tests = [
            "That doesn't answer my question",
            "You're going off topic",
            "Can you stay focused on what I asked?",
            "This is not what I need"
        ]
        return relevance_tests[self._turn_count % len(relevance_tests)]
    
    def test_response_completeness(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test response completeness."""
        completeness_tests = [
            "That's not a complete answer",
            "You only answered part of my question",
            "I need more details",
            "Can you be more thorough?"
        ]
        return completeness_tests[self._turn_count % len(completeness_tests)]
    
    def test_response_accuracy(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test response accuracy."""
        accuracy_tests = [
            "That doesn't sound right",
            "Are you sure about that?",
            "I think that's incorrect",
            "Can you double-check that information?"
        ]
        return accuracy_tests[self._turn_count % len(accuracy_tests)]
    
    def test_response_consistency(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test response consistency."""
        consistency_tests = [
            "You said something different earlier",
            "That contradicts what you told me before",
            "You're being inconsistent",
            "Which answer is correct?"
        ]
        return consistency_tests[self._turn_count % len(consistency_tests)]
    
    def test_response_helpfulness(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test response helpfulness."""
        helpfulness_tests = [
            "That's not very helpful",
            "Can you be more useful?",
            "I need practical advice",
            "How does this help me?"
        ]
        return helpfulness_tests[self._turn_count % len(helpfulness_tests)]
    
    def test_response_clarity(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test response clarity."""
        clarity_tests = [
            "That's not clear to me",
            "Can you explain that better?",
            "I don't understand what you mean",
            "Can you be more specific?"
        ]
        return clarity_tests[self._turn_count % len(clarity_tests)]
    
    def test_response_appropriateness(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test response appropriateness."""
        appropriateness_tests = [
            "That's not appropriate",
            "That's too personal",
            "That's not professional",
            "That's not what I expected"
        ]
        return appropriateness_tests[self._turn_count % len(appropriateness_tests)]
    
    def test_response_timeliness(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test response timeliness."""
        timeliness_tests = [
            "That took too long",
            "I needed a faster response",
            "Can you respond more quickly?",
            "That was too slow"
        ]
        return timeliness_tests[self._turn_count % len(timeliness_tests)]
