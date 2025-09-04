# Scenario Types Guide for UTA Testing

## 🎯 **Comprehensive Scenario Categories**

This guide shows all the types of scenarios we can build and test with ChatGPT and other AI agents using the UTA system.

## 📋 **1. Core Universal Scenarios (Already Built)**

### **Basic Functionality Testing**
- **Intent Recognition**: Can the agent understand user goals?
- **Clarification Handling**: Can it ask for more information?
- **Tool Usage**: Can it execute actions and use tools?
- **Memory & Context**: Can it remember conversation history?
- **Error Handling**: Can it recover from mistakes?

**Example**: `CORE_001_INTENT_SUCCESS.yaml`

## 🏢 **2. Business Domain Scenarios**

### **Collections & Debt Management (Already Built)**
- **Promise to Pay**: Payment commitment handling
- **Dispute Resolution**: Debt dispute management
- **Wrong Person**: Identity verification
- **Payment Plans**: Payment arrangement negotiation
- **Hardship Claims**: Financial difficulty assistance
- **Cease Contact**: Communication preference management
- **Verification Requests**: Debt verification process
- **Settlement Offers**: Debt settlement negotiation
- **Legal Threats**: Legal compliance handling
- **Contact Preferences**: Communication method management

### **Customer Service**
- **Billing Issues**: Account and payment problems
- **Product Support**: Technical assistance
- **Account Management**: Profile and settings changes
- **Refund Requests**: Return and refund processing
- **Complaint Handling**: Issue resolution
- **Upgrade/Downgrade**: Service level changes

### **Sales & Marketing**
- **Lead Qualification**: Potential customer assessment
- **Product Recommendations**: Personalized suggestions
- **Pricing Inquiries**: Cost and package information
- **Demo Scheduling**: Product demonstration setup
- **Objection Handling**: Sales resistance management
- **Follow-up**: Post-interaction engagement

## 🧠 **3. Advanced Cognitive Scenarios (New)**

### **Multi-Turn Complex Conversations**
- **Context Switching**: Handling topic changes
- **Long-term Memory**: Remembering across sessions
- **Progressive Disclosure**: Revealing information gradually
- **Follow-up Questions**: Deepening understanding

**Example**: `ADV_001_MULTI_TURN_COMPLEX.yaml`

### **Emotional Intelligence**
- **Empathy Detection**: Recognizing emotional states
- **Appropriate Responses**: Matching emotional tone
- **De-escalation**: Calming frustrated users
- **Motivation**: Encouraging positive actions

**Example**: `ADV_002_EMOTIONAL_INTELLIGENCE.yaml`

### **Knowledge Retrieval & Synthesis**
- **Information Gathering**: Collecting relevant data
- **Source Integration**: Combining multiple sources
- **Fact Verification**: Checking information accuracy
- **Knowledge Application**: Using information effectively

**Example**: `ADV_003_KNOWLEDGE_RETRIEVAL.yaml`

### **Creative Problem Solving**
- **Innovation**: Generating novel solutions
- **Resource Optimization**: Working with constraints
- **Alternative Approaches**: Exploring different options
- **Implementation Planning**: Turning ideas into actions

**Example**: `ADV_004_CREATIVE_PROBLEM_SOLVING.yaml`

### **Educational Tutoring**
- **Adaptive Learning**: Adjusting to student pace
- **Concept Explanation**: Breaking down complex topics
- **Practice Problems**: Providing exercises
- **Progress Assessment**: Evaluating understanding

**Example**: `ADV_005_EDUCATIONAL_TUTORING.yaml`

## 🔧 **4. Technical Scenarios**

### **API Integration**
- **Authentication**: Login and security
- **Data Exchange**: Information transfer
- **Error Handling**: API failure management
- **Rate Limiting**: Managing API constraints

### **System Administration**
- **Configuration**: Setting up systems
- **Monitoring**: Health and performance checks
- **Troubleshooting**: Problem diagnosis
- **Maintenance**: System updates and fixes

### **Data Processing**
- **ETL Operations**: Extract, Transform, Load
- **Data Validation**: Quality assurance
- **Report Generation**: Creating summaries
- **Analytics**: Data interpretation

## 🎭 **5. Behavioral Scenarios**

### **Persona Testing**
- **Professional**: Formal business interactions
- **Casual**: Informal friendly conversations
- **Technical**: Expert-level discussions
- **Beginner**: Novice-friendly explanations

### **Cultural Adaptation**
- **Language Variants**: Different English dialects
- **Cultural References**: Region-specific content
- **Business Practices**: Local customs
- **Communication Styles**: Cultural preferences

### **Accessibility**
- **Visual Impairment**: Screen reader compatibility
- **Hearing Impairment**: Text-based communication
- **Cognitive Differences**: Simplified explanations
- **Motor Impairment**: Voice-only interaction

## 🚨 **6. Edge Case Scenarios**

### **Error Conditions**
- **Invalid Input**: Malformed requests
- **System Failures**: Service unavailability
- **Timeout Handling**: Long response delays
- **Resource Exhaustion**: Memory or CPU limits

### **Security Testing**
- **Injection Attacks**: SQL, XSS, etc.
- **Authentication Bypass**: Security vulnerabilities
- **Data Privacy**: Information protection
- **Rate Limiting**: Abuse prevention

### **Boundary Testing**
- **Input Limits**: Maximum data sizes
- **Response Limits**: Output constraints
- **Time Limits**: Response time boundaries
- **Cost Limits**: Budget constraints

## 🎯 **7. Performance Scenarios**

