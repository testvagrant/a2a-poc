# Real Agent Testing Guide for UTA

## Overview

This guide shows how to test the Universal Tester-Agent (UTA) with real chatbot agents instead of mock agents. We'll cover several open-source and public chatbot options that can be integrated with our UTA system.

## 🤖 Available Real Chatbot Agents

### 1. **Ollama (Recommended - Local & Free)**

**What**: Local LLM server that runs open-source models on your machine
**Models**: Llama2, Mistral, CodeLlama, Phi, and many others
**Cost**: Completely free
**Setup**: Easy local installation

#### Installation & Setup

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama server
ollama serve

# Pull a model (in another terminal)
ollama pull llama2
# or
ollama pull mistral
# or
ollama pull codellama
```

#### Testing with UTA

```bash
# Test with Ollama
python3 -m runner.run --suite scenarios/core --report out_ollama --http-url http://localhost:11434/api/generate --http-config examples/ollama_config.yaml
```

### 2. **HuggingChat (Public API)**

**What**: Open-source chatbot powered by Llama2
**Cost**: Free with rate limits
**Setup**: Simple HTTP integration

#### Testing with UTA

```bash
# Test with HuggingChat
python3 -m runner.run --suite scenarios/core --report out_huggingchat --http-url https://huggingface.co/chat/api --http-config examples/huggingchat_config.yaml
```

### 3. **Rasa (Custom Bot)**

**What**: Open-source conversational AI framework
**Cost**: Free
**Setup**: Requires custom bot deployment

#### Installation & Setup

```bash
# Install Rasa
pip install rasa

# Create new Rasa project
rasa init --no-prompt

# Start Rasa server
rasa run --enable-api --cors "*"
```

## 🔧 Configuration Files

### Ollama Configuration

Create `examples/ollama_config.yaml`:

```yaml
base_url: "http://localhost:11434"
model: "llama2"
timeout: 60
headers:
  Content-Type: "application/json"
parameters:
  temperature: 0.7
  max_tokens: 1000
  top_p: 0.9
```

### HuggingChat Configuration

Create `examples/huggingchat_config.yaml`:

```yaml
base_url: "https://huggingface.co/chat"
timeout: 60
headers:
  User-Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  Accept: "application/json"
  Content-Type: "application/json"
parameters:
  temperature: 0.7
  max_new_tokens: 1000
  top_p: 0.9
```

## 🚀 Testing Commands

### Basic Testing

```bash
# Test core scenarios with Ollama
python3 -m runner.run --suite scenarios/core --report out_ollama --http-url http://localhost:11434/api/generate

# Test collections scenarios with Ollama
python3 -m runner.run --suite scenarios/collections --report out_collections_ollama --http-url http://localhost:11434/api/generate

# Test with specific seed for reproducibility
python3 -m runner.run --suite scenarios/core --report out_ollama_seeded --http-url http://localhost:11434/api/generate --seed 42
```

### Advanced Testing

```bash
# Test with LLM judge
python3 -m runner.run --suite scenarios/core --report out_ollama_llm_judge --http-url http://localhost:11434/api/generate --judge-mode llm --llm-api-key YOUR_API_KEY

# Test with hybrid judge
python3 -m runner.run --suite scenarios/core --report out_ollama_hybrid --http-url http://localhost:11434/api/generate --judge-mode hybrid --llm-api-key YOUR_API_KEY

# Test with budget enforcement
python3 -m runner.run --suite scenarios/core --report out_ollama_budget --http-url http://localhost:11434/api/generate --tags core
```

## 📊 Expected Results

### Performance Comparison

| Agent Type | Response Time | Cost | Quality | Setup Complexity |
|------------|---------------|------|---------|------------------|
| **Mock Agents** | ~1ms | Free | Basic | None |
| **Ollama (Local)** | ~500-2000ms | Free | High | Easy |
| **HuggingChat** | ~1000-3000ms | Free | High | Easy |
| **Rasa (Custom)** | ~100-500ms | Free | Medium | Medium |

### Success Rates

- **Mock Agents**: 100% (designed to pass)
- **Real Agents**: 60-80% (realistic performance)
- **Ollama**: 70-85% (good quality)
- **HuggingChat**: 65-80% (decent quality)

## 🔍 Troubleshooting

### Common Issues

#### Ollama Not Responding
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve

# Check available models
ollama list
```

