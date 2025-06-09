import pytest
import time
from typing import Dict, Any

from ..agents.integration.workflow_step_metrics import (
    WorkflowStepMetrics,
    WorkflowStepMetricsCollector,
    WorkflowStepMetricsAggregator
)

class TestWorkflowStepMetrics:
    """Test suite for WorkflowStepMetrics."""
    
    def test_initialization(self):
        """Test proper initialization of step metrics."""
        metrics = WorkflowStepMetrics(
            step_id="step1",
            execution_time=1.5,
            memory_usage=1024,
            cpu_usage=50.0,
            network_usage=2048,
            disk_usage=512,
            error_count=0,
            retry_count=0,
            custom_metrics={
                "custom1": 100,
                "custom2": 200
            }
        )
        
        assert metrics.step_id == "step1"
        assert metrics.execution_time == 1.5
        assert metrics.memory_usage == 1024
        assert metrics.cpu_usage == 50.0
        assert metrics.network_usage == 2048
        assert metrics.disk_usage == 512
        assert metrics.error_count == 0
        assert metrics.retry_count == 0
        assert metrics.custom_metrics["custom1"] == 100
        assert metrics.custom_metrics["custom2"] == 200
    
    def test_metrics_creation(self):
        """Test creating metrics with different values."""
        # Test with minimal values
        minimal_metrics = WorkflowStepMetrics.create_minimal(
            step_id="step1",
            execution_time=1.5
        )
        assert minimal_metrics.step_id == "step1"
        assert minimal_metrics.execution_time == 1.5
        assert minimal_metrics.memory_usage == 0
        assert minimal_metrics.cpu_usage == 0.0
        
        # Test with all values
        full_metrics = WorkflowStepMetrics.create_full(
            step_id="step1",
            execution_time=1.5,
            memory_usage=1024,
            cpu_usage=50.0,
            network_usage=2048,
            disk_usage=512,
            error_count=1,
            retry_count=2,
            custom_metrics={"custom": 100}
        )
        assert full_metrics.step_id == "step1"
        assert full_metrics.execution_time == 1.5
        assert full_metrics.memory_usage == 1024
        assert full_metrics.cpu_usage == 50.0
        assert full_metrics.network_usage == 2048
        assert full_metrics.disk_usage == 512
        assert full_metrics.error_count == 1
        assert full_metrics.retry_count == 2
        assert full_metrics.custom_metrics["custom"] == 100
    
    def test_metrics_serialization(self):
        """Test serializing metrics to dictionary."""
        metrics = WorkflowStepMetrics(
            step_id="step1",
            execution_time=1.5,
            memory_usage=1024,
            cpu_usage=50.0,
            network_usage=2048,
            disk_usage=512,
            error_count=0,
            retry_count=0,
            custom_metrics={
                "custom1": 100,
                "custom2": 200
            }
        )
        
        serialized = metrics.to_dict()
        assert serialized["step_id"] == "step1"
        assert serialized["execution_time"] == 1.5
        assert serialized["memory_usage"] == 1024
        assert serialized["cpu_usage"] == 50.0
        assert serialized["network_usage"] == 2048
        assert serialized["disk_usage"] == 512
        assert serialized["error_count"] == 0
        assert serialized["retry_count"] == 0
        assert serialized["custom_metrics"]["custom1"] == 100
        assert serialized["custom_metrics"]["custom2"] == 200
    
    def test_metrics_deserialization(self):
        """Test deserializing metrics from dictionary."""
        data = {
            "step_id": "step1",
            "execution_time": 1.5,
            "memory_usage": 1024,
            "cpu_usage": 50.0,
            "network_usage": 2048,
            "disk_usage": 512,
            "error_count": 0,
            "retry_count": 0,
            "custom_metrics": {
                "custom1": 100,
                "custom2": 200
            }
        }
        
        metrics = WorkflowStepMetrics.from_dict(data)
        assert metrics.step_id == "step1"
        assert metrics.execution_time == 1.5
        assert metrics.memory_usage == 1024
        assert metrics.cpu_usage == 50.0
        assert metrics.network_usage == 2048
        assert metrics.disk_usage == 512
        assert metrics.error_count == 0
        assert metrics.retry_count == 0
        assert metrics.custom_metrics["custom1"] == 100
        assert metrics.custom_metrics["custom2"] == 200

