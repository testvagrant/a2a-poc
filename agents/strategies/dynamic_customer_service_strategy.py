"""
Dynamic Customer Service Strategy - Domain-Specific Strategy with AI-Powered Messages

This strategy combines:
1. Domain-specific knowledge (customer service)
2. AI-powered dynamic message generation
3. Context-aware conversation flow
"""

import json
import time
from typing import Dict, Any, Optional, List
from .base_strategy import BaseStrategy

class DynamicCustomerServiceStrategy(BaseStrategy):
    """
    Dynamic Customer Service Strategy: Domain-specific customer service testing with AI-powered messages.
    
    Domain Knowledge:
    - Support ticket management
    - Issue resolution workflows
    - Escalation procedures
    - Product knowledge and troubleshooting
    - Customer satisfaction and feedback
    
    AI-Powered Features:
    - Dynamic message generation based on agent responses
    - Context-aware conversation flow
    - Adaptive to different customer service agent capabilities
    """
    
    def __init__(self, llm_config: Dict[str, Any] = None):
        super().__init__(
            name="DynamicCustomerService",
            description="Domain-specific customer service strategy with AI-powered dynamic messages"
        )
        self.llm_config = llm_config or {
            'model': 'gpt-4o-mini',
            'temperature': 0.7,
            'max_tokens': 500
        }
        
        # Domain-specific knowledge
        self.service_domains = {
            'technical_support': {
                'keywords': ['technical', 'bug', 'error', 'issue', 'problem', 'not working'],
                'common_goals': ['resolve_technical_issue', 'bug_report', 'system_troubleshooting'],
                'typical_flows': ['issue_description', 'troubleshooting_steps', 'resolution_confirmation']
            },
            'billing_support': {
                'keywords': ['billing', 'charge', 'payment', 'invoice', 'refund', 'cost'],
                'common_goals': ['billing_inquiry', 'payment_issue', 'refund_request'],
                'typical_flows': ['billing_question', 'payment_investigation', 'resolution_offer']
            },
            'account_support': {
                'keywords': ['account', 'profile', 'settings', 'password', 'login', 'access'],
                'common_goals': ['account_management', 'password_reset', 'profile_update'],
                'typical_flows': ['account_issue', 'verification_process', 'account_resolution']
            },
            'product_support': {
                'keywords': ['product', 'feature', 'how to', 'tutorial', 'guide', 'help'],
                'common_goals': ['product_question', 'feature_explanation', 'usage_guidance'],
                'typical_flows': ['product_inquiry', 'feature_demonstration', 'usage_confirmation']
            },
            'complaint_handling': {
                'keywords': ['complaint', 'dissatisfied', 'unhappy', 'poor service', 'escalate'],
                'common_goals': ['complaint_resolution', 'service_improvement', 'escalation_request'],
                'typical_flows': ['complaint_acknowledgment', 'investigation_process', 'resolution_offer']
            }
        }
        
        self._conversation_context = []
        self._turn_count = 0
        self._detected_domain = None
        self._agent_capabilities = None
        self._escalation_level = 0
        
    def first_message(self, scenario: Dict[str, Any]) -> str:
        """Send the scenario's initial user message."""
        self._conversation_context = []
        self._turn_count = 0
        self._detected_domain = None
        self._escalation_level = 0
        return scenario["conversation"]["initial_user_msg"]
        
    def next_message(self, last_agent_response: Dict[str, Any], scenario: Dict[str, Any]) -> Optional[str]:
        """Generate next message using domain knowledge + AI-powered generation."""
        self._turn_count += 1
        
        # Update conversation context
        self._conversation_context.append({
            'role': 'assistant',
            'content': last_agent_response.get('text', ''),
            'structured': last_agent_response.get('structured', {}),
            'turn': self._turn_count
        })
        
        # Detect service domain from conversation
        if not self._detected_domain:
            self._detected_domain = self._detect_service_domain(scenario, last_agent_response)
        
        # Analyze agent capabilities if not done yet
        if not self._agent_capabilities:
            self._agent_capabilities = self._analyze_service_agent_capabilities(last_agent_response)
        
        # Check for escalation triggers
        self._check_escalation_triggers(last_agent_response)
        
        # Generate domain-aware AI message
        next_message = self._generate_domain_aware_message(scenario, last_agent_response)
        
        # Add to context
        if next_message:
            self._conversation_context.append({
                'role': 'user',
                'content': next_message,
                'turn': self._turn_count + 1
            })
        
        return next_message
        
    def should_continue(self, conversation: List[Dict[str, str]], scenario: Dict[str, Any]) -> bool:
        """Determine if conversation should continue based on service domain logic."""
        max_turns = scenario["conversation"].get("max_turns", 5)
        
        if len(conversation) >= max_turns:
            return False
            
        # Check if service goal is achieved
        goal_achieved = self._check_service_goal_achievement(scenario, conversation)
        
        # Don't continue if escalated to manager
        if self._escalation_level >= 2:
            return False
            
        return not goal_achieved
        
    def _detect_service_domain(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Detect which service domain this conversation is about."""
        user_goal = scenario.get('goal', {}).get('user_goal', '').lower()
        agent_text = last_response.get('text', '').lower()
        
        # Score each domain based on keywords
        domain_scores = {}
        for domain, info in self.service_domains.items():
            score = 0
            for keyword in info['keywords']:
                if keyword in user_goal:
                    score += 2  # User goal keywords are more important
                if keyword in agent_text:
                    score += 1
            domain_scores[domain] = score
            
        # Return domain with highest score
        return max(domain_scores, key=domain_scores.get) if domain_scores else 'technical_support'
        
    def _analyze_service_agent_capabilities(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze customer service agent capabilities from response."""
        text = response.get('text', '').lower()
        structured = response.get('structured', {})
        
        capabilities = {
            'supports_structured_data': bool(structured),
            'technical_knowledge': self._assess_technical_knowledge(text),
            'escalation_awareness': self._assess_escalation_awareness(text),
            'empathy_level': self._assess_empathy_level(text),
            'resolution_skills': self._assess_resolution_skills(text),
            'conversation_style': self._assess_conversation_style(text)
        }
        
        return capabilities
        
    def _assess_technical_knowledge(self, text: str) -> str:
        """Assess agent's technical knowledge level."""
        technical_terms = [
            'api', 'database', 'server', 'configuration', 'settings',
            'browser', 'cache', 'cookies', 'javascript', 'network'
        ]
        
        advanced_terms = [
            'debugging', 'log analysis', 'performance', 'optimization',
            'architecture', 'integration', 'deployment', 'monitoring'
        ]
        
        if any(term in text for term in advanced_terms):
            return 'advanced'
        elif any(term in text for term in technical_terms):
            return 'intermediate'
        else:
            return 'basic'
            
    def _assess_escalation_awareness(self, text: str) -> str:
        """Assess agent's escalation awareness."""
        escalation_indicators = [
            'escalate', 'manager', 'supervisor', 'specialist', 'senior',
            'transfer', 'higher level', 'advanced support'
        ]
        
        if any(indicator in text for indicator in escalation_indicators):
            return 'high'
        else:
            return 'low'
            
    def _assess_empathy_level(self, text: str) -> str:
        """Assess agent's empathy level."""
        empathy_indicators = [
            'understand', 'sorry', 'apologize', 'frustrating', 'difficult',
            'appreciate', 'thank you', 'help', 'support', 'assist'
        ]
        
        empathy_count = sum(1 for indicator in empathy_indicators if indicator in text)
        
        if empathy_count >= 3:
            return 'high'
        elif empathy_count >= 1:
            return 'medium'
        else:
            return 'low'
            
    def _assess_resolution_skills(self, text: str) -> str:
        """Assess agent's resolution skills."""
        resolution_indicators = [
            'solution', 'resolve', 'fix', 'correct', 'update',
            'restart', 'refresh', 'clear', 'reset', 'configure'
        ]
        
        if any(indicator in text for indicator in resolution_indicators):
            return 'high'
        else:
            return 'low'
            
    def _assess_conversation_style(self, text: str) -> str:
        """Assess agent's conversation style."""
        if '?' in text:
            return 'inquisitive'
        elif len(text.split()) > 30:
            return 'detailed'
        elif any(word in text for word in ['please', 'thank you', 'appreciate']):
            return 'polite'
        else:
            return 'direct'
            
    def _check_escalation_triggers(self, last_response: Dict[str, Any]):
        """Check for escalation triggers in agent response."""
        text = last_response.get('text', '').lower()
        
        escalation_triggers = [
            'escalate', 'manager', 'supervisor', 'specialist',
            'transfer', 'higher level', 'advanced support'
        ]
        
        if any(trigger in text for trigger in escalation_triggers):
            self._escalation_level += 1
            
    def _generate_domain_aware_message(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> Optional[str]:
        """Generate message using domain knowledge + AI."""
        
        # Create domain-aware prompt
        prompt = self._create_service_domain_prompt(scenario, last_response)
        
        # Get AI response (this would integrate with LLM service)
        try:
            ai_response = self._call_ai_for_service_message(prompt)
            return self._parse_ai_message_response(ai_response)
        except Exception as e:
            # Fallback to domain-specific heuristics
            return self._fallback_service_message(scenario, last_response)
            
    def _create_service_domain_prompt(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Create domain-aware prompt for service message generation."""
        
        # Get domain information
        domain_info = self.service_domains.get(self._detected_domain, {})
        domain_keywords = domain_info.get('keywords', [])
        typical_flows = domain_info.get('typical_flows', [])
        
        # Get conversation context
        conversation_history = self._format_conversation_history()
        
        # Get scenario context
        user_goal = scenario.get('goal', {}).get('user_goal', '')
        scenario_title = scenario.get('title', '')
        
        # Get last agent response
        last_text = last_response.get('text', '')
        last_structured = last_response.get('structured', {})
        
        # Get agent capabilities
        capabilities_summary = json.dumps(self._agent_capabilities, indent=2)
        
        prompt = f"""
You are a customer service testing agent. Generate the next user message for testing a customer service AI agent.

SERVICE DOMAIN: {self._detected_domain}
Domain Keywords: {', '.join(domain_keywords)}
Typical Flows: {', '.join(typical_flows)}
Escalation Level: {self._escalation_level}

SCENARIO CONTEXT:
- Title: {scenario_title}
- User Goal: {user_goal}
- Turn: {self._turn_count}

AGENT CAPABILITIES:
{capabilities_summary}

CONVERSATION HISTORY:
{conversation_history}

LAST AGENT RESPONSE:
Text: {last_text}
Structured Data: {json.dumps(last_structured, indent=2)}

CUSTOMER SERVICE DOMAIN GUIDELINES:
- Use appropriate customer service terminology for {self._detected_domain}
- Follow typical customer service conversation flows
- Be realistic and customer-like
- Test agent's service knowledge appropriately
- Consider escalation scenarios if appropriate
- Maintain appropriate customer tone

Generate a natural, contextually appropriate user message that:
1. Follows customer service conversation patterns
2. Tests the agent's {self._detected_domain} capabilities
3. Moves toward achieving the user goal
4. Is appropriate for turn {self._turn_count}
5. Uses realistic customer language
6. Considers escalation level {self._escalation_level}

Generate only the user message text, no additional formatting.
"""
        
        return prompt
        
    def _call_ai_for_service_message(self, prompt: str) -> str:
        """Call AI service for service message generation."""
        # TODO: Integrate with actual LLM service
        # This would use the same HTTP adapter pattern as the judge
        
        # For now, return domain-specific fallback
        return self._get_domain_specific_fallback()
        
    def _get_domain_specific_fallback(self) -> str:
        """Get domain-specific fallback message."""
        fallback_messages = {
            'technical_support': [
                "The issue is still not resolved. Can you help me troubleshoot further?",
                "I tried that but it didn't work. What else can I try?",
                "This is getting frustrating. I need a solution."
            ],
            'billing_support': [
                "I don't understand this charge. Can you explain it?",
                "I want to dispute this charge. How do I do that?",
                "Can you help me with a refund for this service?"
            ],
            'account_support': [
                "I still can't access my account. What's wrong?",
                "Can you help me reset my password?",
                "I need to update my account information."
            ],
            'product_support': [
                "How do I use this feature?",
                "Can you show me how to set this up?",
                "I'm having trouble understanding how this works."
            ],
            'complaint_handling': [
                "I'm not satisfied with this resolution.",
                "I want to speak to a manager.",
                "This is unacceptable service."
            ]
        }
        
        messages = fallback_messages.get(self._detected_domain, ["I need help with this issue."])
        return messages[self._turn_count % len(messages)]
        
    def _fallback_service_message(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> Optional[str]:
        """Fallback message generation using service domain heuristics."""
        text = last_response.get('text', '').lower()
        
        # Domain-specific fallback logic
        if self._detected_domain == 'technical_support':
            if 'try' in text or 'step' in text:
                return "I tried that but it didn't work. What else can I try?"
            elif 'restart' in text:
                return "I restarted but the issue persists."
            else:
                return "The problem is still there. Can you help me further?"
                
        elif self._detected_domain == 'billing_support':
            if 'charge' in text:
                return "I don't understand this charge. Can you explain it?"
            elif 'refund' in text:
                return "When will I receive the refund?"
            else:
                return "I need help with my billing issue."
                
        elif self._detected_domain == 'account_support':
            if 'password' in text:
                return "I still can't log in. What should I do?"
            elif 'verify' in text:
                return "I've verified my identity. What's next?"
            else:
                return "I need help with my account access."
                
        elif self._detected_domain == 'product_support':
            if 'feature' in text:
                return "How do I use this feature?"
            elif 'tutorial' in text:
                return "Can you walk me through this step by step?"
            else:
                return "I need help understanding how this works."
                
        elif self._detected_domain == 'complaint_handling':
            if 'escalate' in text:
                return "I want to speak to a manager."
            elif 'resolve' in text:
                return "I'm not satisfied with this resolution."
            else:
                return "This is unacceptable. I want to file a complaint."
        
        return "I need help with this issue."
        
    def _check_service_goal_achievement(self, scenario: Dict[str, Any], conversation: List[Dict[str, str]]) -> bool:
        """Check if service goal has been achieved."""
        user_goal = scenario.get('goal', {}).get('user_goal', '').lower()
        
        # Get last assistant message
        last_assistant_msg = ""
        for msg in reversed(conversation):
            if msg.get('role') == 'assistant':
                last_assistant_msg = msg.get('content', '').lower()
                break
                
        # Check domain-specific goal achievement
        if self._detected_domain == 'technical_support':
            if 'issue' in user_goal and ('resolve' in last_assistant_msg or 'fix' in last_assistant_msg):
                return True
                
        elif self._detected_domain == 'billing_support':
            if 'billing' in user_goal and ('resolve' in last_assistant_msg or 'refund' in last_assistant_msg):
                return True
                
        elif self._detected_domain == 'account_support':
            if 'account' in user_goal and ('access' in last_assistant_msg or 'login' in last_assistant_msg):
                return True
                
        elif self._detected_domain == 'product_support':
            if 'product' in user_goal and ('understand' in last_assistant_msg or 'explain' in last_assistant_msg):
                return True
                
        elif self._detected_domain == 'complaint_handling':
            if 'complaint' in user_goal and ('escalate' in last_assistant_msg or 'manager' in last_assistant_msg):
                return True
                
        return False
        
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
        
    def _parse_ai_message_response(self, ai_response: str) -> str:
        """Parse AI response to extract the user message."""
        message = ai_response.strip()
        
        # Clean up the response
        if message.startswith('"') and message.endswith('"'):
            message = message[1:-1]
            
        return message
        
    def get_strategy_info(self) -> Dict[str, Any]:
        """Get information about this strategy."""
        return {
            'name': self.name,
            'description': self.description,
            'type': 'domain_specific_ai_powered',
            'domain': 'customer_service',
            'capabilities': [
                'domain_specific_knowledge',
                'ai_powered_message_generation',
                'context_aware_conversation',
                'service_goal_oriented_testing',
                'adaptive_to_service_agents',
                'escalation_awareness'
            ],
            'service_domains': list(self.service_domains.keys()),
            'detected_domain': self._detected_domain,
            'escalation_level': self._escalation_level,
            'agent_capabilities': self._agent_capabilities
        }
