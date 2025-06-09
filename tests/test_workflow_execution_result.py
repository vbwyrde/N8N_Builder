import pytest
from typing import Dict, Any, List

from ..agents.integration.workflow_execution_result import (
    WorkflowExecutionResult,
    WorkflowExecutionError
)

class TestWorkflowExecutionResult:
    """Test suite for WorkflowExecutionResult."""
    
    def test_initialization(self):
        """Test proper initialization of execution result."""
        result = WorkflowExecutionResult(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            status="completed",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:30Z",
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    },
                    "outputs": {
                        "output1": {
                            "type": "string",
                            "value": "test output"
                        }
                    },
                    "parameters": {
                        "param1": {
                            "type": "number",
                            "value": 42
                        }
                    }
                }
            },
            metadata={
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        )
        
        assert result.execution_id == "test_execution_1"
        assert result.workflow_id == "test_workflow_1"
        assert result.status == "completed"
        assert result.start_time == "2024-01-01T00:00:00Z"
        assert result.end_time == "2024-01-01T00:01:00Z"
        assert len(result.steps) == 1
        assert result.steps["step1"]["step_id"] == "step1"
        assert result.steps["step1"]["status"] == "completed"
        assert result.steps["step1"]["start_time"] == "2024-01-01T00:00:00Z"
        assert result.steps["step1"]["end_time"] == "2024-01-01T00:00:30Z"
        assert result.steps["step1"]["inputs"]["input1"]["type"] == "string"
        assert result.steps["step1"]["inputs"]["input1"]["value"] == "test input"
        assert result.steps["step1"]["outputs"]["output1"]["type"] == "string"
        assert result.steps["step1"]["outputs"]["output1"]["value"] == "test output"
        assert result.steps["step1"]["parameters"]["param1"]["type"] == "number"
        assert result.steps["step1"]["parameters"]["param1"]["value"] == 42
        assert result.metadata["author"] == "Test Author"
        assert result.metadata["tags"] == ["test", "example"]
    
    def test_result_creation(self):
        """Test creating results with different configurations."""
        # Test successful result
        success_result = WorkflowExecutionResult.create_success_result(
            execution_id="success_result_1",
            workflow_id="test_workflow_1",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:30Z",
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    },
                    "outputs": {
                        "output1": {
                            "type": "string",
                            "value": "test output"
                        }
                    }
                }
            }
        )
        assert success_result.execution_id == "success_result_1"
        assert success_result.workflow_id == "test_workflow_1"
        assert success_result.status == "completed"
        assert success_result.start_time == "2024-01-01T00:00:00Z"
        assert success_result.end_time == "2024-01-01T00:01:00Z"
        assert len(success_result.steps) == 1
        assert success_result.steps["step1"]["status"] == "completed"
        assert success_result.steps["step1"]["outputs"]["output1"]["value"] == "test output"
        
        # Test failed result
        failed_result = WorkflowExecutionResult.create_failed_result(
            execution_id="failed_result_1",
            workflow_id="test_workflow_1",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            error=WorkflowExecutionError(
                code="execution_failed",
                message="Execution failed due to invalid inputs",
                details={
                    "step_id": "step1",
                    "reason": "Missing required input"
                }
            )
        )
        assert failed_result.execution_id == "failed_result_1"
        assert failed_result.workflow_id == "test_workflow_1"
        assert failed_result.status == "failed"
        assert failed_result.start_time == "2024-01-01T00:00:00Z"
        assert failed_result.end_time == "2024-01-01T00:01:00Z"
        assert failed_result.error.code == "execution_failed"
        assert failed_result.error.message == "Execution failed due to invalid inputs"
        assert failed_result.error.details["step_id"] == "step1"
        assert failed_result.error.details["reason"] == "Missing required input"
    
    def test_result_serialization(self):
        """Test serializing result to dictionary."""
        result = WorkflowExecutionResult(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            status="completed",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:30Z",
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    },
                    "outputs": {
                        "output1": {
                            "type": "string",
                            "value": "test output"
                        }
                    },
                    "parameters": {
                        "param1": {
                            "type": "number",
                            "value": 42
                        }
                    }
                }
            },
            metadata={
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        )
        
        serialized = result.to_dict()
        assert serialized["execution_id"] == "test_execution_1"
        assert serialized["workflow_id"] == "test_workflow_1"
        assert serialized["status"] == "completed"
        assert serialized["start_time"] == "2024-01-01T00:00:00Z"
        assert serialized["end_time"] == "2024-01-01T00:01:00Z"
        assert len(serialized["steps"]) == 1
        assert serialized["steps"]["step1"]["step_id"] == "step1"
        assert serialized["steps"]["step1"]["status"] == "completed"
        assert serialized["steps"]["step1"]["start_time"] == "2024-01-01T00:00:00Z"
        assert serialized["steps"]["step1"]["end_time"] == "2024-01-01T00:00:30Z"
        assert serialized["steps"]["step1"]["inputs"]["input1"]["type"] == "string"
        assert serialized["steps"]["step1"]["inputs"]["input1"]["value"] == "test input"
        assert serialized["steps"]["step1"]["outputs"]["output1"]["type"] == "string"
        assert serialized["steps"]["step1"]["outputs"]["output1"]["value"] == "test output"
        assert serialized["steps"]["step1"]["parameters"]["param1"]["type"] == "number"
        assert serialized["steps"]["step1"]["parameters"]["param1"]["value"] == 42
        assert serialized["metadata"]["author"] == "Test Author"
        assert serialized["metadata"]["tags"] == ["test", "example"]
    
    def test_result_deserialization(self):
        """Test deserializing result from dictionary."""
        data = {
            "execution_id": "test_execution_1",
            "workflow_id": "test_workflow_1",
            "status": "completed",
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": "2024-01-01T00:01:00Z",
            "steps": {
                "step1": {
                    "step_id": "step1",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:30Z",
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    },
                    "outputs": {
                        "output1": {
                            "type": "string",
                            "value": "test output"
                        }
                    },
                    "parameters": {
                        "param1": {
                            "type": "number",
                            "value": 42
                        }
                    }
                }
            },
            "metadata": {
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        }
        
        result = WorkflowExecutionResult.from_dict(data)
        assert result.execution_id == "test_execution_1"
        assert result.workflow_id == "test_workflow_1"
        assert result.status == "completed"
        assert result.start_time == "2024-01-01T00:00:00Z"
        assert result.end_time == "2024-01-01T00:01:00Z"
        assert len(result.steps) == 1
        assert result.steps["step1"]["step_id"] == "step1"
        assert result.steps["step1"]["status"] == "completed"
        assert result.steps["step1"]["start_time"] == "2024-01-01T00:00:00Z"
        assert result.steps["step1"]["end_time"] == "2024-01-01T00:00:30Z"
        assert result.steps["step1"]["inputs"]["input1"]["type"] == "string"
        assert result.steps["step1"]["inputs"]["input1"]["value"] == "test input"
        assert result.steps["step1"]["outputs"]["output1"]["type"] == "string"
        assert result.steps["step1"]["outputs"]["output1"]["value"] == "test output"
        assert result.steps["step1"]["parameters"]["param1"]["type"] == "number"
        assert result.steps["step1"]["parameters"]["param1"]["value"] == 42
        assert result.metadata["author"] == "Test Author"
        assert result.metadata["tags"] == ["test", "example"]

