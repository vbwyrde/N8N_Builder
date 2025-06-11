#!/usr/bin/env python3
"""
Test Suite for Enhanced Retry Logic System
Verifies that retry strategies, circuit breakers, and fallback mechanisms work correctly.

Task 1.1.6: Add retry logic for LLM API failures - Testing
"""

import unittest
import asyncio
import time
from unittest.mock import patch, Mock, AsyncMock
import httpx
import logging
from pathlib import Path
import sys
from datetime import datetime, timedelta

# Add the n8n_builder module to path
sys.path.append(str(Path(__file__).parent.parent))

from n8n_builder.retry_manager import (
    RetryManager,
    RetryConfig, 
    RetryStrategy,
    FailureType,
    CircuitBreaker,
    CircuitBreakerState,
    RetryMetrics,
    retry_manager
)
from n8n_builder.n8n_builder import N8NBuilder

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestRetryConfig(unittest.TestCase):
    """Test retry configuration and strategy definitions."""
    
    def test_retry_config_defaults(self):
        """Test default retry configuration values."""
        config = RetryConfig()
        
        self.assertEqual(config.max_attempts, 3)
        self.assertEqual(config.base_delay, 1.0)
        self.assertEqual(config.max_delay, 60.0)
        self.assertEqual(config.strategy, RetryStrategy.EXPONENTIAL_BACKOFF)
        self.assertTrue(config.jitter)
        self.assertEqual(config.failure_threshold, 5)
        self.assertEqual(config.recovery_timeout, 60)
    
    def test_retry_config_custom_values(self):
        """Test custom retry configuration values."""
        config = RetryConfig(
            max_attempts=5,
            base_delay=2.0,
            strategy=RetryStrategy.LINEAR_BACKOFF,
            jitter=False
        )
        
        self.assertEqual(config.max_attempts, 5)
        self.assertEqual(config.base_delay, 2.0)
        self.assertEqual(config.strategy, RetryStrategy.LINEAR_BACKOFF)
        self.assertFalse(config.jitter)
    
    def test_failure_type_specific_configs(self):
        """Test failure-type specific configurations."""
        timeout_config = RetryConfig(max_attempts=5, strategy=RetryStrategy.EXPONENTIAL_BACKOFF)
        rate_limit_config = RetryConfig(max_attempts=4, strategy=RetryStrategy.LINEAR_BACKOFF)
        
        main_config = RetryConfig(
            failure_configs={
                FailureType.TIMEOUT: timeout_config,
                FailureType.RATE_LIMIT: rate_limit_config
            }
        )
        
        self.assertEqual(len(main_config.failure_configs), 2)
        self.assertEqual(main_config.failure_configs[FailureType.TIMEOUT].max_attempts, 5)
        self.assertEqual(main_config.failure_configs[FailureType.RATE_LIMIT].strategy, RetryStrategy.LINEAR_BACKOFF)

