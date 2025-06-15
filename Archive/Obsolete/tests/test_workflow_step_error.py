import pytest
from typing import Dict, Any

from ..agents.integration.workflow_step_error import (
    WorkflowStepError,
    WorkflowStepErrorType,
    WorkflowStepErrorHandler
)

class TestWorkflowStepError:
    """Test suite for WorkflowStepError."""
    
    def test_initialization(self):
        """Test proper initialization of step error."""
        error = WorkflowStepError(
            step_id="step1",
            error_type=WorkflowStepErrorType.EXECUTION_ERROR,
            message="Test error message",
            details={
                "error_code": "E001",
                "error_context": "test_context"
            },
            stack_trace="Test stack trace",
            timestamp=1234567890
        )
        
        assert error.step_id == "step1"
        assert error.error_type == WorkflowStepErrorType.EXECUTION_ERROR
        assert error.message == "Test error message"
        assert error.details["error_code"] == "E001"
        assert error.details["error_context"] == "test_context"
        assert error.stack_trace == "Test stack trace"
        assert error.timestamp == 1234567890
    
    def test_error_creation(self):
        """Test creating errors with different types."""
        # Test execution error
        execution_error = WorkflowStepError.create_execution_error(
            step_id="step1",
            message="Execution failed",
            details={"error_code": "E001"}
        )
        assert execution_error.step_id == "step1"
        assert execution_error.error_type == WorkflowStepErrorType.EXECUTION_ERROR
        assert execution_error.message == "Execution failed"
        assert execution_error.details["error_code"] == "E001"
        
        # Test validation error
        validation_error = WorkflowStepError.create_validation_error(
            step_id="step1",
            message="Validation failed",
            details={"error_code": "V001"}
        )
        assert validation_error.step_id == "step1"
        assert validation_error.error_type == WorkflowStepErrorType.VALIDATION_ERROR
        assert validation_error.message == "Validation failed"
        assert validation_error.details["error_code"] == "V001"
        
        # Test timeout error
        timeout_error = WorkflowStepError.create_timeout_error(
            step_id="step1",
            message="Operation timed out",
            details={"timeout": 30}
        )
        assert timeout_error.step_id == "step1"
        assert timeout_error.error_type == WorkflowStepErrorType.TIMEOUT_ERROR
        assert timeout_error.message == "Operation timed out"
        assert timeout_error.details["timeout"] == 30
    
    def test_error_serialization(self):
        """Test serializing error to dictionary."""
        error = WorkflowStepError(
            step_id="step1",
            error_type=WorkflowStepErrorType.EXECUTION_ERROR,
            message="Test error message",
            details={
                "error_code": "E001",
                "error_context": "test_context"
            },
            stack_trace="Test stack trace",
            timestamp=1234567890
        )
        
        serialized = error.to_dict()
        assert serialized["step_id"] == "step1"
        assert serialized["error_type"] == "EXECUTION_ERROR"
        assert serialized["message"] == "Test error message"
        assert serialized["details"]["error_code"] == "E001"
        assert serialized["details"]["error_context"] == "test_context"
        assert serialized["stack_trace"] == "Test stack trace"
        assert serialized["timestamp"] == 1234567890
    
    def test_error_deserialization(self):
        """Test deserializing error from dictionary."""
        data = {
            "step_id": "step1",
            "error_type": "EXECUTION_ERROR",
            "message": "Test error message",
            "details": {
                "error_code": "E001",
                "error_context": "test_context"
            },
            "stack_trace": "Test stack trace",
            "timestamp": 1234567890
        }
        
        error = WorkflowStepError.from_dict(data)
        assert error.step_id == "step1"
        assert error.error_type == WorkflowStepErrorType.EXECUTION_ERROR
        assert error.message == "Test error message"
        assert error.details["error_code"] == "E001"
        assert error.details["error_context"] == "test_context"
        assert error.stack_trace == "Test stack trace"
        assert error.timestamp == 1234567890

class TestWorkflowStepErrorHandler:
    """Test suite for WorkflowStepErrorHandler."""
    
    def test_initialization(self):
        """Test proper initialization of error handler."""
        handler = WorkflowStepErrorHandler()
        assert handler is not None
        assert handler.errors is not None
    
    def test_handle_error(self):
        """Test handling step error."""
        handler = WorkflowStepErrorHandler()
        
        # Handle error
        error = WorkflowStepError.create_execution_error(
            step_id="step1",
            message="Test error"
        )
        handler.handle_error(error)
        
        # Verify error was handled
        handled_error = handler.get_error("step1")
        assert handled_error.step_id == "step1"
        assert handled_error.error_type == WorkflowStepErrorType.EXECUTION_ERROR
        assert handled_error.message == "Test error"
    
    def test_get_error_history(self):
        """Test retrieving error history."""
        handler = WorkflowStepErrorHandler()
        
        # Handle multiple errors
        error1 = WorkflowStepError.create_execution_error(
            step_id="step1",
            message="Error 1"
        )
        error2 = WorkflowStepError.create_execution_error(
            step_id="step1",
            message="Error 2"
        )
        
        handler.handle_error(error1)
        handler.handle_error(error2)
        
        history = handler.get_error_history("step1")
        assert len(history) == 2
        assert history[0].message == "Error 1"
        assert history[1].message == "Error 2"
    
    def test_get_unknown_error(self):
        """Test retrieving error for unknown step."""
        handler = WorkflowStepErrorHandler()
        
        with pytest.raises(KeyError):
            handler.get_error("unknown_step")
    
    def test_get_unknown_error_history(self):
        """Test retrieving error history for unknown step."""
        handler = WorkflowStepErrorHandler()
        
        with pytest.raises(KeyError):
            handler.get_error_history("unknown_step")
    
    def test_clear_error(self):
        """Test clearing step error."""
        handler = WorkflowStepErrorHandler()
        
        # Handle error
        error = WorkflowStepError.create_execution_error(
            step_id="step1",
            message="Test error"
        )
        handler.handle_error(error)
        
        # Clear error
        handler.clear_error("step1")
        with pytest.raises(KeyError):
            handler.get_error("step1")
    
    def test_get_all_errors(self):
        """Test retrieving all handled errors."""
        handler = WorkflowStepErrorHandler()
        
        # Handle errors for multiple steps
        error1 = WorkflowStepError.create_execution_error(
            step_id="step1",
            message="Error 1"
        )
        error2 = WorkflowStepError.create_execution_error(
            step_id="step2",
            message="Error 2"
        )
        
        handler.handle_error(error1)
        handler.handle_error(error2)
        
        all_errors = handler.get_all_errors()
        assert len(all_errors) == 2
        assert all_errors["step1"].message == "Error 1"
        assert all_errors["step2"].message == "Error 2"
    
    def test_get_errors_by_type(self):
        """Test retrieving errors by type."""
        handler = WorkflowStepErrorHandler()
        
        # Handle different types of errors
        execution_error = WorkflowStepError.create_execution_error(
            step_id="step1",
            message="Execution error"
        )
        validation_error = WorkflowStepError.create_validation_error(
            step_id="step2",
            message="Validation error"
        )
        
        handler.handle_error(execution_error)
        handler.handle_error(validation_error)
        
        execution_errors = handler.get_errors_by_type(WorkflowStepErrorType.EXECUTION_ERROR)
        assert len(execution_errors) == 1
        assert execution_errors["step1"].message == "Execution error"
        
        validation_errors = handler.get_errors_by_type(WorkflowStepErrorType.VALIDATION_ERROR)
        assert len(validation_errors) == 1
        assert validation_errors["step2"].message == "Validation error" 