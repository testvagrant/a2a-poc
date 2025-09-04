"""
LLM Judge for Advanced AI Agent Evaluation

This module provides LLM-based judging capabilities as an alternative
to heuristic judging. It uses language models to evaluate AI agent
responses for relevance, completeness, groundedness, and other metrics.
"""

import json
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class JudgeType(Enum):
    """Types of LLM judges available."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE = "azure"
    CUSTOM = "custom"

@dataclass
class LLMJudgeConfig:
    """Configuration for LLM judge."""
    judge_type: JudgeType
    model_name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.1
    max_tokens: int = 1000
    timeout: int = 30

@dataclass
class JudgeResult:
    """Result from LLM judge evaluation."""
    relevance: float
    completeness: float
    groundedness: float
    reasoning: str
    confidence: float
    judge_model: str
    evaluation_time_ms: float

class LLMJudge:
    """
    LLM-based judge for evaluating AI agent responses.
    
    This judge uses language models to provide sophisticated evaluation
    of AI agent responses, including relevance, completeness, and groundedness.
    """
    
    def __init__(self, config: LLMJudgeConfig):
        """
        Initialize LLM judge with configuration.
        
        Args:
            config: LLM judge configuration
        """
        self.config = config
        self._setup_client()
    
    def _setup_client(self):
        """Set up the appropriate LLM client based on configuration."""
        if self.config.judge_type == JudgeType.OPENAI:
            self._setup_openai_client()
        elif self.config.judge_type == JudgeType.ANTHROPIC:
            self._setup_anthropic_client()
        elif self.config.judge_type == JudgeType.AZURE:
            self._setup_azure_client()
        else:
            raise ValueError(f"Unsupported judge type: {self.config.judge_type}")
    
    def _setup_openai_client(self):
        """Set up OpenAI client."""
        try:
            import openai
            self.client = openai.OpenAI(
                api_key=self.config.api_key,
                base_url=self.config.base_url
            )
        except ImportError:
            raise ImportError("OpenAI library not installed. Install with: pip install openai")
    
    def _setup_anthropic_client(self):
        """Set up Anthropic client."""
        try:
            import anthropic
            self.client = anthropic.Anthropic(
                api_key=self.config.api_key,
                base_url=self.config.base_url
            )
        except ImportError:
            raise ImportError("Anthropic library not installed. Install with: pip install anthropic")
    
    def _setup_azure_client(self):
        """Set up Azure OpenAI client."""
        try:
            import openai
            self.client = openai.AzureOpenAI(
                api_key=self.config.api_key,
                azure_endpoint=self.config.base_url,
                api_version="2024-02-15-preview"
            )
        except ImportError:
            raise ImportError("OpenAI library not installed. Install with: pip install openai")
    
    def evaluate_response(self, scenario: Dict[str, Any], 
                         messages: List[Dict[str, str]], 
                         agent_structured: Dict[str, Any]) -> JudgeResult:
        """
        Evaluate AI agent response using LLM judge.
        
        Args:
            scenario: Scenario configuration
            messages: Conversation messages
            agent_structured: Structured response from agent
            
        Returns:
            JudgeResult with evaluation metrics
        """
        start_time = time.time()
        
        # Prepare evaluation prompt
        prompt = self._create_evaluation_prompt(scenario, messages, agent_structured)
        
        # Get LLM evaluation
        evaluation = self._get_llm_evaluation(prompt)
        
        # Parse evaluation result
        result = self._parse_evaluation_result(evaluation)
        
        evaluation_time = (time.time() - start_time) * 1000
        
        return JudgeResult(
            relevance=result.get('relevance', 0.0),
            completeness=result.get('completeness', 0.0),
            groundedness=result.get('groundedness', 0.0),
            reasoning=result.get('reasoning', ''),
            confidence=result.get('confidence', 0.0),
            judge_model=self.config.model_name,
            evaluation_time_ms=evaluation_time
        )
    
    def _create_evaluation_prompt(self, scenario: Dict[str, Any], 
                                 messages: List[Dict[str, str]], 
                                 agent_structured: Dict[str, Any]) -> str:
        """Create evaluation prompt for LLM judge."""
        
        # Extract key information
        user_goal = scenario.get('goal', {}).get('user_goal', '')
        scenario_title = scenario.get('title', '')
        tags = scenario.get('tags', [])
        
        # Get last assistant message
        last_assistant_msg = ""
        for msg in reversed(messages):
            if msg.get('role') == 'assistant':
                last_assistant_msg = msg.get('content', '')
                break
        
        # Create structured data summary
        structured_summary = json.dumps(agent_structured, indent=2) if agent_structured else "None"
        
        prompt = f"""
