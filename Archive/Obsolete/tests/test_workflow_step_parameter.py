import pytest
from typing import Dict, Any, List

from ..agents.integration.workflow_step_parameter import (
    WorkflowStepParameter,
    WorkflowStepParameterType,
    WorkflowStepParameterValidator
)

class TestWorkflowStepParameter:
    """Test suite for WorkflowStepParameter."""
    
    def test_initialization(self):
        """Test proper initialization of step parameter."""
        parameter = WorkflowStepParameter(
            step_id="step1",
            parameter_type=WorkflowStepParameterType.STRING,
            name="test_param",
            value="test value",
            metadata={
                "description": "Test parameter",
                "required": True
            },
            validation_rules={
                "min_length": 1,
                "max_length": 100
            }
        )
        
        assert parameter.step_id == "step1"
        assert parameter.parameter_type == WorkflowStepParameterType.STRING
        assert parameter.name == "test_param"
        assert parameter.value == "test value"
        assert parameter.metadata["description"] == "Test parameter"
        assert parameter.metadata["required"] is True
        assert parameter.validation_rules["min_length"] == 1
        assert parameter.validation_rules["max_length"] == 100
    
    def test_parameter_creation(self):
        """Test creating parameters with different types."""
        # Test string parameter
        string_param = WorkflowStepParameter.create_string_parameter(
            step_id="step1",
            name="string_param",
            value="test string",
            required=True
        )
        assert string_param.step_id == "step1"
        assert string_param.parameter_type == WorkflowStepParameterType.STRING
        assert string_param.name == "string_param"
        assert string_param.value == "test string"
        assert string_param.metadata["required"] is True
        
        # Test number parameter
        number_param = WorkflowStepParameter.create_number_parameter(
            step_id="step1",
            name="number_param",
            value=42,
            min_value=0,
            max_value=100
        )
        assert number_param.step_id == "step1"
        assert number_param.parameter_type == WorkflowStepParameterType.NUMBER
        assert number_param.name == "number_param"
        assert number_param.value == 42
        assert number_param.validation_rules["min_value"] == 0
        assert number_param.validation_rules["max_value"] == 100
        
        # Test boolean parameter
        boolean_param = WorkflowStepParameter.create_boolean_parameter(
            step_id="step1",
            name="boolean_param",
            value=True
        )
        assert boolean_param.step_id == "step1"
        assert boolean_param.parameter_type == WorkflowStepParameterType.BOOLEAN
        assert boolean_param.name == "boolean_param"
        assert boolean_param.value is True
        
        # Test array parameter
        array_param = WorkflowStepParameter.create_array_parameter(
            step_id="step1",
            name="array_param",
            value=["item1", "item2"],
            min_items=1,
            max_items=10
        )
        assert array_param.step_id == "step1"
        assert array_param.parameter_type == WorkflowStepParameterType.ARRAY
        assert array_param.name == "array_param"
        assert array_param.value == ["item1", "item2"]
        assert array_param.validation_rules["min_items"] == 1
        assert array_param.validation_rules["max_items"] == 10
        
        # Test object parameter
        object_param = WorkflowStepParameter.create_object_parameter(
            step_id="step1",
            name="object_param",
            value={"key": "value"},
            required_properties=["key"]
        )
        assert object_param.step_id == "step1"
        assert object_param.parameter_type == WorkflowStepParameterType.OBJECT
        assert object_param.name == "object_param"
        assert object_param.value == {"key": "value"}
        assert object_param.validation_rules["required_properties"] == ["key"]
    
    def test_parameter_serialization(self):
        """Test serializing parameter to dictionary."""
        parameter = WorkflowStepParameter(
            step_id="step1",
            parameter_type=WorkflowStepParameterType.STRING,
            name="test_param",
            value="test value",
            metadata={
                "description": "Test parameter",
                "required": True
            },
            validation_rules={
                "min_length": 1,
                "max_length": 100
            }
        )
        
        serialized = parameter.to_dict()
        assert serialized["step_id"] == "step1"
        assert serialized["parameter_type"] == "STRING"
        assert serialized["name"] == "test_param"
        assert serialized["value"] == "test value"
        assert serialized["metadata"]["description"] == "Test parameter"
        assert serialized["metadata"]["required"] is True
        assert serialized["validation_rules"]["min_length"] == 1
        assert serialized["validation_rules"]["max_length"] == 100
    
    def test_parameter_deserialization(self):
        """Test deserializing parameter from dictionary."""
        data = {
            "step_id": "step1",
            "parameter_type": "STRING",
            "name": "test_param",
            "value": "test value",
            "metadata": {
                "description": "Test parameter",
                "required": True
            },
            "validation_rules": {
                "min_length": 1,
                "max_length": 100
            }
        }
        
        parameter = WorkflowStepParameter.from_dict(data)
        assert parameter.step_id == "step1"
        assert parameter.parameter_type == WorkflowStepParameterType.STRING
        assert parameter.name == "test_param"
        assert parameter.value == "test value"
        assert parameter.metadata["description"] == "Test parameter"
        assert parameter.metadata["required"] is True
        assert parameter.validation_rules["min_length"] == 1
        assert parameter.validation_rules["max_length"] == 100

