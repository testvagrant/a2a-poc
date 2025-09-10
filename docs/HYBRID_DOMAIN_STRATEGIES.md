# Hybrid Domain Strategies: The Best of Both Worlds

## 🎯 **The Perfect Solution**

You're absolutely right! The ideal approach is:
- **Strategies**: Domain-specific (Financial, Customer Service, etc.)
- **Messages**: AI-powered and dynamic

This hybrid approach combines:
1. **Domain Expertise**: Each strategy understands its domain deeply
2. **AI-Powered Messages**: Dynamic message generation based on context
3. **Scalability**: Easy to add new domains
4. **Maintainability**: Domain knowledge is centralized and reusable

## 🏗️ **Architecture Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                    Strategy Level                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Financial     │  │ Customer Service│  │   Generic    │ │
│  │   Strategy      │  │   Strategy      │  │   Strategy   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Message Level                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   AI-Powered    │  │   AI-Powered    │  │   AI-Powered │ │
│  │   Message       │  │   Message       │  │   Message    │ │
│  │   Generation    │  │   Generation    │  │   Generation │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 **Implementation Details**

### 1. **Domain-Specific Strategies**

Each strategy contains domain knowledge:

#### **Financial Strategy** (`DynamicFinancialStrategy`)
```python
# Domain knowledge
self.financial_domains = {
    'account_management': {
        'keywords': ['account', 'balance', 'statement', 'transaction'],
        'common_goals': ['check_balance', 'view_transactions'],
        'typical_flows': ['balance_inquiry', 'transaction_history']
    },
    'payment_processing': {
        'keywords': ['payment', 'transfer', 'bill', 'pay'],
        'common_goals': ['make_payment', 'transfer_funds'],
        'typical_flows': ['payment_setup', 'transfer_confirmation']
    }
}
```

#### **Customer Service Strategy** (`DynamicCustomerServiceStrategy`)
```python
# Domain knowledge
self.service_domains = {
    'technical_support': {
        'keywords': ['technical', 'bug', 'error', 'issue'],
        'common_goals': ['resolve_technical_issue', 'bug_report'],
        'typical_flows': ['issue_description', 'troubleshooting_steps']
    },
    'billing_support': {
        'keywords': ['billing', 'charge', 'payment', 'refund'],
        'common_goals': ['billing_inquiry', 'refund_request'],
        'typical_flows': ['billing_question', 'payment_investigation']
    }
}
```

### 2. **AI-Powered Message Generation**

Each strategy uses AI to generate contextually appropriate messages:

```python
def _generate_domain_aware_message(self, scenario, last_response):
    # Create domain-aware prompt
    prompt = self._create_financial_domain_prompt(scenario, last_response)
    
    # Get AI response
    ai_response = self._call_ai_for_financial_message(prompt)
    
    return self._parse_ai_message_response(ai_response)
```

### 3. **Automatic Domain Detection**

The `DynamicStrategyFactory` automatically selects the right strategy:

```python
def _detect_domain(self, agent_url, scenario):
    # Analyze scenario content
    user_goal = scenario.get('goal', {}).get('user_goal', '').lower()
    tags = scenario.get('tags', [])
    
    # Score each domain
    domain_scores = {}
    for domain, keywords in self.domain_keywords.items():
        score = 0
        for keyword in keywords:
            if keyword in user_goal:
                score += 3  # User goal is most important
        domain_scores[domain] = score
    
    # Return best domain
    return max(domain_scores, key=domain_scores.get)
```

## 🚀 **Usage Examples**

### **Example 1: Financial Agent Testing**

```python
# Scenario for financial agent
financial_scenario = {
    'title': 'Account Balance Inquiry',
    'goal': {'user_goal': 'Check my account balance and recent transactions'},
    'tags': ['financial', 'account_management'],
    'conversation': {
        'initial_user_msg': 'Hi, I want to check my account balance.',
        'tester_strategy': 'DynamicFinancial'
    }
}

# Factory automatically selects financial strategy
factory = DynamicStrategyFactory()
strategy = factory.create_strategy("https://api.bank.com/chat", financial_scenario)

# Strategy generates domain-aware AI messages
first_msg = strategy.first_message(financial_scenario)
# "Hi, I want to check my account balance."

# AI generates next message based on agent response
next_msg = strategy.next_message(agent_response, financial_scenario)
# "Can you show me my recent transactions?" (AI-generated, context-aware)
```

### **Example 2: Customer Service Agent Testing**

