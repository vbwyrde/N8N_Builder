import asyncio
import time
from typing import Dict, Any, Optional, List, Callable, Awaitable
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import logging

class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"         # Failing, rejecting requests
    HALF_OPEN = "half_open"  # Testing if service recovered

@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""
    failure_threshold: int = 5
    recovery_timeout: int = 30
    half_open_timeout: int = 10
    success_threshold: int = 2

@dataclass
class RetryConfig:
    """Configuration for retry mechanism."""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 30.0
    backoff_factor: float = 2.0
    retry_on_exceptions: tuple = (Exception,)

class ErrorRecoveryManager:
    """Manages error recovery and resilience features."""
    
    def __init__(self, config: Dict[str, Any]):
        self.logger = logging.getLogger(__name__)
        self.config = config
        
        # Circuit breaker configurations
        self.circuit_breakers: Dict[str, Dict[str, Any]] = {}
        self.circuit_config = CircuitBreakerConfig(
            failure_threshold=config.get('circuit_breaker', {}).get('failure_threshold', 5),
            recovery_timeout=config.get('circuit_breaker', {}).get('recovery_timeout', 30),
            half_open_timeout=config.get('circuit_breaker', {}).get('half_open_timeout', 10),
            success_threshold=config.get('circuit_breaker', {}).get('success_threshold', 2)
        )
        
        # Retry configurations
        self.retry_configs: Dict[str, RetryConfig] = {}
        self.default_retry_config = RetryConfig(
            max_attempts=config.get('retry', {}).get('max_attempts', 3),
            initial_delay=config.get('retry', {}).get('initial_delay', 1.0),
            max_delay=config.get('retry', {}).get('max_delay', 30.0),
            backoff_factor=config.get('retry', {}).get('backoff_factor', 2.0)
        )
        
        # Error tracking
        self.error_counts: Dict[str, int] = {}
        self.last_errors: Dict[str, List[Dict[str, Any]]] = {}
        self.max_error_history = config.get('max_error_history', 100)
    
    def _get_circuit_breaker(self, service_id: str) -> Dict[str, Any]:
        """Get or create a circuit breaker for a service."""
        if service_id not in self.circuit_breakers:
            self.circuit_breakers[service_id] = {
                'state': CircuitState.CLOSED,
                'failure_count': 0,
                'success_count': 0,
                'last_failure_time': None,
                'last_state_change': datetime.now()
            }
        return self.circuit_breakers[service_id]
    
    def _get_retry_config(self, operation_id: str) -> RetryConfig:
        """Get retry configuration for an operation."""
        return self.retry_configs.get(operation_id, self.default_retry_config)
    
    async def execute_with_circuit_breaker(self, service_id: str, 
                                         operation: Callable[..., Awaitable[Any]],
                                         *args, **kwargs) -> Any:
        """Execute an operation with circuit breaker protection."""
        circuit = self._get_circuit_breaker(service_id)
        
        # Check circuit state
        if circuit['state'] == CircuitState.OPEN:
            if (datetime.now() - circuit['last_state_change']).total_seconds() > self.circuit_config.recovery_timeout:
                circuit['state'] = CircuitState.HALF_OPEN
                circuit['last_state_change'] = datetime.now()
                self.logger.info(f"Circuit breaker for {service_id} moved to HALF_OPEN state")
            else:
                raise Exception(f"Circuit breaker is OPEN for service {service_id}")
        
        try:
            result = await operation(*args, **kwargs)
            
            # Handle success
            if circuit['state'] == CircuitState.HALF_OPEN:
                circuit['success_count'] += 1
                if circuit['success_count'] >= self.circuit_config.success_threshold:
                    circuit['state'] = CircuitState.CLOSED
                    circuit['failure_count'] = 0
                    circuit['success_count'] = 0
                    circuit['last_state_change'] = datetime.now()
                    self.logger.info(f"Circuit breaker for {service_id} moved to CLOSED state")
            
            return result
            
        except Exception as e:
            # Handle failure
            circuit['failure_count'] += 1
            circuit['last_failure_time'] = datetime.now()
            
            if circuit['state'] == CircuitState.CLOSED:
                if circuit['failure_count'] >= self.circuit_config.failure_threshold:
                    circuit['state'] = CircuitState.OPEN
                    circuit['last_state_change'] = datetime.now()
                    self.logger.warning(f"Circuit breaker for {service_id} moved to OPEN state")
            elif circuit['state'] == CircuitState.HALF_OPEN:
                circuit['state'] = CircuitState.OPEN
                circuit['last_state_change'] = datetime.now()
                self.logger.warning(f"Circuit breaker for {service_id} moved to OPEN state")
            
            raise
    
    async def execute_with_retry(self, operation_id: str,
                               operation: Callable[..., Awaitable[Any]],
                               *args, **kwargs) -> Any:
        """Execute an operation with retry mechanism."""
        retry_config = self._get_retry_config(operation_id)
        attempt = 0
        last_exception = None
        
        while attempt < retry_config.max_attempts:
            try:
                return await operation(*args, **kwargs)
            except retry_config.retry_on_exceptions as e:
                last_exception = e
                attempt += 1
                
                if attempt == retry_config.max_attempts:
                    break
                
                # Calculate delay with exponential backoff
                delay = min(
                    retry_config.initial_delay * (retry_config.backoff_factor ** (attempt - 1)),
                    retry_config.max_delay
                )
                
                self.logger.warning(
                    f"Operation {operation_id} failed (attempt {attempt}/{retry_config.max_attempts}). "
                    f"Retrying in {delay:.2f} seconds. Error: {str(e)}"
                )
                
                await asyncio.sleep(delay)
        
        raise last_exception
    
    async def execute_with_graceful_degradation(self, primary_operation: Callable[..., Awaitable[Any]],
                                              fallback_operation: Callable[..., Awaitable[Any]],
                                              *args, **kwargs) -> Any:
        """Execute an operation with graceful degradation."""
        try:
            return await primary_operation(*args, **kwargs)
        except Exception as e:
            self.logger.warning(f"Primary operation failed, falling back to alternative. Error: {str(e)}")
            return await fallback_operation(*args, **kwargs)
    
    def track_error(self, service_id: str, error: Exception, context: Dict[str, Any] = None):
        """Track an error occurrence."""
        if service_id not in self.error_counts:
            self.error_counts[service_id] = 0
            self.last_errors[service_id] = []
        
        self.error_counts[service_id] += 1
        
        error_info = {
            'timestamp': datetime.now(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {}
        }
        
        self.last_errors[service_id].append(error_info)
        
        # Maintain error history size
        if len(self.last_errors[service_id]) > self.max_error_history:
            self.last_errors[service_id] = self.last_errors[service_id][-self.max_error_history:]
    
    def get_error_stats(self, service_id: str) -> Dict[str, Any]:
        """Get error statistics for a service."""
        return {
            'total_errors': self.error_counts.get(service_id, 0),
            'recent_errors': self.last_errors.get(service_id, []),
            'circuit_state': self.circuit_breakers.get(service_id, {}).get('state', CircuitState.CLOSED)
        }
    
    async def reset_circuit_breaker(self, service_id: str):
        """Reset a circuit breaker to CLOSED state."""
        if service_id in self.circuit_breakers:
            self.circuit_breakers[service_id].update({
                'state': CircuitState.CLOSED,
                'failure_count': 0,
                'success_count': 0,
                'last_failure_time': None,
                'last_state_change': datetime.now()
            })
            self.logger.info(f"Circuit breaker for {service_id} has been reset")
    
    async def cleanup_old_errors(self, max_age_hours: int = 24):
        """Clean up old error records."""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        for service_id in self.last_errors:
            self.last_errors[service_id] = [
                error for error in self.last_errors[service_id]
                if error['timestamp'] > cutoff_time
            ] 