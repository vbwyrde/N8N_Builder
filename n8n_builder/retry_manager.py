"""
Enhanced Retry Management System for N8N Builder
Provides intelligent retry strategies, circuit breaker patterns, and fallback mechanisms for LLM API failures.

Task 1.1.6: Add retry logic for LLM API failures
"""

import asyncio
import logging
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import httpx
from functools import wraps
import random

logger = logging.getLogger(__name__)
retry_logger = logging.getLogger('n8n_builder.retry')

class RetryStrategy(Enum):
    """Different retry strategies for different types of failures."""
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR_BACKOFF = "linear_backoff"
    FIXED_DELAY = "fixed_delay"
    IMMEDIATE = "immediate"
    RANDOM_JITTER = "random_jitter"

class CircuitBreakerState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class FailureType(Enum):
    """Types of failures for different retry strategies."""
    TIMEOUT = "timeout"
    HTTP_ERROR = "http_error"
    VALIDATION_ERROR = "validation_error"
    CONNECTION_ERROR = "connection_error"
    RATE_LIMIT = "rate_limit"
    SERVER_ERROR = "server_error"
    CLIENT_ERROR = "client_error"
    UNKNOWN = "unknown"

@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    jitter: bool = True
    timeout_multiplier: float = 1.5
    
    # Circuit breaker settings
    failure_threshold: int = 5
    recovery_timeout: int = 60
    success_threshold: int = 2
    
    # Specific retry strategies per failure type
    failure_configs: Dict[FailureType, 'RetryConfig'] = field(default_factory=dict)

@dataclass
class RetryAttempt:
    """Record of a single retry attempt."""
    attempt_number: int
    timestamp: datetime
    duration: float
    error_type: str
    error_message: str
    success: bool = False
    response_length: Optional[int] = None

