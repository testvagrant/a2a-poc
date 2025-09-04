"""
Error Handling for UTA

This module provides comprehensive error handling and recovery mechanisms
for the Universal Tester-Agent system.
"""

import traceback
import sys
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging_config import get_logger

class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Error categories."""
    VALIDATION = "validation"
    NETWORK = "network"
    CONFIGURATION = "configuration"
    RUNTIME = "runtime"
    JUDGE = "judge"
    AGENT = "agent"
    BUDGET = "budget"
    UNKNOWN = "unknown"

@dataclass
class UTAError:
    """UTA-specific error information."""
    error_type: str
    message: str
    category: ErrorCategory
    severity: ErrorSeverity
    context: Dict[str, Any]
    timestamp: datetime
    traceback: Optional[str] = None
    recoverable: bool = True
    suggested_action: Optional[str] = None

class UTAErrorHandler:
    """
    Comprehensive error handler for UTA system.
    
    This class provides error handling, recovery, and reporting capabilities
    for the Universal Tester-Agent system.
    """
    
    def __init__(self):
        """Initialize error handler."""
        self.logger = get_logger("uta.error_handler")
        self.error_history: List[UTAError] = []
        self.recovery_strategies: Dict[str, Callable] = {}
        self._setup_default_recovery_strategies()
    
    def _setup_default_recovery_strategies(self):
        """Set up default recovery strategies."""
        self.recovery_strategies = {
            'network_error': self._recover_network_error,
            'validation_error': self._recover_validation_error,
            'configuration_error': self._recover_configuration_error,
            'budget_violation': self._recover_budget_violation,
            'judge_error': self._recover_judge_error,
            'agent_error': self._recover_agent_error
        }
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> UTAError:
        """
        Handle an error and attempt recovery.
        
        Args:
            error: The exception that occurred
            context: Additional context information
            
        Returns:
            UTAError object with error details
        """
        if context is None:
            context = {}
        
        # Analyze error
        uta_error = self._analyze_error(error, context)
        
        # Log error
        self._log_error(uta_error)
        
        # Add to history
        self.error_history.append(uta_error)
        
        # Attempt recovery
        if uta_error.recoverable:
            self._attempt_recovery(uta_error)
        
        return uta_error
    
    def _analyze_error(self, error: Exception, context: Dict[str, Any]) -> UTAError:
        """Analyze error and determine category, severity, and recovery options."""
        error_type = type(error).__name__
        message = str(error)
        
        # Determine category and severity
        category, severity = self._classify_error(error, context)
        
        # Determine if recoverable
        recoverable = self._is_recoverable(error, context)
        
        # Get suggested action
        suggested_action = self._get_suggested_action(error, context)
        
        # Get traceback
        traceback_str = traceback.format_exc() if sys.exc_info()[0] else None
        
        return UTAError(
            error_type=error_type,
            message=message,
            category=category,
            severity=severity,
            context=context,
            timestamp=datetime.now(),
            traceback=traceback_str,
            recoverable=recoverable,
            suggested_action=suggested_action
        )
    
    def _classify_error(self, error: Exception, context: Dict[str, Any]) -> tuple[ErrorCategory, ErrorSeverity]:
        """Classify error by category and severity."""
        error_type = type(error).__name__
        message = str(error).lower()
        
        # Network errors
        if any(keyword in error_type.lower() for keyword in ['connection', 'timeout', 'network', 'http']):
            return ErrorCategory.NETWORK, ErrorSeverity.MEDIUM
        
        # Validation errors
        if any(keyword in error_type.lower() for keyword in ['validation', 'value', 'type', 'schema']):
            return ErrorCategory.VALIDATION, ErrorSeverity.LOW
        
        # Configuration errors
        if any(keyword in error_type.lower() for keyword in ['config', 'setting', 'parameter']):
            return ErrorCategory.CONFIGURATION, ErrorSeverity.HIGH
        
        # Budget violations
        if 'budget' in message or 'violation' in message:
            return ErrorCategory.BUDGET, ErrorSeverity.MEDIUM
        
        # Judge errors
        if 'judge' in message or 'evaluation' in message:
            return ErrorCategory.JUDGE, ErrorSeverity.MEDIUM
        
        # Agent errors
        if 'agent' in message or 'response' in message:
            return ErrorCategory.AGENT, ErrorSeverity.MEDIUM
        
        # Runtime errors
        if any(keyword in error_type.lower() for keyword in ['runtime', 'attribute', 'key']):
            return ErrorCategory.RUNTIME, ErrorSeverity.HIGH
        
        # Default classification
        return ErrorCategory.UNKNOWN, ErrorSeverity.MEDIUM
    
    def _is_recoverable(self, error: Exception, context: Dict[str, Any]) -> bool:
        """Determine if error is recoverable."""
        error_type = type(error).__name__
        message = str(error).lower()
        
        # Non-recoverable errors
        if any(keyword in error_type.lower() for keyword in ['systemexit', 'keyboardinterrupt']):
            return False
        
        # Budget violations are not recoverable
        if 'budget' in message or 'violation' in message:
            return False
        
        # Configuration errors are usually not recoverable
        if any(keyword in error_type.lower() for keyword in ['config', 'setting']):
            return False
        
        # Most other errors are recoverable
        return True
    
    def _get_suggested_action(self, error: Exception, context: Dict[str, Any]) -> str:
        """Get suggested action for error recovery."""
        error_type = type(error).__name__
        message = str(error).lower()
        
        if 'connection' in message or 'timeout' in message:
            return "Retry request with exponential backoff"
        elif 'validation' in message:
            return "Check input data format and retry"
        elif 'config' in message:
            return "Verify configuration file and settings"
        elif 'budget' in message:
            return "Adjust budget constraints or optimize scenario"
        elif 'judge' in message:
            return "Fall back to heuristic judge or check LLM configuration"
        elif 'agent' in message:
            return "Retry with different agent or check agent configuration"
        else:
            return "Review error details and retry if appropriate"
    
    def _log_error(self, uta_error: UTAError):
        """Log error with appropriate level."""
        log_message = f"{uta_error.error_type}: {uta_error.message}"
        
        if uta_error.severity == ErrorSeverity.CRITICAL:
            self.logger.critical(log_message, **uta_error.context)
        elif uta_error.severity == ErrorSeverity.HIGH:
            self.logger.error(log_message, **uta_error.context)
        elif uta_error.severity == ErrorSeverity.MEDIUM:
            self.logger.warning(log_message, **uta_error.context)
        else:
            self.logger.info(log_message, **uta_error.context)
        
        # Log traceback for high severity errors
        if uta_error.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL] and uta_error.traceback:
            self.logger.error(f"Traceback: {uta_error.traceback}")
    
    def _attempt_recovery(self, uta_error: UTAError):
        """Attempt to recover from error."""
        recovery_func = self.recovery_strategies.get(uta_error.error_type.lower())
        if recovery_func:
            try:
                recovery_func(uta_error)
                self.logger.info(f"Recovery attempted for {uta_error.error_type}")
            except Exception as recovery_error:
                self.logger.error(f"Recovery failed: {recovery_error}")
    
    def _recover_network_error(self, uta_error: UTAError):
        """Recovery strategy for network errors."""
        # Implement network error recovery (retry, fallback, etc.)
        pass
    
    def _recover_validation_error(self, uta_error: UTAError):
        """Recovery strategy for validation errors."""
        # Implement validation error recovery (default values, format correction, etc.)
        pass
    
    def _recover_configuration_error(self, uta_error: UTAError):
        """Recovery strategy for configuration errors."""
        # Implement configuration error recovery (default configs, etc.)
        pass
    
    def _recover_budget_violation(self, uta_error: UTAError):
        """Recovery strategy for budget violations."""
        # Budget violations are not recoverable, but we can log them
        self.logger.warning("Budget violation detected - stopping scenario execution")
    
    def _recover_judge_error(self, uta_error: UTAError):
        """Recovery strategy for judge errors."""
        # Implement judge error recovery (fallback to heuristic, etc.)
        pass
    
    def _recover_agent_error(self, uta_error: UTAError):
        """Recovery strategy for agent errors."""
        # Implement agent error recovery (retry, fallback agent, etc.)
        pass
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of all errors encountered."""
        if not self.error_history:
            return {"total_errors": 0}
        
        # Count errors by category and severity
        category_counts = {}
        severity_counts = {}
        
        for error in self.error_history:
            category_counts[error.category.value] = category_counts.get(error.category.value, 0) + 1
            severity_counts[error.severity.value] = severity_counts.get(error.severity.value, 0) + 1
        
        return {
            "total_errors": len(self.error_history),
            "category_counts": category_counts,
            "severity_counts": severity_counts,
            "recoverable_errors": sum(1 for e in self.error_history if e.recoverable),
            "unrecoverable_errors": sum(1 for e in self.error_history if not e.recoverable),
            "latest_error": self.error_history[-1].__dict__ if self.error_history else None
        }
    
    def clear_history(self):
        """Clear error history."""
        self.error_history.clear()
        self.logger.info("Error history cleared")

