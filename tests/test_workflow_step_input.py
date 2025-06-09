import pytest
from typing import Dict, Any, List

from ..agents.integration.workflow_step_input import (
    WorkflowStepInput,
    WorkflowStepInputType,
    WorkflowStepInputValidator
)

class TestWorkflowStepInput:
    """Test suite for WorkflowStepInput."""
    
    def test_initialization(self):
        """Test proper initialization of step input."""
        input_data = WorkflowStepInput(
            step_id="step1",
            input_type=WorkflowStepInputType.STRING,
            value="test value",
            metadata={
                "description": "Test input",
                "required": True
            },
            validation_rules={
                "min_length": 1,
                "max_length": 100
            }
        )
        
        assert input_data.step_id == "step1"
        assert input_data.input_type == WorkflowStepInputType.STRING
        assert input_data.value == "test value"
        assert input_data.metadata["description"] == "Test input"
        assert input_data.metadata["required"] is True
        assert input_data.validation_rules["min_length"] == 1
        assert input_data.validation_rules["max_length"] == 100
    
    def test_input_creation(self):
        """Test creating inputs with different types."""
        # Test string input
        string_input = WorkflowStepInput.create_string_input(
            step_id="step1",
            value="test string",
            required=True
        )
        assert string_input.step_id == "step1"
        assert string_input.input_type == WorkflowStepInputType.STRING
        assert string_input.value == "test string"
        assert string_input.metadata["required"] is True
        
        # Test number input
        number_input = WorkflowStepInput.create_number_input(
            step_id="step1",
            value=42,
            min_value=0,
            max_value=100
        )
        assert number_input.step_id == "step1"
        assert number_input.input_type == WorkflowStepInputType.NUMBER
        assert number_input.value == 42
        assert number_input.validation_rules["min_value"] == 0
        assert number_input.validation_rules["max_value"] == 100
        
        # Test boolean input
        boolean_input = WorkflowStepInput.create_boolean_input(
            step_id="step1",
            value=True
        )
        assert boolean_input.step_id == "step1"
        assert boolean_input.input_type == WorkflowStepInputType.BOOLEAN
        assert boolean_input.value is True
        
        # Test array input
        array_input = WorkflowStepInput.create_array_input(
            step_id="step1",
            value=["item1", "item2"],
            min_items=1,
            max_items=10
        )
        assert array_input.step_id == "step1"
        assert array_input.input_type == WorkflowStepInputType.ARRAY
        assert array_input.value == ["item1", "item2"]
        assert array_input.validation_rules["min_items"] == 1
        assert array_input.validation_rules["max_items"] == 10
        
        # Test object input
        object_input = WorkflowStepInput.create_object_input(
            step_id="step1",
            value={"key": "value"},
            required_properties=["key"]
        )
        assert object_input.step_id == "step1"
        assert object_input.input_type == WorkflowStepInputType.OBJECT
        assert object_input.value == {"key": "value"}
        assert object_input.validation_rules["required_properties"] == ["key"]
    
    def test_input_serialization(self):
        """Test serializing input to dictionary."""
        input_data = WorkflowStepInput(
            step_id="step1",
            input_type=WorkflowStepInputType.STRING,
            value="test value",
            metadata={
                "description": "Test input",
                "required": True
            },
            validation_rules={
                "min_length": 1,
                "max_length": 100
            }
        )
        
        serialized = input_data.to_dict()
        assert serialized["step_id"] == "step1"
        assert serialized["input_type"] == "STRING"
        assert serialized["value"] == "test value"
        assert serialized["metadata"]["description"] == "Test input"
        assert serialized["metadata"]["required"] is True
        assert serialized["validation_rules"]["min_length"] == 1
        assert serialized["validation_rules"]["max_length"] == 100
    
    def test_input_deserialization(self):
        """Test deserializing input from dictionary."""
        data = {
            "step_id": "step1",
            "input_type": "STRING",
            "value": "test value",
            "metadata": {
                "description": "Test input",
                "required": True
            },
            "validation_rules": {
                "min_length": 1,
                "max_length": 100
            }
        }
        
        input_data = WorkflowStepInput.from_dict(data)
        assert input_data.step_id == "step1"
        assert input_data.input_type == WorkflowStepInputType.STRING
        assert input_data.value == "test value"
        assert input_data.metadata["description"] == "Test input"
        assert input_data.metadata["required"] is True
        assert input_data.validation_rules["min_length"] == 1
        assert input_data.validation_rules["max_length"] == 100

