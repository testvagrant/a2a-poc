"""
HTTP Adapter for Real Product Integration

This adapter allows the UTA to test real AI agents via HTTP API calls.
It implements the same interface as mock agents but communicates with actual services.
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class HTTPAdapterConfig:
    """Configuration for HTTP adapter."""
    base_url: str
    api_key: Optional[str] = None
    model: Optional[str] = None
    timeout: int = 30
    headers: Optional[Dict[str, str]] = None
    retry_attempts: int = 3
    retry_delay: float = 1.0

class HTTPAdapter:
    """
    HTTP adapter for communicating with real AI agents.
    
    This adapter sends HTTP requests to actual AI agent services and
    formats responses to match the expected interface.
    """
    
    def __init__(self, config: HTTPAdapterConfig):
        """
        Initialize HTTP adapter with configuration.
        
        Args:
            config: HTTP adapter configuration
        """
        self.config = config
        self.session = requests.Session()
        
        # Set up headers
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'UTA-HTTP-Adapter/1.0'
        }
        
        if config.api_key:
            headers['Authorization'] = f'Bearer {config.api_key}'
            
        if config.headers:
            headers.update(config.headers)
            
        self.session.headers.update(headers)
    
    def send(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Send messages to the AI agent via HTTP.
        
        Args:
            messages: List of conversation messages
            **kwargs: Additional parameters (debtor_id, etc.)
            
        Returns:
            Response dictionary with 'text' and 'structured' fields
        """
        # Prepare request payload
        payload = self._prepare_payload(messages, kwargs)
        
        # Make HTTP request with retries
        response = self._make_request_with_retries(payload)
        
        # Parse and format response
        return self._parse_response(response)
    
    def _prepare_payload(self, messages: List[Dict[str, str]], kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the HTTP request payload for OpenAI API."""
        # Convert UTA messages to OpenAI format
        openai_messages = []
        for msg in messages:
            if isinstance(msg, dict):
                # Handle UTA message format
                role = msg.get('role', 'user')
                content = msg.get('content', msg.get('text', ''))
                openai_messages.append({
                    'role': role,
                    'content': content
                })
            else:
                # Handle string messages
                openai_messages.append({
                    'role': 'user',
                    'content': str(msg)
                })
        
        # Prepare OpenAI API payload
        payload = {
            'model': self.config.model or 'gpt-3.5-turbo',
            'messages': openai_messages,
            'temperature': 0.7,
            'max_tokens': 1000
        }
        
        # Add any additional parameters
        if 'temperature' in kwargs:
            payload['temperature'] = kwargs['temperature']
        if 'max_tokens' in kwargs:
            payload['max_tokens'] = kwargs['max_tokens']
            
        return payload
    
    def _make_request_with_retries(self, payload: Dict[str, Any]) -> requests.Response:
        """Make HTTP request with retry logic."""
        last_exception = None
        
        for attempt in range(self.config.retry_attempts):
            try:
                # Construct the full URL with endpoint
                url = self.config.base_url
                if not url.endswith('/v1/chat/completions'):
                    url = url.rstrip('/') + '/v1/chat/completions'
                
                response = self.session.post(
                    url,
                    json=payload,
                    timeout=self.config.timeout
                )
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                last_exception = e
                if attempt < self.config.retry_attempts - 1:
                    time.sleep(self.config.retry_delay * (2 ** attempt))  # Exponential backoff
                    
        # If all retries failed, raise the last exception
        raise last_exception
    
    def _parse_response(self, response: requests.Response) -> Dict[str, Any]:
        """Parse HTTP response and format for UTA."""
        try:
            data = response.json()
        except json.JSONDecodeError:
            # If response is not JSON, treat as plain text
            return {
                'text': response.text,
                'structured': {},
                'metadata': {
                    'status_code': response.status_code,
                    'response_time_ms': response.elapsed.total_seconds() * 1000,
                    'headers': dict(response.headers)
                }
            }
        
        # Handle OpenAI API response format
        if 'choices' in data and len(data['choices']) > 0:
            choice = data['choices'][0]
            message = choice.get('message', {})
            text = message.get('content', 'No response received')
            
            # Extract any structured data from the response
            structured = {}
            
            # Try to parse JSON from the response if it contains structured data
            try:
                # Look for JSON-like content in the response
                import re
                json_match = re.search(r'\{.*\}', text, re.DOTALL)
                if json_match:
                    structured = json.loads(json_match.group())
            except (json.JSONDecodeError, AttributeError):
                pass
            
            return {
                'text': text,
                'structured': structured,
                'metadata': {
                    'status_code': response.status_code,
                    'response_time_ms': response.elapsed.total_seconds() * 1000,
                    'headers': dict(response.headers),
                    'openai_usage': data.get('usage', {}),
                    'openai_model': data.get('model', '')
                }
            }
        
        # Fallback for other response formats
        text = data.get('text', data.get('message', 'No response received'))
        structured = data.get('structured', data.get('data', {}))
        
        # Ensure structured data is a dictionary
        if not isinstance(structured, dict):
            structured = {}
        
        return {
            'text': text,
            'structured': structured,
            'metadata': {
                'status_code': response.status_code,
                'response_time_ms': response.elapsed.total_seconds() * 1000,
                'headers': dict(response.headers)
            }
        }
    
    def health_check(self) -> bool:
        """
        Check if the HTTP service is healthy.
        
        Returns:
            True if service is healthy, False otherwise
        """
        try:
            # Try to make a simple request to check health
            response = self.session.get(
                f"{self.config.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def get_capabilities(self) -> Dict[str, Any]:
        """
        Get capabilities of the connected AI agent.
        
        Returns:
            Dictionary of agent capabilities
        """
        try:
            response = self.session.get(
                f"{self.config.base_url}/capabilities",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except:
            # Return default capabilities if endpoint not available
            return {
                'supports_structured_data': True,
                'supports_context': True,
                'max_message_length': 4000,
                'supported_languages': ['en-US'],
                'capabilities': ['chat', 'collections', 'payment_processing']
            }

class HTTPAdapterFactory:
    """Factory for creating HTTP adapters with different configurations."""
    
    @staticmethod
    def create_collections_adapter(base_url: str, api_key: Optional[str] = None, 
                                 model: Optional[str] = None) -> HTTPAdapter:
        """Create HTTP adapter for collections domain."""
        config = HTTPAdapterConfig(
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout=30,
            headers={
                'X-Domain': 'collections',
                'X-Version': '1.0'
            }
        )
        return HTTPAdapter(config)
    
    @staticmethod
    def create_generic_adapter(base_url: str, api_key: Optional[str] = None, 
                             model: Optional[str] = None) -> HTTPAdapter:
        """Create HTTP adapter for generic AI agent."""
        config = HTTPAdapterConfig(
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout=30,
            headers={
                'X-Domain': 'generic',
                'X-Version': '1.0'
            }
        )
        return HTTPAdapter(config)
    
    @staticmethod
    def create_custom_adapter(base_url: str, api_key: Optional[str] = None, 
                            model: Optional[str] = None,
                            custom_headers: Optional[Dict[str, str]] = None) -> HTTPAdapter:
        """Create HTTP adapter with custom configuration."""
        config = HTTPAdapterConfig(
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout=30,
            headers=custom_headers or {}
        )
        return HTTPAdapter(config)

# Example usage and testing
if __name__ == "__main__":
    # Example configuration
    config = HTTPAdapterConfig(
        base_url="https://api.example.com/chat",
        api_key="your-api-key-here",
        timeout=30
    )
    
    adapter = HTTPAdapter(config)
    
    # Test health check
    if adapter.health_check():
        print("Service is healthy")
    else:
        print("Service is not responding")
    
    # Test capabilities
    capabilities = adapter.get_capabilities()
    print(f"Agent capabilities: {capabilities}")
    
    # Test message sending
    messages = [
        {'role': 'user', 'content': 'Hello, I need help with my account.'}
    ]
    
    try:
        response = adapter.send(messages, debtor_id='D-1001')
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
