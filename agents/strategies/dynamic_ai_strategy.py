"""
Dynamic AI Strategy - AI-Powered Message Generation

This strategy uses AI to dynamically generate appropriate messages based on:
1. Agent capabilities analysis
2. Conversation context
3. Scenario goals
4. Agent response patterns

This makes the UTA system truly scalable across different applications and domains.
"""

import json
import time
from typing import Dict, Any, Optional, List
from .base_strategy import BaseStrategy

class DynamicAIStrategy(BaseStrategy):
    """
    Dynamic AI Strategy: Uses AI to generate contextually appropriate messages.
    
    This strategy analyzes the agent under test and generates messages dynamically
    based on the agent's capabilities, conversation context, and scenario goals.
    """
    
    def __init__(self, llm_config: Dict[str, Any] = None):
        super().__init__(
            name="DynamicAI",
            description="AI-powered dynamic message generation based on agent analysis"
        )
        self.llm_config = llm_config or {
            'model': 'gpt-4o-mini',
            'temperature': 0.7,
            'max_tokens': 500
        }
        self._agent_capabilities = None
        self._conversation_context = []
        self._turn_count = 0
        
    def first_message(self, scenario: Dict[str, Any]) -> str:
        """Send the scenario's initial user message."""
        self._conversation_context = []
        self._turn_count = 0
        return scenario["conversation"]["initial_user_msg"]
        
    def next_message(self, last_agent_response: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[str]:
        """Generate next message using AI based on agent response and context."""
        self._turn_count += 1
        
        # Analyze agent capabilities if not done yet
        if self._agent_capabilities is None:
            self._agent_capabilities = self._analyze_agent_capabilities(last_agent_response, scenario)
        
        # Update conversation context
        self._conversation_context.append({
            'role': 'assistant',
            'content': last_agent_response.get('text', ''),
            'structured': last_agent_response.get('structured', {}),
            'turn': self._turn_count
        })
        
        # Generate next message using AI
        next_message = self._generate_ai_message(scenario, last_agent_response)
        
        # Add to context
        if next_message:
            self._conversation_context.append({
                'role': 'user',
                'content': next_message,
                'turn': self._turn_count + 1
            })
        
        return next_message
        
    def should_continue(self, conversation: List[Dict[str, str]], scenario: Dict[str, Any]) -> bool:
        """Determine if conversation should continue based on AI analysis."""
        max_turns = scenario["conversation"].get("max_turns", 5)
        
        if len(conversation) >= max_turns:
            return False
            
        # Use AI to determine if goal is achieved
        goal_achieved = self._check_goal_achievement(scenario, conversation)
        
        return not goal_achieved
        
    def _analyze_agent_capabilities(self, response: Dict[str, Any], scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze agent capabilities from its response."""
        capabilities = {
            'supports_structured_data': bool(response.get('structured')),
            'response_quality': 'high' if len(response.get('text', '')) > 50 else 'low',
            'domain_knowledge': self._infer_domain_knowledge(response, scenario),
            'conversation_style': self._infer_conversation_style(response),
            'capabilities': self._extract_capabilities_from_response(response)
        }
        
        return capabilities
        
    def _infer_domain_knowledge(self, response: Dict[str, Any], scenario: Dict[str, Any]) -> str:
        """Infer domain knowledge from agent response."""
        text = response.get('text', '').lower()
        tags = scenario.get('tags', [])
        
        if any(tag in text for tag in ['account', 'balance', 'payment', 'transaction']):
            return 'financial'
        elif any(tag in text for tag in ['support', 'help', 'issue', 'problem']):
            return 'customer_service'
        elif any(tag in text for tag in ['collections', 'debt', 'payment_plan']):
            return 'collections'
        else:
            return 'general'
            
    def _infer_conversation_style(self, response: Dict[str, Any]) -> str:
        """Infer conversation style from agent response."""
        text = response.get('text', '')
        
        if '?' in text:
            return 'inquisitive'
        elif len(text.split()) > 20:
            return 'detailed'
        elif any(word in text.lower() for word in ['please', 'thank you', 'appreciate']):
            return 'polite'
        else:
            return 'direct'
            
    def _extract_capabilities_from_response(self, response: Dict[str, Any]) -> List[str]:
        """Extract specific capabilities from agent response."""
        capabilities = []
        text = response.get('text', '').lower()
        structured = response.get('structured', {})
        
        if 'can help' in text or 'assist' in text:
            capabilities.append('assistance')
        if 'account' in text:
            capabilities.append('account_management')
        if 'payment' in text:
            capabilities.append('payment_processing')
        if structured:
            capabilities.append('structured_data')
        if '?' in text:
            capabilities.append('clarification')
            
        return capabilities
        
    def _generate_ai_message(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> Optional[str]:
        """Generate next message using AI based on context and agent response."""
        
        # Create AI prompt for message generation
        prompt = self._create_message_generation_prompt(scenario, last_response)
        
        # Get AI response (this would use the same LLM infrastructure as the judge)
        try:
            ai_response = self._call_ai_for_message_generation(prompt)
            return self._parse_ai_message_response(ai_response)
        except Exception as e:
            # Fallback to heuristic approach
            return self._fallback_message_generation(scenario, last_response)
            
    def _create_message_generation_prompt(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Create prompt for AI message generation."""
        
        # Extract scenario context
        user_goal = scenario.get('goal', {}).get('user_goal', '')
        scenario_title = scenario.get('title', '')
        tags = scenario.get('tags', [])
        
        # Get conversation history
        conversation_history = self._format_conversation_history()
        
        # Get agent capabilities
        capabilities_summary = json.dumps(self._agent_capabilities, indent=2)
        
        # Get last agent response
        last_text = last_response.get('text', '')
        last_structured = last_response.get('structured', {})
        
        prompt = f"""
You are an AI testing agent that generates realistic user messages to test other AI agents.

SCENARIO CONTEXT:
- Title: {scenario_title}
- User Goal: {user_goal}
- Tags: {', '.join(tags)}
- Turn: {self._turn_count}

AGENT CAPABILITIES:
{capabilities_summary}

CONVERSATION HISTORY:
{conversation_history}

LAST AGENT RESPONSE:
Text: {last_text}
Structured Data: {json.dumps(last_structured, indent=2)}

TASK:
Generate the next user message that would naturally follow in this conversation. The message should:
1. Be realistic and human-like
2. Test the agent's capabilities appropriately
3. Move toward achieving the user goal
4. Be contextually appropriate for turn {self._turn_count}
5. Consider the agent's conversation style and capabilities

CONSTRAINTS:
- Keep messages concise (1-2 sentences)
- Be natural and conversational
- Don't repeat information already provided
- Test different aspects of the agent's capabilities
- Progress toward the user goal

Generate only the user message text, no additional formatting or explanation.
"""
        
        return prompt
        
    def _format_conversation_history(self) -> str:
        """Format conversation history for the prompt."""
        if not self._conversation_context:
            return "No previous conversation."
            
        formatted = []
        for msg in self._conversation_context:
            role = msg['role'].upper()
            content = msg['content']
            turn = msg.get('turn', '?')
            formatted.append(f"Turn {turn} - {role}: {content}")
            
        return "\n".join(formatted)
        
    def _call_ai_for_message_generation(self, prompt: str) -> str:
        """Call AI service to generate message."""
        # This would integrate with the same LLM infrastructure as the judge
        # For now, return a placeholder that would be replaced with actual AI call
        
        # TODO: Integrate with LLM service (OpenAI, Anthropic, etc.)
        # This would use the same HTTP adapter pattern as the judge
        
        return "I need more information about that. Can you help me understand the details?"
        
    def _parse_ai_message_response(self, ai_response: str) -> str:
        """Parse AI response to extract the user message."""
        # Clean up the response
        message = ai_response.strip()
        
        # Remove any formatting or explanations
        if message.startswith('"') and message.endswith('"'):
            message = message[1:-1]
            
        return message
        
    def _fallback_message_generation(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> Optional[str]:
        """Fallback message generation using heuristics."""
        text = last_response.get('text', '').lower()
        
        # Simple heuristic-based fallback
        if '?' in text:
            return "Yes, that sounds good. What's the next step?"
        elif 'help' in text:
            return "I need assistance with that. Can you guide me through it?"
        elif 'confirm' in text:
            return "Yes, I confirm that information."
        else:
            return "I understand. What should I do next?"
            
    def _check_goal_achievement(self, scenario: Dict[str, Any], conversation: List[Dict[str, str]]) -> bool:
        """Check if the user goal has been achieved."""
        user_goal = scenario.get('goal', {}).get('user_goal', '').lower()
        
        # Simple heuristic to check goal achievement
        if not user_goal:
            return False
            
        # Get last assistant message
        last_assistant_msg = ""
        for msg in reversed(conversation):
            if msg.get('role') == 'assistant':
                last_assistant_msg = msg.get('content', '').lower()
                break
                
        # Check if goal-related keywords are present
        goal_keywords = user_goal.split()
        goal_achieved = any(keyword in last_assistant_msg for keyword in goal_keywords)
        
        return goal_achieved
        
    def get_strategy_info(self) -> Dict[str, Any]:
        """Get information about this strategy."""
        return {
            'name': self.name,
            'description': self.description,
            'type': 'ai_powered',
            'domain': 'generic',
            'capabilities': [
                'dynamic_message_generation',
                'agent_capability_analysis',
                'context_aware_conversation',
                'goal_oriented_testing',
                'adaptive_behavior'
            ],
            'llm_config': self.llm_config,
            'agent_capabilities': self._agent_capabilities
        }
