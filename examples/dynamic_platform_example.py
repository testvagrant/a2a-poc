"""
Dynamic UTA Platform Example

This example demonstrates how the dynamic UTA platform can automatically:
1. Discover and analyze any AI agent
2. Generate appropriate testing strategies
3. Create test scenarios dynamically
4. Run tests with adaptive message generation

This makes the UTA system truly scalable across different applications and domains.
"""

import json
import time
from platform.dynamic_platform import DynamicUTAPlatform
from agents.agent_analyzer import AgentAnalyzer
from agents.strategies.dynamic_ai_strategy import DynamicAIStrategy

def demonstrate_dynamic_platform():
    """Demonstrate the dynamic UTA platform capabilities."""
    
    print("🚀 Dynamic UTA Platform Demonstration")
    print("=" * 50)
    
    # Initialize the dynamic platform
    platform = DynamicUTAPlatform({
        'model': 'gpt-4o-mini',
        'temperature': 0.7,
        'max_tokens': 1000
    })
    
    # Example 1: Analyze a financial AI agent
    print("\n📊 Example 1: Analyzing Financial AI Agent")
    print("-" * 40)
    
    financial_agent_capabilities = platform.discover_and_analyze_agent(
        agent_url="https://api.financial-bot.com/chat",
        api_key="financial-api-key",
        agent_name="financial_agent"
    )
    
    print(f"✅ Financial Agent Analysis Complete:")
    print(f"   - Domain Expertise: {financial_agent_capabilities.domain_expertise}")
    print(f"   - Conversation Style: {financial_agent_capabilities.conversation_style}")
    print(f"   - Confidence Score: {financial_agent_capabilities.confidence_score}")
    
    # Example 2: Analyze a customer service AI agent
    print("\n📊 Example 2: Analyzing Customer Service AI Agent")
    print("-" * 40)
    
    cs_agent_capabilities = platform.discover_and_analyze_agent(
        agent_url="https://api.support-bot.com/chat",
        api_key="support-api-key",
        agent_name="customer_service_agent"
    )
    
    print(f"✅ Customer Service Agent Analysis Complete:")
    print(f"   - Domain Expertise: {cs_agent_capabilities.domain_expertise}")
    print(f"   - Conversation Style: {cs_agent_capabilities.conversation_style}")
    print(f"   - Confidence Score: {cs_agent_capabilities.confidence_score}")
    
    # Example 3: Generate adaptive strategies
    print("\n🎯 Example 3: Generating Adaptive Strategies")
    print("-" * 40)
    
    financial_strategy = platform.generate_adaptive_strategy("financial_agent", "FinancialDynamicStrategy")
    cs_strategy = platform.generate_adaptive_strategy("customer_service_agent", "CSDynamicStrategy")
    
    print(f"✅ Generated Strategies:")
    print(f"   - Financial Strategy: {financial_strategy.name}")
    print(f"   - Customer Service Strategy: {cs_strategy.name}")
    
    # Example 4: Create dynamic scenarios
    print("\n📝 Example 4: Creating Dynamic Scenarios")
    print("-" * 40)
    
    financial_scenarios = platform.create_dynamic_scenarios("financial_agent", scenario_count=3)
    cs_scenarios = platform.create_dynamic_scenarios("customer_service_agent", scenario_count=2)
    
    print(f"✅ Generated Scenarios:")
    print(f"   - Financial Scenarios: {len(financial_scenarios)}")
    print(f"   - Customer Service Scenarios: {len(cs_scenarios)}")
    
    # Show example scenario
    if financial_scenarios:
        print(f"\n📋 Example Financial Scenario:")
        scenario = financial_scenarios[0]
        print(f"   - ID: {scenario['id']}")
        print(f"   - Title: {scenario['title']}")
        print(f"   - Initial Message: {scenario['conversation']['initial_user_msg']}")
        print(f"   - Strategy: {scenario['conversation']['tester_strategy']}")
    
    # Example 5: Create platform configurations
    print("\n⚙️ Example 5: Creating Platform Configurations")
    print("-" * 40)
    
    platform.save_platform_config("financial_agent", "configs/financial_agent_config.yaml")
    platform.save_platform_config("customer_service_agent", "configs/cs_agent_config.yaml")
    
    print("✅ Platform configurations saved")
    
    # Example 6: Get agent summaries
    print("\n📋 Example 6: Agent Summaries")
    print("-" * 40)
    
    financial_summary = platform.get_agent_summary("financial_agent")
    cs_summary = platform.get_agent_summary("customer_service_agent")
    
    print(f"Financial Agent Summary:")
    print(f"   - Domain Expertise: {financial_summary['domain_expertise']}")
    print(f"   - Conversation Style: {financial_summary['conversation_style']}")
    print(f"   - Confidence Score: {financial_summary['confidence_score']}")
    print(f"   - Testing Recommendations: {financial_summary['testing_recommendations']}")
    
    print(f"\nCustomer Service Agent Summary:")
    print(f"   - Domain Expertise: {cs_summary['domain_expertise']}")
    print(f"   - Conversation Style: {cs_summary['conversation_style']}")
    print(f"   - Confidence Score: {cs_summary['confidence_score']}")
    print(f"   - Testing Recommendations: {cs_summary['testing_recommendations']}")
    
    # Example 7: Demonstrate cross-platform scalability
    print("\n🌐 Example 7: Cross-Platform Scalability")
    print("-" * 40)
    
    # Simulate analyzing different types of agents
    agent_types = [
        {"name": "ecommerce_agent", "url": "https://api.shop-bot.com/chat", "domain": "ecommerce"},
        {"name": "healthcare_agent", "url": "https://api.health-bot.com/chat", "domain": "healthcare"},
        {"name": "education_agent", "url": "https://api.edu-bot.com/chat", "domain": "education"},
        {"name": "travel_agent", "url": "https://api.travel-bot.com/chat", "domain": "travel"}
    ]
    
    print("✅ The platform can automatically analyze and adapt to:")
    for agent_type in agent_types:
        print(f"   - {agent_type['domain'].title()} Agent: {agent_type['name']}")
    
    print("\n🎉 Dynamic Platform Demonstration Complete!")
    print("=" * 50)
    
    return {
        'financial_agent': financial_summary,
        'customer_service_agent': cs_summary,
        'scenarios_generated': len(financial_scenarios) + len(cs_scenarios),
        'strategies_generated': 2
    }

