"""
Collections Chatbot Server using Ollama

This creates a collections-specific chatbot that UTA can test.
It demonstrates how to build a domain-specific chatbot for testing.
"""

from flask import Flask, request, jsonify
import requests
import time
import json
from typing import Dict, Any

app = Flask(__name__)

class CollectionsChatbot:
    """Collections-specific chatbot using Ollama."""
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama2"):
        self.ollama_url = ollama_url
        self.model = model
        self.conversation_history = []
        self.account_info = {
            "debtor_id": "D-1001",
            "balance": 1500.00,
            "last_payment": "2024-01-15",
            "status": "active",
            "account_type": "credit_card"
        }
    
    def chat(self, message: str) -> dict:
        """Process collections-related messages."""
        # Add collections context to the prompt
        context = f"""
You are a professional collections agent helping with debt collection. 
You are helpful, respectful, but firm about payment obligations.

Account Information:
- Debtor ID: {self.account_info['debtor_id']}
- Current Balance: ${self.account_info['balance']:.2f}
- Last Payment: {self.account_info['last_payment']}
- Account Status: {self.account_info['status']}
- Account Type: {self.account_info['account_type']}

User Message: {message}

Respond as a professional collections agent. Be helpful but firm about payment obligations.
If the user mentions payment, ask for specific details like amount and date.
If they mention disputes, ask for more information.
If they mention hardship, offer payment plan options.
"""
        
        # Call Ollama with context
        response = self._call_ollama(context)
        
        # Parse response for structured data
        structured = self._extract_structured_data(response, message)
        
        return {
            "text": response,
            "structured": structured
        }
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "max_tokens": 1000
            }
        }
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "No response received")
            else:
                return f"Error: HTTP {response.status_code}"
                
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
    
    def _extract_structured_data(self, response: str, user_message: str) -> dict:
        """Extract structured data from response."""
        structured = {
            "intent": "unknown",
            "outcome": "partial"
        }
        
        # Simple intent detection based on user message
        user_msg_lower = user_message.lower()
        
        if "payment" in user_msg_lower or "pay" in user_msg_lower:
            structured["intent"] = "payment"
            if "promise" in user_msg_lower or "will pay" in user_msg_lower:
                structured["intent"] = "promise_to_pay"
                structured["promise_to_pay"] = {
                    "date": "2024-02-15",
                    "amount": 500.00
                }
        elif "dispute" in user_msg_lower:
            structured["intent"] = "dispute"
        elif "hardship" in user_msg_lower or "can't pay" in user_msg_lower:
            structured["intent"] = "hardship"
        elif "wrong person" in user_msg_lower or "not me" in user_msg_lower:
            structured["intent"] = "wrong_person"
        elif "cease" in user_msg_lower or "stop calling" in user_msg_lower:
            structured["intent"] = "cease_contact"
        elif "balance" in user_msg_lower or "how much" in user_msg_lower:
            structured["intent"] = "balance_inquiry"
        elif "settlement" in user_msg_lower or "offer" in user_msg_lower:
            structured["intent"] = "settlement"
        elif "legal" in user_msg_lower or "lawyer" in user_msg_lower:
            structured["intent"] = "legal_threat"
        elif "verification" in user_msg_lower or "prove" in user_msg_lower:
            structured["intent"] = "verification"
        elif "payment method" in user_msg_lower or "card" in user_msg_lower:
            structured["intent"] = "payment_method"
        elif "contact" in user_msg_lower or "preference" in user_msg_lower:
            structured["intent"] = "contact_preferences"
        else:
            structured["intent"] = "general_inquiry"
        
        # Determine outcome based on intent
        if structured["intent"] in ["promise_to_pay", "payment", "settlement"]:
            structured["outcome"] = "success"
        elif structured["intent"] in ["dispute", "wrong_person", "legal_threat"]:
            structured["outcome"] = "escalated"
        else:
            structured["outcome"] = "partial"
        
        return structured

# Initialize chatbot
chatbot = CollectionsChatbot()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy", 
        "model": chatbot.model,
        "domain": "collections",
        "account_info": chatbot.account_info
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for UTA."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        conversation_history = data.get("conversation_history", [])
        
        # Get last user message
        last_user_message = ""
        for msg in reversed(conversation_history):
            if msg.get("role") == "user":
                last_user_message = msg.get("content", "")
                break
        
        if not last_user_message:
            return jsonify({"error": "No user message found"}), 400
        
        # Process message
        start_time = time.time()
        response = chatbot.chat(last_user_message)
        response_time_ms = (time.time() - start_time) * 1000
        
        return jsonify({
            "text": response["text"],
            "structured": response["structured"],
            "metadata": {
                "status_code": 200,
                "response_time_ms": response_time_ms,
                "model": chatbot.model,
                "domain": "collections"
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history."""
    chatbot.conversation_history = []
    return jsonify({"status": "conversation reset"})

@app.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Get chatbot capabilities."""
    return jsonify({
        "model": chatbot.model,
        "provider": "ollama",
        "type": "collections_chatbot",
        "domain": "collections",
        "supports_streaming": False,
        "supports_tools": False,
        "max_tokens": 1000,
        "temperature_range": [0.0, 1.0],
        "account_info": chatbot.account_info
    })

if __name__ == "__main__":
    print("🏦 Starting Collections Chatbot Server...")
    print(f"📋 Model: {chatbot.model}")
    print(f"🔗 Ollama URL: {chatbot.ollama_url}")
    print(f"💳 Account: {chatbot.account_info['debtor_id']} (${chatbot.account_info['balance']:.2f})")
    print("🚀 Server will be available at: http://localhost:5001")
    print("📡 Endpoints:")
    print("   GET  /health - Health check")
    print("   POST /chat - Chat endpoint")
    print("   POST /reset - Reset conversation")
    print("   GET  /capabilities - Get capabilities")
    print("")
    print("🧪 Test with UTA:")
    print("   python3 -m runner.run --suite scenarios/collections --report out_collections_chatbot --http-url http://localhost:5001")
    print("")
    
    app.run(host='0.0.0.0', port=5001, debug=True)

