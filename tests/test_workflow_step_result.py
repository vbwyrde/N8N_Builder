import pytest
from typing import Dict, Any

from ..agents.integration.workflow_step_result import (
    WorkflowStepResult,
    WorkflowStepResultType,
    WorkflowStepResultCollector
)

class TestWorkflowStepResult:
    """Test suite for WorkflowStepResult."""
    
    def test_initialization(self):
        """Test proper initialization of step result."""
        result = WorkflowStepResult(
            step_id="step1",
            result_type=WorkflowStepResultType.SUCCESS,
            output={"key": "value"},
            error=None,
            metrics={
                "execution_time": 1.5,
                "memory_usage": 1024
            }
        )
        
        assert result.step_id == "step1"
        assert result.result_type == WorkflowStepResultType.SUCCESS
        assert result.output["key"] == "value"
        assert result.error is None
        assert result.metrics["execution_time"] == 1.5
        assert result.metrics["memory_usage"] == 1024
    
    def test_success_result_creation(self):
        """Test creating a success result."""
        result = WorkflowStepResult.create_success(
            step_id="step1",
            output={"key": "value"},
            metrics={"execution_time": 1.5}
        )
        
        assert result.step_id == "step1"
        assert result.result_type == WorkflowStepResultType.SUCCESS
        assert result.output["key"] == "value"
        assert result.error is None
        assert result.metrics["execution_time"] == 1.5
    
    def test_error_result_creation(self):
        """Test creating an error result."""
        result = WorkflowStepResult.create_error(
            step_id="step1",
            error="Test error",
            metrics={"execution_time": 1.5}
        )
        
        assert result.step_id == "step1"
        assert result.result_type == WorkflowStepResultType.ERROR
        assert result.output is None
        assert result.error == "Test error"
        assert result.metrics["execution_time"] == 1.5
    
    def test_timeout_result_creation(self):
        """Test creating a timeout result."""
        result = WorkflowStepResult.create_timeout(
            step_id="step1",
            metrics={"execution_time": 1.5}
        )
        
        assert result.step_id == "step1"
        assert result.result_type == WorkflowStepResultType.TIMEOUT
        assert result.output is None
        assert "timeout" in result.error.lower()
        assert result.metrics["execution_time"] == 1.5
    
    def test_cancelled_result_creation(self):
        """Test creating a cancelled result."""
        result = WorkflowStepResult.create_cancelled(
            step_id="step1",
            metrics={"execution_time": 1.5}
        )
        
        assert result.step_id == "step1"
        assert result.result_type == WorkflowStepResultType.CANCELLED
        assert result.output is None
        assert "cancelled" in result.error.lower()
        assert result.metrics["execution_time"] == 1.5
    
    def test_result_serialization(self):
        """Test serializing result to dictionary."""
        result = WorkflowStepResult(
            step_id="step1",
            result_type=WorkflowStepResultType.SUCCESS,
            output={"key": "value"},
            error=None,
            metrics={
                "execution_time": 1.5,
                "memory_usage": 1024
            }
        )
        
        serialized = result.to_dict()
        assert serialized["step_id"] == "step1"
        assert serialized["result_type"] == "SUCCESS"
        assert serialized["output"]["key"] == "value"
        assert serialized["error"] is None
        assert serialized["metrics"]["execution_time"] == 1.5
        assert serialized["metrics"]["memory_usage"] == 1024
    
    def test_result_deserialization(self):
        """Test deserializing result from dictionary."""
        data = {
            "step_id": "step1",
            "result_type": "SUCCESS",
            "output": {"key": "value"},
            "error": None,
            "metrics": {
                "execution_time": 1.5,
                "memory_usage": 1024
            }
        }
        
        result = WorkflowStepResult.from_dict(data)
        assert result.step_id == "step1"
        assert result.result_type == WorkflowStepResultType.SUCCESS
        assert result.output["key"] == "value"
        assert result.error is None
        assert result.metrics["execution_time"] == 1.5
        assert result.metrics["memory_usage"] == 1024

