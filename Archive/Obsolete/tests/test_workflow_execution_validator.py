import pytest
from typing import Dict, Any, List

from ..agents.integration.workflow_execution_validator import (
    WorkflowExecutionValidator,
    WorkflowExecution,
    WorkflowExecutionResult,
    WorkflowExecutionError
)

class TestWorkflowExecutionValidator:
    """Test suite for WorkflowExecutionValidator."""
    
    def test_initialization(self):
        """Test proper initialization of execution validator."""
        validator = WorkflowExecutionValidator()
        assert validator is not None
    
    def test_validate_execution(self):
        """Test validating execution."""
        validator = WorkflowExecutionValidator()
        
        # Test valid execution
        execution = WorkflowExecution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            status="running",
            start_time="2024-01-01T00:00:00Z",
            end_time=None,
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "running",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": None,
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    }
                }
            }
        )
        
        result = validator.validate_execution(execution)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid execution (missing required fields)
        invalid_execution = WorkflowExecution(
            execution_id="test_execution_1",
            workflow_id="",
            status="",
            start_time=None
        )
        
        result = validator.validate_execution(invalid_execution)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("workflow_id" in error.message for error in result.errors)
        assert any("status" in error.message for error in result.errors)
        assert any("start_time" in error.message for error in result.errors)
    
    def test_validate_execution_steps(self):
        """Test validating execution steps."""
        validator = WorkflowExecutionValidator()
        
        # Test valid steps
        execution = WorkflowExecution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            status="running",
            start_time="2024-01-01T00:00:00Z",
            end_time=None,
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "running",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": None,
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    }
                },
                "step2": {
                    "step_id": "step2",
                    "status": "pending",
                    "start_time": None,
                    "end_time": None,
                    "inputs": {
                        "input2": {
                            "type": "number",
                            "value": 42
                        }
                    }
                }
            }
        )
        
        result = validator.validate_execution_steps(execution)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid steps (missing required fields)
        invalid_execution = WorkflowExecution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            status="running",
            start_time="2024-01-01T00:00:00Z",
            end_time=None,
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "",
                    "start_time": None,
                    "end_time": None,
                    "inputs": {}
                }
            }
        )
        
        result = validator.validate_execution_steps(invalid_execution)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("status" in error.message for error in result.errors)
        assert any("start_time" in error.message for error in result.errors)
    
    def test_validate_execution_result(self):
        """Test validating execution result."""
        validator = WorkflowExecutionValidator()
        
        # Test valid result
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
                    }
                }
            }
        )
        
        validation_result = validator.validate_execution_result(result)
        assert validation_result.is_valid
        assert len(validation_result.errors) == 0
        
        # Test invalid result (missing required fields)
        invalid_result = WorkflowExecutionResult(
            execution_id="test_execution_1",
            workflow_id="",
            status="",
            start_time=None,
            end_time=None
        )
        
        validation_result = validator.validate_execution_result(invalid_result)
        assert not validation_result.is_valid
        assert len(validation_result.errors) > 0
        assert any("workflow_id" in error.message for error in validation_result.errors)
        assert any("status" in error.message for error in validation_result.errors)
        assert any("start_time" in error.message for error in validation_result.errors)
        assert any("end_time" in error.message for error in validation_result.errors)
    
    def test_validate_execution_result_steps(self):
        """Test validating execution result steps."""
        validator = WorkflowExecutionValidator()
        
        # Test valid result steps
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
                    }
                },
                "step2": {
                    "step_id": "step2",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:30Z",
                    "end_time": "2024-01-01T00:01:00Z",
                    "inputs": {
                        "input2": {
                            "type": "number",
                            "value": 42
                        }
                    },
                    "outputs": {
                        "output2": {
                            "type": "number",
                            "value": 84
                        }
                    }
                }
            }
        )
        
        validation_result = validator.validate_execution_result_steps(result)
        assert validation_result.is_valid
        assert len(validation_result.errors) == 0
        
        # Test invalid result steps (missing required fields)
        invalid_result = WorkflowExecutionResult(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            status="completed",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "",
                    "start_time": None,
                    "end_time": None,
                    "inputs": {},
                    "outputs": {}
                }
            }
        )
        
        validation_result = validator.validate_execution_result_steps(invalid_result)
        assert not validation_result.is_valid
        assert len(validation_result.errors) > 0
        assert any("status" in error.message for error in validation_result.errors)
        assert any("start_time" in error.message for error in validation_result.errors)
        assert any("end_time" in error.message for error in validation_result.errors)
    
    def test_validate_execution_error(self):
        """Test validating execution error."""
        validator = WorkflowExecutionValidator()
        
        # Test valid error
        error = WorkflowExecutionError(
            code="execution_failed",
            message="Execution failed due to invalid inputs",
            details={
                "step_id": "step1",
                "reason": "Missing required input"
            }
        )
        
        validation_result = validator.validate_execution_error(error)
        assert validation_result.is_valid
        assert len(validation_result.errors) == 0
        
        # Test invalid error (missing required fields)
        invalid_error = WorkflowExecutionError(
            code="",
            message="",
            details={}
        )
        
        validation_result = validator.validate_execution_error(invalid_error)
        assert not validation_result.is_valid
        assert len(validation_result.errors) > 0
        assert any("code" in error.message for error in validation_result.errors)
        assert any("message" in error.message for error in validation_result.errors)
    
    def test_validate_execution_step_error(self):
        """Test validating execution step error."""
        validator = WorkflowExecutionValidator()
        
        # Test valid step error
        error = WorkflowExecutionError(
            code="step_execution_failed",
            message="Step execution failed",
            details={
                "step_id": "step1",
                "reason": "Timeout exceeded"
            }
        )
        
        validation_result = validator.validate_execution_step_error(error)
        assert validation_result.is_valid
        assert len(validation_result.errors) == 0
        
        # Test invalid step error (missing required fields)
        invalid_error = WorkflowExecutionError(
            code="",
            message="",
            details={}
        )
        
        validation_result = validator.validate_execution_step_error(invalid_error)
        assert not validation_result.is_valid
        assert len(validation_result.errors) > 0
        assert any("code" in error.message for error in validation_result.errors)
        assert any("message" in error.message for error in validation_result.errors)
        assert any("step_id" in error.message for error in validation_result.errors) 