You are an expert AI agent evaluator. Please evaluate the following AI agent response based on the given scenario.

SCENARIO:
Title: {scenario_title}
User Goal: {user_goal}
Tags: {', '.join(tags)}

CONVERSATION:
{self._format_messages(messages)}

AGENT RESPONSE:
Text: {last_assistant_msg}
Structured Data: {structured_summary}

EVALUATION CRITERIA:
1. Relevance (0.0-1.0): How relevant is the response to the user's goal and context?
2. Completeness (0.0-1.0): How complete is the response in addressing the user's needs?
3. Groundedness (0.0-1.0): How well-grounded is the response in the provided context?
4. Confidence (0.0-1.0): How confident are you in this evaluation?

Please provide your evaluation in the following JSON format:
{{
    "relevance": 0.0-1.0,
    "completeness": 0.0-1.0,
    "groundedness": 0.0-1.0,
    "confidence": 0.0-1.0,
    "reasoning": "Brief explanation of your evaluation"
}}

Focus on:
- Whether the response addresses the user's actual goal
- If the response is appropriate for the scenario context
- Whether the response demonstrates understanding of the user's needs
- If the response is helpful and actionable
"""
        
        return prompt
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Format conversation messages for the prompt."""
        formatted = []
        for msg in messages:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            formatted.append(f"{role.upper()}: {content}")
        return "\n".join(formatted)
    
    def _get_llm_evaluation(self, prompt: str) -> str:
        """Get evaluation from LLM."""
        try:
            if self.config.judge_type == JudgeType.OPENAI:
                return self._get_openai_evaluation(prompt)
            elif self.config.judge_type == JudgeType.ANTHROPIC:
                return self._get_anthropic_evaluation(prompt)
            elif self.config.judge_type == JudgeType.AZURE:
                return self._get_azure_evaluation(prompt)
            else:
                raise ValueError(f"Unsupported judge type: {self.config.judge_type}")
        except Exception as e:
            # Fallback to default evaluation
            return self._get_fallback_evaluation(str(e))
    
    def _get_openai_evaluation(self, prompt: str) -> str:
        """Get evaluation from OpenAI using requests (same as HTTP adapter)."""
        import requests
        
        url = self.config.base_url.rstrip('/') + '/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {self.config.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': self.config.model_name,
            'messages': [{"role": "user", "content": prompt}],
            'temperature': self.config.temperature,
            'max_tokens': self.config.max_tokens
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=self.config.timeout)
        response.raise_for_status()
        
        data = response.json()
        return data['choices'][0]['message']['content']
    
    def _get_anthropic_evaluation(self, prompt: str) -> str:
        """Get evaluation from Anthropic."""
        response = self.client.messages.create(
            model=self.config.model_name,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def _get_azure_evaluation(self, prompt: str) -> str:
        """Get evaluation from Azure OpenAI."""
        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            timeout=self.config.timeout
        )
        return response.choices[0].message.content
    
    def _get_fallback_evaluation(self, error: str) -> str:
        """Get fallback evaluation when LLM fails."""
        # Extract error type for better reporting
        if "404" in error:
            error_type = "API endpoint not found - check model access and API key permissions"
        elif "401" in error:
            error_type = "Unauthorized - check API key validity"
        elif "429" in error:
            error_type = "Rate limit exceeded - try again later"
        elif "500" in error:
            error_type = "Server error - OpenAI service issue"
        else:
            error_type = "Unknown error - check network and API configuration"
        
        return json.dumps({
            "relevance": 0.5,
            "completeness": 0.5,
            "groundedness": 0.5,
            "confidence": 0.0,
            "reasoning": f"LLM evaluation failed: {error_type}. Using heuristic fallback evaluation."
        })
    
    def _parse_evaluation_result(self, evaluation: str) -> Dict[str, Any]:
        """Parse LLM evaluation result."""
        try:
            # Try to extract JSON from the response
            if "```json" in evaluation:
                json_start = evaluation.find("```json") + 7
                json_end = evaluation.find("```", json_start)
                json_str = evaluation[json_start:json_end].strip()
            elif "{" in evaluation and "}" in evaluation:
                json_start = evaluation.find("{")
                json_end = evaluation.rfind("}") + 1
                json_str = evaluation[json_start:json_end]
            else:
                json_str = evaluation
            
            result = json.loads(json_str)
            
            # Validate and normalize values
            for key in ['relevance', 'completeness', 'groundedness', 'confidence']:
                if key in result:
                    result[key] = max(0.0, min(1.0, float(result[key])))
                else:
                    result[key] = 0.5
            
            if 'reasoning' not in result:
                result['reasoning'] = 'No reasoning provided'
            
            return result
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Return default values if parsing fails
            return {
                'relevance': 0.5,
                'completeness': 0.5,
                'groundedness': 0.5,
                'confidence': 0.0,
                'reasoning': f'Failed to parse evaluation: {str(e)}'
            }