class TestCircuitBreaker(unittest.TestCase):
    """Test circuit breaker functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=3,
            recovery_timeout=5,
            success_threshold=2
        )
    
    def test_circuit_breaker_initial_state(self):
        """Test circuit breaker starts in CLOSED state."""
        self.assertEqual(self.circuit_breaker.state, CircuitBreakerState.CLOSED)
        self.assertTrue(self.circuit_breaker.can_attempt())
        self.assertEqual(self.circuit_breaker.failure_count, 0)
    
    def test_circuit_breaker_failure_threshold(self):
        """Test circuit breaker opens after failure threshold."""
        # Record failures up to threshold
        for i in range(3):
            self.circuit_breaker.record_failure()
            if i < 2:
                self.assertEqual(self.circuit_breaker.state, CircuitBreakerState.CLOSED)
            else:
                self.assertEqual(self.circuit_breaker.state, CircuitBreakerState.OPEN)
        
        # Should not allow attempts when open
        self.assertFalse(self.circuit_breaker.can_attempt())
    
    def test_circuit_breaker_recovery_timeout(self):
        """Test circuit breaker transitions to half-open after timeout."""
        # Force circuit breaker to open
        for _ in range(3):
            self.circuit_breaker.record_failure()
        
        self.assertEqual(self.circuit_breaker.state, CircuitBreakerState.OPEN)
        
        # Simulate time passing (we'll need to mock this in a real test)
        # For test purposes, manually set the time
        self.circuit_breaker.last_failure_time = datetime.now() - timedelta(seconds=10)
        
        # Now it should transition to half-open
        self.assertTrue(self.circuit_breaker.can_attempt())
        self.assertEqual(self.circuit_breaker.state, CircuitBreakerState.HALF_OPEN)
    
    def test_circuit_breaker_half_open_success(self):
        """Test circuit breaker closes after successful recovery."""
        # Set to half-open state
        self.circuit_breaker.state = CircuitBreakerState.HALF_OPEN
        
        # Record successful operations
        self.circuit_breaker.record_success()
        self.assertEqual(self.circuit_breaker.state, CircuitBreakerState.HALF_OPEN)
        
        self.circuit_breaker.record_success()  # Should close now
        self.assertEqual(self.circuit_breaker.state, CircuitBreakerState.CLOSED)
        self.assertEqual(self.circuit_breaker.failure_count, 0)
    
    def test_circuit_breaker_half_open_failure(self):
        """Test circuit breaker goes back to open on failure during recovery."""
        # Set to half-open state
        self.circuit_breaker.state = CircuitBreakerState.HALF_OPEN
        
        # Record failure during recovery
        self.circuit_breaker.record_failure()
        
        self.assertEqual(self.circuit_breaker.state, CircuitBreakerState.OPEN)
        self.assertEqual(self.circuit_breaker.success_count, 0)
    
    def test_circuit_breaker_state_info(self):
        """Test circuit breaker state information."""
        state_info = self.circuit_breaker.get_state_info()
        
        self.assertIn('state', state_info)
        self.assertIn('failure_count', state_info)
        self.assertIn('success_count', state_info)
        self.assertIn('time_in_current_state', state_info)
        
        self.assertEqual(state_info['state'], 'closed')
        self.assertEqual(state_info['failure_count'], 0)

class TestRetryMetrics(unittest.TestCase):
    """Test retry metrics tracking."""
    
    def test_retry_metrics_creation(self):
        """Test creating retry metrics."""
        metrics = RetryMetrics("test_op_123", "test_operation")
        
        self.assertEqual(metrics.operation_id, "test_op_123")
        self.assertEqual(metrics.operation_type, "test_operation")
        self.assertEqual(metrics.total_attempts, 0)
        self.assertFalse(metrics.final_success)
        self.assertIsNotNone(metrics.start_time)
    
    def test_retry_metrics_attempt_tracking(self):
        """Test tracking retry attempts."""
        from n8n_builder.retry_manager import RetryAttempt
        
        metrics = RetryMetrics("test_op_123", "test_operation")
        
        # Add successful attempt
        success_attempt = RetryAttempt(
            attempt_number=1,
            timestamp=datetime.now(),
            duration=1.5,
            error_type="none",
            error_message="success",
            success=True,
            response_length=100
        )
        metrics.add_attempt(success_attempt)
        
        self.assertEqual(metrics.total_attempts, 1)
        self.assertEqual(metrics.successful_attempts, 1)
        self.assertEqual(metrics.failed_attempts, 0)
        
        # Add failed attempt
        failure_attempt = RetryAttempt(
            attempt_number=2,
            timestamp=datetime.now(),
            duration=0.5,
            error_type="TimeoutException",
            error_message="Request timeout",
            success=False
        )
        metrics.add_attempt(failure_attempt)
        
        self.assertEqual(metrics.total_attempts, 2)
        self.assertEqual(metrics.successful_attempts, 1)
        self.assertEqual(metrics.failed_attempts, 1)
        self.assertEqual(metrics.timeout_failures, 1)
    
    def test_retry_metrics_failure_classification(self):
        """Test failure type classification in metrics."""
        from n8n_builder.retry_manager import RetryAttempt
        
        metrics = RetryMetrics("test_op_123", "test_operation")
        
        # Test different failure types
        test_cases = [
            ("TimeoutException", "Request timeout", "timeout_failures"),
            ("HTTPStatusError", "HTTP 500 Server Error", "server_error_failures"),
            ("HTTPStatusError", "HTTP 429 Rate Limited", "rate_limit_failures"),
            ("HTTPStatusError", "HTTP 404 Not Found", "client_error_failures"),
            ("ValidationError", "Invalid response", "validation_failures"),
            ("ConnectionError", "Connection failed", "connection_failures"),
            ("UnknownError", "Unknown issue", "unknown_failures")
        ]
        
        for error_type, error_message, expected_field in test_cases:
            attempt = RetryAttempt(
                attempt_number=1,
                timestamp=datetime.now(),
                duration=1.0,
                error_type=error_type,
                error_message=error_message,
                success=False
            )
            
            # Reset metrics for each test
            metrics = RetryMetrics("test_op_123", "test_operation")
            metrics.add_attempt(attempt)
            
            # Check that the correct failure type was incremented
            failure_count = getattr(metrics, expected_field)
            self.assertEqual(failure_count, 1, f"Failed for {error_type}: {expected_field}")
    
    def test_retry_metrics_to_dict(self):
        """Test converting metrics to dictionary."""
        metrics = RetryMetrics("test_op_123", "test_operation")
        metrics.finish(success=True)
        
        data = metrics.to_dict()
        
        self.assertEqual(data['operation_id'], "test_op_123")
        self.assertEqual(data['operation_type'], "test_operation")
        self.assertTrue(data['final_success'])
        self.assertIn('total_retry_time', data)
        self.assertIn('attempts_detail', data)
        self.assertIsInstance(data['attempts_detail'], list)

class TestRetryManager(unittest.TestCase):
    """Test the main retry manager functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.retry_manager = RetryManager()
    
    def test_retry_manager_initialization(self):
        """Test retry manager initialization."""
        self.assertIsInstance(self.retry_manager.default_config, RetryConfig)
        self.assertIsInstance(self.retry_manager.endpoint_configs, dict)
        self.assertIsInstance(self.retry_manager.circuit_breakers, dict)
        self.assertIsInstance(self.retry_manager.fallback_strategies, dict)
    
    def test_endpoint_configuration(self):
        """Test configuring retry behavior for specific endpoints."""
        test_config = RetryConfig(max_attempts=5, base_delay=2.0)
        
        self.retry_manager.configure_endpoint("test_endpoint", test_config)
        
        self.assertIn("test_endpoint", self.retry_manager.endpoint_configs)
        retrieved_config = self.retry_manager._get_config("test_endpoint")
        self.assertEqual(retrieved_config.max_attempts, 5)
        self.assertEqual(retrieved_config.base_delay, 2.0)
    
    def test_fallback_strategy_registration(self):
        """Test registering fallback strategies."""
        async def test_fallback(*args, **kwargs):
            return "fallback_result"
        
        self.retry_manager.register_fallback_strategy("test_fallback", test_fallback)
        
        self.assertIn("test_fallback", self.retry_manager.fallback_strategies)
        self.assertEqual(self.retry_manager.fallback_strategies["test_fallback"], test_fallback)
    
    def test_error_classification(self):
        """Test error classification for retry strategies."""
        # Test different error types
        timeout_error = httpx.TimeoutException("Request timeout")
        self.assertEqual(self.retry_manager._classify_error(timeout_error), FailureType.TIMEOUT)
        
        # Mock HTTP status error
        mock_response = Mock()
        mock_response.status_code = 500
        http_error = httpx.HTTPStatusError("Server error", request=Mock(), response=mock_response)
        self.assertEqual(self.retry_manager._classify_error(http_error), FailureType.SERVER_ERROR)
        
        # Rate limiting
        mock_response.status_code = 429
        rate_limit_error = httpx.HTTPStatusError("Rate limited", request=Mock(), response=mock_response)
        self.assertEqual(self.retry_manager._classify_error(rate_limit_error), FailureType.RATE_LIMIT)
        
        # Connection error
        connection_error = httpx.ConnectError("Connection failed")
        self.assertEqual(self.retry_manager._classify_error(connection_error), FailureType.CONNECTION_ERROR)
        
        # Validation error
        validation_error = ValueError("Validation failed in response")
        self.assertEqual(self.retry_manager._classify_error(validation_error), FailureType.VALIDATION_ERROR)
        
        # Unknown error
        unknown_error = Exception("Unknown error")
        self.assertEqual(self.retry_manager._classify_error(unknown_error), FailureType.UNKNOWN)
    
    def test_delay_calculation_exponential_backoff(self):
        """Test delay calculation for exponential backoff."""
        config = RetryConfig(
            base_delay=1.0,
            max_delay=10.0,
            strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
            jitter=False
        )
        
        # Test exponential progression
        delay1 = self.retry_manager._calculate_delay(1, config, FailureType.UNKNOWN)
        delay2 = self.retry_manager._calculate_delay(2, config, FailureType.UNKNOWN)
        delay3 = self.retry_manager._calculate_delay(3, config, FailureType.UNKNOWN)
        
        self.assertEqual(delay1, 1.0)  # base_delay * 2^(1-1) = 1.0
        self.assertEqual(delay2, 2.0)  # base_delay * 2^(2-1) = 2.0
        self.assertEqual(delay3, 4.0)  # base_delay * 2^(3-1) = 4.0
        
        # Test max delay cap
        delay_high = self.retry_manager._calculate_delay(10, config, FailureType.UNKNOWN)
        self.assertEqual(delay_high, 10.0)  # Should be capped at max_delay
    
    def test_delay_calculation_linear_backoff(self):
        """Test delay calculation for linear backoff."""
        config = RetryConfig(
            base_delay=2.0,
            max_delay=10.0,
            strategy=RetryStrategy.LINEAR_BACKOFF,
            jitter=False
        )
        
        delay1 = self.retry_manager._calculate_delay(1, config, FailureType.UNKNOWN)
        delay2 = self.retry_manager._calculate_delay(2, config, FailureType.UNKNOWN)
        delay3 = self.retry_manager._calculate_delay(3, config, FailureType.UNKNOWN)
        
        self.assertEqual(delay1, 2.0)  # base_delay * 1 = 2.0
        self.assertEqual(delay2, 4.0)  # base_delay * 2 = 4.0
        self.assertEqual(delay3, 6.0)  # base_delay * 3 = 6.0
    
    def test_delay_calculation_fixed_delay(self):
        """Test delay calculation for fixed delay."""
        config = RetryConfig(
            base_delay=3.0,
            strategy=RetryStrategy.FIXED_DELAY,
            jitter=False
        )
        
        delay1 = self.retry_manager._calculate_delay(1, config, FailureType.UNKNOWN)
        delay2 = self.retry_manager._calculate_delay(5, config, FailureType.UNKNOWN)
        
        self.assertEqual(delay1, 3.0)
        self.assertEqual(delay2, 3.0)  # Should always be the same
    
    async def test_execute_with_retry_success_first_attempt(self):
        """Test successful operation on first attempt."""
        async def successful_operation(*args, **kwargs):
            return "success_result"
        
        result, metrics = await self.retry_manager.execute_with_retry(
            successful_operation,
            "test_op_123",
            "test_operation",
            "test_endpoint"
        )
        
        self.assertEqual(result, "success_result")
        self.assertEqual(metrics.total_attempts, 1)
        self.assertEqual(metrics.successful_attempts, 1)
        self.assertEqual(metrics.failed_attempts, 0)
        self.assertTrue(metrics.final_success)
    
    async def test_execute_with_retry_success_after_failures(self):
        """Test successful operation after some failures."""
        attempt_count = 0
        
        async def failing_then_success_operation(*args, **kwargs):
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise httpx.TimeoutException("Timeout on attempt")
            return "success_after_retries"
        
        result, metrics = await self.retry_manager.execute_with_retry(
            failing_then_success_operation,
            "test_op_123",
            "test_operation",
            "test_endpoint"
        )
        
        self.assertEqual(result, "success_after_retries")
        self.assertEqual(metrics.total_attempts, 3)
        self.assertEqual(metrics.successful_attempts, 1)
        self.assertEqual(metrics.failed_attempts, 2)
        self.assertTrue(metrics.final_success)
        self.assertEqual(metrics.timeout_failures, 2)
    
    async def test_execute_with_retry_all_failures_then_fallback(self):
        """Test fallback strategies when all retries fail."""
        async def always_failing_operation(*args, **kwargs):
            raise httpx.TimeoutException("Always fails")
        
        async def successful_fallback(*args, **kwargs):
            return "fallback_success"
        
        # Register fallback strategy
        self.retry_manager.register_fallback_strategy("test_fallback", successful_fallback)
        
        result, metrics = await self.retry_manager.execute_with_retry(
            always_failing_operation,
            "test_op_123",
            "test_operation",
            "test_endpoint"
        )
        
        self.assertEqual(result, "fallback_success")
        self.assertTrue(metrics.fallback_used)
        self.assertEqual(metrics.fallback_type, "test_fallback")
        self.assertTrue(metrics.final_success)
    
    async def test_execute_with_retry_complete_failure(self):
        """Test complete failure when retries and fallbacks fail."""
        async def always_failing_operation(*args, **kwargs):
            raise ValueError("Always fails")
        
        # Clear any existing fallback strategies
        self.retry_manager.fallback_strategies.clear()
        
        with self.assertRaises(ValueError):
            await self.retry_manager.execute_with_retry(
                always_failing_operation,
                "test_op_123",
                "test_operation",
                "test_endpoint"
            )
    
    def test_retry_statistics_empty(self):
        """Test retry statistics when no operations recorded."""
        stats = self.retry_manager.get_retry_statistics()
        
        self.assertIn("message", stats)
        self.assertEqual(stats["message"], "No retry operations recorded")
    
    def test_retry_statistics_with_data(self):
        """Test retry statistics with recorded operations."""
        # Manually add some metrics for testing
        metrics1 = RetryMetrics("op1", "test")
        metrics1.total_attempts = 3
        metrics1.timeout_failures = 2
        metrics1.finish(success=True)
        
        metrics2 = RetryMetrics("op2", "test")
        metrics2.total_attempts = 1
        metrics2.finish(success=True)
        
        self.retry_manager.retry_metrics = [metrics1, metrics2]
        
        stats = self.retry_manager.get_retry_statistics()
        
        self.assertEqual(stats['total_operations'], 2)
        self.assertEqual(stats['successful_operations'], 2)
        self.assertEqual(stats['success_rate'], 100.0)
        self.assertEqual(stats['total_attempts'], 4)
        self.assertEqual(stats['average_attempts_per_operation'], 2.0)
        self.assertEqual(stats['failure_breakdown']['timeout_failures'], 2)