class TestWorkflowExecutionError:
    """Test suite for WorkflowExecutionError."""
    
    def test_initialization(self):
        """Test proper initialization of execution error."""
        error = WorkflowExecutionError(
            code="execution_failed",
            message="Execution failed due to invalid inputs",
            details={
                "step_id": "step1",
                "reason": "Missing required input"
            }
        )
        
        assert error.code == "execution_failed"
        assert error.message == "Execution failed due to invalid inputs"
        assert error.details["step_id"] == "step1"
        assert error.details["reason"] == "Missing required input"
    
    def test_error_creation(self):
        """Test creating errors with different configurations."""
        # Test validation error
        validation_error = WorkflowExecutionError.create_validation_error(
            message="Invalid workflow configuration",
            details={
                "field": "steps",
                "reason": "Missing required step"
            }
        )
        assert validation_error.code == "validation_error"
        assert validation_error.message == "Invalid workflow configuration"
        assert validation_error.details["field"] == "steps"
        assert validation_error.details["reason"] == "Missing required step"
        
        # Test execution error
        execution_error = WorkflowExecutionError.create_execution_error(
            message="Step execution failed",
            details={
                "step_id": "step1",
                "reason": "Timeout exceeded"
            }
        )
        assert execution_error.code == "execution_error"
        assert execution_error.message == "Step execution failed"
        assert execution_error.details["step_id"] == "step1"
        assert execution_error.details["reason"] == "Timeout exceeded"
    
    def test_error_serialization(self):
        """Test serializing error to dictionary."""
        error = WorkflowExecutionError(
            code="execution_failed",
            message="Execution failed due to invalid inputs",
            details={
                "step_id": "step1",
                "reason": "Missing required input"
            }
        )
        
        serialized = error.to_dict()
        assert serialized["code"] == "execution_failed"
        assert serialized["message"] == "Execution failed due to invalid inputs"
        assert serialized["details"]["step_id"] == "step1"
        assert serialized["details"]["reason"] == "Missing required input"
    
    def test_error_deserialization(self):
        """Test deserializing error from dictionary."""
        data = {
            "code": "execution_failed",
            "message": "Execution failed due to invalid inputs",
            "details": {
                "step_id": "step1",
                "reason": "Missing required input"
            }
        }
        
        error = WorkflowExecutionError.from_dict(data)
        assert error.code == "execution_failed"
        assert error.message == "Execution failed due to invalid inputs"
        assert error.details["step_id"] == "step1"
        assert error.details["reason"] == "Missing required input" 