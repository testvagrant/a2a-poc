# Real-World UTA Flow: How Agent-to-Agent Testing Works

## 🎯 Overview

The Universal Tester-Agent (UTA) system enables **agent-to-agent testing** - using AI agents to test other AI agents. This document explains how UTA works in real-world scenarios, where test user agents initiate conversations with real product agents, and the entire conversation is evaluated by sophisticated LLM judges.

## 🔄 The Complete Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Test User      │    │  Real Product   │    │  Budget         │
│  Agent          │───▶│  Agent          │───▶│  Enforcer       │
│  (UTA System)   │    │  (ChatGPT/etc)  │    │  (Cost Control) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Initial        │    │  Natural        │    │  Turn/Latency/  │
│  Message        │    │  Response       │    │  Cost Limits    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────┐
                    │  LLM Judge      │
                    │  (GPT-4o)       │
                    │  Evaluation     │
                    └─────────────────┘
                                 │
                                 ▼
                    ┌─────────────────┐
                    │  Quality        │
                    │  Assessment     │
                    │  & Report       │
                    └─────────────────┘
```

### 1. **Test User Agent Initiates Conversation**
The UTA system starts by sending an initial message to your real AI agent, simulating a real user interaction.

### 2. **Real Product Agent Responds**
Your actual AI agent (ChatGPT, Claude, etc.) receives the message and responds naturally based on its training and capabilities.

### 3. **Budget Enforcement Controls the Flow**
The system monitors conversation length, latency, and cost to ensure tests stay within defined limits.

### 4. **LLM Judge Evaluates the Entire Conversation**
After the conversation completes, a sophisticated LLM judge (GPT-4o) analyzes the entire interaction for quality, relevance, and compliance.

## 📋 Detailed Step-by-Step Process

### Step 1: Scenario Definition
```yaml
# scenarios/collections/s01_promise_to_pay.yaml
id: COL_S01_PROMISE_TO_PAY
title: Promise to pay within 7 days (compliant tone)

conversation:
  initial_user_msg: "Hi, I got a call about dues. I can pay next week; is that okay?"
  max_turns: 5
  tester_strategy: FlowIntent

budgets:
  max_turns: 5
  max_latency_ms_avg: 3000
  max_cost_usd_per_session: 0.05
```

### Step 2: Test User Agent Sends Initial Message
```
Turn 1: User Agent → "Hi, I got a call about dues. I can pay next week; is that okay?"
```

### Step 3: Real Product Agent Responds
```
Turn 2: Product Agent → "I understand you're having payment difficulties. Let me help you set up a payment plan. Can you tell me more about your current situation?"
```

### Step 4: Conversation Continues Naturally
```
Turn 3: User Agent → "I lost my job last month, but I start a new one next week. I can pay the full amount then."
Turn 4: Product Agent → "I'm sorry to hear about your job loss. Congratulations on the new position! I can set up a promise to pay for next week. Let me get that arranged for you."
Turn 5: User Agent → "That would be perfect, thank you!"
Turn 6: Product Agent → "Great! I've set up your promise to pay for next week. You'll receive a confirmation email shortly. Is there anything else I can help you with today?"
```

### Step 5: Budget Enforcement
The system continuously monitors:
- **Turn Count**: Stops at 5 turns (as defined in budget)
- **Latency**: Ensures average response time < 3000ms
- **Cost**: Tracks estimated API costs < $0.05 per session

### Step 6: LLM Judge Evaluation
The complete conversation is sent to GPT-4o for evaluation:

```
LLM Judge Analysis:
"The agent demonstrated excellent customer service skills:
- Showed empathy for the customer's situation
- Provided appropriate solutions (promise to pay)
- Maintained professional and compliant tone
- Successfully completed the required action
- No compliance violations detected

Scores:
- Relevance: 0.95 (highly relevant to customer needs)
- Completeness: 0.90 (addressed all customer concerns)
- Groundedness: 0.88 (responses were appropriate and factual)
- Confidence: 0.92 (high confidence in evaluation)"
```

## 🏗️ Technical Implementation

### Conversation Loop
```python
# runner/run.py - Main conversation loop
turn = 0
while budget_enforcer.should_continue():
    # Send user message (first message or next from strategy)
    if turn == 0:
        user_msg = strategy.first_message(sc)
    else:
        user_msg = strategy.next_message(last_resp, sc)
        if not user_msg:
            break
            
    messages.append({'role': 'user', 'content': user_msg})
    
    # Get agent response with timing
    resp = product.send(messages, debtor_id=debtor_id)
    messages.append({'role': 'assistant', 'content': resp['text']})
    
    # Check budget constraints
    if not budget_enforcer.record_turn(turn_latency, estimated_cost):
        break
        
    turn += 1
```

### LLM Judge Evaluation
```python
# judges/llm_judge.py - Evaluation process
def evaluate_response(self, scenario, messages, agent_structured):
    # Create evaluation prompt with full conversation
    prompt = self._create_evaluation_prompt(scenario, messages, agent_structured)
    
    # Get LLM evaluation
    evaluation = self._get_llm_evaluation(prompt)
    
    # Parse and return results
    return JudgeResult(
        relevance=result.get('relevance', 0.0),
        completeness=result.get('completeness', 0.0),
        groundedness=result.get('groundedness', 0.0),
        reasoning=result.get('reasoning', ''),
        confidence=result.get('confidence', 0.0)
    )
