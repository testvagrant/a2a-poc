"""
Core conversation capabilities for universal testing.
Tests fundamental conversation skills that all AI agents should have.
"""

from typing import Dict, Any, List, Optional


class CoreConversationTests:
    """Test methods for core conversation capabilities."""
    
    def __init__(self, turn_count: int):
        self._turn_count = turn_count
    
    def test_conversation_flow(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test basic conversation flow."""
        if self._turn_count == 1:
            return "Can you help me understand what you can do?"
        elif self._turn_count == 2:
            return "That's helpful. Can you tell me more about your capabilities?"
        else:
            return "Let's continue our conversation"
    
    def test_intent_understanding(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test intent understanding capabilities."""
        intent_tests = [
            "I want to know about your features",
            "Can you help me solve a problem?",
            "I need information about something",
            "I want to make a request"
        ]
        return intent_tests[self._turn_count % len(intent_tests)]
    
    def test_context_retention(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test context retention across turns."""
        context_tests = [
            "What did I ask you about earlier?",
            "Can you remember what we discussed?",
            "Do you recall my previous question?",
            "What was the topic we were on?"
        ]
        return context_tests[self._turn_count % len(context_tests)]
    
    def test_turn_taking(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test turn-taking in conversation."""
        turn_tests = [
            "Let me ask you something else",
            "Can I interrupt you for a moment?",
            "I have another question",
            "Let me change the topic"
        ]
        return turn_tests[self._turn_count % len(turn_tests)]
    
    def test_conversation_repair(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test conversation repair capabilities."""
        repair_tests = [
            "I didn't understand that, can you explain?",
            "Can you rephrase that?",
            "I'm confused, can you clarify?",
            "Let me try asking this differently"
        ]
        return repair_tests[self._turn_count % len(repair_tests)]
