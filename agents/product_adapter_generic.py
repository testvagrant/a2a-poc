import re
import json
from typing import List, Dict, Any
from pathlib import Path
import yaml

class GenericMockAgent:
    """
    A generic mock agent that can handle various types of scenarios.
    It simulates different types of AI agents (customer service, banking, etc.)
    """
    
    def __init__(self, fixtures_dir: str):
        self.fixtures_dir = Path(fixtures_dir)
        self._load_fixtures()
        
    def _load_fixtures(self):
        """Load fixtures and policies."""
        try:
            with open(self.fixtures_dir / "debtors.json", "r", encoding="utf-8") as f:
                self.debtors = json.load(f)
        except FileNotFoundError:
            self.debtors = {}
            
        try:
            with open(self.fixtures_dir / "policies.yaml", "r", encoding="utf-8") as f:
                self.policies = yaml.safe_load(f)
        except FileNotFoundError:
            self.policies = {"mandatory_disclosures": [], "forbidden_phrases": []}

    def send(self, conversation: List[Dict[str, str]], debtor_id: str = None) -> Dict[str, Any]:
        user_last = next((m for m in reversed(conversation) if m["role"] == "user"), {"content": ""})
        user_text = user_last["content"].lower()
        
        # Determine the type of request and respond accordingly
        if self._is_tool_request(user_text):
            return self._handle_tool_request(user_text)
        elif self._is_account_help_request(user_text):
            return self._handle_account_help(user_text)
        elif self._is_generic_greeting(user_text):
            return self._handle_generic_greeting(user_text)
        else:
            return self._handle_generic_request(user_text)
            
    def _is_account_help_request(self, text: str) -> bool:
        """Check if this is an account help request."""
        account_indicators = ["account", "balance", "transaction", "help"]
        return any(indicator in text for indicator in account_indicators)
        
    def _is_tool_request(self, text: str) -> bool:
        """Check if this is a tool/action request."""
        tool_indicators = ["create", "make", "schedule", "book", "pay", "transfer"]
        return any(indicator in text for indicator in tool_indicators)
        
    def _is_generic_greeting(self, text: str) -> bool:
        """Check if this is a generic greeting."""
        greeting_indicators = ["hello", "hi", "hey", "good morning", "good afternoon"]
        return any(indicator in text for indicator in greeting_indicators)
        
    def _handle_account_help(self, text: str) -> Dict[str, Any]:
        """Handle account-related requests."""
        if "balance" in text:
            return {
                "text": "Hello! I can help you with your account. Your current balance is $1,250.00. Is there anything specific you'd like to know?",
                "structured": {
                    "intent": "account_inquiry",
                    "outcome": "success",
                    "balance": 1250.00,
                    "actions": []
                }
            }
        else:
            return {
                "text": "Hello! I'm here to help with your account. What would you like to do today?",
                "structured": {
                    "intent": "account_help",
                    "outcome": "partial",
                    "actions": []
                }
            }
            
    def _handle_tool_request(self, text: str) -> Dict[str, Any]:
        """Handle tool/action requests."""
        if "create account" in text:
            return {
                "text": "I'd be happy to help you create a new account. I'll need some information from you. What type of account would you like?",
                "structured": {
                    "intent": "tool_execution",
                    "outcome": "pending_input",
                    "tool_name": "create_account",
                    "actions": [],
                    "tool_calls": [
                        {
                            "name": "create_account",
                            "args": {"status": "pending"},
                            "ok": True
                        }
                    ]
                }
            }
        elif "make payment" in text:
            return {
                "text": "I can help you make a payment. Please provide the payment amount and method you'd like to use.",
                "structured": {
                    "intent": "tool_execution",
                    "outcome": "pending_input",
                    "tool_name": "make_payment",
                    "actions": [],
                    "tool_calls": [
                        {
                            "name": "make_payment",
                            "args": {"status": "pending"},
                            "ok": True
                        }
                    ]
                }
            }
        else:
            return {
                "text": "I understand you want to perform an action. Let me help you with that. What specific details do you need to provide?",
                "structured": {
                    "intent": "tool_execution",
                    "outcome": "pending_input",
                    "actions": [],
                    "tool_calls": [
                        {
                            "name": "generic_action",
                            "args": {"status": "pending"},
                            "ok": True
                        }
                    ]
                }
            }
            
    def _handle_generic_greeting(self, text: str) -> Dict[str, Any]:
        """Handle generic greetings."""
        return {
            "text": "Hello! Welcome to our service. How can I assist you today?",
            "structured": {
                "intent": "greeting",
                "outcome": "success",
                "actions": []
            }
        }
        
    def _handle_generic_request(self, text: str) -> Dict[str, Any]:
        """Handle generic requests."""
        return {
            "text": "I understand you need assistance. Let me help you with that. Could you please provide more details about what you need?",
            "structured": {
                "intent": "general_help",
                "outcome": "partial",
                "actions": []
            }
        }
