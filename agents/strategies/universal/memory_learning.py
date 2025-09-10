"""
Memory and learning capabilities for universal testing.
Tests short-term memory, long-term memory, learning adaptation, etc.
"""

from typing import Dict, Any, List, Optional


class MemoryLearningTests:
    """Test methods for memory and learning capabilities."""
    
    def __init__(self, turn_count: int):
        self._turn_count = turn_count
    
    def test_short_term_memory(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test short-term memory capabilities."""
        short_memory_tests = [
            "What did I just tell you?",
            "Can you remember what we discussed in this conversation?",
            "What was the last thing I asked?",
            "Do you recall our recent exchange?"
        ]
        return short_memory_tests[self._turn_count % len(short_memory_tests)]
    
    def test_long_term_memory(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test long-term memory capabilities."""
        long_memory_tests = [
            "Do you remember our previous conversations?",
            "What did we talk about before?",
            "Can you recall our past interactions?",
            "Do you remember what I told you earlier?"
        ]
        return long_memory_tests[self._turn_count % len(long_memory_tests)]
    
    def test_episodic_memory(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test episodic memory capabilities."""
        episodic_tests = [
            "What happened in our last conversation?",
            "Can you tell me about our previous session?",
            "What events did we discuss?",
            "Do you remember the sequence of our conversation?"
        ]
        return episodic_tests[self._turn_count % len(episodic_tests)]
    
    def test_semantic_memory(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test semantic memory capabilities."""
        semantic_tests = [
            "What do you know about this topic?",
            "Can you recall facts about this subject?",
            "What information do you have stored?",
            "Do you remember the knowledge we discussed?"
        ]
        return semantic_tests[self._turn_count % len(semantic_tests)]
    
    def test_learning_adaptation(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test learning adaptation capabilities."""
        learning_tests = [
            "Can you learn from our conversation?",
            "Will you remember this for next time?",
            "Can you adapt based on what I tell you?",
            "Do you improve from our interactions?"
        ]
        return learning_tests[self._turn_count % len(learning_tests)]
    
    def test_context_switching(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test context switching capabilities."""
        context_tests = [
            "Let's switch to a different topic",
            "Can you change context?",
            "Let's talk about something else",
            "Can you handle topic changes?"
        ]
        return context_tests[self._turn_count % len(context_tests)]
    
    def test_memory_consolidation(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test memory consolidation capabilities."""
        consolidation_tests = [
            "Can you summarize what we've discussed?",
            "What are the key points from our conversation?",
            "Can you consolidate the information?",
            "What's the main takeaway?"
        ]
        return consolidation_tests[self._turn_count % len(consolidation_tests)]
    
    def test_forgetting_curves(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Test forgetting curve handling."""
        forgetting_tests = [
            "Do you forget information over time?",
            "How long do you remember things?",
            "What happens to old information?",
            "Do you have memory limits?"
        ]
        return forgetting_tests[self._turn_count % len(forgetting_tests)]
