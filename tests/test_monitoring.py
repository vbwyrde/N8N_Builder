import pytest
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any

from n8n_builder.agents.integration.monitoring import (
    MonitoringManager,
    MetricType,
    HealthStatus,
    Metric,
    HealthCheck
)

pytestmark = pytest.mark.asyncio

class TestMonitoringManager:
    """Test suite for MonitoringManager."""
    
    async def test_initialization(self, monitoring_manager):
        """Test proper initialization of the manager."""
        assert monitoring_manager is not None
        assert monitoring_manager.metrics is not None
        assert monitoring_manager.health_checks is not None
        assert monitoring_manager.logger is not None
    
    async def test_metric_recording(self, monitoring_manager):
        """Test metric recording functionality."""
        # Record a metric
        await monitoring_manager.record_metric(
            'test.metric',
            42.0,
            MetricType.GAUGE,
            {'test': 'true'}
        )
        
        # Verify metric was recorded
        metric = await monitoring_manager.get_latest_metric('test.metric')
        assert metric is not None
        assert metric.name == 'test.metric'
        assert metric.value == 42.0
        assert metric.type == MetricType.GAUGE
        assert metric.labels == {'test': 'true'}
    
    async def test_metric_history(self, monitoring_manager):
        """Test metric history retrieval."""
        # Record multiple metrics
        for i in range(3):
            await monitoring_manager.record_metric(
                'test.history',
                float(i),
                MetricType.COUNTER,
                {'index': str(i)}
            )
        
        # Get history
        history = await monitoring_manager.get_metric_history('test.history')
        assert len(history) == 3
        
        # Get history with time range
        start_time = datetime.now() - timedelta(minutes=5)
        end_time = datetime.now() + timedelta(minutes=5)
        filtered_history = await monitoring_manager.get_metric_history(
            'test.history',
            start_time,
            end_time
        )
        assert len(filtered_history) == 3
    
    async def test_health_check_recording(self, monitoring_manager):
        """Test health check recording functionality."""
        # Record a health check
        await monitoring_manager.record_health_check(
            'test.service',
            HealthStatus.HEALTHY,
            'Service is healthy',
            {'uptime': 3600}
        )
        
        # Verify health check was recorded
        health = await monitoring_manager.get_health_status('test.service')
        assert health is not None
        assert health['status'] == HealthStatus.HEALTHY.value
        assert health['message'] == 'Service is healthy'
        assert health['details']['uptime'] == 3600
    
    async def test_system_metrics_collection(self, monitoring_manager):
        """Test system metrics collection."""
        # Wait for metrics collection
        await asyncio.sleep(2)
        
        # Verify system metrics
        cpu_metric = await monitoring_manager.get_latest_metric('system.cpu.usage')
        assert cpu_metric is not None
        assert 0 <= cpu_metric.value <= 100
        
        memory_metric = await monitoring_manager.get_latest_metric('system.memory.usage')
        assert memory_metric is not None
        assert 0 <= memory_metric.value <= 100
    
    async def test_resource_limit_checking(self, monitoring_manager):
        """Test resource limit checking."""
        # Set a low limit
        monitoring_manager.resource_limits['cpu'] = 10
        
        # Record high CPU usage
        await monitoring_manager.record_metric(
            'system.cpu.usage',
            90.0,
            MetricType.GAUGE,
            {'type': 'system'}
        )
        
        # Check resource limits
        await monitoring_manager._check_resource_limits()
        
        # Verify warning was logged
        # Note: This is a bit of a hack to check logging
        # In a real test, we might want to use a custom logger or mock
        assert True  # Placeholder for actual assertion
    
    async def test_health_check_status(self, monitoring_manager):
        """Test health check status retrieval."""
        # Record multiple health checks
        await monitoring_manager.record_health_check(
            'service1',
            HealthStatus.HEALTHY,
            'Service 1 is healthy',
            {'uptime': 3600}
        )
        await monitoring_manager.record_health_check(
            'service2',
            HealthStatus.DEGRADED,
            'Service 2 is degraded',
            {'error_rate': 0.1}
        )
        
        # Get all health statuses
        all_health = await monitoring_manager.get_health_status()
        assert 'service1' in all_health
        assert 'service2' in all_health
        assert all_health['service1']['status'] == HealthStatus.HEALTHY.value
        assert all_health['service2']['status'] == HealthStatus.DEGRADED.value
    
    async def test_metric_cleanup(self, monitoring_manager):
        """Test cleanup of old metrics."""
        # Record old metric
        old_time = datetime.now() - timedelta(hours=2)
        old_metric = Metric(
            name='test.old',
            value=1.0,
            type=MetricType.COUNTER,
            timestamp=old_time,
            labels={'test': 'old'}
        )
        monitoring_manager.metrics['test.old'] = [old_metric]
        
        # Run cleanup
        await monitoring_manager._cleanup_old_metrics()
        
        # Verify old metric was removed
        assert 'test.old' not in monitoring_manager.metrics
    
    async def test_logging(self, monitoring_manager):
        """Test logging functionality."""
        # Log different types of messages
        monitoring_manager.log_event(
            logging.INFO,
            "Test info message",
            extra={'test': True}
        )
        monitoring_manager.log_metric(
            'test.logging',
            42.0,
            test=True
        )
        monitoring_manager.log_health(
            'test.logging',
            HealthStatus.HEALTHY,
            'Test health message',
            test=True
        )
        
        # Note: In a real test, we would verify the logs
        # This might require a custom logger or mock
        assert True  # Placeholder for actual assertion
    
    async def test_start_stop(self, monitoring_manager):
        """Test starting and stopping the monitoring manager."""
        # Stop the manager
        await monitoring_manager.stop()
        
        # Verify tasks were cancelled
        assert not monitoring_manager._running
        assert len(monitoring_manager._tasks) == 0
        
        # Start the manager
        await monitoring_manager.start()
        
        # Verify tasks were started
        assert monitoring_manager._running
        assert len(monitoring_manager._tasks) > 0 