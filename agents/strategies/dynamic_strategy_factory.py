"""
Dynamic Strategy Factory - Automatic Domain Strategy Selection

This factory automatically selects the appropriate domain-specific strategy
based on the agent being tested and the scenario context.
"""

from typing import Dict, Any, Optional, Type
from .base_strategy import BaseStrategy
from .dynamic_financial_strategy import DynamicFinancialStrategy
from .dynamic_customer_service_strategy import DynamicCustomerServiceStrategy
from .dynamic_ai_strategy import DynamicAIStrategy

class DynamicStrategyFactory:
    """
    Factory for automatically selecting domain-specific strategies with AI-powered messages.
    
    This factory:
    1. Analyzes the agent and scenario to determine the appropriate domain
    2. Selects the corresponding domain-specific strategy
    3. Configures the strategy with AI-powered message generation
    4. Provides fallback to generic dynamic strategy if domain is unknown
    """
    
    def __init__(self, llm_config: Dict[str, Any] = None):
        """
        Initialize the dynamic strategy factory.
        
        Args:
            llm_config: Configuration for LLM services
        """
        self.llm_config = llm_config or {
            'model': 'gpt-4o-mini',
            'temperature': 0.7,
            'max_tokens': 500
        }
        
        # Domain strategy mapping
        self.domain_strategies = {
            'financial': DynamicFinancialStrategy,
            'customer_service': DynamicCustomerServiceStrategy,
            'support': DynamicCustomerServiceStrategy,  # Alias
            'collections': DynamicFinancialStrategy,    # Alias
            'banking': DynamicFinancialStrategy,        # Alias
            'generic': DynamicAIStrategy
        }
        
        # Domain detection keywords
        self.domain_keywords = {
            'financial': [
                'account', 'balance', 'payment', 'transaction', 'bank', 'loan',
                'credit', 'debit', 'transfer', 'deposit', 'withdrawal', 'interest',
                'mortgage', 'investment', 'portfolio', 'financial', 'money'
            ],
            'customer_service': [
                'support', 'help', 'issue', 'problem', 'trouble', 'assistance',
                'service', 'complaint', 'escalate', 'manager', 'technical',
                'billing', 'account', 'login', 'password', 'access'
            ]
        }
        
    def create_strategy(self, agent_url: str, scenario: Dict[str, Any], 
                       agent_name: str = None) -> BaseStrategy:
        """
        Create the appropriate domain-specific strategy for the given agent and scenario.
        
        Args:
            agent_url: URL of the agent being tested
            agent_name: Optional name for the agent
            scenario: Scenario configuration
            
        Returns:
            Configured domain-specific strategy
        """
        # Detect domain from scenario and agent URL
        detected_domain = self._detect_domain(agent_url, scenario)
        
        # Select appropriate strategy class
        strategy_class = self.domain_strategies.get(detected_domain, DynamicAIStrategy)
        
        # Create and configure strategy
        strategy = strategy_class(self.llm_config)
        
        # Add domain information to strategy
        strategy._detected_domain = detected_domain
        strategy._agent_url = agent_url
        strategy._agent_name = agent_name or f"agent_{hash(agent_url)}"
        
        return strategy
        
    def _detect_domain(self, agent_url: str, scenario: Dict[str, Any]) -> str:
        """
        Detect the appropriate domain for the agent and scenario.
        
        Args:
            agent_url: URL of the agent
            scenario: Scenario configuration
            
        Returns:
            Detected domain name
        """
        # Extract context from scenario
        user_goal = scenario.get('goal', {}).get('user_goal', '').lower()
        scenario_title = scenario.get('title', '').lower()
        tags = scenario.get('tags', [])
        initial_msg = scenario.get('conversation', {}).get('initial_user_msg', '').lower()
        
        # Extract context from agent URL
        url_lower = agent_url.lower()
        
        # Score each domain
        domain_scores = {}
        
        for domain, keywords in self.domain_keywords.items():
            score = 0
            
            # Score based on user goal
            for keyword in keywords:
                if keyword in user_goal:
                    score += 3  # User goal is most important
                    
            # Score based on scenario title
            for keyword in keywords:
                if keyword in scenario_title:
                    score += 2
                    
            # Score based on tags
            for tag in tags:
                if tag.lower() in keywords:
                    score += 2
                    
            # Score based on initial message
            for keyword in keywords:
                if keyword in initial_msg:
                    score += 1
                    
            # Score based on agent URL
            for keyword in keywords:
                if keyword in url_lower:
                    score += 1
                    
            domain_scores[domain] = score
            
        # Return domain with highest score, or 'generic' if no clear winner
        if domain_scores:
            max_score = max(domain_scores.values())
            if max_score > 0:
                return max(domain_scores, key=domain_scores.get)
                
        return 'generic'
        
    def get_available_domains(self) -> list:
        """Get list of available domain strategies."""
        return list(self.domain_strategies.keys())
        
    def get_domain_keywords(self, domain: str) -> list:
        """Get keywords for a specific domain."""
        return self.domain_keywords.get(domain, [])
        
    def add_domain_strategy(self, domain: str, strategy_class: Type[BaseStrategy], 
                           keywords: list = None):
        """
        Add a new domain strategy to the factory.
        
        Args:
            domain: Domain name
            strategy_class: Strategy class for the domain
            keywords: Keywords for domain detection
        """
        self.domain_strategies[domain] = strategy_class
        if keywords:
            self.domain_keywords[domain] = keywords
            
    def create_strategy_for_domain(self, domain: str) -> BaseStrategy:
        """
        Create a strategy for a specific domain.
        
        Args:
            domain: Domain name
            
        Returns:
            Configured strategy for the domain
        """
        strategy_class = self.domain_strategies.get(domain, DynamicAIStrategy)
        strategy = strategy_class(self.llm_config)
        strategy._detected_domain = domain
        return strategy
        
    def analyze_scenario_domain(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a scenario to determine its domain characteristics.
        
        Args:
            scenario: Scenario configuration
            
        Returns:
            Analysis results including detected domain and confidence
        """
        user_goal = scenario.get('goal', {}).get('user_goal', '').lower()
        scenario_title = scenario.get('title', '').lower()
        tags = scenario.get('tags', [])
        initial_msg = scenario.get('conversation', {}).get('initial_user_msg', '').lower()
        
        # Analyze each domain
        domain_analysis = {}
        
        for domain, keywords in self.domain_keywords.items():
            matches = []
            total_score = 0
            
            # Check user goal
            for keyword in keywords:
                if keyword in user_goal:
                    matches.append(f"user_goal: {keyword}")
                    total_score += 3
                    
            # Check scenario title
            for keyword in keywords:
                if keyword in scenario_title:
                    matches.append(f"title: {keyword}")
                    total_score += 2
                    
            # Check tags
            for tag in tags:
                if tag.lower() in keywords:
                    matches.append(f"tag: {tag}")
                    total_score += 2
                    
            # Check initial message
            for keyword in keywords:
                if keyword in initial_msg:
                    matches.append(f"initial_msg: {keyword}")
                    total_score += 1
                    
            domain_analysis[domain] = {
                'score': total_score,
                'matches': matches,
                'confidence': min(total_score / 10.0, 1.0)  # Normalize to 0-1
            }
            
        # Find best domain
        best_domain = max(domain_analysis, key=lambda x: domain_analysis[x]['score'])
        best_score = domain_analysis[best_domain]['score']
        
        return {
            'detected_domain': best_domain if best_score > 0 else 'generic',
            'confidence': domain_analysis[best_domain]['confidence'],
            'domain_analysis': domain_analysis,
            'recommended_strategy': self.domain_strategies.get(best_domain, DynamicAIStrategy).__name__
        }

# Example usage
if __name__ == "__main__":
    # Initialize factory
    factory = DynamicStrategyFactory()
    
    # Example scenarios
    financial_scenario = {
        'title': 'Account Balance Inquiry',
        'goal': {'user_goal': 'Check my account balance and recent transactions'},
        'tags': ['financial', 'account_management'],
        'conversation': {
            'initial_user_msg': 'Hi, I want to check my account balance.'
        }
    }
    
    service_scenario = {
        'title': 'Technical Support Request',
        'goal': {'user_goal': 'Get help with a technical issue'},
        'tags': ['support', 'technical'],
        'conversation': {
            'initial_user_msg': 'I need help with a technical problem.'
        }
    }
    
    # Create strategies
    financial_strategy = factory.create_strategy(
        "https://api.bank.com/chat", 
        financial_scenario, 
        "bank_agent"
    )
    
    service_strategy = factory.create_strategy(
        "https://api.support.com/chat", 
        service_scenario, 
        "support_agent"
    )
    
    print(f"Financial Strategy: {financial_strategy.name}")
    print(f"Service Strategy: {service_strategy.name}")
    
    # Analyze scenarios
    financial_analysis = factory.analyze_scenario_domain(financial_scenario)
    service_analysis = factory.analyze_scenario_domain(service_scenario)
    
    print(f"Financial Analysis: {financial_analysis['detected_domain']} (confidence: {financial_analysis['confidence']:.2f})")
    print(f"Service Analysis: {service_analysis['detected_domain']} (confidence: {service_analysis['confidence']:.2f})")