# Global error handler instance
_global_error_handler: Optional[UTAErrorHandler] = None

def get_error_handler() -> UTAErrorHandler:
    """
    Get global error handler instance.
    
    Returns:
        UTA error handler instance
    """
    global _global_error_handler
    if _global_error_handler is None:
        _global_error_handler = UTAErrorHandler()
    return _global_error_handler

def handle_error(error: Exception, context: Dict[str, Any] = None) -> UTAError:
    """
    Handle error using global error handler.
    
    Args:
        error: The exception that occurred
        context: Additional context information
        
    Returns:
        UTAError object with error details
    """
    return get_error_handler().handle_error(error, context)

# Example usage and testing
if __name__ == "__main__":
    print("Testing UTA Error Handler...")
    
    error_handler = get_error_handler()
    
    # Test different error types
    try:
        raise ConnectionError("Failed to connect to API")
    except Exception as e:
        error_handler.handle_error(e, {"url": "https://api.example.com"})
    
    try:
        raise ValueError("Invalid input format")
    except Exception as e:
        error_handler.handle_error(e, {"input": "test"})
    
    try:
        raise RuntimeError("Unexpected runtime error")
    except Exception as e:
        error_handler.handle_error(e, {"context": "test"})
    
    # Get error summary
    summary = error_handler.get_error_summary()
    print(f"Error summary: {summary}")
    
    print("UTA Error Handler test completed!")
