"""
Environment Configuration Loader for UTA

This module loads configuration from environment variables and .env files
for the Universal Tester-Agent system.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

@dataclass
class OpenAIConfig:
    """OpenAI configuration."""
    api_key: str
    model: str = "gpt-3.5-turbo"
    base_url: str = "https://api.openai.com/v1/chat/completions"
    temperature: float = 0.7
    max_tokens: int = 1000

@dataclass
class LLMJudgeConfig:
    """LLM Judge configuration."""
    api_key: str
    model: str = "gpt-4"
    judge_type: str = "openai"
    temperature: float = 0.1
    max_tokens: int = 1000
    base_url: Optional[str] = None

@dataclass
class AnthropicConfig:
    """Anthropic configuration."""
    api_key: str
    model: str = "claude-3-haiku-20240307"
    base_url: str = "https://api.anthropic.com"

@dataclass
class AzureOpenAIConfig:
    """Azure OpenAI configuration."""
    api_key: str
    endpoint: str
    model: str = "gpt-35-turbo"
    api_version: str = "2024-02-15-preview"

@dataclass
class UTAConfig:
    """UTA system configuration."""
    log_level: str = "INFO"
    report_dir: str = "reports"
    seed: Optional[int] = None
    http_timeout: int = 60
    http_retries: int = 3
    http_backoff_factor: float = 0.5

class ConfigLoader:
    """Configuration loader for UTA system."""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration loader.
        
        Args:
            env_file: Path to .env file (optional)
        """
        self.env_file = env_file or ".env"
        self._load_environment()
    
    def _load_environment(self):
        """Load environment variables from .env file if available."""
        if DOTENV_AVAILABLE and os.path.exists(self.env_file):
            load_dotenv(self.env_file)
            print(f"✅ Loaded environment from {self.env_file}")
        elif os.path.exists(self.env_file):
            print(f"⚠️ .env file found but python-dotenv not installed. Install with: pip install python-dotenv")
        else:
            print(f"ℹ️ No .env file found, using system environment variables")
    
    def get_openai_config(self) -> OpenAIConfig:
        """Get OpenAI configuration."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        return OpenAIConfig(
            api_key=api_key,
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1/chat/completions"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        )
    
    def get_llm_judge_config(self) -> LLMJudgeConfig:
        """Get LLM Judge configuration."""
        api_key = os.getenv("LLM_JUDGE_API_KEY")
        if not api_key:
            raise ValueError("LLM_JUDGE_API_KEY not found in environment variables")
        
        # For LLM judge, use the base URL without the endpoint path
        base_url = os.getenv("LLM_JUDGE_BASE_URL")
        if not base_url:
            # Default to OpenAI base URL without endpoint
            base_url = "https://api.openai.com"
        
        return LLMJudgeConfig(
            api_key=api_key,
            model=os.getenv("LLM_JUDGE_MODEL", "gpt-4"),
            judge_type=os.getenv("LLM_JUDGE_TYPE", "openai"),
            temperature=float(os.getenv("LLM_JUDGE_TEMPERATURE", "0.1")),
            max_tokens=int(os.getenv("LLM_JUDGE_MAX_TOKENS", "1000")),
            base_url=base_url
        )
    
    def get_anthropic_config(self) -> Optional[AnthropicConfig]:
        """Get Anthropic configuration if available."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return None
        
        return AnthropicConfig(
            api_key=api_key,
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307"),
            base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
        )
    
    def get_azure_openai_config(self) -> Optional[AzureOpenAIConfig]:
        """Get Azure OpenAI configuration if available."""
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        
        if not api_key or not endpoint:
            return None
        
        return AzureOpenAIConfig(
            api_key=api_key,
            endpoint=endpoint,
            model=os.getenv("AZURE_OPENAI_MODEL", "gpt-35-turbo"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        )
    
    def get_uta_config(self) -> UTAConfig:
        """Get UTA system configuration."""
        return UTAConfig(
            log_level=os.getenv("UTA_LOG_LEVEL", "INFO"),
            report_dir=os.getenv("UTA_REPORT_DIR", "reports"),
            seed=int(os.getenv("UTA_SEED")) if os.getenv("UTA_SEED") else None,
            http_timeout=int(os.getenv("HTTP_TIMEOUT", "60")),
            http_retries=int(os.getenv("HTTP_RETRIES", "3")),
            http_backoff_factor=float(os.getenv("HTTP_BACKOFF_FACTOR", "0.5"))
        )
    
    def get_all_configs(self) -> Dict[str, Any]:
        """Get all available configurations."""
        configs = {
            "uta": self.get_uta_config()
        }
        
        try:
            configs["openai"] = self.get_openai_config()
        except ValueError:
            pass
        
        try:
            configs["llm_judge"] = self.get_llm_judge_config()
        except ValueError:
            pass
        
        anthropic_config = self.get_anthropic_config()
        if anthropic_config:
            configs["anthropic"] = anthropic_config
        
        azure_config = self.get_azure_openai_config()
        if azure_config:
            configs["azure_openai"] = azure_config
        
        return configs
    
    def validate_config(self) -> Dict[str, bool]:
        """Validate that required configurations are available."""
        validation = {}
        
        try:
            self.get_openai_config()
            validation["openai"] = True
        except ValueError:
            validation["openai"] = False
        
        try:
            self.get_llm_judge_config()
            validation["llm_judge"] = True
        except ValueError:
            validation["llm_judge"] = False
        
        validation["anthropic"] = self.get_anthropic_config() is not None
        validation["azure_openai"] = self.get_azure_openai_config() is not None
        
        return validation

# Global configuration loader instance
_config_loader: Optional[ConfigLoader] = None

def get_config_loader(env_file: Optional[str] = None) -> ConfigLoader:
    """
    Get global configuration loader instance.
    
    Args:
        env_file: Path to .env file (optional)
        
    Returns:
        Configuration loader instance
    """
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader(env_file)
    return _config_loader

def get_openai_config() -> OpenAIConfig:
    """Get OpenAI configuration."""
    return get_config_loader().get_openai_config()

def get_llm_judge_config() -> LLMJudgeConfig:
    """Get LLM Judge configuration."""
    return get_config_loader().get_llm_judge_config()

def get_uta_config() -> UTAConfig:
    """Get UTA system configuration."""
    return get_config_loader().get_uta_config()

# Example usage and testing
if __name__ == "__main__":
    print("Testing Configuration Loader...")
    
    # Initialize config loader
    config_loader = ConfigLoader()
    
    # Validate configurations
    validation = config_loader.validate_config()
    print(f"Configuration validation: {validation}")
    
    # Get available configs
    configs = config_loader.get_all_configs()
    print(f"Available configurations: {list(configs.keys())}")
    
    # Test specific configs
    try:
        openai_config = config_loader.get_openai_config()
        print(f"✅ OpenAI config loaded: {openai_config.model}")
    except ValueError as e:
        print(f"❌ OpenAI config error: {e}")
    
    try:
        llm_judge_config = config_loader.get_llm_judge_config()
        print(f"✅ LLM Judge config loaded: {llm_judge_config.model}")
    except ValueError as e:
        print(f"❌ LLM Judge config error: {e}")
    
    uta_config = config_loader.get_uta_config()
    print(f"✅ UTA config loaded: {uta_config.log_level}")
    
    print("Configuration loader test completed!")