class LLMJudgeFactory:
    """Factory for creating LLM judges with different configurations."""
    
    @staticmethod
    def create_openai_judge(model_name: str = "gpt-3.5-turbo", 
                           api_key: Optional[str] = None) -> LLMJudge:
        """Create OpenAI-based judge."""
        config = LLMJudgeConfig(
            judge_type=JudgeType.OPENAI,
            model_name=model_name,
            api_key=api_key
        )
        return LLMJudge(config)
    
    @staticmethod
    def create_anthropic_judge(model_name: str = "claude-3-haiku-20240307",
                              api_key: Optional[str] = None) -> LLMJudge:
        """Create Anthropic-based judge."""
        config = LLMJudgeConfig(
            judge_type=JudgeType.ANTHROPIC,
            model_name=model_name,
            api_key=api_key
        )
        return LLMJudge(config)
    
    @staticmethod
    def create_azure_judge(model_name: str = "gpt-35-turbo",
                          api_key: Optional[str] = None,
                          base_url: Optional[str] = None) -> LLMJudge:
        """Create Azure OpenAI-based judge."""
        config = LLMJudgeConfig(
            judge_type=JudgeType.AZURE,
            model_name=model_name,
            api_key=api_key,
            base_url=base_url
        )
        return LLMJudge(config)

# Example usage and testing
if __name__ == "__main__":
    # Test LLM judge (requires API key)
    print("Testing LLM Judge...")
    
    # Example configuration (replace with your API key)
    config = LLMJudgeConfig(
        judge_type=JudgeType.OPENAI,
        model_name="gpt-3.5-turbo",
        api_key="your-api-key-here"
    )
    
    try:
        judge = LLMJudge(config)
        
        # Example scenario and messages
        scenario = {
            "title": "Test Scenario",
            "goal": {"user_goal": "Get help with account"},
            "tags": ["test"]
        }
        
        messages = [
            {"role": "user", "content": "Hello, I need help with my account."},
            {"role": "assistant", "content": "Hello! I'm here to help with your account. What would you like to do today?"}
        ]
        
        agent_structured = {
            "intent": "account_help",
            "outcome": "partial"
        }
        
        # Evaluate response
        result = judge.evaluate_response(scenario, messages, agent_structured)
        print(f"Evaluation result: {result}")
        
    except Exception as e:
        print(f"Error testing LLM judge: {e}")
    
    print("LLM Judge test completed!")
