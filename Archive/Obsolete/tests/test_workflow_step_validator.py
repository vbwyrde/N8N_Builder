import pytest
from typing import Dict, Any, List

from ..agents.integration.workflow_step_validator import (
    WorkflowStepValidator,
    WorkflowStepValidationResult,
    WorkflowStepValidationError
)

class TestWorkflowStepValidator:
    """Test suite for WorkflowStepValidator."""
    
    def test_initialization(self):
        """Test proper initialization of step validator."""
        validator = WorkflowStepValidator()
        assert validator is not None
    
    def test_validate_step_type(self):
        """Test validating step type."""
        validator = WorkflowStepValidator()
        
        # Test valid step type
        step_type = {
            "name": "test_step",
            "description": "Test step type",
            "version": "1.0.0",
            "category": "test",
            "inputs": {
                "input1": {
                    "type": "string",
                    "required": True
                }
            },
            "outputs": {
                "output1": {
                    "type": "string"
                }
            },
            "parameters": {
                "param1": {
                    "type": "number",
                    "required": True
                }
            }
        }
        
        result = validator.validate_step_type(step_type)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid step type (missing required fields)
        invalid_step_type = {
            "name": "test_step"
        }
        
        result = validator.validate_step_type(invalid_step_type)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("description" in error.message for error in result.errors)
        assert any("version" in error.message for error in result.errors)
    
    def test_validate_step_inputs(self):
        """Test validating step inputs."""
        validator = WorkflowStepValidator()
        
        # Test valid inputs
        step_type = {
            "inputs": {
                "input1": {
                    "type": "string",
                    "required": True
                },
                "input2": {
                    "type": "number",
                    "required": False
                }
            }
        }
        
        inputs = {
            "input1": "test value",
            "input2": 42
        }
        
        result = validator.validate_step_inputs(step_type, inputs)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test missing required input
        inputs = {
            "input2": 42
        }
        
        result = validator.validate_step_inputs(step_type, inputs)
        assert not result.is_valid
        assert len(result.errors) == 1
        assert "input1" in result.errors[0].message
        
        # Test invalid input type
        inputs = {
            "input1": 42,
            "input2": "test value"
        }
        
        result = validator.validate_step_inputs(step_type, inputs)
        assert not result.is_valid
        assert len(result.errors) == 2
        assert any("input1" in error.message for error in result.errors)
        assert any("input2" in error.message for error in result.errors)
    
    def test_validate_step_outputs(self):
        """Test validating step outputs."""
        validator = WorkflowStepValidator()
        
        # Test valid outputs
        step_type = {
            "outputs": {
                "output1": {
                    "type": "string"
                },
                "output2": {
                    "type": "number"
                }
            }
        }
        
        outputs = {
            "output1": "test value",
            "output2": 42
        }
        
        result = validator.validate_step_outputs(step_type, outputs)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid output type
        outputs = {
            "output1": 42,
            "output2": "test value"
        }
        
        result = validator.validate_step_outputs(step_type, outputs)
        assert not result.is_valid
        assert len(result.errors) == 2
        assert any("output1" in error.message for error in result.errors)
        assert any("output2" in error.message for error in result.errors)
    
    def test_validate_step_parameters(self):
        """Test validating step parameters."""
        validator = WorkflowStepValidator()
        
        # Test valid parameters
        step_type = {
            "parameters": {
                "param1": {
                    "type": "string",
                    "required": True
                },
                "param2": {
                    "type": "number",
                    "required": False
                }
            }
        }
        
        parameters = {
            "param1": "test value",
            "param2": 42
        }
        
        result = validator.validate_step_parameters(step_type, parameters)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test missing required parameter
        parameters = {
            "param2": 42
        }
        
        result = validator.validate_step_parameters(step_type, parameters)
        assert not result.is_valid
        assert len(result.errors) == 1
        assert "param1" in result.errors[0].message
        
        # Test invalid parameter type
        parameters = {
            "param1": 42,
            "param2": "test value"
        }
        
        result = validator.validate_step_parameters(step_type, parameters)
        assert not result.is_valid
        assert len(result.errors) == 2
        assert any("param1" in error.message for error in result.errors)
        assert any("param2" in error.message for error in result.errors)
    
    def test_validate_step_transitions(self):
        """Test validating step transitions."""
        validator = WorkflowStepValidator()
        
        # Test valid transitions
        step_type = {
            "transitions": {
                "success": {
                    "to": "next_step",
                    "condition": "result.status == 'success'"
                },
                "error": {
                    "to": "error_handler",
                    "condition": "result.error is not None"
                }
            }
        }
        
        transitions = [
            {
                "from_step_id": "step1",
                "to_step_id": "next_step",
                "transition_type": "SUCCESS",
                "condition": "result.status == 'success'"
            },
            {
                "from_step_id": "step1",
                "to_step_id": "error_handler",
                "transition_type": "ERROR",
                "condition": "result.error is not None"
            }
        ]
        
        result = validator.validate_step_transitions(step_type, transitions)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid transition (missing required field)
        transitions = [
            {
                "from_step_id": "step1",
                "to_step_id": "next_step"
            }
        ]
        
        result = validator.validate_step_transitions(step_type, transitions)
        assert not result.is_valid
        assert len(result.errors) == 1
        assert "transition_type" in result.errors[0].message
        
        # Test invalid transition (unknown type)
        transitions = [
            {
                "from_step_id": "step1",
                "to_step_id": "next_step",
                "transition_type": "UNKNOWN",
                "condition": "result.status == 'success'"
            }
        ]
        
        result = validator.validate_step_transitions(step_type, transitions)
        assert not result.is_valid
        assert len(result.errors) == 1
        assert "UNKNOWN" in result.errors[0].message

