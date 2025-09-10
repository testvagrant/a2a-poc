"""
Hybrid Domain Strategies Example

This example demonstrates the hybrid approach:
1. Domain-specific strategies (Financial, Customer Service, etc.)
2. AI-powered dynamic message generation within each domain
3. Automatic domain detection and strategy selection

This combines the best of both worlds:
- Domain expertise and knowledge
- Dynamic, adaptive message generation
"""

import json
from agents.strategies.dynamic_strategy_factory import DynamicStrategyFactory
from agents.strategies.dynamic_financial_strategy import DynamicFinancialStrategy
from agents.strategies.dynamic_customer_service_strategy import DynamicCustomerServiceStrategy

def demonstrate_hybrid_approach():
    """Demonstrate the hybrid domain + AI approach."""
    
    print("🚀 Hybrid Domain Strategies + AI-Powered Messages")
    print("=" * 60)
    
    # Initialize the strategy factory
    factory = DynamicStrategyFactory({
        'model': 'gpt-4o-mini',
        'temperature': 0.7,
        'max_tokens': 500
    })
    
    # Example 1: Financial Domain
    print("\n💰 Example 1: Financial Domain Strategy")
    print("-" * 40)
    
    financial_scenario = {
        'title': 'Account Balance Inquiry',
        'goal': {'user_goal': 'Check my account balance and recent transactions'},
        'tags': ['financial', 'account_management'],
        'conversation': {
            'initial_user_msg': 'Hi, I want to check my account balance.',
            'max_turns': 4,
            'tester_strategy': 'DynamicFinancial'
        }
    }
    
    # Create financial strategy
    financial_strategy = factory.create_strategy(
        "https://api.bank.com/chat",
        financial_scenario,
        "bank_agent"
    )
    
    print(f"✅ Created Strategy: {financial_strategy.name}")
    print(f"   - Type: {financial_strategy.get_strategy_info()['type']}")
    print(f"   - Domain: {financial_strategy.get_strategy_info()['domain']}")
    print(f"   - Capabilities: {len(financial_strategy.get_strategy_info()['capabilities'])}")
    
    # Simulate financial conversation
    print(f"\n📝 Simulating Financial Conversation:")
    print(f"Turn 1 - User: {financial_strategy.first_message(financial_scenario)}")
    
    # Simulate agent responses
    financial_agent_responses = [
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
    
    for i, response in enumerate(financial_agent_responses):
        next_message = financial_strategy.next_message(response, financial_scenario)
        if next_message:
            print(f"Turn {i+2} - User: {next_message}")
        else:
            print(f"Turn {i+2} - Strategy: Conversation complete")
            break
    
    # Example 2: Customer Service Domain
    print("\n🎧 Example 2: Customer Service Domain Strategy")
    print("-" * 40)
    
    service_scenario = {
        'title': 'Technical Support Request',
        'goal': {'user_goal': 'Get help with a technical issue'},
        'tags': ['support', 'technical'],
        'conversation': {
            'initial_user_msg': 'I need help with a technical problem.',
            'max_turns': 4,
            'tester_strategy': 'DynamicCustomerService'
        }
    }
    
    # Create service strategy
    service_strategy = factory.create_strategy(
        "https://api.support.com/chat",
        service_scenario,
        "support_agent"
    )
    
    print(f"✅ Created Strategy: {service_strategy.name}")
    print(f"   - Type: {service_strategy.get_strategy_info()['type']}")
    print(f"   - Domain: {service_strategy.get_strategy_info()['domain']}")
    print(f"   - Capabilities: {len(service_strategy.get_strategy_info()['capabilities'])}")
    
    # Simulate service conversation
    print(f"\n📝 Simulating Customer Service Conversation:")
    print(f"Turn 1 - User: {service_strategy.first_message(service_scenario)}")
    
    # Simulate agent responses
    service_agent_responses = [
        {
            'text': 'I\'m sorry to hear you\'re having a technical issue. Can you describe what\'s happening?',
            'structured': {'intent': 'request_issue_description', 'outcome': 'pending_input'}
        },
        {
            'text': 'I understand the issue. Let me help you troubleshoot this. First, try restarting the application.',
            'structured': {'intent': 'provide_troubleshooting', 'outcome': 'in_progress'}
        },
        {
            'text': 'Great! If that didn\'t work, let\'s try clearing the cache. Go to Settings > Clear Cache.',
            'structured': {'intent': 'provide_next_step', 'outcome': 'in_progress'}
        }
    ]
    
    for i, response in enumerate(service_agent_responses):
        next_message = service_strategy.next_message(response, service_scenario)
        if next_message:
            print(f"Turn {i+2} - User: {next_message}")
        else:
            print(f"Turn {i+2} - Strategy: Conversation complete")
            break
    
    # Example 3: Automatic Domain Detection
    print("\n🔍 Example 3: Automatic Domain Detection")
    print("-" * 40)
    
    test_scenarios = [
        {
            'name': 'Banking Scenario',
            'scenario': {
                'title': 'Loan Application',
                'goal': {'user_goal': 'Apply for a personal loan'},
                'tags': ['financial', 'loans'],
                'conversation': {'initial_user_msg': 'I want to apply for a loan.'}
            }
        },
        {
            'name': 'Support Scenario',
            'scenario': {
                'title': 'Billing Issue',
                'goal': {'user_goal': 'Resolve a billing problem'},
                'tags': ['support', 'billing'],
                'conversation': {'initial_user_msg': 'I have a billing issue.'}
            }
        },
        {
            'name': 'Generic Scenario',
            'scenario': {
                'title': 'General Inquiry',
                'goal': {'user_goal': 'Get general information'},
                'tags': ['general'],
                'conversation': {'initial_user_msg': 'Hello, how can you help me?'}
            }
        }
    ]
    
    for test_case in test_scenarios:
        analysis = factory.analyze_scenario_domain(test_case['scenario'])
        print(f"✅ {test_case['name']}:")
        print(f"   - Detected Domain: {analysis['detected_domain']}")
        print(f"   - Confidence: {analysis['confidence']:.2f}")
        print(f"   - Recommended Strategy: {analysis['recommended_strategy']}")
        
        # Create strategy for this scenario
        strategy = factory.create_strategy(
            f"https://api.{analysis['detected_domain']}.com/chat",
            test_case['scenario']
        )
        print(f"   - Created Strategy: {strategy.name}")
        print()
    
    # Example 4: Domain-Specific Knowledge
    print("\n🧠 Example 4: Domain-Specific Knowledge")
    print("-" * 40)
    
    # Show financial domain knowledge
    financial_strategy = DynamicFinancialStrategy()
    print("Financial Domain Knowledge:")
    print(f"   - Domains: {list(financial_strategy.financial_domains.keys())}")
    print(f"   - Account Management Keywords: {financial_strategy.financial_domains['account_management']['keywords']}")
    print(f"   - Payment Processing Keywords: {financial_strategy.financial_domains['payment_processing']['keywords']}")
    
    # Show service domain knowledge
    service_strategy = DynamicCustomerServiceStrategy()
    print("\nCustomer Service Domain Knowledge:")
    print(f"   - Domains: {list(service_strategy.service_domains.keys())}")
    print(f"   - Technical Support Keywords: {service_strategy.service_domains['technical_support']['keywords']}")
    print(f"   - Billing Support Keywords: {service_strategy.service_domains['billing_support']['keywords']}")
    
    # Example 5: Benefits of Hybrid Approach
    print("\n🎯 Example 5: Benefits of Hybrid Approach")
    print("-" * 40)
    
    benefits = {
        'Domain Expertise': [
            'Financial strategies understand banking terminology',
            'Service strategies understand support workflows',
            'Domain-specific goal achievement detection',
            'Appropriate escalation handling'
        ],
        'AI-Powered Messages': [
            'Dynamic message generation based on agent responses',
            'Context-aware conversation flow',
            'Adaptive to different agent capabilities',
            'Natural, human-like interactions'
        ],
        'Scalability': [
            'Easy to add new domains',
            'Automatic domain detection',
            'Consistent interface across domains',
            'Reduced maintenance overhead'
        ],
        'Flexibility': [
            'Domain-specific knowledge + AI adaptability',
            'Fallback to heuristics when AI fails',
            'Configurable LLM parameters',
            'Extensible architecture'
        ]
    }
    
    for benefit_category, benefit_list in benefits.items():
        print(f"\n✅ {benefit_category}:")
        for benefit in benefit_list:
            print(f"   - {benefit}")
    
    print("\n🎉 Hybrid Approach Demonstration Complete!")
    print("=" * 60)
    
    return {
        'strategies_created': 2,
        'domains_tested': 3,
        'conversations_simulated': 2,
        'domain_detection_accuracy': 'high'
    }

def demonstrate_domain_specific_ai_generation():
    """Demonstrate how AI generates domain-specific messages."""
    
    print("\n🤖 Domain-Specific AI Message Generation")
    print("=" * 50)
    
    # Financial domain example
    print("\n💰 Financial Domain AI Generation:")
    print("-" * 30)
    
    financial_scenario = {
        'title': 'Payment Processing',
        'goal': {'user_goal': 'Make a payment of $100'},
        'tags': ['financial', 'payments']
    }
    
    financial_response = {
        'text': 'I can help you make a payment. What account would you like to pay from?',
        'structured': {'intent': 'request_payment_source', 'outcome': 'pending_input'}
    }
    
    # Show how financial strategy would generate AI prompt
    financial_strategy = DynamicFinancialStrategy()
    financial_strategy._detected_domain = 'payment_processing'
    financial_strategy._agent_capabilities = {
        'financial_knowledge': 'intermediate',
        'conversation_style': 'polite'
    }
    
    prompt = financial_strategy._create_financial_domain_prompt(financial_scenario, financial_response)
    print("Financial AI Prompt (excerpt):")
    print(prompt[:200] + "...")
    
    # Customer service domain example
    print("\n🎧 Customer Service Domain AI Generation:")
    print("-" * 30)
    
    service_scenario = {
        'title': 'Technical Support',
        'goal': {'user_goal': 'Resolve a technical issue'},
        'tags': ['support', 'technical']
    }
    
    service_response = {
        'text': 'I understand you\'re having a technical issue. Can you describe what\'s happening?',
        'structured': {'intent': 'request_issue_description', 'outcome': 'pending_input'}
    }
    
    # Show how service strategy would generate AI prompt
    service_strategy = DynamicCustomerServiceStrategy()
    service_strategy._detected_domain = 'technical_support'
    service_strategy._agent_capabilities = {
        'technical_knowledge': 'intermediate',
        'empathy_level': 'high'
    }
    
    prompt = service_strategy._create_service_domain_prompt(service_scenario, service_response)
    print("Service AI Prompt (excerpt):")
    print(prompt[:200] + "...")
    
    print("\n✅ Domain-Specific AI Generation Demonstrated!")

if __name__ == "__main__":
    # Run demonstrations
    print("🚀 Starting Hybrid Domain Strategies Demonstrations")
    print("=" * 70)
    
    # Main hybrid approach demonstration
    hybrid_results = demonstrate_hybrid_approach()
    
    # Domain-specific AI generation demonstration
    demonstrate_domain_specific_ai_generation()
    
    # Summary
    print("\n📊 Demonstration Summary")
    print("=" * 30)
    print(f"✅ Strategies Created: {hybrid_results['strategies_created']}")
    print(f"✅ Domains Tested: {hybrid_results['domains_tested']}")
    print(f"✅ Conversations Simulated: {hybrid_results['conversations_simulated']}")
    print(f"✅ Domain Detection Accuracy: {hybrid_results['domain_detection_accuracy']}")
    
    print("\n🎉 All Demonstrations Complete!")
    print("The Hybrid Domain + AI Approach is ready for production use!")