@dataclass
class RetryMetrics:
    """Comprehensive retry metrics for analysis."""
    operation_id: str
    operation_type: str
    total_attempts: int = 0
    successful_attempts: int = 0
    failed_attempts: int = 0
    total_retry_time: float = 0.0
    final_success: bool = False
    final_error: Optional[str] = None
    
    # Detailed attempt tracking
    attempts: List[RetryAttempt] = field(default_factory=list)
    
    # Failure type breakdown
    timeout_failures: int = 0
    http_error_failures: int = 0
    validation_failures: int = 0
    connection_failures: int = 0
    rate_limit_failures: int = 0
    server_error_failures: int = 0
    client_error_failures: int = 0
    unknown_failures: int = 0
    
    # Circuit breaker interactions
    circuit_breaker_triggered: bool = False
    fallback_used: bool = False
    fallback_type: Optional[str] = None
    
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    def finish(self, success: bool, final_error: Optional[str] = None):
        """Mark retry sequence as finished."""
        self.end_time = datetime.now()
        self.final_success = success
        self.final_error = final_error
        
        if self.start_time and self.end_time:
            self.total_retry_time = (self.end_time - self.start_time).total_seconds()
    
    def add_attempt(self, attempt: RetryAttempt):
        """Add a retry attempt to tracking."""
        self.attempts.append(attempt)
        self.total_attempts += 1
        
        if attempt.success:
            self.successful_attempts += 1
        else:
            self.failed_attempts += 1
            
            # Track failure types
            if "timeout" in attempt.error_type.lower():
                self.timeout_failures += 1
            elif "http" in attempt.error_type.lower():
                if "5" in attempt.error_message:  # 5xx errors
                    self.server_error_failures += 1
                elif "4" in attempt.error_message:  # 4xx errors
                    if "429" in attempt.error_message:  # Rate limiting
                        self.rate_limit_failures += 1
                    else:
                        self.client_error_failures += 1
                else:
                    self.http_error_failures += 1
            elif "validation" in attempt.error_type.lower():
                self.validation_failures += 1
            elif "connection" in attempt.error_type.lower():
                self.connection_failures += 1
            else:
                self.unknown_failures += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for logging."""
        return {
            'operation_id': self.operation_id,
            'operation_type': self.operation_type,
            'total_attempts': self.total_attempts,
            'successful_attempts': self.successful_attempts,
            'failed_attempts': self.failed_attempts,
            'total_retry_time': self.total_retry_time,
            'final_success': self.final_success,
            'final_error': self.final_error,
            'timeout_failures': self.timeout_failures,
            'http_error_failures': self.http_error_failures,
            'validation_failures': self.validation_failures,
            'connection_failures': self.connection_failures,
            'rate_limit_failures': self.rate_limit_failures,
            'server_error_failures': self.server_error_failures,
            'client_error_failures': self.client_error_failures,
            'unknown_failures': self.unknown_failures,
            'circuit_breaker_triggered': self.circuit_breaker_triggered,
            'fallback_used': self.fallback_used,
            'fallback_type': self.fallback_type,
            'attempts_detail': [
                {
                    'attempt_number': a.attempt_number,
                    'timestamp': a.timestamp.isoformat(),
                    'duration': a.duration,
                    'error_type': a.error_type,
                    'error_message': a.error_message,
                    'success': a.success,
                    'response_length': a.response_length
                }
                for a in self.attempts
            ]
        }

class CircuitBreaker:
    """Circuit breaker implementation for LLM API failures."""
    
    def __init__(self, 
                 failure_threshold: int = 5,
                 recovery_timeout: int = 60,
                 success_threshold: int = 2):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state_change_time = datetime.now()
        
    def can_attempt(self) -> bool:
        """Check if we can attempt the operation."""
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            # Check if we should transition to half-open
            if (datetime.now() - self.last_failure_time).total_seconds() > self.recovery_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                self.state_change_time = datetime.now()
                retry_logger.info(f"Circuit breaker transitioning to HALF_OPEN for recovery test")
                return True
            return False
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return True
        
        return False
    
    def record_success(self):
        """Record a successful operation."""
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                self.state_change_time = datetime.now()
                retry_logger.info(f"Circuit breaker CLOSED - service recovered")
        elif self.state == CircuitBreakerState.CLOSED:
            # Reset failure count on success
            self.failure_count = 0
    
    def record_failure(self):
        """Record a failed operation."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.state == CircuitBreakerState.CLOSED:
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN
                self.state_change_time = datetime.now()
                retry_logger.warning(f"Circuit breaker OPEN - too many failures ({self.failure_count})")
        elif self.state == CircuitBreakerState.HALF_OPEN:
            # Failed during recovery test, go back to open
            self.state = CircuitBreakerState.OPEN
            self.success_count = 0
            self.state_change_time = datetime.now()
            retry_logger.warning(f"Circuit breaker back to OPEN - recovery test failed")
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get current circuit breaker state information."""
        return {
            'state': self.state.value,
            'failure_count': self.failure_count,
            'success_count': self.success_count,
            'time_in_current_state': (datetime.now() - self.state_change_time).total_seconds(),
            'last_failure_time': self.last_failure_time.isoformat() if self.last_failure_time else None
        }

class RetryManager:
    """Advanced retry manager with circuit breaker and fallback strategies."""
    
    def __init__(self):
        # Default retry configurations
        self.default_config = RetryConfig()
        self.endpoint_configs: Dict[str, RetryConfig] = {}
        
        # Circuit breakers per endpoint
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        
        # Retry metrics tracking
        self.retry_metrics: List[RetryMetrics] = []
        
        # Fallback strategies
        self.fallback_strategies: Dict[str, Callable] = {}
        
        # Alternative endpoints for failover
        self.alternative_endpoints: List[str] = []
        
        retry_logger.info("Retry Manager initialized with advanced failure handling")
    
    def register_fallback_strategy(self, strategy_name: str, strategy_func: Callable):
        """Register a fallback strategy function."""
        self.fallback_strategies[strategy_name] = strategy_func
        retry_logger.info(f"Registered fallback strategy: {strategy_name}")
    
    def add_alternative_endpoint(self, endpoint: str):
        """Add an alternative endpoint for failover."""
        self.alternative_endpoints.append(endpoint)
        retry_logger.info(f"Added alternative endpoint: {endpoint}")
    
    def configure_endpoint(self, endpoint: str, config: RetryConfig):
        """Configure retry behavior for a specific endpoint."""
        self.endpoint_configs[endpoint] = config
        retry_logger.info(f"Configured retry behavior for endpoint: {endpoint}")
    
    def _get_config(self, endpoint: str) -> RetryConfig:
        """Get retry configuration for an endpoint."""
        return self.endpoint_configs.get(endpoint, self.default_config)
    
    def _get_circuit_breaker(self, endpoint: str) -> CircuitBreaker:
        """Get or create circuit breaker for an endpoint."""
        if endpoint not in self.circuit_breakers:
            config = self._get_config(endpoint)
            self.circuit_breakers[endpoint] = CircuitBreaker(
                failure_threshold=config.failure_threshold,
                recovery_timeout=config.recovery_timeout,
                success_threshold=config.success_threshold
            )
        return self.circuit_breakers[endpoint]
    
    def _classify_error(self, error: Exception) -> FailureType:
        """Classify the type of error for appropriate retry strategy."""
        if isinstance(error, httpx.TimeoutException):
            return FailureType.TIMEOUT
        elif isinstance(error, httpx.HTTPStatusError):
            if error.response.status_code == 429:
                return FailureType.RATE_LIMIT
            elif 500 <= error.response.status_code < 600:
                return FailureType.SERVER_ERROR
            elif 400 <= error.response.status_code < 500:
                return FailureType.CLIENT_ERROR
            else:
                return FailureType.HTTP_ERROR
        elif isinstance(error, httpx.ConnectError):
            return FailureType.CONNECTION_ERROR
        elif isinstance(error, ValueError) and "validation" in str(error).lower():
            return FailureType.VALIDATION_ERROR
        else:
            return FailureType.UNKNOWN
    
    def _calculate_delay(self, attempt: int, config: RetryConfig, failure_type: FailureType) -> float:
        """Calculate delay before next retry attempt."""
        # Use specific config for failure type if available
        if failure_type in config.failure_configs:
            config = config.failure_configs[failure_type]
        
        if config.strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
            delay = min(config.base_delay * (2 ** (attempt - 1)), config.max_delay)
        elif config.strategy == RetryStrategy.LINEAR_BACKOFF:
            delay = min(config.base_delay * attempt, config.max_delay)
        elif config.strategy == RetryStrategy.FIXED_DELAY:
            delay = config.base_delay
        elif config.strategy == RetryStrategy.IMMEDIATE:
            delay = 0
        elif config.strategy == RetryStrategy.RANDOM_JITTER:
            base_delay = min(config.base_delay * (2 ** (attempt - 1)), config.max_delay)
            delay = base_delay + random.uniform(0, base_delay * 0.1)  # Add 10% jitter
        else:
            delay = config.base_delay
        
        # Add jitter if enabled
        if config.jitter and config.strategy != RetryStrategy.RANDOM_JITTER:
            jitter = random.uniform(0, delay * 0.1)  # 10% jitter
            delay += jitter
        
        return delay
    
    async def execute_with_retry(self,
                                operation: Callable,
                                operation_id: str,
                                operation_type: str,
                                endpoint: str,
                                *args,
                                **kwargs) -> Tuple[Any, RetryMetrics]:
        """Execute an operation with intelligent retry logic."""
        config = self._get_config(endpoint)
        circuit_breaker = self._get_circuit_breaker(endpoint)
        
        metrics = RetryMetrics(
            operation_id=operation_id,
            operation_type=operation_type
        )
        
        retry_logger.info(f"Starting retry operation [ID: {operation_id}]", extra={
            'operation_id': operation_id,
            'operation_type': operation_type,
            'endpoint': endpoint,
            'max_attempts': config.max_attempts
        })
        
        last_error = None
        
        for attempt in range(1, config.max_attempts + 1):
            # Check circuit breaker
            if not circuit_breaker.can_attempt():
                metrics.circuit_breaker_triggered = True
                retry_logger.warning(f"Circuit breaker OPEN, attempting fallback [ID: {operation_id}]")
                
                # Try fallback strategies
                fallback_result = await self._try_fallback_strategies(operation_id, *args, **kwargs)
                if fallback_result is not None:
                    result, fallback_type = fallback_result
                    metrics.fallback_used = True
                    metrics.fallback_type = fallback_type
                    metrics.finish(success=True)
                    retry_logger.info(f"Fallback successful [ID: {operation_id}]: {fallback_type}")
                    return result, metrics
                
                # No fallback worked
                break
            
            attempt_start = time.time()
            
            try:
                retry_logger.info(f"Attempt {attempt}/{config.max_attempts} [ID: {operation_id}]")
                
                # Execute the operation
                result = await operation(*args, **kwargs)
                
                attempt_duration = time.time() - attempt_start
                
                # Success!
                attempt_record = RetryAttempt(
                    attempt_number=attempt,
                    timestamp=datetime.now(),
                    duration=attempt_duration,
                    error_type="none",
                    error_message="success",
                    success=True,
                    response_length=len(str(result)) if result else 0
                )
                
                metrics.add_attempt(attempt_record)
                circuit_breaker.record_success()
                metrics.finish(success=True)
                
                retry_logger.info(f"Operation successful on attempt {attempt} [ID: {operation_id}]", extra={
                    'operation_id': operation_id,
                    'attempt': attempt,
                    'duration': attempt_duration,
                    'total_retry_time': metrics.total_retry_time
                })
                
                return result, metrics
                
            except Exception as e:
                attempt_duration = time.time() - attempt_start
                last_error = e
                failure_type = self._classify_error(e)
                
                attempt_record = RetryAttempt(
                    attempt_number=attempt,
                    timestamp=datetime.now(),
                    duration=attempt_duration,
                    error_type=type(e).__name__,
                    error_message=str(e),
                    success=False
                )
                
                metrics.add_attempt(attempt_record)
                circuit_breaker.record_failure()
                
                retry_logger.exception(f"Attempt {attempt} failed [ID: {operation_id}]", extra={
                    'operation_id': operation_id,
                    'attempt': attempt,
                    'error_type': type(e).__name__,
                    'error_message': str(e)[:200],
                    'failure_type': failure_type.value,
                    'duration': attempt_duration
                })
                
                # Check if we should retry
                if attempt < config.max_attempts:
                    delay = self._calculate_delay(attempt, config, failure_type)
                    
                    retry_logger.info(f"Waiting {delay:.2f}s before retry [ID: {operation_id}]")
                    await asyncio.sleep(delay)
                else:
                    retry_logger.error(f"All retry attempts exhausted [ID: {operation_id}]")
        
        # All retries failed, try fallback strategies
        retry_logger.warning(f"All retries failed, attempting fallback [ID: {operation_id}]")
        fallback_result = await self._try_fallback_strategies(operation_id, *args, **kwargs)
        if fallback_result is not None:
            result, fallback_type = fallback_result
            metrics.fallback_used = True
            metrics.fallback_type = fallback_type
            metrics.finish(success=True)
            retry_logger.info(f"Fallback successful after retry failure [ID: {operation_id}]: {fallback_type}")
            return result, metrics
        
        # Complete failure
        metrics.finish(success=False, final_error=str(last_error))
        self.retry_metrics.append(metrics)
        
        retry_logger.error(f"Operation completely failed [ID: {operation_id}]", extra={
            'operation_id': operation_id,
            'total_attempts': metrics.total_attempts,
            'final_error': str(last_error),
            'total_retry_time': metrics.total_retry_time
        })
        
        raise last_error
    
    async def _try_fallback_strategies(self, operation_id: str, *args, **kwargs) -> Optional[Tuple[Any, str]]:
        """Try all available fallback strategies."""
        for strategy_name, strategy_func in self.fallback_strategies.items():
            try:
                retry_logger.info(f"Trying fallback strategy: {strategy_name} [ID: {operation_id}]")
                result = await strategy_func(*args, **kwargs)
                if result is not None:
                    return result, strategy_name
            except Exception as e:
                retry_logger.exception(f"Fallback strategy {strategy_name} failed [ID: {operation_id}]", extra={
                    'operation_id': operation_id,
                    'strategy_name': strategy_name,
                    'error_type': type(e).__name__,
                    'error_message': str(e)[:200]
                })
                continue
        
        return None
    
    def get_retry_statistics(self) -> Dict[str, Any]:
        """Get comprehensive retry statistics."""
        if not self.retry_metrics:
            return {"message": "No retry operations recorded"}
        
        total_operations = len(self.retry_metrics)
        successful_operations = sum(1 for m in self.retry_metrics if m.final_success)
        
        total_attempts = sum(m.total_attempts for m in self.retry_metrics)
        total_retry_time = sum(m.total_retry_time for m in self.retry_metrics)
        
        # Failure type breakdown
        failure_breakdown = {
            'timeout_failures': sum(m.timeout_failures for m in self.retry_metrics),
            'http_error_failures': sum(m.http_error_failures for m in self.retry_metrics),
            'validation_failures': sum(m.validation_failures for m in self.retry_metrics),
            'connection_failures': sum(m.connection_failures for m in self.retry_metrics),
            'rate_limit_failures': sum(m.rate_limit_failures for m in self.retry_metrics),
            'server_error_failures': sum(m.server_error_failures for m in self.retry_metrics),
            'client_error_failures': sum(m.client_error_failures for m in self.retry_metrics),
            'unknown_failures': sum(m.unknown_failures for m in self.retry_metrics)
        }
        
        # Circuit breaker statistics
        circuit_breaker_stats = {}
        for endpoint, cb in self.circuit_breakers.items():
            circuit_breaker_stats[endpoint] = cb.get_state_info()
        
        return {
            'total_operations': total_operations,
            'successful_operations': successful_operations,
            'success_rate': (successful_operations / total_operations * 100) if total_operations > 0 else 0,
            'total_attempts': total_attempts,
            'average_attempts_per_operation': total_attempts / total_operations if total_operations > 0 else 0,
            'total_retry_time': total_retry_time,
            'average_retry_time': total_retry_time / total_operations if total_operations > 0 else 0,
            'failure_breakdown': failure_breakdown,
            'circuit_breaker_triggers': sum(1 for m in self.retry_metrics if m.circuit_breaker_triggered),
            'fallback_usage': sum(1 for m in self.retry_metrics if m.fallback_used),
            'circuit_breaker_states': circuit_breaker_stats
        }
    
    def clear_metrics(self):
        """Clear retry metrics for fresh statistics."""
        self.retry_metrics.clear()
        retry_logger.info("Retry metrics cleared")

# Global retry manager instance
retry_manager = RetryManager()

def with_retry(operation_type: str, endpoint: str = "default"):
    """Decorator for automatic retry functionality."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            operation_id = f"{operation_type}_{int(time.time() * 1000)}"
            result, metrics = await retry_manager.execute_with_retry(
                func, operation_id, operation_type, endpoint, *args, **kwargs
            )
            return result
        return wrapper
    return decorator 