"""
Logging Configuration for UTA

This module provides comprehensive logging configuration for the Universal Tester-Agent.
It supports different log levels, file output, and structured logging for production use.
"""

import logging
import logging.handlers
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

class UTAFormatter(logging.Formatter):
    """Custom formatter for UTA logs with structured output."""
    
    def __init__(self, include_timestamp=True, include_level=True, include_module=True):
        """
        Initialize UTA formatter.
        
        Args:
            include_timestamp: Whether to include timestamp in log format
            include_level: Whether to include log level in log format
            include_module: Whether to include module name in log format
        """
        self.include_timestamp = include_timestamp
        self.include_level = include_level
        self.include_module = include_module
        
        # Build format string
        parts = []
        if include_timestamp:
            parts.append("%(asctime)s")
        if include_level:
            parts.append("[%(levelname)s]")
        if include_module:
            parts.append("%(name)s:")
        parts.append("%(message)s")
        
        super().__init__(fmt=" ".join(parts), datefmt="%Y-%m-%d %H:%M:%S")
    
    def format(self, record):
        """Format log record with additional context."""
        # Add session context if available
        if hasattr(record, 'session_id'):
            record.msg = f"[{record.session_id}] {record.msg}"
        if hasattr(record, 'scenario_id'):
            record.msg = f"[{record.scenario_id}] {record.msg}"
        
        return super().format(record)

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record):
        """Format log record as JSON."""
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add additional context
        if hasattr(record, 'session_id'):
            log_entry['session_id'] = record.session_id
        if hasattr(record, 'scenario_id'):
            log_entry['scenario_id'] = record.scenario_id
        if hasattr(record, 'judge_mode'):
            log_entry['judge_mode'] = record.judge_mode
        if hasattr(record, 'strategy'):
            log_entry['strategy'] = record.strategy
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)

class UTALogger:
    """UTA-specific logger with enhanced functionality."""
    
    def __init__(self, name: str = "uta"):
        """
        Initialize UTA logger.
        
        Args:
            name: Logger name
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up log handlers."""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = UTAFormatter(include_timestamp=True, include_level=True, include_module=False)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "uta.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = UTAFormatter(include_timestamp=True, include_level=True, include_module=True)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # JSON file handler for structured logs
        json_handler = logging.handlers.RotatingFileHandler(
            log_dir / "uta_structured.json",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        json_handler.setLevel(logging.DEBUG)
        json_formatter = JSONFormatter()
        json_handler.setFormatter(json_formatter)
        self.logger.addHandler(json_handler)
    
    def set_level(self, level: str):
        """Set logging level."""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        self.logger.setLevel(level_map.get(level.upper(), logging.INFO))
    
    def debug(self, message: str, **kwargs):
        """Log debug message with context."""
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message with context."""
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message with context."""
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message with context."""
        self._log(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message with context."""
        self._log(logging.CRITICAL, message, **kwargs)
    
    def _log(self, level: int, message: str, **kwargs):
        """Log message with additional context."""
        # Create log record with extra context
        extra = {}
        for key, value in kwargs.items():
            extra[key] = value
        
        self.logger.log(level, message, extra=extra)
    
    def log_scenario_start(self, scenario_id: str, title: str, strategy: str, judge_mode: str):
        """Log scenario start with context."""
        self.info(f"Starting scenario: {title}", 
                 scenario_id=scenario_id, strategy=strategy, judge_mode=judge_mode)
    
    def log_scenario_end(self, scenario_id: str, title: str, passed: bool, duration_ms: float):
        """Log scenario end with results."""
        status = "PASSED" if passed else "FAILED"
        self.info(f"Scenario completed: {title} - {status} ({duration_ms:.2f}ms)",
                 scenario_id=scenario_id)
    
    def log_budget_violation(self, scenario_id: str, violations: list):
        """Log budget violations."""
        self.warning(f"Budget violations: {', '.join(violations)}", 
                    scenario_id=scenario_id)
    
    def log_judge_evaluation(self, scenario_id: str, judge_mode: str, metrics: Dict[str, float]):
        """Log judge evaluation results."""
        metrics_str = ", ".join([f"{k}: {v:.3f}" for k, v in metrics.items()])
        self.info(f"Judge evaluation ({judge_mode}): {metrics_str}", 
                 scenario_id=scenario_id, judge_mode=judge_mode)
    
    def log_http_request(self, url: str, method: str, status_code: int, duration_ms: float):
        """Log HTTP request details."""
        self.info(f"HTTP {method} {url} - {status_code} ({duration_ms:.2f}ms)")
    
    def log_llm_evaluation(self, scenario_id: str, model: str, duration_ms: float, confidence: float):
        """Log LLM evaluation details."""
        self.info(f"LLM evaluation ({model}): {duration_ms:.2f}ms, confidence: {confidence:.3f}",
                 scenario_id=scenario_id)

# Global logger instance
_global_logger: Optional[UTALogger] = None

def get_logger(name: str = "uta") -> UTALogger:
    """
    Get global logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        UTA logger instance
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = UTALogger(name)
    return _global_logger

def setup_logging(level: str = "INFO", log_dir: Optional[str] = None):
    """
    Set up global logging configuration.
    
    Args:
        level: Logging level
        log_dir: Log directory (optional)
    """
    logger = get_logger()
    logger.set_level(level)
    
    if log_dir:
        # Update log directory if specified
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
        
        # Update file handlers
        for handler in logger.logger.handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                handler.baseFilename = str(log_path / handler.baseFilename.split('/')[-1])

# Example usage and testing
if __name__ == "__main__":
    print("Testing UTA Logging...")
    
    # Set up logging
    setup_logging(level="DEBUG")
    logger = get_logger()
    
    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Test contextual logging
    logger.log_scenario_start("TEST_001", "Test Scenario", "FlowIntent", "heuristic")
    logger.log_judge_evaluation("TEST_001", "heuristic", {"relevance": 0.8, "completeness": 0.7})
    logger.log_scenario_end("TEST_001", "Test Scenario", True, 150.5)
    
    # Test HTTP logging
    logger.log_http_request("https://api.example.com/chat", "POST", 200, 250.3)
    
    # Test LLM logging
    logger.log_llm_evaluation("TEST_001", "gpt-3.5-turbo", 1200.5, 0.85)
    
    print("UTA Logging test completed!")