class TestN8NBuilderRetryIntegration(unittest.TestCase):
    """Test N8N Builder integration with retry logic."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.builder = N8NBuilder()
    
    def test_builder_has_retry_manager(self):
        """Test that N8N Builder has retry manager initialized."""
        self.assertIsNotNone(self.builder.retry_manager)
        self.assertIsInstance(self.builder.retry_manager, RetryManager)
    
    def test_retry_configurations_setup(self):
        """Test that retry configurations are properly setup."""
        endpoint_key = self.builder.llm_config.endpoint or "default_llm"
        
        # Check that the endpoint has been configured
        config = self.builder.retry_manager._get_config(endpoint_key)
        self.assertIsInstance(config, RetryConfig)
        
        # Check that failure-specific configs are present
        self.assertIn(FailureType.TIMEOUT, config.failure_configs)
        self.assertIn(FailureType.RATE_LIMIT, config.failure_configs)
        self.assertIn(FailureType.SERVER_ERROR, config.failure_configs)
    
    def test_fallback_strategies_registered(self):
        """Test that fallback strategies are registered."""
        strategies = self.builder.retry_manager.fallback_strategies
        
        self.assertIn("mock_response", strategies)
        self.assertIn("simplified_response", strategies)
        self.assertIn("basic_workflow", strategies)
        self.assertEqual(len(strategies), 3)
    
    @patch('n8n_builder.n8n_builder.httpx.AsyncClient')
    async def test_llm_call_with_retry_success(self, mock_client):
        """Test LLM call with retry manager success."""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "test response"}}]
        }
        mock_response.raise_for_status.return_value = None
        
        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        result = await self.builder._call_mimo_vl7b("test prompt")
        
        self.assertEqual(result, "test response")
        mock_client_instance.post.assert_called_once()
    
    async def test_fallback_mock_response(self):
        """Test mock response fallback strategy."""
        # Test email-related prompt
        result = await self.builder._fallback_mock_response("Add an email node to send notifications")
        
        self.assertIsInstance(result, str)
        parsed = eval(result)  # Safe since we control the input
        self.assertIsInstance(parsed, list)
        self.assertEqual(parsed[0]["action"], "add_node")
        self.assertEqual(parsed[0]["details"]["node_type"], "n8n-nodes-base.emailSend")
    
    async def test_fallback_simplified_response(self):
        """Test simplified response fallback strategy."""
        result = await self.builder._fallback_simplified_response("Add some processing logic")
        
        self.assertIsInstance(result, str)
        parsed = eval(result)  # Safe since we control the input
        self.assertIsInstance(parsed, list)
        self.assertEqual(parsed[0]["action"], "add_node")
        self.assertEqual(parsed[0]["details"]["node_type"], "n8n-nodes-base.function")
    
    async def test_fallback_basic_workflow(self):
        """Test basic workflow fallback strategy."""
        result = await self.builder._fallback_basic_workflow("Create a basic workflow")
        
        self.assertIsInstance(result, str)
        parsed = eval(result)  # Safe since we control the input
        self.assertIsInstance(parsed, dict)
        self.assertIn("nodes", parsed)
        self.assertIn("connections", parsed)
        self.assertEqual(len(parsed["nodes"]), 2)

class TestRetryDecorator(unittest.TestCase):
    """Test the retry decorator functionality."""
    
    async def test_with_retry_decorator(self):
        """Test the with_retry decorator."""
        from n8n_builder.retry_manager import with_retry
        
        attempt_count = 0
        
        @with_retry("test_operation", "test_endpoint")
        async def test_function():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 2:
                raise httpx.TimeoutException("Test timeout")
            return "success"
        
        result = await test_function()
        
        self.assertEqual(result, "success")
        self.assertEqual(attempt_count, 2)  # Should have retried once

if __name__ == '__main__':
    # Run with increased verbosity to see detailed test output
    unittest.main(verbosity=2) 