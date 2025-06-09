import pytest
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any

from n8n_builder.agents.integration.error_recovery import (
    ErrorRecoveryManager,
    CircuitState,
    CircuitBreakerConfig,
    RetryConfig
)

pytestmark = pytest.mark.asyncio

class TestErrorRecoveryManager:
    """Test suite for ErrorRecoveryManager."""
    
    async def test_initialization(self, error_recovery_manager):
        """Test proper initialization of the manager."""
        assert error_recovery_manager is not None
        assert error_recovery_manager.circuit_breakers is not None
        assert error_recovery_manager.error_history is not None
        assert error_recovery_manager.config is not None
    
    async def test_circuit_breaker_execution(self, error_recovery_manager):
        """Test circuit breaker execution."""
        # Define a successful operation
        async def success_operation():
            return "success"
        
        # Execute with circuit breaker
        result = await error_recovery_manager.execute_with_circuit_breaker(
            'test.service',
            success_operation
        )
        
        # Verify result
        assert result == "success"
        
        # Verify circuit state
        circuit = error_recovery_manager.circuit_breakers['test.service']
        assert circuit.state == CircuitState.CLOSED
        assert circuit.failure_count == 0
    
    async def test_circuit_breaker_failure(self, error_recovery_manager):
        """Test circuit breaker with failing operation."""
        # Define a failing operation
        async def failing_operation():
            raise Exception("Test failure")
        
        # Execute with circuit breaker
        with pytest.raises(Exception):
            await error_recovery_manager.execute_with_circuit_breaker(
                'test.service',
                failing_operation
            )
        
        # Verify circuit state
        circuit = error_recovery_manager.circuit_breakers['test.service']
        assert circuit.failure_count == 1
        
        # Execute multiple times to trigger circuit open
        for _ in range(5):
            with pytest.raises(Exception):
                await error_recovery_manager.execute_with_circuit_breaker(
                    'test.service',
                    failing_operation
                )
        
        # Verify circuit is open
        assert circuit.state == CircuitState.OPEN
    
    async def test_circuit_breaker_recovery(self, error_recovery_manager):
        """Test circuit breaker recovery."""
        # Define operations
        async def failing_operation():
            raise Exception("Test failure")
        
        async def success_operation():
            return "success"
        
        # Trigger circuit open
        for _ in range(5):
            with pytest.raises(Exception):
                await error_recovery_manager.execute_with_circuit_breaker(
                    'test.service',
                    failing_operation
                )
        
        # Wait for recovery timeout
        await asyncio.sleep(1)  # Use a shorter timeout for testing
        
        # Execute with success
        result = await error_recovery_manager.execute_with_circuit_breaker(
            'test.service',
            success_operation
        )
        
        # Verify result and circuit state
        assert result == "success"
        circuit = error_recovery_manager.circuit_breakers['test.service']
        assert circuit.state == CircuitState.HALF_OPEN
    
    async def test_retry_execution(self, error_recovery_manager):
        """Test retry mechanism."""
        # Define an operation that succeeds after retries
        attempt_count = 0
        async def retry_operation():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise Exception("Temporary failure")
            return "success"
        
        # Execute with retry
        result = await error_recovery_manager.execute_with_retry(
            'test.operation',
            retry_operation
        )
        
        # Verify result and attempts
        assert result == "success"
        assert attempt_count == 3
    
    async def test_retry_max_attempts(self, error_recovery_manager):
        """Test retry mechanism with max attempts."""
        # Define a consistently failing operation
        async def failing_operation():
            raise Exception("Persistent failure")
        
        # Execute with retry
        with pytest.raises(Exception):
            await error_recovery_manager.execute_with_retry(
                'test.operation',
                failing_operation
            )
        
        # Verify error was tracked
        errors = error_recovery_manager.error_history['test.operation']
        assert len(errors) > 0
    
    async def test_graceful_degradation(self, error_recovery_manager):
        """Test graceful degradation."""
        # Define operations
        async def primary_operation():
            raise Exception("Primary operation failed")
        
        async def fallback_operation():
            return "fallback result"
        
        # Execute with graceful degradation
        result = await error_recovery_manager.execute_with_graceful_degradation(
            primary_operation,
            fallback_operation
        )
        
        # Verify fallback was used
        assert result == "fallback result"
    
    async def test_error_tracking(self, error_recovery_manager):
        """Test error tracking functionality."""
        # Track an error
        error = Exception("Test error")
        context = {'test': True}
        error_recovery_manager.track_error('test.service', error, context)
        
        # Verify error was tracked
        errors = error_recovery_manager.error_history['test.service']
        assert len(errors) == 1
        assert errors[0]['error'] == str(error)
        assert errors[0]['context'] == context
    
    async def test_error_stats(self, error_recovery_manager):
        """Test error statistics retrieval."""
        # Track multiple errors
        for _ in range(3):
            error_recovery_manager.track_error(
                'test.service',
                Exception("Test error"),
                {'count': _}
            )
        
        # Get error stats
        stats = await error_recovery_manager.get_error_stats('test.service')
        assert stats['total_errors'] == 3
        assert stats['error_rate'] > 0
    
    async def test_circuit_breaker_reset(self, error_recovery_manager):
        """Test circuit breaker reset."""
        # Define a failing operation
        async def failing_operation():
            raise Exception("Test failure")
        
        # Trigger circuit open
        for _ in range(5):
            with pytest.raises(Exception):
                await error_recovery_manager.execute_with_circuit_breaker(
                    'test.service',
                    failing_operation
                )
        
        # Reset circuit breaker
        await error_recovery_manager.reset_circuit_breaker('test.service')
        
        # Verify circuit state
        circuit = error_recovery_manager.circuit_breakers['test.service']
        assert circuit.state == CircuitState.CLOSED
        assert circuit.failure_count == 0
    
    async def test_error_cleanup(self, error_recovery_manager):
        """Test cleanup of old errors."""
        # Track old error
        old_time = datetime.now() - timedelta(hours=2)
        error_recovery_manager.error_history['test.service'] = [{
            'error': 'Old error',
            'timestamp': old_time,
            'context': {}
        }]
        
        # Run cleanup
        await error_recovery_manager.cleanup_old_errors()
        
        # Verify old error was removed
        assert 'test.service' not in error_recovery_manager.error_history 