class TestWorkflowStepMetricsCollector:
    """Test suite for WorkflowStepMetricsCollector."""
    
    def test_initialization(self):
        """Test proper initialization of metrics collector."""
        collector = WorkflowStepMetricsCollector()
        assert collector is not None
        assert collector.metrics is not None
    
    def test_collect_metrics(self):
        """Test collecting step metrics."""
        collector = WorkflowStepMetricsCollector()
        
        # Collect metrics
        metrics = WorkflowStepMetrics.create_minimal(
            step_id="step1",
            execution_time=1.5
        )
        collector.collect_metrics(metrics)
        
        # Verify metrics were collected
        collected_metrics = collector.get_metrics("step1")
        assert collected_metrics.step_id == "step1"
        assert collected_metrics.execution_time == 1.5
    
    def test_get_metrics_history(self):
        """Test retrieving metrics history."""
        collector = WorkflowStepMetricsCollector()
        
        # Collect multiple metrics
        metrics1 = WorkflowStepMetrics.create_minimal(
            step_id="step1",
            execution_time=1.5
        )
        metrics2 = WorkflowStepMetrics.create_minimal(
            step_id="step1",
            execution_time=2.5
        )
        
        collector.collect_metrics(metrics1)
        collector.collect_metrics(metrics2)
        
        history = collector.get_metrics_history("step1")
        assert len(history) == 2
        assert history[0].execution_time == 1.5
        assert history[1].execution_time == 2.5
    
    def test_get_unknown_metrics(self):
        """Test retrieving metrics for unknown step."""
        collector = WorkflowStepMetricsCollector()
        
        with pytest.raises(KeyError):
            collector.get_metrics("unknown_step")
    
    def test_get_unknown_metrics_history(self):
        """Test retrieving metrics history for unknown step."""
        collector = WorkflowStepMetricsCollector()
        
        with pytest.raises(KeyError):
            collector.get_metrics_history("unknown_step")
    
    def test_clear_metrics(self):
        """Test clearing step metrics."""
        collector = WorkflowStepMetricsCollector()
        
        # Collect metrics
        metrics = WorkflowStepMetrics.create_minimal(
            step_id="step1",
            execution_time=1.5
        )
        collector.collect_metrics(metrics)
        
        # Clear metrics
        collector.clear_metrics("step1")
        with pytest.raises(KeyError):
            collector.get_metrics("step1")
    
    def test_get_all_metrics(self):
        """Test retrieving all collected metrics."""
        collector = WorkflowStepMetricsCollector()
        
        # Collect metrics for multiple steps
        metrics1 = WorkflowStepMetrics.create_minimal(
            step_id="step1",
            execution_time=1.5
        )
        metrics2 = WorkflowStepMetrics.create_minimal(
            step_id="step2",
            execution_time=2.5
        )
        
        collector.collect_metrics(metrics1)
        collector.collect_metrics(metrics2)
        
        all_metrics = collector.get_all_metrics()
        assert len(all_metrics) == 2
        assert all_metrics["step1"].execution_time == 1.5
        assert all_metrics["step2"].execution_time == 2.5

class TestWorkflowStepMetricsAggregator:
    """Test suite for WorkflowStepMetricsAggregator."""
    
    def test_initialization(self):
        """Test proper initialization of metrics aggregator."""
        aggregator = WorkflowStepMetricsAggregator()
        assert aggregator is not None
    
    def test_aggregate_metrics(self):
        """Test aggregating step metrics."""
        aggregator = WorkflowStepMetricsAggregator()
        
        # Create metrics to aggregate
        metrics1 = WorkflowStepMetrics.create_full(
            step_id="step1",
            execution_time=1.0,
            memory_usage=1000,
            cpu_usage=50.0,
            network_usage=2000,
            disk_usage=500,
            error_count=0,
            retry_count=0
        )
        metrics2 = WorkflowStepMetrics.create_full(
            step_id="step1",
            execution_time=2.0,
            memory_usage=2000,
            cpu_usage=75.0,
            network_usage=3000,
            disk_usage=1000,
            error_count=1,
            retry_count=1
        )
        
        # Aggregate metrics
        aggregated = aggregator.aggregate_metrics([metrics1, metrics2])
        
        # Verify aggregation
        assert aggregated.step_id == "step1"
        assert aggregated.execution_time == 1.5  # Average
        assert aggregated.memory_usage == 1500  # Average
        assert aggregated.cpu_usage == 62.5  # Average
        assert aggregated.network_usage == 2500  # Average
        assert aggregated.disk_usage == 750  # Average
        assert aggregated.error_count == 1  # Sum
        assert aggregated.retry_count == 1  # Sum
    
    def test_aggregate_empty_metrics(self):
        """Test aggregating empty metrics list."""
        aggregator = WorkflowStepMetricsAggregator()
        
        with pytest.raises(ValueError):
            aggregator.aggregate_metrics([])
    
    def test_aggregate_different_steps(self):
        """Test aggregating metrics from different steps."""
        aggregator = WorkflowStepMetricsAggregator()
        
        # Create metrics for different steps
        metrics1 = WorkflowStepMetrics.create_minimal(
            step_id="step1",
            execution_time=1.0
        )
        metrics2 = WorkflowStepMetrics.create_minimal(
            step_id="step2",
            execution_time=2.0
        )
        
        with pytest.raises(ValueError):
            aggregator.aggregate_metrics([metrics1, metrics2])
    
    def test_aggregate_custom_metrics(self):
        """Test aggregating custom metrics."""
        aggregator = WorkflowStepMetricsAggregator()
        
        # Create metrics with custom values
        metrics1 = WorkflowStepMetrics.create_full(
            step_id="step1",
            execution_time=1.0,
            custom_metrics={"custom": 100}
        )
        metrics2 = WorkflowStepMetrics.create_full(
            step_id="step1",
            execution_time=2.0,
            custom_metrics={"custom": 200}
        )
        
        # Aggregate metrics
        aggregated = aggregator.aggregate_metrics([metrics1, metrics2])
        
        # Verify custom metrics aggregation
        assert aggregated.custom_metrics["custom"] == 150  # Average 