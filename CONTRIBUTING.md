# Contributing to Universal Tester-Agent (UTA)

Thank you for your interest in contributing to UTA! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

- **Bug Reports**: Use the GitHub issue tracker with the "bug" label
- **Feature Requests**: Use the GitHub issue tracker with the "enhancement" label
- **Documentation Issues**: Use the GitHub issue tracker with the "documentation" label

### Making Changes

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Submit a pull request**

## 🏗️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- OpenAI API key (for testing)

### Setup Steps

1. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/uta.git
   cd uta
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set up environment**
   ```bash
   cp config/env.example .env
   # Edit .env with your API keys
   ```

5. **Run tests**
   ```bash
   python3 -m pytest tests/
   ```

## 📝 Code Style Guidelines

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints for all functions and methods
- Add docstrings for all classes, methods, and functions
- Keep line length under 100 characters
- Use meaningful variable and function names

### Example Code Style

```python
from typing import Dict, List, Optional

class MyStrategy(BaseStrategy):
    """
    My custom testing strategy.
    
    This strategy implements a specific testing approach for AI agents.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the strategy with optional configuration."""
        super().__init__(config)
        self.config = config or {}
    
    def get_next_turn(self, conversation: List[Dict], context: Dict) -> Dict:
        """
        Get the next turn in the conversation.
        
        Args:
            conversation: List of conversation turns
            context: Additional context information
            
        Returns:
            Dictionary containing the next turn information
        """
        # Implementation here
        pass
```

### File Organization

- **Strategies**: Place in `agents/strategies/`
- **Scenarios**: Place in `scenarios/` with appropriate subdirectory
- **Tests**: Place in `tests/` with matching structure
- **Documentation**: Place in `docs/`

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

### Test Structure

```python
import pytest
from unittest.mock import Mock, patch
from agents.strategies.my_strategy import MyStrategy

class TestMyStrategy:
    """Test cases for MyStrategy."""
    
    def test_initialization(self):
        """Test strategy initialization."""
        strategy = MyStrategy()
        assert strategy is not None
    
    def test_get_next_turn_success(self):
        """Test successful next turn generation."""
        strategy = MyStrategy()
        conversation = [{"role": "user", "content": "Hello"}]
        context = {}
        
        result = strategy.get_next_turn(conversation, context)
        
        assert result is not None
        assert "role" in result
        assert "content" in result
    
    @patch('some_external_dependency')
    def test_external_dependency_handling(self, mock_dependency):
        """Test handling of external dependencies."""
        mock_dependency.return_value = "mocked_result"
        
        strategy = MyStrategy()
        result = strategy.some_method()
        
        assert result == "expected_result"
        mock_dependency.assert_called_once()
```

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test file
python3 -m pytest tests/test_strategies.py

# Run with coverage
python3 -m pytest --cov=agents tests/

# Run with verbose output
python3 -m pytest -v tests/
```

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No merge conflicts
- [ ] Commit messages are clear

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

### Commit Message Format

Use clear, descriptive commit messages:

```
feat: add new FlowIntent strategy for conversation testing
fix: resolve issue with LLM judge API calls
docs: update user guide with new examples
test: add unit tests for budget enforcer
refactor: improve error handling in test runner
```

## 🎯 Contribution Areas

### High Priority

- **New Testing Strategies**: Implement additional testing approaches
- **Real Agent Integrations**: Add support for more AI providers
- **Performance Improvements**: Optimize test execution and reporting
- **Documentation**: Improve user guides and API documentation

### Medium Priority

- **UI Improvements**: Enhance dashboard and reporting interfaces
- **CI/CD Integration**: Add GitHub Actions workflows
- **Monitoring**: Add observability and monitoring features
- **Security**: Implement security best practices

### Low Priority

- **Examples**: Add more example scenarios and use cases
- **Templates**: Create scenario and strategy templates
- **Utilities**: Add helper scripts and tools

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Python version
   - Operating system
   - UTA version

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Expected vs actual behavior
   - Minimal reproduction case

3. **Additional Context**
   - Error messages and stack traces
   - Relevant configuration
   - Screenshots if applicable

### Bug Report Template

```markdown
## Bug Description
Brief description of the bug

## Environment
- Python version: 3.9.7
- OS: macOS 12.0
- UTA version: 1.0.0

## Steps to Reproduce
1. Run command: `python3 -m runner.run scenarios/core/CORE_001_INTENT_SUCCESS.yaml`
2. Observe error: [error message]

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Additional Context
Any other relevant information
```

## 🚀 Feature Requests

When requesting features, please include:

1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Other approaches considered
4. **Additional Context**: Any other relevant information

### Feature Request Template

```markdown
## Feature Description
Brief description of the requested feature

## Use Case
Why is this feature needed? What problem does it solve?

## Proposed Solution
How should this feature work?

## Alternatives Considered
What other approaches were considered?

## Additional Context
Any other relevant information, mockups, examples, etc.
```

## 📚 Documentation Contributions

### Types of Documentation

- **User Guides**: Step-by-step instructions for users
- **API Documentation**: Technical reference for developers
- **Examples**: Code examples and use cases
- **Tutorials**: Learning materials for new users

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots for UI elements
- Keep documentation up-to-date with code changes

## 🏷️ Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated
- [ ] CHANGELOG.md updated
- [ ] Release notes prepared
- [ ] Tag created

## 🤔 Questions?

If you have questions about contributing:

- **GitHub Discussions**: For general questions and discussions
- **GitHub Issues**: For specific bugs or feature requests
- **Email**: contributors@uta.ai

## 📄 License

By contributing to UTA, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to UTA! 🚀