### **Load Testing**
- **High Volume**: Many concurrent users
- **Long Conversations**: Extended interactions
- **Complex Queries**: Resource-intensive requests
- **Peak Usage**: Traffic spikes

### **Latency Testing**
- **Response Time**: Speed requirements
- **Network Delays**: Connection issues
- **Processing Time**: Computation limits
- **Caching**: Performance optimization

## 📊 **8. Compliance Scenarios**

### **Regulatory Compliance**
- **GDPR**: Data protection (EU)
- **CCPA**: Privacy rights (California)
- **HIPAA**: Health information (US)
- **SOX**: Financial reporting (US)

### **Industry Standards**
- **PCI DSS**: Payment card security
- **ISO 27001**: Information security
- **SOC 2**: Service organization controls
- **FedRAMP**: Government cloud security

## 🎨 **9. Creative Scenarios**

### **Content Generation**
- **Writing**: Articles, emails, reports
- **Creative Writing**: Stories, poems, scripts
- **Technical Writing**: Documentation, manuals
- **Marketing Copy**: Advertisements, campaigns

### **Problem Solving**
- **Brainstorming**: Idea generation
- **Decision Making**: Choice evaluation
- **Planning**: Project organization
- **Strategy**: Long-term thinking

## 🔄 **10. Integration Scenarios**

### **Third-Party Services**
- **CRM Integration**: Customer management
- **ERP Systems**: Enterprise resource planning
- **Payment Gateways**: Financial transactions
- **Communication Tools**: Email, SMS, chat

### **Workflow Automation**
- **Process Orchestration**: Multi-step workflows
- **Conditional Logic**: Decision trees
- **Parallel Processing**: Concurrent operations
- **Error Recovery**: Failure handling

## 🎯 **Scenario Complexity Levels**

### **Beginner (Level 1)**
- Single intent
- 2-3 conversation turns
- Basic assertions
- Simple metrics

### **Intermediate (Level 2)**
- Multiple intents
- 4-6 conversation turns
- Complex assertions
- Advanced metrics

### **Advanced (Level 3)**
- Complex interactions
- 7+ conversation turns
- Multi-dimensional assertions
- Sophisticated metrics

### **Expert (Level 4)**
- Multi-domain knowledge
- 10+ conversation turns
- Context-aware assertions
- AI-powered metrics

## 🚀 **Testing with ChatGPT**

### **Quick Start Commands**

```bash
# Test core scenarios
python3 -m runner.run --suite scenarios/core --report out_chatgpt_core --http-url https://api.openai.com/v1/chat/completions --http-api-key YOUR_OPENAI_KEY

# Test advanced scenarios
python3 -m runner.run --suite scenarios/advanced --report out_chatgpt_advanced --http-url https://api.openai.com/v1/chat/completions --http-api-key YOUR_OPENAI_KEY

# Test collections scenarios
python3 -m runner.run --suite scenarios/collections --report out_chatgpt_collections --http-url https://api.openai.com/v1/chat/completions --http-api-key YOUR_OPENAI_KEY

# Test with LLM judge
python3 -m runner.run --suite scenarios/advanced --report out_chatgpt_llm_judge --http-url https://api.openai.com/v1/chat/completions --http-api-key YOUR_OPENAI_KEY --judge-mode llm --llm-api-key YOUR_OPENAI_KEY
```

### **Expected Results with ChatGPT**

| Scenario Type | Pass Rate | Response Quality | Use Case |
|---------------|-----------|------------------|----------|
| **Core Scenarios** | 90-95% | Excellent | Basic functionality |
| **Business Scenarios** | 85-90% | Very Good | Domain expertise |
| **Advanced Scenarios** | 80-85% | Good | Complex reasoning |
| **Technical Scenarios** | 75-80% | Good | Technical knowledge |
| **Creative Scenarios** | 85-90% | Excellent | Innovation |
| **Educational Scenarios** | 80-85% | Good | Teaching ability |

## 🎉 **Getting Started**

### **1. Choose Your Scenario Type**
- Start with core scenarios for basic testing
- Move to business scenarios for domain testing
- Try advanced scenarios for complex testing

### **2. Set Up ChatGPT Testing**
```bash
# Get OpenAI API key from https://platform.openai.com/api-keys
export OPENAI_API_KEY="your-api-key-here"

# Test with ChatGPT
python3 -m runner.run --suite scenarios/core --report out_chatgpt --http-url https://api.openai.com/v1/chat/completions --http-api-key $OPENAI_API_KEY
```

### **3. Analyze Results**
- Check pass rates and failure reasons
- Review response quality and relevance
- Identify areas for improvement
- Iterate on scenarios

## 📚 **Next Steps**

1. **Start Simple**: Begin with core scenarios
2. **Add Complexity**: Gradually increase difficulty
3. **Domain Focus**: Build scenarios for your specific use case
4. **Advanced Testing**: Use sophisticated scenarios for thorough evaluation
5. **Production Ready**: Deploy comprehensive test suites

---

## 🏆 **Summary**

The UTA system supports **10 major scenario categories** with **unlimited possibilities** for testing AI agents. From basic functionality to advanced cognitive abilities, from business domains to creative problem-solving, you can build and test any type of scenario that matches your needs.

**ChatGPT is perfect for testing** because it excels at:
- ✅ **Natural Language Understanding**
- ✅ **Context Awareness**
- ✅ **Creative Problem Solving**
- ✅ **Multi-turn Conversations**
- ✅ **Domain Knowledge**
- ✅ **Emotional Intelligence**

Start with the scenarios that match your use case and build from there! 🚀