class TestWorkflowStepInputValidator:
    """Test suite for WorkflowStepInputValidator."""
    
    def test_initialization(self):
        """Test proper initialization of input validator."""
        validator = WorkflowStepInputValidator()
        assert validator is not None
    
    def test_validate_string_input(self):
        """Test validating string input."""
        validator = WorkflowStepInputValidator()
        
        # Test valid string input
        input_data = WorkflowStepInput.create_string_input(
            step_id="step1",
            value="test string",
            min_length=1,
            max_length=100
        )
        assert validator.validate(input_data) is True
        
        # Test invalid string input (too short)
        input_data = WorkflowStepInput.create_string_input(
            step_id="step1",
            value="",
            min_length=1,
            max_length=100
        )
        assert validator.validate(input_data) is False
        
        # Test invalid string input (too long)
        input_data = WorkflowStepInput.create_string_input(
            step_id="step1",
            value="x" * 101,
            min_length=1,
            max_length=100
        )
        assert validator.validate(input_data) is False
    
    def test_validate_number_input(self):
        """Test validating number input."""
        validator = WorkflowStepInputValidator()
        
        # Test valid number input
        input_data = WorkflowStepInput.create_number_input(
            step_id="step1",
            value=42,
            min_value=0,
            max_value=100
        )
        assert validator.validate(input_data) is True
        
        # Test invalid number input (too small)
        input_data = WorkflowStepInput.create_number_input(
            step_id="step1",
            value=-1,
            min_value=0,
            max_value=100
        )
        assert validator.validate(input_data) is False
        
        # Test invalid number input (too large)
        input_data = WorkflowStepInput.create_number_input(
            step_id="step1",
            value=101,
            min_value=0,
            max_value=100
        )
        assert validator.validate(input_data) is False
    
    def test_validate_array_input(self):
        """Test validating array input."""
        validator = WorkflowStepInputValidator()
        
        # Test valid array input
        input_data = WorkflowStepInput.create_array_input(
            step_id="step1",
            value=["item1", "item2"],
            min_items=1,
            max_items=10
        )
        assert validator.validate(input_data) is True
        
        # Test invalid array input (too few items)
        input_data = WorkflowStepInput.create_array_input(
            step_id="step1",
            value=[],
            min_items=1,
            max_items=10
        )
        assert validator.validate(input_data) is False
        
        # Test invalid array input (too many items)
        input_data = WorkflowStepInput.create_array_input(
            step_id="step1",
            value=["item"] * 11,
            min_items=1,
            max_items=10
        )
        assert validator.validate(input_data) is False
    
    def test_validate_object_input(self):
        """Test validating object input."""
        validator = WorkflowStepInputValidator()
        
        # Test valid object input
        input_data = WorkflowStepInput.create_object_input(
            step_id="step1",
            value={"key": "value"},
            required_properties=["key"]
        )
        assert validator.validate(input_data) is True
        
        # Test invalid object input (missing required property)
        input_data = WorkflowStepInput.create_object_input(
            step_id="step1",
            value={},
            required_properties=["key"]
        )
        assert validator.validate(input_data) is False
    
    def test_validate_required_input(self):
        """Test validating required input."""
        validator = WorkflowStepInputValidator()
        
        # Test valid required input
        input_data = WorkflowStepInput.create_string_input(
            step_id="step1",
            value="test string",
            required=True
        )
        assert validator.validate(input_data) is True
        
        # Test invalid required input (missing value)
        input_data = WorkflowStepInput.create_string_input(
            step_id="step1",
            value=None,
            required=True
        )
        assert validator.validate(input_data) is False
    
    def test_validate_unknown_input_type(self):
        """Test validating input with unknown type."""
        validator = WorkflowStepInputValidator()
        
        input_data = WorkflowStepInput(
            step_id="step1",
            input_type="UNKNOWN",
            value="test value"
        )
        
        with pytest.raises(ValueError):
            validator.validate(input_data) 