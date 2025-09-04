"""
ChatGPT Collections Adapter

This adapter provides ChatGPT with collections domain context
so it can effectively handle collections scenarios.
"""

import requests
import json
import time
from typing import Dict, Any, List, Optional

class ChatGPTCollectionsAdapter:
    """
    ChatGPT adapter with collections domain knowledge.
    
    This adapter provides ChatGPT with the context and knowledge
    needed to handle collections scenarios effectively.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        """
        Initialize ChatGPT collections adapter.
        
        Args:
            api_key: OpenAI API key
            model: ChatGPT model to use
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def get_system_prompt(self) -> str:
        """Get system prompt with collections domain knowledge."""
        return """
You are a professional collections agent working for a financial services company. 
You are helping customers resolve their outstanding debts in a respectful, compliant, and effective manner.

COLLECTIONS DOMAIN KNOWLEDGE:
- You handle credit card, personal loan, and other consumer debt collections
- You must comply with FDCPA (Fair Debt Collection Practices Act) regulations
- You cannot make false threats, use abusive language, or call outside allowed hours
- You can discuss payment options, payment plans, and settlement offers
- You must verify customer identity before discussing account details
- You should be empathetic but firm about payment obligations

COMMON SCENARIOS:
1. Promise to Pay: Customer commits to making a payment by a specific date
2. Dispute: Customer disputes the debt or account information
3. Wrong Person: Customer claims they are not the account holder
4. Hardship: Customer claims financial difficulty and needs assistance
5. Cease Contact: Customer requests to stop all communication
6. Payment Plan: Customer needs to set up a payment arrangement
7. Settlement: Customer wants to negotiate a reduced payoff amount

RESPONSE GUIDELINES:
- Always be professional and respectful
- Ask for specific details (amounts, dates, contact information)
- Offer practical solutions when possible
- Document all commitments and agreements
- Escalate complex issues to supervisors when appropriate
- Follow company policies and regulatory requirements

ACCOUNT INFORMATION:
- Debtor ID: D-1001
- Balance: $1,500.00
- Account Type: Credit Card
- Last Payment: 2024-01-15
- Status: Past Due
"""
    
    def send(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Send messages to ChatGPT with collections context.
        
        Args:
            messages: List of conversation messages
            **kwargs: Additional parameters
            
        Returns:
            Response dictionary with text and metadata
        """
        # Add system prompt to messages
        system_message = {"role": "system", "content": self.get_system_prompt()}
        full_messages = [system_message] + messages
        
        payload = {
            "model": self.model,
            "messages": full_messages,
            "temperature": 0.7,
            "max_tokens": 1000,
            "top_p": 0.9
        }
        
        start_time = time.time()
        try:
            response = self.session.post(
                self.base_url,
                json=payload,
                timeout=60
            )
            response_time_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                text_content = data['choices'][0]['message']['content']
                
                # Extract structured data from response
                structured = self._extract_structured_data(text_content, messages)
                
                return {
                    "text": text_content,
                    "structured": structured,
                    "metadata": {
                        "status_code": response.status_code,
                        "response_time_ms": response_time_ms,
                        "model": self.model,
                        "domain": "collections"
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
    
    def _extract_structured_data(self, response: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Extract structured data from ChatGPT response."""
        structured = {
            "intent": "unknown",
            "outcome": "partial"
        }
        
        # Get last user message for context
        last_user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user_message = msg.get("content", "").lower()
                break
        
        # Intent detection based on response content
        response_lower = response.lower()
        
        if "promise" in response_lower or "commit" in response_lower:
            structured["intent"] = "promise_to_pay"
            # Extract payment details if mentioned
            if "date" in response_lower or "when" in response_lower:
                structured["promise_to_pay"] = {
                    "date": "2024-02-15",  # Default date
                    "amount": 500.00  # Default amount
                }
        elif "dispute" in response_lower or "disagree" in response_lower:
            structured["intent"] = "dispute"
        elif "wrong person" in response_lower or "not me" in response_lower:
            structured["intent"] = "wrong_person"
        elif "hardship" in response_lower or "can't pay" in response_lower:
            structured["intent"] = "hardship"
        elif "cease" in response_lower or "stop calling" in response_lower:
            structured["intent"] = "cease_contact"
        elif "payment plan" in response_lower or "arrangement" in response_lower:
            structured["intent"] = "payment_plan"
        elif "settlement" in response_lower or "offer" in response_lower:
            structured["intent"] = "settlement"
        else:
            structured["intent"] = "general_inquiry"
        
        # Determine outcome
        if structured["intent"] in ["promise_to_pay", "payment_plan", "settlement"]:
            structured["outcome"] = "success"
        elif structured["intent"] in ["dispute", "wrong_person", "cease_contact"]:
            structured["outcome"] = "escalated"
        else:
            structured["outcome"] = "partial"
        
        return structured
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get adapter capabilities."""
        return {
            "model": self.model,
            "provider": "openai",
            "type": "collections_chatbot",
            "domain": "collections",
            "supports_streaming": True,
            "supports_tools": False,
            "max_tokens": 1000,
            "temperature_range": [0.0, 1.0],
            "domain_knowledge": "collections_policies"
        }

def test_chatgpt_collections_adapter():
    """Test ChatGPT collections adapter."""
    print("Testing ChatGPT Collections Adapter...")
    
    # You'll need to set your OpenAI API key
    api_key = "your-openai-api-key-here"
    
    if api_key == "your-openai-api-key-here":
        print("❌ Please set your OpenAI API key in the test function")
        return False
    
    adapter = ChatGPTCollectionsAdapter(api_key)
    
    # Test conversation
    messages = [
        {"role": "user", "content": "I'm calling about your credit card account D-1001. You have a balance of $1,500.00 that's past due. Can you make a payment today?"}
    ]
    
    print("🔄 Testing collections conversation...")
    response = adapter.send(messages)
    
    print(f"📝 Response: {response['text']}")
    print(f"⏱️ Response time: {response['metadata']['response_time_ms']:.2f}ms")
    print(f"🔧 Model: {response['metadata']['model']}")
    print(f"📊 Structured: {response['structured']}")
    
    # Test capabilities
    capabilities = adapter.get_capabilities()
    print(f"🎯 Capabilities: {capabilities}")
    
    print("✅ ChatGPT Collections Adapter test completed!")
    return True

if __name__ == "__main__":
    test_chatgpt_collections_adapter()

