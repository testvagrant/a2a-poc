"""
HuggingChat Integration Example for UTA

This example shows how to integrate HuggingChat (open-source chatbot) with the UTA system.
HuggingChat is powered by Llama2 and provides a free alternative to commercial chatbots.
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional

class HuggingChatAdapter:
    """
    Adapter for integrating HuggingChat with UTA.
    
    HuggingChat is an open-source chatbot powered by Llama2 model,
    providing a free alternative to commercial chatbots.
    """
    
    def __init__(self, base_url: str = "https://huggingface.co/chat"):
        """
        Initialize HuggingChat adapter.
        
        Args:
            base_url: HuggingChat base URL
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def health_check(self) -> bool:
        """Check if HuggingChat is accessible."""
        try:
            response = self.session.get(self.base_url, timeout=10)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def send(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Send messages to HuggingChat and get response.
        
        Args:
            messages: List of conversation messages
            **kwargs: Additional parameters
            
        Returns:
            Response dictionary with text and metadata
        """
        # Convert messages to HuggingChat format
        conversation = self._format_messages(messages)
        
        payload = {
            "inputs": conversation,
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 1000,
                "top_p": 0.9,
                "repetition_penalty": 1.1
            },
            "options": {
                "use_cache": False,
                "wait_for_model": True
            }
        }
        
        start_time = time.time()
        try:
            # Note: This is a simplified example. In practice, you might need
            # to handle authentication, rate limiting, and different endpoints
            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=60
            )
            response_time_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                text_content = data.get('generated_text', 'No response received')
                
                return {
                    "text": text_content,
                    "structured": {
                        "model": "llama2",
                        "response_time_ms": response_time_ms,
                        "provider": "huggingface"
                    },
                    "metadata": {
                        "status_code": response.status_code,
                        "response_time_ms": response_time_ms,
                        "model": "llama2"
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
        """Format messages for HuggingChat."""
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
            "model": "llama2",
            "provider": "huggingface",
            "type": "open_source_llm",
            "supports_streaming": False,
            "supports_tools": False,
            "max_tokens": 1000,
            "temperature_range": [0.0, 1.0],
            "cost": "free"
        }

def test_huggingchat_integration():
    """Test HuggingChat integration with UTA."""
    print("Testing HuggingChat Integration...")
    
    # Initialize adapter
    adapter = HuggingChatAdapter()
    
    # Check health
    if not adapter.health_check():
        print("❌ HuggingChat is not accessible!")
        print("Please check your internet connection and try again.")
        return False
    
    print("✅ HuggingChat is accessible")
    
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
    
    print("✅ HuggingChat integration test completed!")
    return True

if __name__ == "__main__":
    test_huggingchat_integration()

