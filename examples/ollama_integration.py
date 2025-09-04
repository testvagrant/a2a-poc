"""
Ollama Integration Example for UTA

This example shows how to integrate Ollama (local LLM server) with the UTA system.
Ollama provides a simple API for running open-source language models locally.
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional

class OllamaAdapter:
    """
    Adapter for integrating Ollama with UTA.
    
    Ollama is a local LLM server that provides a simple API for running
    open-source language models like Llama2, Mistral, CodeLlama, etc.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        """
        Initialize Ollama adapter.
        
        Args:
            base_url: Ollama server URL (default: http://localhost:11434)
            model: Model name to use (default: llama2)
        """
        self.base_url = base_url
        self.model = model
        self.session = requests.Session()
    
    def health_check(self) -> bool:
        """Check if Ollama server is running."""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        try:
            response = self.session.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except requests.exceptions.RequestException:
            return []
    
    def send(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Send messages to Ollama and get response.
        
        Args:
            messages: List of conversation messages
            **kwargs: Additional parameters
            
        Returns:
            Response dictionary with text and metadata
        """
        # Convert messages to Ollama format
        prompt = self._format_messages(messages)
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 1000
            }
        }
        
        start_time = time.time()
        try:
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            response_time_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                text_content = data.get('response', 'No response received')
                
                return {
                    "text": text_content,
                    "structured": {
                        "model": self.model,
                        "response_time_ms": response_time_ms,
                        "tokens_generated": data.get('eval_count', 0),
                        "tokens_prompt": data.get('prompt_eval_count', 0)
                    },
                    "metadata": {
                        "status_code": response.status_code,
                        "response_time_ms": response_time_ms,
                        "model": self.model
                    }
                }
            else:
                return {
                    "text": f"Error: HTTP {response.status_code}",
                    "structured": {},
                    "metadata": {
                        "status_code": response.status_code,
                        "response_time_ms": response_time_ms,
                        "error": response.text
                    }
                }
                
        except requests.exceptions.RequestException as e:
            response_time_ms = (time.time() - start_time) * 1000
            return {
                "text": f"Error: {str(e)}",
                "structured": {},
                "metadata": {
                    "status_code": 500,
                    "response_time_ms": response_time_ms,
                    "error": str(e)
                }
            }
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Format messages for Ollama prompt."""
        formatted = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            
            if role == 'user':
                formatted.append(f"Human: {content}")
            elif role == 'assistant':
                formatted.append(f"Assistant: {content}")
        
        # Add final prompt for response
        formatted.append("Assistant:")
        return "\n\n".join(formatted)
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get model capabilities."""
        return {
            "model": self.model,
            "provider": "ollama",
            "type": "local_llm",
            "supports_streaming": True,
            "supports_tools": False,
            "max_tokens": 1000,
            "temperature_range": [0.0, 1.0]
        }

def test_ollama_integration():
    """Test Ollama integration with UTA."""
    print("Testing Ollama Integration...")
    
    # Initialize adapter
    adapter = OllamaAdapter()
    
    # Check health
    if not adapter.health_check():
        print("❌ Ollama server is not running!")
        print("Please start Ollama server with: ollama serve")
        print("And pull a model with: ollama pull llama2")
        return False
    
    print("✅ Ollama server is running")
    
    # Get available models
    models = adapter.get_available_models()
    print(f"📋 Available models: {models}")
    
    if not models:
        print("❌ No models available!")
        print("Please pull a model with: ollama pull llama2")
        return False
    
    # Test conversation
    messages = [
        {"role": "user", "content": "Hello! I need help with my account."}
    ]
    
    print("🔄 Testing conversation...")
    response = adapter.send(messages)
    
    print(f"📝 Response: {response['text']}")
    print(f"⏱️ Response time: {response['metadata']['response_time_ms']:.2f}ms")
    print(f"🔧 Model: {response['metadata']['model']}")
    
    # Test capabilities
    capabilities = adapter.get_capabilities()
    print(f"🎯 Capabilities: {capabilities}")
    
    print("✅ Ollama integration test completed!")
    return True

if __name__ == "__main__":
    test_ollama_integration()

