import pytest
from enum import Enum
from typing import Dict, Any, List

from ..agents.integration.workflow_step_type import (
    WorkflowStepType,
    WorkflowStepTypeConfig,
    WorkflowStepTypeValidator,
    WorkflowStepTypeRegistry
)

class TestWorkflowStepType:
    """Test suite for WorkflowStepType."""
    
    def test_enum_values(self):
        """Test that all expected step types are defined."""
        assert WorkflowStepType.ACTION in WorkflowStepType
        assert WorkflowStepType.CONDITION in WorkflowStepType
        assert WorkflowStepType.LOOP in WorkflowStepType
        assert WorkflowStepType.PARALLEL in WorkflowStepType
        assert WorkflowStepType.WAIT in WorkflowStepType
        assert WorkflowStepType.TRIGGER in WorkflowStepType
    
    def test_enum_comparison(self):
        """Test step type comparison operations."""
        assert WorkflowStepType.ACTION == WorkflowStepType.ACTION
        assert WorkflowStepType.ACTION != WorkflowStepType.CONDITION
        assert WorkflowStepType.ACTION in [WorkflowStepType.ACTION, WorkflowStepType.CONDITION]
    
    def test_enum_string_representation(self):
        """Test string representation of step types."""
        assert str(WorkflowStepType.ACTION) == "ACTION"
        assert str(WorkflowStepType.CONDITION) == "CONDITION"
        assert str(WorkflowStepType.LOOP) == "LOOP"
        assert str(WorkflowStepType.PARALLEL) == "PARALLEL"
        assert str(WorkflowStepType.WAIT) == "WAIT"
        assert str(WorkflowStepType.TRIGGER) == "TRIGGER"
    
    def test_enum_value_access(self):
        """Test accessing enum values."""
        assert WorkflowStepType.ACTION.value == "ACTION"
        assert WorkflowStepType.CONDITION.value == "CONDITION"
        assert WorkflowStepType.LOOP.value == "LOOP"
        assert WorkflowStepType.PARALLEL.value == "PARALLEL"
        assert WorkflowStepType.WAIT.value == "WAIT"
        assert WorkflowStepType.TRIGGER.value == "TRIGGER"

    def test_initialization(self):
        """Test proper initialization of step type."""
        step_type = WorkflowStepType(
            name="test_step",
            description="Test step type",
            version="1.0.0",
            category="test",
            inputs={
                "input1": {
                    "type": "string",
                    "required": True
                }
            },
            outputs={
                "output1": {
                    "type": "string"
                }
            },
            parameters={
                "param1": {
                    "type": "number",
                    "required": True
                }
            },
            metadata={
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        )
        
        assert step_type.name == "test_step"
        assert step_type.description == "Test step type"
        assert step_type.version == "1.0.0"
        assert step_type.category == "test"
        assert step_type.inputs["input1"]["type"] == "string"
        assert step_type.inputs["input1"]["required"] is True
        assert step_type.outputs["output1"]["type"] == "string"
        assert step_type.parameters["param1"]["type"] == "number"
        assert step_type.parameters["param1"]["required"] is True
        assert step_type.metadata["author"] == "Test Author"
        assert step_type.metadata["tags"] == ["test", "example"]

    def test_step_type_creation(self):
        """Test creating step types with different configurations."""
        # Test simple step type
        simple_step = WorkflowStepType.create_simple_step_type(
            name="simple_step",
            description="Simple step type",
            category="test"
        )
        assert simple_step.name == "simple_step"
        assert simple_step.description == "Simple step type"
        assert simple_step.category == "test"
        assert len(simple_step.inputs) == 0
        assert len(simple_step.outputs) == 0
        assert len(simple_step.parameters) == 0
        
        # Test step type with inputs
        input_step = WorkflowStepType.create_input_step_type(
            name="input_step",
            description="Step type with inputs",
            category="test",
            inputs={
                "input1": {
                    "type": "string",
                    "required": True
                }
            }
        )
        assert input_step.name == "input_step"
        assert input_step.description == "Step type with inputs"
        assert input_step.category == "test"
        assert len(input_step.inputs) == 1
        assert input_step.inputs["input1"]["type"] == "string"
        assert input_step.inputs["input1"]["required"] is True
        
        # Test step type with outputs
        output_step = WorkflowStepType.create_output_step_type(
            name="output_step",
            description="Step type with outputs",
            category="test",
            outputs={
                "output1": {
                    "type": "string"
                }
            }
        )
        assert output_step.name == "output_step"
        assert output_step.description == "Step type with outputs"
        assert output_step.category == "test"
        assert len(output_step.outputs) == 1
        assert output_step.outputs["output1"]["type"] == "string"
        
        # Test step type with parameters
        parameter_step = WorkflowStepType.create_parameter_step_type(
            name="parameter_step",
            description="Step type with parameters",
            category="test",
            parameters={
                "param1": {
                    "type": "number",
                    "required": True
                }
            }
        )
        assert parameter_step.name == "parameter_step"
        assert parameter_step.description == "Step type with parameters"
        assert parameter_step.category == "test"
        assert len(parameter_step.parameters) == 1
        assert parameter_step.parameters["param1"]["type"] == "number"
        assert parameter_step.parameters["param1"]["required"] is True
    
    def test_step_type_serialization(self):
        """Test serializing step type to dictionary."""
        step_type = WorkflowStepType(
            name="test_step",
            description="Test step type",
            version="1.0.0",
            category="test",
            inputs={
                "input1": {
                    "type": "string",
                    "required": True
                }
            },
            outputs={
                "output1": {
                    "type": "string"
                }
            },
            parameters={
                "param1": {
                    "type": "number",
                    "required": True
                }
            },
            metadata={
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        )
        
        serialized = step_type.to_dict()
        assert serialized["name"] == "test_step"
        assert serialized["description"] == "Test step type"
        assert serialized["version"] == "1.0.0"
        assert serialized["category"] == "test"
        assert serialized["inputs"]["input1"]["type"] == "string"
        assert serialized["inputs"]["input1"]["required"] is True
        assert serialized["outputs"]["output1"]["type"] == "string"
        assert serialized["parameters"]["param1"]["type"] == "number"
        assert serialized["parameters"]["param1"]["required"] is True
        assert serialized["metadata"]["author"] == "Test Author"
        assert serialized["metadata"]["tags"] == ["test", "example"]
    
    def test_step_type_deserialization(self):
        """Test deserializing step type from dictionary."""
        data = {
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
            },
            "metadata": {
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        }
        
        step_type = WorkflowStepType.from_dict(data)
        assert step_type.name == "test_step"
        assert step_type.description == "Test step type"
        assert step_type.version == "1.0.0"
        assert step_type.category == "test"
        assert step_type.inputs["input1"]["type"] == "string"
        assert step_type.inputs["input1"]["required"] is True
        assert step_type.outputs["output1"]["type"] == "string"
        assert step_type.parameters["param1"]["type"] == "number"
        assert step_type.parameters["param1"]["required"] is True
        assert step_type.metadata["author"] == "Test Author"
        assert step_type.metadata["tags"] == ["test", "example"]

class TestWorkflowStepTypeConfig:
    """Test suite for WorkflowStepTypeConfig."""
    
    def test_initialization(self):
        """Test proper initialization of step type config."""
        config = WorkflowStepTypeConfig(
            type=WorkflowStepType.ACTION,
            required_fields=["action", "parameters"],
            optional_fields=["timeout", "retries"]
        )
        
        assert config.type == WorkflowStepType.ACTION
        assert "action" in config.required_fields
        assert "parameters" in config.required_fields
        assert "timeout" in config.optional_fields
        assert "retries" in config.optional_fields
    
    def test_config_validation(self):
        """Test step type config validation."""
        config = WorkflowStepTypeConfig(
            type=WorkflowStepType.ACTION,
            required_fields=["action", "parameters"],
            optional_fields=["timeout", "retries"]
        )
        
        # Test valid config
        valid_config = {
            "action": "test_action",
            "parameters": {"param1": "value1"},
            "timeout": 30,
            "retries": 3
        }
        assert config.validate(valid_config) is True
        
        # Test missing required field
        invalid_config = {
            "action": "test_action"
            # Missing parameters
        }
        assert config.validate(invalid_config) is False
    
    def test_config_defaults(self):
        """Test step type config default values."""
        config = WorkflowStepTypeConfig(
            type=WorkflowStepType.ACTION,
            required_fields=["action", "parameters"],
            optional_fields=["timeout", "retries"],
            defaults={
                "timeout": 30,
                "retries": 3
            }
        )
        
        # Test config with defaults
        partial_config = {
            "action": "test_action",
            "parameters": {"param1": "value1"}
        }
        complete_config = config.apply_defaults(partial_config)
        
        assert complete_config["timeout"] == 30
        assert complete_config["retries"] == 3

class TestWorkflowStepTypeValidator:
    """Test suite for WorkflowStepTypeValidator."""
    
    def test_initialization(self):
        """Test proper initialization of step type validator."""
        validator = WorkflowStepTypeValidator()
        assert validator is not None
        assert validator.configs is not None
    
    def test_register_step_type(self):
        """Test registering a step type."""
        validator = WorkflowStepTypeValidator()
        config = WorkflowStepTypeConfig(
            type=WorkflowStepType.ACTION,
            required_fields=["action", "parameters"],
            optional_fields=["timeout", "retries"]
        )
        
        validator.register_step_type(config)
        assert WorkflowStepType.ACTION in validator.configs
    
    def test_validate_step_type(self):
        """Test validating a step type."""
        validator = WorkflowStepTypeValidator()
        config = WorkflowStepTypeConfig(
            type=WorkflowStepType.ACTION,
            required_fields=["action", "parameters"],
            optional_fields=["timeout", "retries"]
        )
        validator.register_step_type(config)
        
        # Test valid step
        valid_step = {
            "type": WorkflowStepType.ACTION,
            "config": {
                "action": "test_action",
                "parameters": {"param1": "value1"}
            }
        }
        assert validator.validate_step(valid_step) is True
        
        # Test invalid step
        invalid_step = {
            "type": WorkflowStepType.ACTION,
            "config": {
                "action": "test_action"
                # Missing parameters
            }
        }
        assert validator.validate_step(invalid_step) is False
    
    def test_validate_unknown_step_type(self):
        """Test validating an unknown step type."""
        validator = WorkflowStepTypeValidator()
        
        unknown_step = {
            "type": "UNKNOWN_TYPE",
            "config": {}
        }
        assert validator.validate_step(unknown_step) is False
    
    def test_get_step_type_config(self):
        """Test retrieving step type configuration."""
        validator = WorkflowStepTypeValidator()
        config = WorkflowStepTypeConfig(
            type=WorkflowStepType.ACTION,
            required_fields=["action", "parameters"],
            optional_fields=["timeout", "retries"]
        )
        validator.register_step_type(config)
        
        retrieved_config = validator.get_step_type_config(WorkflowStepType.ACTION)
        assert retrieved_config is not None
        assert retrieved_config.type == WorkflowStepType.ACTION
    
    def test_get_unknown_step_type_config(self):
        """Test retrieving configuration for unknown step type."""
        validator = WorkflowStepTypeValidator()
        
        with pytest.raises(KeyError):
            validator.get_step_type_config("UNKNOWN_TYPE")

class TestWorkflowStepTypeRegistry:
    """Test suite for WorkflowStepTypeRegistry."""
    
    def test_initialization(self):
        """Test proper initialization of step type registry."""
        registry = WorkflowStepTypeRegistry()
        assert registry is not None
        assert registry.step_types is not None
    
    def test_register_step_type(self):
        """Test registering step type."""
        registry = WorkflowStepTypeRegistry()
        
        # Register step type
        step_type = WorkflowStepType.create_simple_step_type(
            name="test_step",
            description="Test step type",
            category="test"
        )
        registry.register_step_type(step_type)
        
        # Verify step type was registered
        registered_type = registry.get_step_type("test_step")
        assert registered_type.name == "test_step"
        assert registered_type.description == "Test step type"
        assert registered_type.category == "test"
    
    def test_get_step_type(self):
        """Test retrieving step type."""
        registry = WorkflowStepTypeRegistry()
        
        # Register step type
        step_type = WorkflowStepType.create_simple_step_type(
            name="test_step",
            description="Test step type",
            category="test"
        )
        registry.register_step_type(step_type)
        
        # Get step type
        retrieved_type = registry.get_step_type("test_step")
        assert retrieved_type.name == "test_step"
        assert retrieved_type.description == "Test step type"
        assert retrieved_type.category == "test"
    
    def test_get_unknown_step_type(self):
        """Test retrieving unknown step type."""
        registry = WorkflowStepTypeRegistry()
        
        with pytest.raises(KeyError):
            registry.get_step_type("unknown_step")
    
    def test_get_step_types_by_category(self):
        """Test retrieving step types by category."""
        registry = WorkflowStepTypeRegistry()
        
        # Register step types in different categories
        step_type1 = WorkflowStepType.create_simple_step_type(
            name="test_step1",
            description="Test step type 1",
            category="test"
        )
        step_type2 = WorkflowStepType.create_simple_step_type(
            name="test_step2",
            description="Test step type 2",
            category="test"
        )
        step_type3 = WorkflowStepType.create_simple_step_type(
            name="other_step",
            description="Other step type",
            category="other"
        )
        
        registry.register_step_type(step_type1)
        registry.register_step_type(step_type2)
        registry.register_step_type(step_type3)
        
        # Get step types by category
        test_types = registry.get_step_types_by_category("test")
        assert len(test_types) == 2
        assert test_types["test_step1"].name == "test_step1"
        assert test_types["test_step2"].name == "test_step2"
        
        other_types = registry.get_step_types_by_category("other")
        assert len(other_types) == 1
        assert other_types["other_step"].name == "other_step"
    
    def test_get_all_step_types(self):
        """Test retrieving all step types."""
        registry = WorkflowStepTypeRegistry()
        
        # Register step types
        step_type1 = WorkflowStepType.create_simple_step_type(
            name="test_step1",
            description="Test step type 1",
            category="test"
        )
        step_type2 = WorkflowStepType.create_simple_step_type(
            name="test_step2",
            description="Test step type 2",
            category="test"
        )
        
        registry.register_step_type(step_type1)
        registry.register_step_type(step_type2)
        
        # Get all step types
        all_types = registry.get_all_step_types()
        assert len(all_types) == 2
        assert all_types["test_step1"].name == "test_step1"
        assert all_types["test_step2"].name == "test_step2"
    
    def test_unregister_step_type(self):
        """Test unregistering step type."""
        registry = WorkflowStepTypeRegistry()
        
        # Register step type
        step_type = WorkflowStepType.create_simple_step_type(
            name="test_step",
            description="Test step type",
            category="test"
        )
        registry.register_step_type(step_type)
        
        # Unregister step type
        registry.unregister_step_type("test_step")
        
        # Verify step type was unregistered
        with pytest.raises(KeyError):
            registry.get_step_type("test_step")

    def test_validate_step_type(self):
        """Test validating step type."""
        validator = WorkflowStepTypeValidator()
        
        # Test valid step type
        step_type = WorkflowStepType.create_simple_step_type(
            name="test_step",
            description="Test step type",
            category="test"
        )
        assert validator.validate(step_type) is True
        
        # Test invalid step type (missing name)
        step_type = WorkflowStepType(
            name="",
            description="Test step type",
            category="test"
        )
        assert validator.validate(step_type) is False
        
        # Test invalid step type (missing description)
        step_type = WorkflowStepType(
            name="test_step",
            description="",
            category="test"
        )
        assert validator.validate(step_type) is False
        
        # Test invalid step type (missing category)
        step_type = WorkflowStepType(
            name="test_step",
            description="Test step type",
            category=""
        )
        assert validator.validate(step_type) is False
    
    def test_validate_step_type_inputs(self):
        """Test validating step type inputs."""
        validator = WorkflowStepTypeValidator()
        
        # Test valid inputs
        step_type = WorkflowStepType.create_input_step_type(
            name="test_step",
            description="Test step type",
            category="test",
            inputs={
                "input1": {"type": "string", "required": True},
                "input2": {"type": "number"}
            }
        )
        assert validator.validate(step_type) is True
        
        # Test invalid inputs (missing type)
        step_type = WorkflowStepType.create_input_step_type(
            name="test_step",
            description="Test step type",
            category="test",
            inputs={
                "input1": {"required": True}
            }
        )
        assert validator.validate(step_type) is False
        
        # Test invalid inputs (invalid type)
        step_type = WorkflowStepType.create_input_step_type(
            name="test_step",
            description="Test step type",
            category="test",
            inputs={
                "input1": {"type": "invalid", "required": True}
            }
        )
        assert validator.validate(step_type) is False
    
    def test_validate_step_type_outputs(self):
        """Test validating step type outputs."""
        validator = WorkflowStepTypeValidator()
        
        # Test valid outputs
        step_type = WorkflowStepType.create_output_step_type(
            name="test_step",
            description="Test step type",
            category="test",
            outputs={
                "output1": {"type": "string"},
                "output2": {"type": "number"}
            }
        )
        assert validator.validate(step_type) is True
        
        # Test invalid outputs (missing type)
        step_type = WorkflowStepType.create_output_step_type(
            name="test_step",
            description="Test step type",
            category="test",
            outputs={
                "output1": {}
            }
        )
        assert validator.validate(step_type) is False
        
        # Test invalid outputs (invalid type)
        step_type = WorkflowStepType.create_output_step_type(
            name="test_step",
            description="Test step type",
            category="test",
            outputs={
                "output1": {"type": "invalid"}
            }
        )
        assert validator.validate(step_type) is False
    
    def test_validate_step_type_parameters(self):
        """Test validating step type parameters."""
        validator = WorkflowStepTypeValidator()
        
        # Test valid parameters
        step_type = WorkflowStepType.create_parameter_step_type(
            name="test_step",
            description="Test step type",
            category="test",
            parameters={
                "param1": {"type": "string", "required": True},
                "param2": {"type": "number"}
            }
        )
        assert validator.validate(step_type) is True
        
        # Test invalid parameters (missing type)
        step_type = WorkflowStepType.create_parameter_step_type(
            name="test_step",
            description="Test step type",
            category="test",
            parameters={
                "param1": {"required": True}
            }
        )
        assert validator.validate(step_type) is False
        
        # Test invalid parameters (invalid type)
        step_type = WorkflowStepType.create_parameter_step_type(
            name="test_step",
            description="Test step type",
            category="test",
            parameters={
                "param1": {"type": "invalid", "required": True}
            }
        )
        assert validator.validate(step_type) is False 