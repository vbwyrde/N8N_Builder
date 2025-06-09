import pytest
from typing import Dict, Any, List

from ..agents.integration.workflow_step_output import (
    WorkflowStepOutput,
    WorkflowStepOutputType,
    WorkflowStepOutputValidator
)

class TestWorkflowStepOutput:
    """Test suite for WorkflowStepOutput."""
    
    def test_initialization(self):
        """Test proper initialization of step output."""
        output_data = WorkflowStepOutput(
            step_id="step1",
            output_type=WorkflowStepOutputType.STRING,
            value="test value",
            metadata={
                "description": "Test output",
                "format": "text"
            },
            validation_rules={
                "min_length": 1,
                "max_length": 100
            }
        )
        
        assert output_data.step_id == "step1"
        assert output_data.output_type == WorkflowStepOutputType.STRING
        assert output_data.value == "test value"
        assert output_data.metadata["description"] == "Test output"
        assert output_data.metadata["format"] == "text"
        assert output_data.validation_rules["min_length"] == 1
        assert output_data.validation_rules["max_length"] == 100
    
    def test_output_creation(self):
        """Test creating outputs with different types."""
        # Test string output
        string_output = WorkflowStepOutput.create_string_output(
            step_id="step1",
            value="test string",
            format="text"
        )
        assert string_output.step_id == "step1"
        assert string_output.output_type == WorkflowStepOutputType.STRING
        assert string_output.value == "test string"
        assert string_output.metadata["format"] == "text"
        
        # Test number output
        number_output = WorkflowStepOutput.create_number_output(
            step_id="step1",
            value=42,
            format="integer"
        )
        assert number_output.step_id == "step1"
        assert number_output.output_type == WorkflowStepOutputType.NUMBER
        assert number_output.value == 42
        assert number_output.metadata["format"] == "integer"
        
        # Test boolean output
        boolean_output = WorkflowStepOutput.create_boolean_output(
            step_id="step1",
            value=True
        )
        assert boolean_output.step_id == "step1"
        assert boolean_output.output_type == WorkflowStepOutputType.BOOLEAN
        assert boolean_output.value is True
        
        # Test array output
        array_output = WorkflowStepOutput.create_array_output(
            step_id="step1",
            value=["item1", "item2"],
            item_type="string"
        )
        assert array_output.step_id == "step1"
        assert array_output.output_type == WorkflowStepOutputType.ARRAY
        assert array_output.value == ["item1", "item2"]
        assert array_output.metadata["item_type"] == "string"
        
        # Test object output
        object_output = WorkflowStepOutput.create_object_output(
            step_id="step1",
            value={"key": "value"},
            schema={"type": "object"}
        )
        assert object_output.step_id == "step1"
        assert object_output.output_type == WorkflowStepOutputType.OBJECT
        assert object_output.value == {"key": "value"}
        assert object_output.metadata["schema"] == {"type": "object"}
    
    def test_output_serialization(self):
        """Test serializing output to dictionary."""
        output_data = WorkflowStepOutput(
            step_id="step1",
            output_type=WorkflowStepOutputType.STRING,
            value="test value",
            metadata={
                "description": "Test output",
                "format": "text"
            },
            validation_rules={
                "min_length": 1,
                "max_length": 100
            }
        )
        
        serialized = output_data.to_dict()
        assert serialized["step_id"] == "step1"
        assert serialized["output_type"] == "STRING"
        assert serialized["value"] == "test value"
        assert serialized["metadata"]["description"] == "Test output"
        assert serialized["metadata"]["format"] == "text"
        assert serialized["validation_rules"]["min_length"] == 1
        assert serialized["validation_rules"]["max_length"] == 100
    
    def test_output_deserialization(self):
        """Test deserializing output from dictionary."""
        data = {
            "step_id": "step1",
            "output_type": "STRING",
            "value": "test value",
            "metadata": {
                "description": "Test output",
                "format": "text"
            },
            "validation_rules": {
                "min_length": 1,
                "max_length": 100
            }
        }
        
        output_data = WorkflowStepOutput.from_dict(data)
        assert output_data.step_id == "step1"
        assert output_data.output_type == WorkflowStepOutputType.STRING
        assert output_data.value == "test value"
        assert output_data.metadata["description"] == "Test output"
        assert output_data.metadata["format"] == "text"
        assert output_data.validation_rules["min_length"] == 1
        assert output_data.validation_rules["max_length"] == 100

