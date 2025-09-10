"""
Dynamic Base Strategy - All strategies should use AI-powered conversation generation.
This provides a common foundation for all strategies to use dynamic AI conversation.
"""

from typing import Dict, Any, Optional, List
import json
import requests
import os


class DynamicBaseStrategy:
    """Base class for all strategies that use AI-powered dynamic conversation generation."""
    
    def __init__(self, name: str, description: str, domain: str = "generic"):
        self.name = name
        self.description = description
        self.domain = domain
        self._turn_count = 0
        self._conversation_context = []
        self._scenario_goals = []
        
    def first_message(self, scenario: Dict[str, Any]) -> str:
        """Send the scenario's initial user message."""
        self._turn_count = 0
        self._conversation_context = []
        self._scenario_goals = self._extract_scenario_goals(scenario)
        return scenario["conversation"]["initial_user_msg"]
    
    def next_message(self, last_agent_response: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[str]:
        """Generate next message using AI-powered dynamic conversation."""
        self._turn_count += 1
        
        # Update conversation context
        self._conversation_context.append({
            'role': 'assistant',
            'content': last_agent_response.get('text', '')
        })
        
        # Check if we should continue
        if not self.should_continue(scenario):
            return None
        
        # Generate AI-powered message
        return self._generate_ai_message(scenario, last_agent_response)
    
    def should_continue(self, scenario: Dict[str, Any]) -> bool:
        """Check if we should continue the conversation."""
        max_turns = scenario.get("conversation", {}).get("max_turns", 10)
        return self._turn_count < max_turns
    
    def _generate_ai_message(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Generate AI-powered message based on strategy and scenario goals."""
        
        # Build context for AI
        context = {
            'strategy_name': self.name,
            'strategy_description': self.description,
            'domain': self.domain,
            'turn_count': self._turn_count,
            'scenario_goals': self._scenario_goals,
            'conversation_history': self._conversation_context[-5:],  # Last 5 exchanges
            'last_agent_response': last_response.get('text', ''),
            'scenario_context': scenario.get('description', '')
        }
        
        # Generate message using AI
        return self._call_ai_for_message_generation(context)
    
    def _call_ai_for_message_generation(self, context: Dict[str, Any]) -> str:
        """Call AI to generate the next message."""
        
        # Get OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return self._fallback_message()
        
        # Prepare the prompt
        prompt = self._build_ai_prompt(context)
        
        # Call OpenAI API
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'gpt-4o',
                    'messages': [
                        {
                            'role': 'system',
                            'content': prompt
                        }
                    ],
                    'max_tokens': 150,
                    'temperature': 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"AI API error: {response.status_code}")
                return self._fallback_message()
                
        except Exception as e:
            print(f"AI API call failed: {e}")
            return self._fallback_message()
    
    def _build_ai_prompt(self, context: Dict[str, Any]) -> str:
        """Build the AI prompt for message generation."""
        
        return f"""You are a UTA (Universal Tester-Agent) testing an AI agent. Your role is to generate the next user message in a conversation to test the agent's capabilities.

STRATEGY: {context['strategy_name']}
DESCRIPTION: {context['strategy_description']}
DOMAIN: {context['domain']}
TURN: {context['turn_count']}

SCENARIO GOALS: {', '.join(context['scenario_goals'])}

CONVERSATION HISTORY:
{self._format_conversation_history(context['conversation_history'])}

LAST AGENT RESPONSE: "{context['last_agent_response']}"

INSTRUCTIONS:
1. Generate a natural, human-like user message that tests the agent's capabilities
2. Align with the strategy goals and scenario objectives
3. Build on the conversation naturally
4. Test specific capabilities relevant to the strategy
5. Keep the message concise but meaningful
6. Make it sound like a real user would speak

Generate only the user message, no explanations or formatting."""

    def _format_conversation_history(self, history: List[Dict[str, Any]]) -> str:
        """Format conversation history for the prompt."""
        formatted = []
        for i, exchange in enumerate(history):
            role = exchange.get('role', 'assistant')
            content = exchange.get('content', '')
            formatted.append(f"{role.upper()}: {content}")
        return "\n".join(formatted)
    
    def _extract_scenario_goals(self, scenario: Dict[str, Any]) -> List[str]:
        """Extract goals from the scenario."""
        goals = []
        
        # Extract from scenario description
        description = scenario.get('description', '')
        if description:
            goals.append(f"Test scenario: {description}")
        
        # Extract from conversation goals
        conversation = scenario.get('conversation', {})
        if 'goals' in conversation:
            goals.extend(conversation['goals'])
        
        # Extract from preconditions
        preconditions = scenario.get('preconditions', {})
        if preconditions:
            goals.append(f"Test preconditions: {preconditions}")
        
        return goals
    
    def _fallback_message(self) -> str:
        """Fallback message when AI is not available."""
        fallback_messages = [
            "Can you help me with that?",
            "I need more information",
            "What do you think about this?",
            "Can you explain that better?",
            "I have another question"
        ]
        return fallback_messages[self._turn_count % len(fallback_messages)]
    
    def get_strategy_info(self) -> Dict[str, Any]:
        """Get information about this strategy."""
        return {
            'name': self.name,
            'description': self.description,
            'domain': self.domain,
            'turn_count': self._turn_count,
            'uses_ai_generation': True
        }