```

## 🎯 Real-World Use Cases

### 1. **Customer Service Testing**
- **Scenario**: Customer complaint resolution
- **Test**: Agent handles complaint professionally and resolves issue
- **Evaluation**: Empathy, problem-solving, compliance

### 2. **Sales Conversation Testing**
- **Scenario**: Product recommendation and closing
- **Test**: Agent identifies needs and makes appropriate recommendations
- **Evaluation**: Persuasiveness, accuracy, ethical behavior

### 3. **Technical Support Testing**
- **Scenario**: Troubleshooting technical issues
- **Test**: Agent provides accurate solutions and escalates when needed
- **Evaluation**: Technical accuracy, clarity, escalation handling

### 4. **Compliance Testing**
- **Scenario**: Regulatory requirement adherence
- **Test**: Agent follows all compliance rules and disclosures
- **Evaluation**: Regulatory compliance, required disclosures

## 📊 Evaluation Metrics

### Hard Assertions (Pass/Fail)
- **Contains Required Elements**: Specific phrases or information must be present
- **Avoids Forbidden Content**: Certain words or phrases must not appear
- **Structured Data**: Required JSON fields must be populated
- **Compliance Rules**: Regulatory requirements must be met

### Soft Metrics (Quality Scores)
- **Relevance (0-1)**: How relevant are responses to user needs?
- **Completeness (0-1)**: How completely are user concerns addressed?
- **Groundedness (0-1)**: How accurate and factual are the responses?
- **Confidence (0-1)**: How confident is the judge in the evaluation?

## 🔧 Configuration Examples

### Basic Scenario
```yaml
id: BASIC_CUSTOMER_SERVICE
title: Basic customer service interaction

conversation:
  initial_user_msg: "I need help with my account"
  max_turns: 3
  tester_strategy: FlowIntent

budgets:
  max_turns: 3
  max_latency_ms_avg: 2000
  max_cost_usd_per_session: 0.02

oracle:
  hard_assertions:
    - name: helpful_response
      kind: contains_any
      values: ["help", "assist", "support"]
  soft_metrics:
    relevance: ">=0.8"
    completeness: ">=0.7"
```

### Advanced Scenario
```yaml
id: COMPLEX_SALES_CONVERSATION
title: Multi-turn sales conversation

conversation:
  initial_user_msg: "I'm looking for a new phone plan"
  max_turns: 8
  tester_strategy: FlowIntent

budgets:
  max_turns: 8
  max_latency_ms_avg: 3000
  max_cost_usd_per_session: 0.10

oracle:
  hard_assertions:
    - name: needs_assessment
      kind: contains_any
      values: ["usage", "budget", "features"]
    - name: recommendation_made
      kind: jsonpath_exists
      path: "$.recommended_plan"
  soft_metrics:
    relevance: ">=0.85"
    completeness: ">=0.80"
    groundedness: ">=0.75"
```

## 🚀 Benefits of This Approach

### 1. **Real-World Testing**
- Tests actual AI agent behavior, not simulated responses
- Captures natural conversation flow and agent personality
- Identifies real-world issues and edge cases

### 2. **Sophisticated Evaluation**
- LLM judges provide nuanced quality assessment
- Goes beyond simple rule-based checking
- Understands context and conversation flow

### 3. **Cost Control**
- Budget enforcement prevents runaway costs
- Configurable limits for different testing scenarios
- Cost tracking and optimization

### 4. **Scalable Architecture**
- Can test any AI agent via HTTP API
- Pluggable strategies for different testing approaches
- Easy to add new scenarios and evaluation criteria

### 5. **Business-Ready Reports**
- Professional reports for stakeholders
- Detailed conversation analysis
- Performance metrics and recommendations

## 📈 Running Real-World Tests

### Command Line Usage
```bash
# Run a single scenario
python3 -m runner.run scenarios/collections/s01_promise_to_pay.yaml

# Run multiple scenarios
python3 -m runner.run scenarios/collections/*.yaml

# Run with specific output directory
python3 -m runner.run scenarios/core/CORE_001_INTENT_SUCCESS.yaml --output-dir my_test_results
```

### Environment Configuration
```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com
OPENAI_MODEL=gpt-4o

LLM_JUDGE_API_KEY=your_openai_api_key_here
LLM_JUDGE_BASE_URL=https://api.openai.com
LLM_JUDGE_MODEL=gpt-4o
```

## 🎯 Key Takeaways

1. **UTA enables real conversation testing** between AI agents
2. **Test user agents initiate** conversations with real product agents
3. **Budget enforcement** controls conversation length and cost
4. **LLM judges evaluate** the entire conversation for quality
5. **Real-world scenarios** test actual AI agent behavior
6. **Sophisticated evaluation** goes beyond simple rule checking
7. **Scalable architecture** supports any AI agent via API
8. **Business-ready reports** provide actionable insights

## 🔗 Related Documentation

- [UTA User Guide](UTA_USER_GUIDE.md) - Comprehensive usage documentation
- [Strategy Reference](STRATEGIES_REFERENCE.md) - Testing strategy details
- [Real Agent Testing Guide](REAL_AGENT_TESTING_GUIDE.md) - Setting up real agent testing
- [Business Reporting Guide](BUSINESS_REPORTING_GUIDE.md) - Understanding reports
- [LLM Judge Setup](LLM_JUDGE_ENV_SETUP.md) - Configuring LLM evaluation

---

**The Universal Tester-Agent system represents the future of AI quality assurance - testing AI agents with AI agents for comprehensive, real-world evaluation.**