class TestWorkflowStepParameterValidator:
    """Test suite for WorkflowStepParameterValidator."""
    
    def test_initialization(self):
        """Test proper initialization of parameter validator."""
        validator = WorkflowStepParameterValidator()
        assert validator is not None
    
    def test_validate_string_parameter(self):
        """Test validating string parameter."""
        validator = WorkflowStepParameterValidator()
        
        # Test valid string parameter
        parameter = WorkflowStepParameter.create_string_parameter(
            step_id="step1",
            name="string_param",
            value="test string",
            min_length=1,
            max_length=100
        )
        assert validator.validate(parameter) is True
        
        # Test invalid string parameter (too short)
        parameter = WorkflowStepParameter.create_string_parameter(
            step_id="step1",
            name="string_param",
            value="",
            min_length=1,
            max_length=100
        )
        assert validator.validate(parameter) is False
        
        # Test invalid string parameter (too long)
        parameter = WorkflowStepParameter.create_string_parameter(
            step_id="step1",
            name="string_param",
            value="x" * 101,
            min_length=1,
            max_length=100
        )
        assert validator.validate(parameter) is False
    
    def test_validate_number_parameter(self):
        """Test validating number parameter."""
        validator = WorkflowStepParameterValidator()
        
        # Test valid number parameter
        parameter = WorkflowStepParameter.create_number_parameter(
            step_id="step1",
            name="number_param",
            value=42,
            min_value=0,
            max_value=100
        )
        assert validator.validate(parameter) is True
        
        # Test invalid number parameter (too small)
        parameter = WorkflowStepParameter.create_number_parameter(
            step_id="step1",
            name="number_param",
            value=-1,
            min_value=0,
            max_value=100
        )
        assert validator.validate(parameter) is False
        
        # Test invalid number parameter (too large)
        parameter = WorkflowStepParameter.create_number_parameter(
            step_id="step1",
            name="number_param",
            value=101,
            min_value=0,
            max_value=100
        )
        assert validator.validate(parameter) is False
    
    def test_validate_array_parameter(self):
        """Test validating array parameter."""
        validator = WorkflowStepParameterValidator()
        
        # Test valid array parameter
        parameter = WorkflowStepParameter.create_array_parameter(
            step_id="step1",
            name="array_param",
            value=["item1", "item2"],
            min_items=1,
            max_items=10
        )
        assert validator.validate(parameter) is True
        
        # Test invalid array parameter (too few items)
        parameter = WorkflowStepParameter.create_array_parameter(
            step_id="step1",
            name="array_param",
            value=[],
            min_items=1,
            max_items=10
        )
        assert validator.validate(parameter) is False
        
        # Test invalid array parameter (too many items)
        parameter = WorkflowStepParameter.create_array_parameter(
            step_id="step1",
            name="array_param",
            value=["item"] * 11,
            min_items=1,
            max_items=10
        )
        assert validator.validate(parameter) is False
    
    def test_validate_object_parameter(self):
        """Test validating object parameter."""
        validator = WorkflowStepParameterValidator()
        
        # Test valid object parameter
        parameter = WorkflowStepParameter.create_object_parameter(
            step_id="step1",
            name="object_param",
            value={"key": "value"},
            required_properties=["key"]
        )
        assert validator.validate(parameter) is True
        
        # Test invalid object parameter (missing required property)
        parameter = WorkflowStepParameter.create_object_parameter(
            step_id="step1",
            name="object_param",
            value={},
            required_properties=["key"]
        )
        assert validator.validate(parameter) is False
    
    def test_validate_required_parameter(self):
        """Test validating required parameter."""
        validator = WorkflowStepParameterValidator()
        
        # Test valid required parameter
        parameter = WorkflowStepParameter.create_string_parameter(
            step_id="step1",
            name="required_param",
            value="test string",
            required=True
        )
        assert validator.validate(parameter) is True
        
        # Test invalid required parameter (missing value)
        parameter = WorkflowStepParameter.create_string_parameter(
            step_id="step1",
            name="required_param",
            value=None,
            required=True
        )
        assert validator.validate(parameter) is False
    
    def test_validate_unknown_parameter_type(self):
        """Test validating parameter with unknown type."""
        validator = WorkflowStepParameterValidator()
        
        parameter = WorkflowStepParameter(
            step_id="step1",
            parameter_type="UNKNOWN",
            name="unknown_param",
            value="test value"
        )
        
        with pytest.raises(ValueError):
            validator.validate(parameter) 