class TestWorkflowStepValidationResult:
    """Test suite for WorkflowStepValidationResult."""
    
    def test_initialization(self):
        """Test proper initialization of validation result."""
        result = WorkflowStepValidationResult()
        assert result is not None
        assert result.is_valid
        assert len(result.errors) == 0
    
    def test_add_error(self):
        """Test adding validation error."""
        result = WorkflowStepValidationResult()
        
        error = WorkflowStepValidationError(
            message="Test error message",
            field="test_field",
            value="test_value"
        )
        
        result.add_error(error)
        assert not result.is_valid
        assert len(result.errors) == 1
        assert result.errors[0].message == "Test error message"
        assert result.errors[0].field == "test_field"
        assert result.errors[0].value == "test_value"
    
    def test_clear_errors(self):
        """Test clearing validation errors."""
        result = WorkflowStepValidationResult()
        
        error = WorkflowStepValidationError(
            message="Test error message",
            field="test_field",
            value="test_value"
        )
        
        result.add_error(error)
        assert not result.is_valid
        assert len(result.errors) == 1
        
        result.clear_errors()
        assert result.is_valid
        assert len(result.errors) == 0
    
    def test_to_dict(self):
        """Test converting validation result to dictionary."""
        result = WorkflowStepValidationResult()
        
        error = WorkflowStepValidationError(
            message="Test error message",
            field="test_field",
            value="test_value"
        )
        
        result.add_error(error)
        
        data = result.to_dict()
        assert data["is_valid"] is False
        assert len(data["errors"]) == 1
        assert data["errors"][0]["message"] == "Test error message"
        assert data["errors"][0]["field"] == "test_field"
        assert data["errors"][0]["value"] == "test_value"

class TestWorkflowStepValidationError:
    """Test suite for WorkflowStepValidationError."""
    
    def test_initialization(self):
        """Test proper initialization of validation error."""
        error = WorkflowStepValidationError(
            message="Test error message",
            field="test_field",
            value="test_value"
        )
        
        assert error.message == "Test error message"
        assert error.field == "test_field"
        assert error.value == "test_value"
    
    def test_to_dict(self):
        """Test converting validation error to dictionary."""
        error = WorkflowStepValidationError(
            message="Test error message",
            field="test_field",
            value="test_value"
        )
        
        data = error.to_dict()
        assert data["message"] == "Test error message"
        assert data["field"] == "test_field"
        assert data["value"] == "test_value"
    
    def test_str_representation(self):
        """Test string representation of validation error."""
        error = WorkflowStepValidationError(
            message="Test error message",
            field="test_field",
            value="test_value"
        )
        
        error_str = str(error)
        assert "Test error message" in error_str
        assert "test_field" in error_str
        assert "test_value" in error_str 