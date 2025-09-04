# Universal Tester-Agent (UTA) - User Guide

## Overview

The Universal Tester-Agent (UTA) is a comprehensive testing framework designed to validate AI agents across different domains and use cases. It provides deterministic, vendor-agnostic testing capabilities with support for both mock and real AI agent integration.

## Key Features

- **Universal Testing**: Test any AI agent regardless of domain or implementation
- **Deterministic Results**: Reproducible test runs with seeded random number generation
- **Multiple Judge Types**: Heuristic, LLM-based, and hybrid evaluation approaches
- **Budget Enforcement**: Turn limits, latency tracking, and cost monitoring
- **Real Agent Integration**: HTTP adapters for testing live AI services
- **Comprehensive Reporting**: HTML and JSON reports with detailed metrics
- **Policy Compliance**: Configurable policy profiles for different requirements

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd a2a-poc-mock
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
python3 -m runner.run --help
```

## Quick Start

### Basic Usage

Run core scenarios with default settings:
```bash
python3 -m runner.run --suite scenarios/core --report out_core
```

Run collections scenarios:
```bash
python3 -m runner.run --suite scenarios/collections --report out_collections
```

### Advanced Usage

Run with specific seed for reproducibility:
```bash
python3 -m runner.run --suite scenarios/core --report out_core --seed 12345
```

Run with LLM judge:
```bash
python3 -m runner.run --suite scenarios/core --report out_core --judge-mode llm --llm-api-key YOUR_API_KEY
```

Run with HTTP adapter for real agent:
```bash
python3 -m runner.run --suite scenarios/core --report out_core --http-url https://api.example.com/chat --http-api-key YOUR_API_KEY
```

## Configuration

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--suite` | Path to scenarios directory | Required |
| `--report` | Output directory for report | Required |
| `--fixtures` | Fixtures directory | `fixtures` |
| `--profile` | Policy profile to use | `default` |
| `--tags` | Filter scenarios by tags | None |
| `--seed` | Random seed for deterministic runs | Auto-generated |
| `--judge-mode` | Judge mode (heuristic/llm/hybrid) | `heuristic` |
| `--llm-api-key` | API key for LLM judge | None |
| `--llm-model` | LLM model for judge | `gpt-3.5-turbo` |
| `--llm-type` | LLM provider (openai/anthropic/azure) | `openai` |
| `--http-url` | HTTP URL for real agent integration | None |
| `--http-api-key` | API key for HTTP authentication | None |

### Configuration Files

#### HTTP Configuration

Create `fixtures/http_config.yaml`:
```yaml
base_url: "https://api.example.com/chat"
api_key: "your-api-key-here"
timeout: 30
headers:
  X-Domain: "collections"
  X-Version: "1.0"
```

#### Judge Configuration

Create `fixtures/judge_config.yaml`:
```yaml
mode: "hybrid"
llm_config:
  judge_type: "openai"
  model_name: "gpt-3.5-turbo"
  api_key: "your-api-key-here"
  temperature: 0.1
  max_tokens: 1000
hybrid_weights:
  heuristic: 0.3
  llm: 0.7
```

## Scenario Development

### Scenario Structure

Scenarios are defined in YAML files with the following structure:

```yaml
id: SCENARIO_ID
title: "Scenario Title"
dsl_version: "0.1"
tags: [tag1, tag2, tag3]
channel: chat
domain: collections  # Optional
preconditions:
  user_profile:
    persona: "default"
    locale: "en-US"
  data_refs:
    debtor_id: "D-1001"
  policy_profile: "default"
goal:
  user_goal: "User's intended goal"
conversation:
  initial_user_msg: "Initial user message"
  max_turns: 5
  tester_strategy: FlowIntent
oracle:
  hard_assertions:
    - name: assertion_name
      kind: contains_any
      from: agent
      values: ["value1", "value2"]
  soft_metrics:
    relevance: ">=0.65"
    completeness: ">=0.60"
    groundedness: ">=0.70"
budgets:
  max_turns: 5
  max_latency_ms_avg: 3000
  max_cost_usd_per_session: 0.05
artifacts:
  capture_audio: false
  save_transcript: true
  log_structured_data: true
```

### Hard Assertions

| Kind | Description | Parameters |
|------|-------------|------------|
| `contains_any` | Check if response contains any of the values | `values: [list]` |
| `not_contains_any` | Check if response doesn't contain any values | `values: [list]` |
| `matches_regex` | Check if response matches regex pattern | `pattern: string` |
| `jsonpath_exists` | Check if JSONPath exists in structured data | `path: string` |
| `jsonpath_equals` | Check if JSONPath equals expected value | `path: string`, `expected_value: any` |
| `number_between` | Check if number is between min and max | `path: string`, `min_value: number`, `max_value: number` |

### Soft Metrics