def demonstrate_ai_powered_message_generation():
    """Demonstrate AI-powered message generation."""
    
    print("\n🤖 AI-Powered Message Generation Demonstration")
    print("=" * 50)
    
    # Create a dynamic strategy
    strategy = DynamicAIStrategy({
        'model': 'gpt-4o-mini',
        'temperature': 0.7,
        'max_tokens': 500
    })
    
    # Simulate a conversation scenario
    scenario = {
        'title': 'Account Balance Inquiry',
        'goal': {'user_goal': 'Check account balance and recent transactions'},
        'tags': ['financial', 'account_management'],
        'conversation': {
            'initial_user_msg': 'Hi, I want to check my account balance.',
            'max_turns': 4,
            'tester_strategy': 'DynamicAI'
        }
    }
    
    # Simulate agent responses
    agent_responses = [
        {
            'text': 'Hello! I can help you check your account balance. May I have your account number?',
            'structured': {'intent': 'request_account_number', 'outcome': 'pending_input'}
        },
        {
            'text': 'Thank you. I can see your account. Your current balance is $1,234.56. Would you like to see recent transactions?',
            'structured': {'intent': 'provide_balance', 'outcome': 'success', 'balance': 1234.56}
        },
        {
            'text': 'Here are your recent transactions: [Transaction details]. Is there anything else I can help you with?',
            'structured': {'intent': 'provide_transactions', 'outcome': 'success'}
        }
    ]
    
    print("📝 Simulating AI-Powered Message Generation:")
    print("-" * 40)
    
    # Generate first message
    first_message = strategy.first_message(scenario)
    print(f"Turn 1 - User: {first_message}")
    
    # Generate subsequent messages
    for i, agent_response in enumerate(agent_responses):
        next_message = strategy.next_message(agent_response, scenario)
        if next_message:
            print(f"Turn {i+2} - User: {next_message}")
        else:
            print(f"Turn {i+2} - Strategy: Conversation complete")
            break
    
    print("\n✅ AI-Powered Message Generation Complete!")
    
    return {
        'messages_generated': 4,
        'strategy_type': 'DynamicAI',
        'conversation_flow': 'natural'
    }

def demonstrate_scalability_benefits():
    """Demonstrate the scalability benefits of the dynamic approach."""
    
    print("\n📈 Scalability Benefits Demonstration")
    print("=" * 50)
    
    benefits = {
        'automatic_discovery': {
            'description': 'Automatically discover and analyze any AI agent',
            'benefits': [
                'No manual configuration required',
                'Works with any OpenAI-compatible API',
                'Adapts to different conversation styles',
                'Identifies domain expertise automatically'
            ]
        },
        'dynamic_strategy_generation': {
            'description': 'Generate testing strategies based on agent capabilities',
            'benefits': [
                'No hardcoded message templates',
                'AI-powered message generation',
                'Context-aware conversation flow',
                'Adaptive to agent responses'
            ]
        },
        'cross_domain_scalability': {
            'description': 'Scale across different domains and applications',
            'benefits': [
                'Financial services',
                'Customer support',
                'E-commerce',
                'Healthcare',
                'Education',
                'Travel and hospitality'
            ]
        },
        'maintenance_reduction': {
            'description': 'Significantly reduce maintenance overhead',
            'benefits': [
                'No manual strategy updates',
                'Automatic adaptation to agent changes',
                'Self-healing test scenarios',
                'Reduced human intervention'
            ]
        }
    }
    
    for benefit_category, details in benefits.items():
        print(f"\n🎯 {benefit_category.replace('_', ' ').title()}:")
        print(f"   {details['description']}")
        print("   Benefits:")
        for benefit in details['benefits']:
            print(f"   - {benefit}")
    
    print("\n✅ Scalability Benefits Demonstrated!")
    
    return benefits

if __name__ == "__main__":
    # Run all demonstrations
    print("🚀 Starting Dynamic UTA Platform Demonstrations")
    print("=" * 60)
    
    # Main platform demonstration
    platform_results = demonstrate_dynamic_platform()
    
    # AI-powered message generation demonstration
    message_results = demonstrate_ai_powered_message_generation()
    
    # Scalability benefits demonstration
    scalability_results = demonstrate_scalability_benefits()
    
    # Summary
    print("\n📊 Demonstration Summary")
    print("=" * 30)
    print(f"✅ Agents Analyzed: {len(platform_results) - 2}")
    print(f"✅ Scenarios Generated: {platform_results['scenarios_generated']}")
    print(f"✅ Strategies Generated: {platform_results['strategies_generated']}")
    print(f"✅ Messages Generated: {message_results['messages_generated']}")
    print(f"✅ Scalability Categories: {len(scalability_results)}")
    
    print("\n🎉 All Demonstrations Complete!")
    print("The Dynamic UTA Platform is ready for production use!")