class TestWorkflowStepResultCollector:
    """Test suite for WorkflowStepResultCollector."""
    
    def test_initialization(self):
        """Test proper initialization of result collector."""
        collector = WorkflowStepResultCollector()
        assert collector is not None
        assert collector.results is not None
    
    def test_collect_result(self):
        """Test collecting step result."""
        collector = WorkflowStepResultCollector()
        
        # Collect success result
        result = WorkflowStepResult.create_success(
            step_id="step1",
            output={"key": "value"}
        )
        collector.collect_result(result)
        
        # Verify result was collected
        collected_result = collector.get_result("step1")
        assert collected_result.step_id == "step1"
        assert collected_result.result_type == WorkflowStepResultType.SUCCESS
        assert collected_result.output["key"] == "value"
    
    def test_get_result_history(self):
        """Test retrieving result history."""
        collector = WorkflowStepResultCollector()
        
        # Collect multiple results
        result1 = WorkflowStepResult.create_success(
            step_id="step1",
            output={"key": "value1"}
        )
        result2 = WorkflowStepResult.create_success(
            step_id="step1",
            output={"key": "value2"}
        )
        
        collector.collect_result(result1)
        collector.collect_result(result2)
        
        history = collector.get_result_history("step1")
        assert len(history) == 2
        assert history[0].output["key"] == "value1"
        assert history[1].output["key"] == "value2"
    
    def test_get_unknown_result(self):
        """Test retrieving result for unknown step."""
        collector = WorkflowStepResultCollector()
        
        with pytest.raises(KeyError):
            collector.get_result("unknown_step")
    
    def test_get_unknown_result_history(self):
        """Test retrieving result history for unknown step."""
        collector = WorkflowStepResultCollector()
        
        with pytest.raises(KeyError):
            collector.get_result_history("unknown_step")
    
    def test_clear_result(self):
        """Test clearing step result."""
        collector = WorkflowStepResultCollector()
        
        # Collect result
        result = WorkflowStepResult.create_success(
            step_id="step1",
            output={"key": "value"}
        )
        collector.collect_result(result)
        
        # Clear result
        collector.clear_result("step1")
        with pytest.raises(KeyError):
            collector.get_result("step1")
    
    def test_get_all_results(self):
        """Test retrieving all collected results."""
        collector = WorkflowStepResultCollector()
        
        # Collect results for multiple steps
        result1 = WorkflowStepResult.create_success(
            step_id="step1",
            output={"key": "value1"}
        )
        result2 = WorkflowStepResult.create_success(
            step_id="step2",
            output={"key": "value2"}
        )
        
        collector.collect_result(result1)
        collector.collect_result(result2)
        
        all_results = collector.get_all_results()
        assert len(all_results) == 2
        assert all_results["step1"].output["key"] == "value1"
        assert all_results["step2"].output["key"] == "value2"
    
    def test_get_successful_results(self):
        """Test retrieving only successful results."""
        collector = WorkflowStepResultCollector()
        
        # Collect mixed results
        success_result = WorkflowStepResult.create_success(
            step_id="step1",
            output={"key": "value"}
        )
        error_result = WorkflowStepResult.create_error(
            step_id="step2",
            error="Test error"
        )
        
        collector.collect_result(success_result)
        collector.collect_result(error_result)
        
        successful_results = collector.get_successful_results()
        assert len(successful_results) == 1
        assert successful_results["step1"].result_type == WorkflowStepResultType.SUCCESS
    
    def test_get_failed_results(self):
        """Test retrieving only failed results."""
        collector = WorkflowStepResultCollector()
        
        # Collect mixed results
        success_result = WorkflowStepResult.create_success(
            step_id="step1",
            output={"key": "value"}
        )
        error_result = WorkflowStepResult.create_error(
            step_id="step2",
            error="Test error"
        )
        
        collector.collect_result(success_result)
        collector.collect_result(error_result)
        
        failed_results = collector.get_failed_results()
        assert len(failed_results) == 1
        assert failed_results["step2"].result_type == WorkflowStepResultType.ERROR 