```python
# Scenario for customer service agent
service_scenario = {
    'title': 'Technical Support Request',
    'goal': {'user_goal': 'Get help with a technical issue'},
    'tags': ['support', 'technical'],
    'conversation': {
        'initial_user_msg': 'I need help with a technical problem.',
        'tester_strategy': 'DynamicCustomerService'
    }
}

# Factory automatically selects service strategy
strategy = factory.create_strategy("https://api.support.com/chat", service_scenario)

# Strategy generates domain-aware AI messages
first_msg = strategy.first_message(service_scenario)
# "I need help with a technical problem."

# AI generates next message based on agent response
next_msg = strategy.next_message(agent_response, service_scenario)
# "I tried that but it didn't work. What else can I try?" (AI-generated, context-aware)
```

## 📊 **Benefits Comparison**

| Aspect | Traditional Hardcoded | Pure AI Dynamic | **Hybrid Approach** |
|--------|----------------------|-----------------|-------------------|
| **Domain Knowledge** | ❌ Limited | ❌ Generic | ✅ **Rich & Specific** |
| **Message Quality** | ❌ Rigid | ✅ Dynamic | ✅ **Dynamic & Contextual** |
| **Scalability** | ❌ Manual per domain | ✅ Automatic | ✅ **Easy to add domains** |
| **Maintainability** | ❌ High effort | ✅ Low effort | ✅ **Moderate effort** |
| **Accuracy** | ❌ Domain-specific only | ⚠️ Generic | ✅ **Domain-optimized** |
| **Flexibility** | ❌ Fixed patterns | ✅ Adaptive | ✅ **Adaptive + Knowledge** |

## 🎯 **Key Advantages**

### 1. **Domain Expertise**
- **Financial Strategy**: Understands banking terminology, payment flows, security concerns
- **Service Strategy**: Understands support workflows, escalation procedures, empathy levels
- **Generic Strategy**: Fallback for unknown domains

### 2. **AI-Powered Adaptability**
- **Context-Aware**: Messages adapt to conversation flow
- **Agent-Adaptive**: Adjusts to different agent capabilities
- **Goal-Oriented**: Moves toward achieving scenario goals

### 3. **Easy Scalability**
- **Add New Domains**: Just create new strategy class
- **Automatic Detection**: Factory selects appropriate strategy
- **Consistent Interface**: All strategies implement same interface

### 4. **Maintainability**
- **Centralized Knowledge**: Domain expertise in one place
- **Reusable Components**: AI generation logic is shared
- **Clear Separation**: Domain logic vs. message generation

## 🔧 **Implementation Guide**

### **Step 1: Create Domain Strategy**

```python
class DynamicHealthcareStrategy(BaseStrategy):
    def __init__(self, llm_config=None):
        super().__init__(name="DynamicHealthcare", description="...")
        
        # Domain knowledge
        self.healthcare_domains = {
            'patient_support': {
                'keywords': ['patient', 'appointment', 'medical', 'health'],
                'common_goals': ['schedule_appointment', 'medical_inquiry'],
                'typical_flows': ['appointment_booking', 'medical_consultation']
            }
        }
        
    def _generate_domain_aware_message(self, scenario, last_response):
        # AI-powered message generation with healthcare context
        prompt = self._create_healthcare_domain_prompt(scenario, last_response)
        return self._call_ai_for_healthcare_message(prompt)
```

### **Step 2: Register Strategy**

```python
# In registry.py
self.register("DynamicHealthcare", DynamicHealthcareStrategy)

# Add domain keywords
self.domain_keywords['healthcare'] = [
    'patient', 'appointment', 'medical', 'health', 'doctor', 'clinic'
]
```

### **Step 3: Use Strategy**

```python
# Factory automatically detects healthcare domain
strategy = factory.create_strategy("https://api.clinic.com/chat", healthcare_scenario)
```

## 🚀 **Future Enhancements**

### **Planned Domains**
- **E-commerce**: Product recommendations, order management, returns
- **Education**: Student support, course assistance, academic guidance
- **Travel**: Booking assistance, itinerary planning, customer service
- **Real Estate**: Property inquiries, market analysis, client support

### **Advanced Features**
- **Multi-Domain Scenarios**: Test agents that handle multiple domains
- **Domain Transition**: Test agents that switch between domains
- **Cross-Domain Knowledge**: Test agents that apply knowledge across domains

## 📚 **Related Documentation**

- [Dynamic UTA Platform](DYNAMIC_UTA_PLATFORM.md)
- [Real-World UTA Flow](REAL_WORLD_UTA_FLOW.md)
- [Agent Strategies Guide](AGENT_STRATEGIES.md)

## 🎉 **Conclusion**

The hybrid approach gives you the best of both worlds:
- **Domain expertise** for accurate, relevant testing
- **AI-powered messages** for dynamic, adaptive conversations
- **Easy scalability** for adding new domains
- **Maintainable architecture** for long-term success

This approach transforms the UTA from a rigid, domain-specific tool into a flexible, intelligent testing platform that can adapt to any agent while maintaining deep domain knowledge.

---

**The hybrid approach is the perfect solution for scalable, intelligent AI-to-AI testing.**
