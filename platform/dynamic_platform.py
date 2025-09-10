"""
Dynamic UTA Platform

This module provides a platform-level system that can automatically:
1. Discover and analyze any AI agent
2. Generate appropriate testing strategies
3. Create test scenarios dynamically
4. Adapt message generation based on agent capabilities

This makes the UTA system truly scalable across different applications and domains.
"""

import json
import yaml
from typing import Dict, Any, List, Optional
from pathlib import Path
from agents.agent_analyzer import AgentAnalyzer, AgentCapabilities
from agents.strategies.dynamic_ai_strategy import DynamicAIStrategy
from agents.strategies.registry import StrategyRegistry

class DynamicUTAPlatform:
    """
    Dynamic UTA Platform that can adapt to any AI agent automatically.
    
    This platform provides:
    1. Automatic agent discovery and analysis
    2. Dynamic strategy generation
    3. Adaptive test scenario creation
    4. Context-aware message generation
    """
    
    def __init__(self, llm_config: Dict[str, Any] = None):
        """
        Initialize dynamic UTA platform.
        
        Args:
            llm_config: Configuration for LLM services
        """
        self.llm_config = llm_config or {
            'model': 'gpt-4o-mini',
            'temperature': 0.7,
            'max_tokens': 1000
        }
        
        self.agent_analyzer = AgentAnalyzer(llm_config)
        self.strategy_registry = StrategyRegistry()
        self._agent_profiles = {}
        self._generated_strategies = {}
        
    def discover_and_analyze_agent(self, agent_url: str, api_key: str = None, 
                                 agent_name: str = None) -> AgentCapabilities:
        """
        Discover and analyze an AI agent automatically.
        
        Args:
            agent_url: URL of the agent to analyze
            api_key: API key for authentication
            agent_name: Optional name for the agent
            
        Returns:
            AgentCapabilities object with analysis results
        """
        print(f"🔍 Discovering and analyzing agent: {agent_url}")
        
        # Analyze agent capabilities
        capabilities = self.agent_analyzer.analyze_agent(agent_url, api_key)
        
        # Store agent profile
        agent_id = agent_name or f"agent_{hash(agent_url)}"
        self._agent_profiles[agent_id] = {
            'url': agent_url,
            'api_key': api_key,
            'capabilities': capabilities,
            'discovery_time': json.dumps(capabilities.__dict__, default=str)
        }
        
        print(f"✅ Agent analysis complete. Capabilities: {capabilities.domain_expertise}")
        return capabilities
        
    def generate_adaptive_strategy(self, agent_id: str, strategy_name: str = None) -> DynamicAIStrategy:
        """
        Generate an adaptive testing strategy for a specific agent.
        
        Args:
            agent_id: ID of the analyzed agent
            strategy_name: Optional name for the strategy
            
        Returns:
            DynamicAIStrategy configured for the agent
        """
        if agent_id not in self._agent_profiles:
            raise ValueError(f"Agent {agent_id} not found. Please analyze the agent first.")
            
        agent_profile = self._agent_profiles[agent_id]
        capabilities = agent_profile['capabilities']
        
        # Create dynamic strategy
        strategy_name = strategy_name or f"Dynamic_{agent_id}"
        strategy = DynamicAIStrategy(self.llm_config)
        strategy.name = strategy_name
        strategy.description = f"Dynamic strategy for {agent_id} - {capabilities.conversation_style} style"
        
        # Configure strategy based on agent capabilities
        strategy._agent_capabilities = capabilities.__dict__
        
        # Store generated strategy
        self._generated_strategies[strategy_name] = strategy
        
        print(f"✅ Generated adaptive strategy: {strategy_name}")
        return strategy
        
    def create_dynamic_scenarios(self, agent_id: str, scenario_count: int = 5) -> List[Dict[str, Any]]:
        """
        Create test scenarios dynamically based on agent capabilities.
        
        Args:
            agent_id: ID of the analyzed agent
            scenario_count: Number of scenarios to generate
            
        Returns:
            List of dynamically generated scenarios
        """
        if agent_id not in self._agent_profiles:
            raise ValueError(f"Agent {agent_id} not found. Please analyze the agent first.")
            
        agent_profile = self._agent_profiles[agent_id]
        capabilities = agent_profile['capabilities']
        
        scenarios = []
        
        # Generate scenarios based on domain expertise
        for domain in capabilities.domain_expertise:
            domain_scenarios = self._generate_domain_scenarios(domain, capabilities)
            scenarios.extend(domain_scenarios[:scenario_count // len(capabilities.domain_expertise)])
            
        # Fill remaining slots with general scenarios
        while len(scenarios) < scenario_count:
            scenarios.append(self._generate_general_scenario(capabilities))
            
        print(f"✅ Generated {len(scenarios)} dynamic scenarios for {agent_id}")
        return scenarios
        
    def _generate_domain_scenarios(self, domain: str, capabilities: AgentCapabilities) -> List[Dict[str, Any]]:
        """Generate scenarios for a specific domain."""
        domain_templates = {
            'financial': [
                {
                    'id': f'FIN_001_{domain}',
                    'title': 'Account Balance Inquiry',
                    'description': 'User wants to check their account balance',
                    'conversation': {
                        'initial_user_msg': 'Hi, I want to check my account balance.',
                        'max_turns': 3,
                        'tester_strategy': 'DynamicAI'
                    },
                    'goal': {
                        'user_goal': 'Check account balance and recent transactions'
                    },
                    'oracle': {
                        'hard_assertions': {
                            'provides_balance': True,
                            'mentions_account': True
                        },
                        'soft_metrics': {
                            'relevance': '>=0.8',
                            'completeness': '>=0.7'
                        }
                    }
                },
                {
                    'id': f'FIN_002_{domain}',
                    'title': 'Payment Processing',
                    'description': 'User wants to make a payment',
                    'conversation': {
                        'initial_user_msg': 'I need to make a payment of $100.',
                        'max_turns': 4,
                        'tester_strategy': 'DynamicAI'
                    },
                    'goal': {
                        'user_goal': 'Process payment successfully'
                    },
                    'oracle': {
                        'hard_assertions': {
                            'confirms_payment': True,
                            'provides_confirmation': True
                        },
                        'soft_metrics': {
                            'relevance': '>=0.8',
                            'completeness': '>=0.8'
                        }
                    }
                }
            ],
            'customer_service': [
                {
                    'id': f'CS_001_{domain}',
                    'title': 'General Support Request',
                    'description': 'User needs general support',
                    'conversation': {
                        'initial_user_msg': 'I need help with your service.',
                        'max_turns': 3,
                        'tester_strategy': 'DynamicAI'
                    },
                    'goal': {
                        'user_goal': 'Get appropriate support assistance'
                    },
                    'oracle': {
                        'hard_assertions': {
                            'offers_help': True,
                            'asks_for_details': True
                        },
                        'soft_metrics': {
                            'relevance': '>=0.7',
                            'completeness': '>=0.6'
                        }
                    }
                }
            ],
            'collections': [
                {
                    'id': f'COL_001_{domain}',
                    'title': 'Payment Arrangement',
                    'description': 'User wants to set up payment arrangement',
                    'conversation': {
                        'initial_user_msg': 'I\'m having trouble paying my debt. Can you help?',
                        'max_turns': 5,
                        'tester_strategy': 'DynamicAI'
                    },
                    'goal': {
                        'user_goal': 'Set up payment arrangement'
                    },
                    'oracle': {
                        'hard_assertions': {
                            'offers_payment_options': True,
                            'discusses_arrangement': True
                        },
                        'soft_metrics': {
                            'relevance': '>=0.8',
                            'completeness': '>=0.7'
                        }
                    }
                }
            ]
        }
        
        return domain_templates.get(domain, [])
        
    def _generate_general_scenario(self, capabilities: AgentCapabilities) -> Dict[str, Any]:
        """Generate a general scenario based on agent capabilities."""
        return {
            'id': f'GEN_001_{capabilities.conversation_style}',
            'title': 'General Assistance Request',
            'description': 'User needs general assistance',
            'conversation': {
                'initial_user_msg': 'Hello, how can you help me today?',
                'max_turns': 3,
                'tester_strategy': 'DynamicAI'
            },
            'goal': {
                'user_goal': 'Get appropriate assistance'
            },
            'oracle': {
                'hard_assertions': {
                    'responds_appropriately': True,
                    'offers_help': True
                },
                'soft_metrics': {
                    'relevance': '>=0.6',
                    'completeness': '>=0.5'
                }
            }
        }
        
    def create_platform_config(self, agent_id: str) -> Dict[str, Any]:
        """
        Create a complete platform configuration for an agent.
        
        Args:
            agent_id: ID of the analyzed agent
            
        Returns:
            Complete platform configuration
        """
        if agent_id not in self._agent_profiles:
            raise ValueError(f"Agent {agent_id} not found. Please analyze the agent first.")
            
        agent_profile = self._agent_profiles[agent_id]
        capabilities = agent_profile['capabilities']
        
        # Generate strategy
        strategy = self.generate_adaptive_strategy(agent_id)
        
        # Generate scenarios
        scenarios = self.create_dynamic_scenarios(agent_id)
        
        # Create platform configuration
        config = {
            'platform_version': '2.0',
            'agent_profile': {
                'id': agent_id,
                'url': agent_profile['url'],
                'capabilities': capabilities.__dict__,
                'analysis_confidence': capabilities.confidence_score
            },
            'testing_strategy': {
                'name': strategy.name,
                'type': 'dynamic_ai',
                'description': strategy.description,
                'capabilities': strategy.get_strategy_info()
            },
            'scenarios': scenarios,
            'configuration': {
                'llm_config': self.llm_config,
                'max_concurrent_tests': 5,
                'timeout_seconds': 30,
                'retry_attempts': 3
            }
        }
        
        return config
        
    def save_platform_config(self, agent_id: str, output_path: str):
        """Save platform configuration to file."""
        config = self.create_platform_config(agent_id)
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)
            
        print(f"✅ Platform configuration saved to: {output_file}")
        
    def load_platform_config(self, config_path: str) -> Dict[str, Any]:
        """Load platform configuration from file."""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        return config
        
    def get_agent_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get a summary of agent analysis and capabilities."""
        if agent_id not in self._agent_profiles:
            raise ValueError(f"Agent {agent_id} not found.")
            
        agent_profile = self._agent_profiles[agent_id]
        capabilities = agent_profile['capabilities']
        
        return {
            'agent_id': agent_id,
            'url': agent_profile['url'],
            'domain_expertise': capabilities.domain_expertise,
            'conversation_style': capabilities.conversation_style,
            'confidence_score': capabilities.confidence_score,
            'testing_recommendations': capabilities.testing_recommendations,
            'generated_strategies': list(self._generated_strategies.keys()),
            'scenario_count': len(self.create_dynamic_scenarios(agent_id))
        }

# Example usage
if __name__ == "__main__":
    # Initialize dynamic platform
    platform = DynamicUTAPlatform()
    
    # Discover and analyze an agent
    capabilities = platform.discover_and_analyze_agent(
        agent_url="https://api.example.com/chat",
        api_key="your-api-key",
        agent_name="example_agent"
    )
    
    # Generate adaptive strategy
    strategy = platform.generate_adaptive_strategy("example_agent")
    
    # Create dynamic scenarios
    scenarios = platform.create_dynamic_scenarios("example_agent", scenario_count=3)
    
    # Create and save platform configuration
    platform.save_platform_config("example_agent", "configs/example_agent_config.yaml")
    
    # Get agent summary
    summary = platform.get_agent_summary("example_agent")
    print(f"Agent Summary: {summary}")