#### HuggingChat Rate Limits
- Wait between requests
- Use different endpoints
- Consider local alternatives

#### Rasa Server Issues
```bash
# Check Rasa status
rasa run --enable-api --cors "*" --debug

# Test Rasa endpoint
curl -X POST http://localhost:5005/webhooks/rest/webhook -H "Content-Type: application/json" -d '{"message": "Hello"}'
```

### Debug Mode

Enable debug logging for troubleshooting:

```bash
export UTA_LOG_LEVEL=DEBUG
python3 -m runner.run --suite scenarios/core --report out_debug --http-url http://localhost:11434/api/generate
```

## 📈 Performance Optimization

### For Ollama

```bash
# Use faster models
ollama pull phi  # Smaller, faster model
ollama pull mistral  # Good balance

# Optimize parameters
# In config: temperature: 0.3, max_tokens: 500
```

### For HuggingChat

```yaml
# In config file
parameters:
  temperature: 0.3  # Lower for faster responses
  max_new_tokens: 500  # Shorter responses
  top_p: 0.8  # More focused responses
```

## 🎯 Best Practices

### 1. Start Simple
- Begin with core scenarios
- Use mock agents for development
- Test with real agents for validation

### 2. Use Deterministic Seeds
- Always use `--seed` for reproducible results
- Compare results across different agents
- Track performance over time

### 3. Monitor Performance
- Check response times
- Monitor success rates
- Track budget compliance

### 4. Iterate and Improve
- Adjust scenarios based on real agent behavior
- Optimize parameters for better performance
- Update assertions based on real responses

## 🔄 Integration Examples

### Custom HTTP Adapter

Create a custom adapter for your specific chatbot:

```python
# examples/custom_adapter.py
import requests
from typing import Dict, Any, List

class CustomChatbotAdapter:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'
    
    def send(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        # Convert messages to your chatbot's format
        payload = self._format_messages(messages)
        
        response = self.session.post(f"{self.base_url}/chat", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "text": data.get('response', ''),
                "structured": data.get('structured', {}),
                "metadata": {
                    "status_code": response.status_code,
                    "response_time_ms": data.get('response_time_ms', 0)
                }
            }
        else:
            return {
                "text": f"Error: {response.status_code}",
                "structured": {},
                "metadata": {
                    "status_code": response.status_code,
                    "error": response.text
                }
            }
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        # Implement your chatbot's message format
        return {"messages": messages}
```

### Testing Custom Adapter

```bash
# Test with custom adapter
python3 -m runner.run --suite scenarios/core --report out_custom --http-url https://your-chatbot.com/api --http-api-key YOUR_KEY
```

## 📚 Additional Resources

### Documentation
- [Ollama Documentation](https://ollama.ai/docs)
- [HuggingChat API](https://huggingface.co/chat)
- [Rasa Documentation](https://rasa.com/docs)

### Community
- [Ollama GitHub](https://github.com/ollama/ollama)
- [HuggingFace Community](https://huggingface.co/community)
- [Rasa Community](https://forum.rasa.com)

### Models
- [Ollama Model Library](https://ollama.ai/library)
- [HuggingFace Model Hub](https://huggingface.co/models)
- [Rasa Model Training](https://rasa.com/docs/rasa/training-data-format)

## 🎉 Conclusion

Testing with real chatbot agents provides valuable insights into actual AI agent performance. Start with Ollama for local testing, then expand to other options based on your needs. The UTA system is designed to work seamlessly with any HTTP-compatible chatbot API.

Remember to:
- Use deterministic seeds for reproducible results
- Monitor performance and adjust parameters
- Iterate on scenarios based on real agent behavior
- Document your findings for future reference

Happy testing! 🚀