- **Relevance**: How relevant is the response to the user's goal (0.0-1.0)
- **Completeness**: How complete is the response (0.0-1.0)
- **Groundedness**: How well-grounded is the response in context (0.0-1.0)

### Tester Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| `FlowIntent` | Basic conversational flow with clarification | General scenarios |
| `ToolHappyPath` | Tool execution and success path testing | Tool-based scenarios |
| `MemoryCarry` | Memory and context carry testing | Memory-dependent scenarios |
| `ToolError` | Error handling and recovery testing | Resilience testing |

## Judge Types

### Heuristic Judge

Fast, rule-based evaluation using predefined heuristics:
- Token overlap for relevance
- Structured data presence for completeness
- Number presence for groundedness

### LLM Judge

Sophisticated evaluation using language models:
- Context-aware relevance assessment
- Comprehensive completeness evaluation
- Detailed groundedness analysis
- Reasoning and confidence metrics

### Hybrid Judge

Combines heuristic and LLM evaluation:
- Configurable weights for each approach
- Best of both worlds
- Fallback capabilities

## Budget Enforcement

### Turn Limits

Control maximum number of conversation turns:
```yaml
budgets:
  max_turns: 5
```

### Latency Tracking

Monitor and enforce response time limits:
```yaml
budgets:
  max_latency_ms_avg: 3000
```

### Cost Monitoring

Track and limit estimated costs:
```yaml
budgets:
  max_cost_usd_per_session: 0.05
```

## Reporting

### HTML Reports

Comprehensive HTML reports with:
- Executive summary
- Scenario results
- Detailed metrics
- Budget information
- Judge details

### JSON Reports

Machine-readable JSON reports with:
- Complete session data
- Structured metrics
- Budget status
- Seed information
- Judge results

## Best Practices

### Scenario Design

1. **Clear Goals**: Define specific, measurable user goals
2. **Realistic Conversations**: Use natural, realistic user messages
3. **Appropriate Assertions**: Choose assertions that match the scenario intent
4. **Reasonable Budgets**: Set realistic budget constraints
5. **Meaningful Tags**: Use tags for organization and filtering

### Testing Strategy

1. **Start Simple**: Begin with basic scenarios and build complexity
2. **Use Deterministic Seeds**: For reproducible testing and debugging
3. **Monitor Budgets**: Set appropriate limits for your use case
4. **Validate with Real Agents**: Test with actual AI services when possible
5. **Iterate and Improve**: Continuously refine scenarios based on results

### Performance Optimization

1. **Batch Testing**: Run multiple scenarios in single execution
2. **Parallel Execution**: Use multiple processes for large test suites
3. **Efficient Judges**: Use heuristic judge for fast feedback, LLM for detailed analysis
4. **Budget Management**: Set appropriate limits to avoid unnecessary costs

## Troubleshooting

### Common Issues

#### Scenario Validation Errors
- Check required fields in scenario YAML
- Verify DSL version compatibility
- Ensure proper YAML syntax

#### Judge Errors
- Verify API keys for LLM judges
- Check network connectivity
- Review judge configuration

#### Budget Violations
- Adjust budget constraints
- Optimize scenario complexity
- Review agent performance

#### HTTP Adapter Issues
- Verify endpoint URLs
- Check authentication credentials
- Review network connectivity

### Debug Mode

Enable debug logging:
```bash
export UTA_LOG_LEVEL=DEBUG
python3 -m runner.run --suite scenarios/core --report out_core
```

### Error Recovery

The UTA system includes automatic error recovery:
- Network errors: Retry with exponential backoff
- Validation errors: Use default values where appropriate
- Judge errors: Fall back to heuristic evaluation
- Budget violations: Stop execution gracefully

## API Reference

### Core Classes

#### `UnifiedJudge`
Main judge interface supporting multiple evaluation modes.

#### `BudgetEnforcer`
Enforces budget constraints during test execution.

#### `SeedManager`
Manages deterministic seeding for reproducible results.

#### `HTTPAdapter`
HTTP client for real AI agent integration.

#### `StrategyRegistry`
Manages tester agent strategies.

### Utility Classes

#### `UTALogger`
Comprehensive logging with structured output.

#### `UTAErrorHandler`
Error handling and recovery mechanisms.

## Contributing

### Adding New Scenarios

1. Create YAML file in appropriate directory
2. Follow scenario structure guidelines
3. Test with both mock and real agents
4. Document scenario purpose and use cases

### Adding New Strategies

1. Implement `BaseStrategy` interface
2. Register in `StrategyRegistry`
3. Add comprehensive tests
4. Update documentation

### Adding New Judges

1. Implement judge interface
2. Add configuration support
3. Integrate with `UnifiedJudge`
4. Test with various scenarios

## Support

For questions, issues, or contributions:
- Create GitHub issues for bugs and feature requests
- Review documentation for common questions
- Check logs for detailed error information
- Use debug mode for troubleshooting

## License

[Add license information here]
