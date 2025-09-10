# 🤖 Universal Tester-Agent (UTA)

> **AI Agent Testing & Evaluation Platform**

A comprehensive, vendor-agnostic testing system for evaluating AI agents with sophisticated multi-modal judging, real-time integration, and business-ready reporting.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Production Ready](https://img.shields.io/badge/status-production%20ready-green.svg)](https://github.com/your-org/uta)

## 🚀 Overview

The Universal Tester-Agent (UTA) is a revolutionary testing platform that enables **agent-to-agent testing** - using AI agents to test other AI agents. This approach provides sophisticated, nuanced evaluation that goes far beyond traditional rule-based testing.

### ✨ Key Features

- **🤖 Real AI Testing**: Test actual AI agents (ChatGPT, Claude, etc.) with real conversations
- **🧠 LLM Judges**: Sophisticated AI-powered evaluation using GPT-4o for nuanced quality assessment
- **📊 Business Reports**: Professional, stakeholder-ready reports with detailed insights
- **🔧 Pluggable Architecture**: Extensible system with pluggable strategies, judges, and adapters
- **💰 Budget Control**: Cost monitoring and budget enforcement for production-ready testing
- **🎯 Deterministic Testing**: Reproducible results with seeded RNG for consistent evaluation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Test Scenarios │    │  Testing Strategies │    │   AI Agents     │
│   (YAML DSL)    │───▶│  (Pluggable)     │───▶│  (Real/HTTP)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Test Runner   │    │  Multi-modal    │    │   Report        │
│   (Orchestrator)│    │  Judge System   │    │   Generator     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components

- **Test Runner**: Core execution engine that orchestrates test scenarios
- **Strategy System**: Pluggable testing strategies for different evaluation approaches
- **Judge System**: Multi-modal evaluation system (heuristic + LLM judges)
- **HTTP Adapter**: Integration layer for real AI agent testing
- **Report Generator**: Business-ready HTML report generation

## 🎯 Testing Strategies

### Currently Implemented

1. **FlowIntentStrategy**: Tests natural conversation flow and intent understanding
2. **ToolHappyPathStrategy**: Tests successful tool usage and function calling
3. **MemoryCarryStrategy**: Tests context retention across conversation turns
4. **ToolErrorStrategy**: Tests error handling and recovery mechanisms
5. **DynamicAIStrategy**: 🚀 **NEW!** AI-powered dynamic message generation that adapts to any agent automatically

### 🚀 Dynamic AI Strategy (Scalable Solution)

The **DynamicAI** strategy represents a breakthrough in scalability:

- **🤖 AI-Powered**: Uses LLM to generate contextually appropriate messages
- **🔄 Adaptive**: Automatically adapts to any agent's capabilities and conversation style
- **🌐 Cross-Platform**: Works with any OpenAI-compatible API across different domains
- **⚡ Zero Configuration**: No manual setup required - automatically discovers agent capabilities
- **📈 Scalable**: Eliminates the need for hardcoded strategies across different applications

**Learn More**: [Dynamic UTA Platform Documentation](docs/DYNAMIC_UTA_PLATFORM.md)

### Planned Strategies

- **DisturbanceStrategy**: Stress testing and interruptions
- **PlannerStrategy**: Multi-step planning capabilities
- **PersonaStrategy**: Consistent persona maintenance
- **PIIProbeStrategy**: Privacy and data protection
- **InterruptionStrategy**: Conversation interruption handling
- **RepeatProbeStrategy**: Consistency and edge case testing

## 📋 Test Scenarios

### Scenario Categories

- **Core Scenarios**: Fundamental AI agent capabilities
- **Advanced Scenarios**: Complex, multi-turn interactions
- **Collections Scenarios**: Domain-specific business logic testing

### Example Scenario Structure

```yaml
id: "CORE_001_INTENT_SUCCESS"
title: "Basic Intent Recognition Success"
description: "Tests that the agent correctly identifies and responds to user intent"
tags: ["core", "intent", "success"]

system_prompt: |
  You are a helpful AI assistant. Respond naturally to user requests.

budget:
  max_turns: 3
  max_latency_ms_avg: 2000
  max_cost_usd_per_session: 0.10

strategy: "FlowIntent"

conversation:
  - role: "user"
    content: "I need help with my account"
    intent: "account_help"
  
  - role: "assistant"
    expected_intent: "account_help"
    hard_assertions:
      - type: "contains_any"
        values: ["account", "help", "assist"]
    soft_metrics:
      relevance: 0.8
      completeness: 0.7
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for LLM judge and real agent testing)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/uta.git
   cd uta
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   cp config/env.example .env
   # Edit .env with your API keys
   ```

4. **Run your first test**
   ```bash
   python3 -m runner.run scenarios/core/CORE_001_INTENT_SUCCESS.yaml
   ```

### Environment Configuration

Create a `.env` file with your configuration:

```bash
# OpenAI Configuration (for LLM judge and real agent testing)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com
OPENAI_MODEL=gpt-4o

# LLM Judge Configuration
LLM_JUDGE_API_KEY=your_openai_api_key_here
LLM_JUDGE_BASE_URL=https://api.openai.com
LLM_JUDGE_MODEL=gpt-4o
LLM_JUDGE_TEMPERATURE=0.1
LLM_JUDGE_MAX_TOKENS=1000

# UTA Configuration
UTA_LOG_LEVEL=INFO
UTA_OUTPUT_DIR=out
```

## 📊 Usage Examples

### Basic Test Run

```bash
# Run a single scenario
python3 -m runner.run scenarios/core/CORE_001_INTENT_SUCCESS.yaml

# Run multiple scenarios
python3 -m runner.run scenarios/core/*.yaml

# Run with specific output directory
python3 -m runner.run scenarios/core/CORE_001_INTENT_SUCCESS.yaml --output-dir my_test_results
```

### Advanced Configuration

```bash
# Run with custom policy
python3 -m runner.run scenarios/collections/s01_promise_to_pay.yaml --policy fixtures/policies_strict.yaml

# Run with budget enforcement
python3 -m runner.run scenarios/advanced/ADV_001_MULTI_TURN_COMPLEX.yaml --budget-enforcement

# Run with deterministic seeding
python3 -m runner.run scenarios/core/CORE_001_INTENT_SUCCESS.yaml --seed 42
```

### Generate Dashboard

```bash
# Generate comprehensive dashboard
python3 scripts/generate_dashboard.py

# Open dashboard
open dashboard/index.html
```

## 📈 Reports

UTA generates comprehensive, business-ready reports including:

- **Executive Summary**: High-level results and key metrics
- **Scenario Analysis**: Detailed pass/fail status for each test
- **Performance Metrics**: Latency, cost, and efficiency analysis
- **LLM Judge Evaluation**: Sophisticated AI-powered quality assessment
- **Budget Analysis**: Cost tracking and budget compliance
- **Conversation Transcripts**: Full interaction logs with analysis

### Report Features

- **Interactive Dashboard**: Multi-page dashboard for client presentations
- **Collapsible Sections**: Detailed analysis that can be expanded as needed
- **Business Metrics**: Stakeholder-friendly insights and recommendations
- **Technical Details**: Developer-focused implementation information

## 🔧 Development

### Project Structure

```
uta/
├── agents/                 # AI agent adapters and strategies
│   ├── strategies/        # Testing strategies
│   ├── http_adapter.py    # Real agent integration
│   └── product_adapter_*.py # Mock agents
├── judges/                # Evaluation systems
│   ├── schema_judge.py    # Heuristic evaluation
│   ├── llm_judge.py       # AI-powered evaluation
│   └── unified_judge.py   # Multi-modal judging
├── reporters/             # Report generation
│   ├── templates/         # HTML templates
│   └── dashboard_generator.py
├── runner/                # Core execution engine
│   ├── run.py            # Main test runner
│   ├── budget_enforcer.py # Cost and performance monitoring
│   └── seed_manager.py   # Deterministic testing
├── scenarios/             # Test scenarios
│   ├── core/             # Fundamental tests
│   ├── advanced/         # Complex interactions
│   └── collections/      # Domain-specific tests
├── config/               # Configuration management
├── docs/                 # Documentation
├── examples/             # Usage examples
└── scripts/              # Utility scripts
```

### Adding New Strategies

1. **Create strategy class**
   ```python
   # agents/strategies/my_strategy.py
   from .base_strategy import BaseStrategy
   
   class MyStrategy(BaseStrategy):
       """My custom testing strategy."""
       
       def get_next_turn(self, conversation, context):
           # Implement your strategy logic
           pass
   ```

2. **Register strategy**
   ```python
   # agents/strategies/registry.py
   from .my_strategy import MyStrategy
   
   def _register_default_strategies(self):
       # ... existing strategies ...
       self.register("MyStrategy", MyStrategy)
   ```

3. **Use in scenarios**
   ```yaml
   # scenarios/my_scenario.yaml
   strategy: "MyStrategy"
   # ... rest of scenario
   ```

### Adding New Scenarios

1. **Create scenario file**
   ```yaml
   # scenarios/my_category/my_scenario.yaml
   id: "MY_001_EXAMPLE"
   title: "My Test Scenario"
   description: "Tests my specific use case"
   
   system_prompt: |
     You are a helpful assistant.
   
   strategy: "FlowIntent"
   
   conversation:
     - role: "user"
       content: "Hello"
     - role: "assistant"
       hard_assertions:
         - type: "contains_any"
           values: ["hello", "hi", "greeting"]
   ```

2. **Run the scenario**
   ```bash
   python3 -m runner.run scenarios/my_category/my_scenario.yaml
   ```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test category
python3 -m pytest tests/test_strategies.py

# Run with coverage
python3 -m pytest --cov=agents tests/
```

### Test Categories

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end scenario testing
- **Strategy Tests**: Testing strategy implementations
- **Judge Tests**: Evaluation system testing

## 📚 Documentation

- **[Real-World UTA Flow](docs/REAL_WORLD_UTA_FLOW.md)**: How agent-to-agent testing works in practice
- **[User Guide](docs/UTA_USER_GUIDE.md)**: Comprehensive usage documentation
- **[Strategy Reference](docs/STRATEGIES_REFERENCE.md)**: Detailed strategy documentation
- **[Business Reporting Guide](docs/BUSINESS_REPORTING_GUIDE.md)**: Report interpretation guide
- **[Real Agent Testing Guide](docs/REAL_AGENT_TESTING_GUIDE.md)**: Testing with real AI agents

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-awesome-feature
   ```
3. **Make your changes**
4. **Add tests**
5. **Submit a pull request**

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Add docstrings for all classes and methods
- Write tests for new functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT models used in LLM judging
- The Python community for excellent libraries and tools
- Contributors and users who help improve UTA

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/your-org/uta/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/uta/discussions)
- **Email**: support@uta.ai

## 🚀 Roadmap

### Phase 1: Core Platform ✅
- [x] Basic test runner and scenario execution
- [x] Mock agent implementations
- [x] Heuristic judging system
- [x] Basic reporting

### Phase 2: Advanced Features ✅
- [x] LLM-powered judging
- [x] Real agent integration
- [x] Budget enforcement
- [x] Deterministic seeding

### Phase 3: Enterprise Features 🚧
- [ ] Multi-tenant support
- [ ] Advanced analytics
- [ ] CI/CD integration
- [ ] Enterprise security features

### Phase 4: Ecosystem 🌟
- [ ] Plugin marketplace
- [ ] Community scenarios
- [ ] Third-party integrations
- [ ] Advanced AI models

---

**Built with ❤️ for the AI community**

*Testing AI agents with AI agents - the future of AI quality assurance.*