class TestWorkflowStepOutputValidator:
    """Test suite for WorkflowStepOutputValidator."""
    
    def test_initialization(self):
        """Test proper initialization of output validator."""
        validator = WorkflowStepOutputValidator()
        assert validator is not None
    
    def test_validate_string_output(self):
        """Test validating string output."""
        validator = WorkflowStepOutputValidator()
        
        # Test valid string output
        output_data = WorkflowStepOutput.create_string_output(
            step_id="step1",
            value="test string",
            min_length=1,
            max_length=100
        )
        assert validator.validate(output_data) is True
        
        # Test invalid string output (too short)
        output_data = WorkflowStepOutput.create_string_output(
            step_id="step1",
            value="",
            min_length=1,
            max_length=100
        )
        assert validator.validate(output_data) is False
        
        # Test invalid string output (too long)
        output_data = WorkflowStepOutput.create_string_output(
            step_id="step1",
            value="x" * 101,
            min_length=1,
            max_length=100
        )
        assert validator.validate(output_data) is False
    
    def test_validate_number_output(self):
        """Test validating number output."""
        validator = WorkflowStepOutputValidator()
        
        # Test valid number output
        output_data = WorkflowStepOutput.create_number_output(
            step_id="step1",
            value=42,
            min_value=0,
            max_value=100
        )
        assert validator.validate(output_data) is True
        
        # Test invalid number output (too small)
        output_data = WorkflowStepOutput.create_number_output(
            step_id="step1",
            value=-1,
            min_value=0,
            max_value=100
        )
        assert validator.validate(output_data) is False
        
        # Test invalid number output (too large)
        output_data = WorkflowStepOutput.create_number_output(
            step_id="step1",
            value=101,
            min_value=0,
            max_value=100
        )
        assert validator.validate(output_data) is False
    
    def test_validate_array_output(self):
        """Test validating array output."""
        validator = WorkflowStepOutputValidator()
        
        # Test valid array output
        output_data = WorkflowStepOutput.create_array_output(
            step_id="step1",
            value=["item1", "item2"],
            min_items=1,
            max_items=10
        )
        assert validator.validate(output_data) is True
        
        # Test invalid array output (too few items)
        output_data = WorkflowStepOutput.create_array_output(
            step_id="step1",
            value=[],
            min_items=1,
            max_items=10
        )
        assert validator.validate(output_data) is False
        
        # Test invalid array output (too many items)
        output_data = WorkflowStepOutput.create_array_output(
            step_id="step1",
            value=["item"] * 11,
            min_items=1,
            max_items=10
        )
        assert validator.validate(output_data) is False
    
    def test_validate_object_output(self):
        """Test validating object output."""
        validator = WorkflowStepOutputValidator()
        
        # Test valid object output
        output_data = WorkflowStepOutput.create_object_output(
            step_id="step1",
            value={"key": "value"},
            required_properties=["key"]
        )
        assert validator.validate(output_data) is True
        
        # Test invalid object output (missing required property)
        output_data = WorkflowStepOutput.create_object_output(
            step_id="step1",
            value={},
            required_properties=["key"]
        )
        assert validator.validate(output_data) is False
    
    def test_validate_unknown_output_type(self):
        """Test validating output with unknown type."""
        validator = WorkflowStepOutputValidator()
        
        output_data = WorkflowStepOutput(
            step_id="step1",
            output_type="UNKNOWN",
            value="test value"
        )
        
        with pytest.raises(ValueError):
            validator.validate(output_data) 