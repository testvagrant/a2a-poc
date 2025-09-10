"""
Dynamic Financial Strategy - Domain-Specific Strategy with AI-Powered Messages

This strategy combines:
1. Domain-specific knowledge (financial services)
2. AI-powered dynamic message generation
3. Context-aware conversation flow
"""

import json
import time
from typing import Dict, Any, Optional, List
from .base_strategy import BaseStrategy

class DynamicFinancialStrategy(BaseStrategy):
    """
    Dynamic Financial Strategy: Domain-specific financial testing with AI-powered messages.
    
    Domain Knowledge:
    - Account management (balance, transactions, statements)
    - Payment processing (transfers, bill pay, recurring payments)
    - Financial products (loans, credit cards, investments)
    - Security and fraud prevention
    - Regulatory compliance (KYC, AML, etc.)
    
    AI-Powered Features:
    - Dynamic message generation based on agent responses
    - Context-aware conversation flow
    - Adaptive to different financial agent capabilities
    """
    
    def __init__(self, llm_config: Dict[str, Any] = None):
        super().__init__(
            name="DynamicFinancial",
            description="Domain-specific financial strategy with AI-powered dynamic messages"
        )
        self.llm_config = llm_config or {
            'model': 'gpt-4o-mini',
            'temperature': 0.7,
            'max_tokens': 500
        }
        
        # Domain-specific knowledge
        self.financial_domains = {
            'account_management': {
                'keywords': ['account', 'balance', 'statement', 'transaction', 'history'],
                'common_goals': ['check_balance', 'view_transactions', 'account_info'],
                'typical_flows': ['balance_inquiry', 'transaction_history', 'account_summary']
            },
            'payment_processing': {
                'keywords': ['payment', 'transfer', 'bill', 'pay', 'send money'],
                'common_goals': ['make_payment', 'transfer_funds', 'pay_bills'],
                'typical_flows': ['payment_setup', 'transfer_confirmation', 'payment_history']
            },
            'financial_products': {
                'keywords': ['loan', 'credit', 'investment', 'savings', 'mortgage'],
                'common_goals': ['apply_loan', 'credit_inquiry', 'investment_advice'],
                'typical_flows': ['product_inquiry', 'application_process', 'product_comparison']
            },
            'security_fraud': {
                'keywords': ['security', 'fraud', 'suspicious', 'unauthorized', 'alert'],
                'common_goals': ['report_fraud', 'security_concern', 'account_lock'],
                'typical_flows': ['fraud_reporting', 'security_verification', 'account_recovery']
            }
        }
        
        self._conversation_context = []
        self._turn_count = 0
        self._detected_domain = None
        self._agent_capabilities = None
        
    def first_message(self, scenario: Dict[str, Any]) -> str:
        """Send the scenario's initial user message."""
        self._conversation_context = []
        self._turn_count = 0
        self._detected_domain = None
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
        
        # Detect financial domain from conversation
        if not self._detected_domain:
            self._detected_domain = self._detect_financial_domain(scenario, last_agent_response)
        
        # Analyze agent capabilities if not done yet
        if not self._agent_capabilities:
            self._agent_capabilities = self._analyze_financial_agent_capabilities(last_agent_response)
        
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
        """Determine if conversation should continue based on financial domain logic."""
        max_turns = scenario["conversation"].get("max_turns", 5)
        
        if len(conversation) >= max_turns:
            return False
            
        # Check if financial goal is achieved
        goal_achieved = self._check_financial_goal_achievement(scenario, conversation)
        
        return not goal_achieved
        
    def _detect_financial_domain(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Detect which financial domain this conversation is about."""
        user_goal = scenario.get('goal', {}).get('user_goal', '').lower()
        agent_text = last_response.get('text', '').lower()
        
        # Score each domain based on keywords
        domain_scores = {}
        for domain, info in self.financial_domains.items():
            score = 0
            for keyword in info['keywords']:
                if keyword in user_goal:
                    score += 2  # User goal keywords are more important
                if keyword in agent_text:
                    score += 1
            domain_scores[domain] = score
            
        # Return domain with highest score
        return max(domain_scores, key=domain_scores.get) if domain_scores else 'account_management'
        
    def _analyze_financial_agent_capabilities(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze financial agent capabilities from response."""
        text = response.get('text', '').lower()
        structured = response.get('structured', {})
        
        capabilities = {
            'supports_structured_data': bool(structured),
            'financial_knowledge': self._assess_financial_knowledge(text),
            'security_awareness': self._assess_security_awareness(text),
            'compliance_knowledge': self._assess_compliance_knowledge(text),
            'conversation_style': self._assess_conversation_style(text)
        }
        
        return capabilities
        
    def _assess_financial_knowledge(self, text: str) -> str:
        """Assess agent's financial knowledge level."""
        financial_terms = [
            'apr', 'interest rate', 'principal', 'amortization', 'collateral',
            'credit score', 'fico', 'debt-to-income', 'liquidity', 'portfolio'
        ]
        
        advanced_terms = [
            'derivative', 'hedge', 'arbitrage', 'leverage', 'volatility',
            'beta', 'alpha', 'sharpe ratio', 'var', 'stress test'
        ]
        
        if any(term in text for term in advanced_terms):
            return 'advanced'
        elif any(term in text for term in financial_terms):
            return 'intermediate'
        else:
            return 'basic'
            
    def _assess_security_awareness(self, text: str) -> str:
        """Assess agent's security awareness."""
        security_indicators = [
            'security', 'fraud', 'unauthorized', 'suspicious', 'alert',
            'verification', 'authentication', 'encryption', 'secure'
        ]
        
        if any(indicator in text for indicator in security_indicators):
            return 'high'
        else:
            return 'low'
            
    def _assess_compliance_knowledge(self, text: str) -> str:
        """Assess agent's compliance knowledge."""
        compliance_terms = [
            'kyc', 'aml', 'ofac', 'gdpr', 'ccpa', 'sox', 'basel',
            'compliance', 'regulation', 'audit', 'governance'
        ]
        
        if any(term in text for term in compliance_terms):
            return 'high'
        else:
            return 'basic'
            
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
            
    def _generate_domain_aware_message(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> Optional[str]:
        """Generate message using domain knowledge + AI."""
        
        # Create domain-aware prompt
        prompt = self._create_financial_domain_prompt(scenario, last_response)
        
        # Get AI response (this would integrate with LLM service)
        try:
            ai_response = self._call_ai_for_financial_message(prompt)
            return self._parse_ai_message_response(ai_response)
        except Exception as e:
            # Fallback to domain-specific heuristics
            return self._fallback_financial_message(scenario, last_response)
            
    def _create_financial_domain_prompt(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> str:
        """Create domain-aware prompt for financial message generation."""
        
        # Get domain information
        domain_info = self.financial_domains.get(self._detected_domain, {})
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
You are a financial services testing agent. Generate the next user message for testing a financial AI agent.

FINANCIAL DOMAIN: {self._detected_domain}
Domain Keywords: {', '.join(domain_keywords)}
Typical Flows: {', '.join(typical_flows)}

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

FINANCIAL DOMAIN GUIDELINES:
- Use appropriate financial terminology for {self._detected_domain}
- Follow typical financial conversation flows
- Be realistic and professional
- Test agent's financial knowledge appropriately
- Consider security and compliance aspects

Generate a natural, contextually appropriate user message that:
1. Follows financial conversation patterns
2. Tests the agent's {self._detected_domain} capabilities
3. Moves toward achieving the user goal
4. Is appropriate for turn {self._turn_count}
5. Uses realistic financial language

Generate only the user message text, no additional formatting.
"""
        
        return prompt
        
    def _call_ai_for_financial_message(self, prompt: str) -> str:
        """Call AI service for financial message generation."""
        # TODO: Integrate with actual LLM service
        # This would use the same HTTP adapter pattern as the judge
        
        # For now, return domain-specific fallback
        return self._get_domain_specific_fallback()
        
    def _get_domain_specific_fallback(self) -> str:
        """Get domain-specific fallback message."""
        fallback_messages = {
            'account_management': [
                "Can you show me my recent transactions?",
                "What's my current account balance?",
                "I need to update my account information."
            ],
            'payment_processing': [
                "I want to make a payment of $100.",
                "Can you help me set up a recurring payment?",
                "I need to transfer money to another account."
            ],
            'financial_products': [
                "I'm interested in applying for a personal loan.",
                "What investment options do you have?",
                "Can you explain your credit card benefits?"
            ],
            'security_fraud': [
                "I think there's suspicious activity on my account.",
                "I received a fraud alert. What should I do?",
                "I need to report unauthorized transactions."
            ]
        }
        
        messages = fallback_messages.get(self._detected_domain, ["I need help with my account."])
        return messages[self._turn_count % len(messages)]
        
    def _fallback_financial_message(self, scenario: Dict[str, Any], last_response: Dict[str, Any]) -> Optional[str]:
        """Fallback message generation using financial domain heuristics."""
        text = last_response.get('text', '').lower()
        
        # Domain-specific fallback logic
        if self._detected_domain == 'account_management':
            if 'balance' in text:
                return "Can you show me my recent transactions?"
            elif 'transaction' in text:
                return "What's my account summary?"
            else:
                return "I need to check my account details."
                
        elif self._detected_domain == 'payment_processing':
            if 'payment' in text:
                return "Can you confirm the payment details?"
            elif 'transfer' in text:
                return "What's the transfer fee?"
            else:
                return "I want to make a payment."
                
        elif self._detected_domain == 'financial_products':
            if 'loan' in text:
                return "What are the interest rates?"
            elif 'credit' in text:
                return "What's the credit limit?"
            else:
                return "I'm interested in your financial products."
                
        elif self._detected_domain == 'security_fraud':
            if 'fraud' in text:
                return "What should I do next?"
            elif 'security' in text:
                return "How can I secure my account?"
            else:
                return "I'm concerned about my account security."
        
        return "I need help with my financial account."
        
    def _check_financial_goal_achievement(self, scenario: Dict[str, Any], conversation: List[Dict[str, str]]) -> bool:
        """Check if financial goal has been achieved."""
        user_goal = scenario.get('goal', {}).get('user_goal', '').lower()
        
        # Get last assistant message
        last_assistant_msg = ""
        for msg in reversed(conversation):
            if msg.get('role') == 'assistant':
                last_assistant_msg = msg.get('content', '').lower()
                break
                
        # Check domain-specific goal achievement
        if self._detected_domain == 'account_management':
            if 'balance' in user_goal and 'balance' in last_assistant_msg:
                return True
            elif 'transaction' in user_goal and 'transaction' in last_assistant_msg:
                return True
                
        elif self._detected_domain == 'payment_processing':
            if 'payment' in user_goal and ('confirm' in last_assistant_msg or 'success' in last_assistant_msg):
                return True
                
        elif self._detected_domain == 'financial_products':
            if 'loan' in user_goal and 'application' in last_assistant_msg:
                return True
                
        elif self._detected_domain == 'security_fraud':
            if 'fraud' in user_goal and 'report' in last_assistant_msg:
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
            'domain': 'financial_services',
            'capabilities': [
                'domain_specific_knowledge',
                'ai_powered_message_generation',
                'context_aware_conversation',
                'financial_goal_oriented_testing',
                'adaptive_to_financial_agents'
            ],
            'financial_domains': list(self.financial_domains.keys()),
            'detected_domain': self._detected_domain,
            'agent_capabilities': self._agent_capabilities
        }
