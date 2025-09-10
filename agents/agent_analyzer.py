"""
AI-Powered Agent Analyzer

This module provides capabilities to analyze any AI agent and understand its:
1. Capabilities and limitations
2. Conversation patterns
3. Domain expertise
4. Response styles
5. API interfaces

This enables the UTA to dynamically adapt to any agent without manual configuration.
"""

import json
import time
import requests
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class AgentCapabilities:
    """Structured representation of agent capabilities."""
    domain_expertise: List[str]
    conversation_style: str
    response_patterns: Dict[str, Any]
    api_capabilities: Dict[str, Any]
    limitations: List[str]
    testing_recommendations: List[str]
    confidence_score: float

class AgentAnalyzer:
    """
    AI-powered analyzer that can understand any AI agent's capabilities.
    
    This analyzer uses AI to dynamically understand agent capabilities,
    enabling the UTA to adapt its testing strategies without manual configuration.
    """
    
    def __init__(self, llm_config: Dict[str, Any] = None):
        """
        Initialize agent analyzer.
        
        Args:
            llm_config: Configuration for LLM used in analysis
        """
        self.llm_config = llm_config or {
            'model': 'gpt-4o-mini',
            'temperature': 0.3,
            'max_tokens': 1000
        }
        self._analysis_cache = {}
        
    def analyze_agent(self, agent_url: str, api_key: str = None, 
                     sample_messages: List[str] = None) -> AgentCapabilities:
        """
        Analyze an AI agent to understand its capabilities.
        
        Args:
            agent_url: URL of the agent to analyze
            api_key: API key for authentication
            sample_messages: Optional sample messages to test with
            
        Returns:
            AgentCapabilities object with analysis results
        """
        cache_key = f"{agent_url}_{api_key}"
        if cache_key in self._analysis_cache:
            return self._analysis_cache[cache_key]
            
        # Perform multi-stage analysis
        analysis_results = {}
        
        # Stage 1: API Discovery
        analysis_results['api_info'] = self._discover_api_capabilities(agent_url, api_key)
        
        # Stage 2: Response Pattern Analysis
        analysis_results['response_patterns'] = self._analyze_response_patterns(
            agent_url, api_key, sample_messages
        )
        
        # Stage 3: Domain Expertise Analysis
        analysis_results['domain_expertise'] = self._analyze_domain_expertise(
            agent_url, api_key, sample_messages
        )
        
        # Stage 4: AI-Powered Capability Assessment
        analysis_results['ai_assessment'] = self._ai_powered_capability_assessment(
            analysis_results
        )
        
        # Compile results
        capabilities = self._compile_capabilities(analysis_results)
        
        # Cache results
        self._analysis_cache[cache_key] = capabilities
        
        return capabilities
        
    def _discover_api_capabilities(self, agent_url: str, api_key: str = None) -> Dict[str, Any]:
        """Discover API capabilities through endpoint analysis."""
        api_info = {
            'base_url': agent_url,
            'endpoints': [],
            'authentication': 'none',
            'rate_limits': 'unknown',
            'supported_formats': ['json']
        }
        
        try:
            # Try to discover endpoints
            if '/health' in agent_url or agent_url.endswith('/'):
                # Try common endpoints
                common_endpoints = ['/health', '/capabilities', '/status', '/info']
                for endpoint in common_endpoints:
                    try:
                        response = requests.get(
                            f"{agent_url.rstrip('/')}{endpoint}",
                            headers={'Authorization': f'Bearer {api_key}'} if api_key else {},
                            timeout=5
                        )
                        if response.status_code == 200:
                            api_info['endpoints'].append(endpoint)
                    except:
                        continue
                        
        except Exception as e:
            api_info['error'] = str(e)
            
        return api_info
        
    def _analyze_response_patterns(self, agent_url: str, api_key: str = None, 
                                 sample_messages: List[str] = None) -> Dict[str, Any]:
        """Analyze response patterns by sending test messages."""
        if not sample_messages:
            sample_messages = [
                "Hello, how can you help me?",
                "What are your capabilities?",
                "I need help with my account.",
                "Can you process payments?",
                "What information do you need from me?"
            ]
            
        response_patterns = {
            'response_times': [],
            'response_lengths': [],
            'response_structures': [],
            'error_patterns': [],
            'conversation_style': 'unknown'
        }
        
        for message in sample_messages:
            try:
                start_time = time.time()
                
                # Send test message
                response = self._send_test_message(agent_url, api_key, message)
                
                response_time = (time.time() - start_time) * 1000
                response_patterns['response_times'].append(response_time)
                
                if response:
                    response_text = response.get('text', '')
                    response_patterns['response_lengths'].append(len(response_text))
                    response_patterns['response_structures'].append(response.get('structured', {}))
                    
                    # Analyze conversation style
                    style = self._analyze_conversation_style(response_text)
                    response_patterns['conversation_style'] = style
                    
            except Exception as e:
                response_patterns['error_patterns'].append(str(e))
                
        return response_patterns
        
    def _analyze_domain_expertise(self, agent_url: str, api_key: str = None, 
                                sample_messages: List[str] = None) -> List[str]:
        """Analyze domain expertise through targeted questions."""
        domain_questions = {
            'financial': [
                "Can you help me with my bank account?",
                "I need to make a payment.",
                "What's my account balance?"
            ],
            'customer_service': [
                "I have a problem with your service.",
                "How can I get support?",
                "I need to speak to a manager."
            ],
            'collections': [
                "I'm having trouble paying my debt.",
                "Can I set up a payment plan?",
                "What are my payment options?"
            ],
            'technical': [
                "I'm having a technical issue.",
                "How do I troubleshoot this problem?",
                "Can you help me with the API?"
            ]
        }
        
        domain_scores = {}
        
        for domain, questions in domain_questions.items():
            score = 0
            for question in questions:
                try:
                    response = self._send_test_message(agent_url, api_key, question)
                    if response and self._is_domain_relevant(response.get('text', ''), domain):
                        score += 1
                except:
                    continue
                    
            domain_scores[domain] = score / len(questions)
            
        # Return domains with score > 0.3
        return [domain for domain, score in domain_scores.items() if score > 0.3]
        
    def _ai_powered_capability_assessment(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to assess agent capabilities based on analysis results."""
        
        # Create prompt for AI assessment
        prompt = f"""
You are an expert AI agent analyst. Based on the following analysis results, assess the agent's capabilities:

API INFO:
{json.dumps(analysis_results.get('api_info', {}), indent=2)}

RESPONSE PATTERNS:
{json.dumps(analysis_results.get('response_patterns', {}), indent=2)}

DOMAIN EXPERTISE:
{json.dumps(analysis_results.get('domain_expertise', []), indent=2)}

Please provide an assessment in the following JSON format:
{{
    "primary_capabilities": ["capability1", "capability2"],
    "conversation_style": "style_description",
    "strengths": ["strength1", "strength2"],
    "limitations": ["limitation1", "limitation2"],
    "testing_recommendations": ["recommendation1", "recommendation2"],
    "confidence_score": 0.0-1.0,
    "reasoning": "explanation of assessment"
}}
"""
        
        # TODO: Integrate with actual LLM service
        # For now, return heuristic assessment
        return self._heuristic_capability_assessment(analysis_results)
        
    def _heuristic_capability_assessment(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback heuristic assessment when AI is not available."""
        api_info = analysis_results.get('api_info', {})
        response_patterns = analysis_results.get('response_patterns', {})
        domain_expertise = analysis_results.get('domain_expertise', [])
        
        capabilities = []
        if domain_expertise:
            capabilities.extend(domain_expertise)
        if response_patterns.get('response_structures'):
            capabilities.append('structured_data')
        if response_patterns.get('response_times') and min(response_patterns['response_times']) < 1000:
            capabilities.append('fast_response')
            
        return {
            'primary_capabilities': capabilities,
            'conversation_style': response_patterns.get('conversation_style', 'unknown'),
            'strengths': capabilities,
            'limitations': ['unknown_limitations'],
            'testing_recommendations': [
                'Test basic conversation flow',
                'Test domain-specific scenarios',
                'Test error handling'
            ],
            'confidence_score': 0.6,
            'reasoning': 'Heuristic assessment based on response patterns'
        }
        
    def _compile_capabilities(self, analysis_results: Dict[str, Any]) -> AgentCapabilities:
        """Compile analysis results into AgentCapabilities object."""
        ai_assessment = analysis_results.get('ai_assessment', {})
        
        return AgentCapabilities(
            domain_expertise=analysis_results.get('domain_expertise', []),
            conversation_style=ai_assessment.get('conversation_style', 'unknown'),
            response_patterns=analysis_results.get('response_patterns', {}),
            api_capabilities=analysis_results.get('api_info', {}),
            limitations=ai_assessment.get('limitations', []),
            testing_recommendations=ai_assessment.get('testing_recommendations', []),
            confidence_score=ai_assessment.get('confidence_score', 0.0)
        )
        
    def _send_test_message(self, agent_url: str, api_key: str, message: str) -> Optional[Dict[str, Any]]:
        """Send a test message to the agent."""
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}' if api_key else ''
            }
            
            payload = {
                'model': 'gpt-3.5-turbo',  # Default model
                'messages': [{'role': 'user', 'content': message}],
                'temperature': 0.7,
                'max_tokens': 500
            }
            
            # Try OpenAI-compatible endpoint
            url = agent_url.rstrip('/') + '/v1/chat/completions'
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and len(data['choices']) > 0:
                    choice = data['choices'][0]
                    return {
                        'text': choice.get('message', {}).get('content', ''),
                        'structured': {},
                        'metadata': data.get('usage', {})
                    }
                    
        except Exception as e:
            # Try alternative endpoints or formats
            pass
            
        return None
        
    def _analyze_conversation_style(self, response_text: str) -> str:
        """Analyze conversation style from response text."""
        text = response_text.lower()
        
        if '?' in text:
            return 'inquisitive'
        elif len(text.split()) > 30:
            return 'detailed'
        elif any(word in text for word in ['please', 'thank you', 'appreciate']):
            return 'polite'
        elif any(word in text for word in ['sure', 'absolutely', 'definitely']):
            return 'confident'
        else:
            return 'direct'
            
    def _is_domain_relevant(self, response_text: str, domain: str) -> bool:
        """Check if response is relevant to a specific domain."""
        text = response_text.lower()
        
        domain_keywords = {
            'financial': ['account', 'payment', 'balance', 'transaction', 'bank'],
            'customer_service': ['help', 'support', 'assist', 'problem', 'issue'],
            'collections': ['debt', 'payment plan', 'collections', 'outstanding'],
            'technical': ['api', 'technical', 'troubleshoot', 'debug', 'error']
        }
        
        keywords = domain_keywords.get(domain, [])
        return any(keyword in text for keyword in keywords)
        
    def generate_testing_strategy(self, capabilities: AgentCapabilities) -> Dict[str, Any]:
        """Generate a testing strategy based on agent capabilities."""
        strategy = {
            'strategy_type': 'dynamic_ai',
            'focus_areas': capabilities.domain_expertise,
            'conversation_style': capabilities.conversation_style,
            'test_scenarios': [],
            'message_generation': {
                'style': capabilities.conversation_style,
                'complexity': 'medium',
                'domain_focus': capabilities.domain_expertise
            }
        }
        
        # Generate test scenarios based on capabilities
        for domain in capabilities.domain_expertise:
            strategy['test_scenarios'].extend(self._generate_domain_scenarios(domain))
            
        return strategy
        
    def _generate_domain_scenarios(self, domain: str) -> List[Dict[str, Any]]:
        """Generate test scenarios for a specific domain."""
        domain_scenarios = {
            'financial': [
                {'goal': 'check_balance', 'complexity': 'low'},
                {'goal': 'make_payment', 'complexity': 'medium'},
                {'goal': 'account_management', 'complexity': 'high'}
            ],
            'customer_service': [
                {'goal': 'basic_support', 'complexity': 'low'},
                {'goal': 'escalation', 'complexity': 'medium'},
                {'goal': 'complex_issue', 'complexity': 'high'}
            ],
            'collections': [
                {'goal': 'payment_arrangement', 'complexity': 'medium'},
                {'goal': 'debt_negotiation', 'complexity': 'high'},
                {'goal': 'payment_plan', 'complexity': 'medium'}
            ]
        }
        
        return domain_scenarios.get(domain, [{'goal': 'general_assistance', 'complexity': 'low'}])

# Example usage
if __name__ == "__main__":
    analyzer = AgentAnalyzer()
    
    # Example: Analyze an agent
    capabilities = analyzer.analyze_agent(
        agent_url="https://api.example.com/chat",
        api_key="your-api-key",
        sample_messages=[
            "Hello, how can you help me?",
            "I need help with my account."
        ]
    )
    
    print(f"Agent Capabilities: {capabilities}")
    
    # Generate testing strategy
    strategy = analyzer.generate_testing_strategy(capabilities)
    print(f"Testing Strategy: {strategy}")
