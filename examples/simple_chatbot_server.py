"""
Simple Chatbot Server using Ollama

This creates a simple HTTP API server that wraps Ollama's LLM capabilities
into a chatbot interface that UTA can test.
"""

from flask import Flask, request, jsonify
import requests
import time
import json
from typing import Dict, Any, List

app = Flask(__name__)

class OllamaChatbot:
    """Simple chatbot wrapper around Ollama."""
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama2"):
        self.ollama_url = ollama_url
        self.model = model
        self.conversation_history = []
    
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Process a chat message and return response.
        
        Args:
            message: User message
            
        Returns:
            Response dictionary
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Format conversation for Ollama
        prompt = self._format_conversation()
        
        # Call Ollama
        response = self._call_ollama(prompt)
        
        # Add assistant response to history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return {
            "text": response,
            "structured": {
                "model": self.model,
                "conversation_length": len(self.conversation_history)
            }
    }
    
    def _format_conversation(self) -> str:
        """Format conversation history for Ollama."""
        formatted = []
        for msg in self.conversation_history:
            role = msg["role"]
            content = msg["content"]
            if role == "user":
                formatted.append(f"Human: {content}")
            elif role == "assistant":
                formatted.append(f"Assistant: {content}")
        
        # Add prompt for response
        formatted.append("Assistant:")
        return "\n\n".join(formatted)
    
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
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []

# Initialize chatbot
chatbot = OllamaChatbot()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "model": chatbot.model})

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint that UTA can call.
    
    Expected JSON:
    {
        "conversation_history": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ],
        "metadata": {}
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Get conversation history
        conversation_history = data.get("conversation_history", [])
        
        # Get the last user message
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
        
        # Return response in UTA format
        return jsonify({
            "text": response["text"],
            "structured": response["structured"],
            "metadata": {
                "status_code": 200,
                "response_time_ms": response_time_ms,
                "model": chatbot.model
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history."""
    chatbot.reset_conversation()
    return jsonify({"status": "conversation reset"})

@app.route('/capabilities', methods=['GET'])
def get_capabilities():
    """Get chatbot capabilities."""
    return jsonify({
        "model": chatbot.model,
        "provider": "ollama",
        "type": "local_llm",
        "supports_streaming": False,
        "supports_tools": False,
        "max_tokens": 1000,
        "temperature_range": [0.0, 1.0]
    })

if __name__ == "__main__":
    print("🤖 Starting Simple Chatbot Server...")
    print(f"📋 Model: {chatbot.model}")
    print(f"🔗 Ollama URL: {chatbot.ollama_url}")
    print("🚀 Server will be available at: http://localhost:5000")
    print("📡 Endpoints:")
    print("   GET  /health - Health check")
    print("   POST /chat - Chat endpoint")
    print("   POST /reset - Reset conversation")
    print("   GET  /capabilities - Get capabilities")
    print("")
    print("🧪 Test with UTA:")
    print("   python3 -m runner.run --suite scenarios/core --report out_chatbot --http-url http://localhost:5000")
    print("")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

