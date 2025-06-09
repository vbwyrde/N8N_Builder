import pytest
from typing import Dict, Any, List

from ..agents.integration.workflow_step import (
    WorkflowStep,
    WorkflowStepManager,
    WorkflowStepValidator
)

class TestWorkflowStep:
    """Test suite for WorkflowStep."""
    
    def test_initialization(self):
        """Test proper initialization of workflow step."""
        step = WorkflowStep(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step",
            inputs={
                "input1": {
                    "type": "string",
                    "value": "test input"
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
                    "value": 42
                }
            },
            metadata={
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        )
        
        assert step.step_id == "test_step_1"
        assert step.step_type == "test_step"
        assert step.name == "Test Step"
        assert step.description == "Test workflow step"
        assert step.inputs["input1"]["type"] == "string"
        assert step.inputs["input1"]["value"] == "test input"
        assert step.outputs["output1"]["type"] == "string"
        assert step.parameters["param1"]["type"] == "number"
        assert step.parameters["param1"]["value"] == 42
        assert step.metadata["author"] == "Test Author"
        assert step.metadata["tags"] == ["test", "example"]
    
    def test_step_creation(self):
        """Test creating steps with different configurations."""
        # Test simple step
        simple_step = WorkflowStep.create_simple_step(
            step_id="simple_step_1",
            step_type="simple_step",
            name="Simple Step",
            description="Simple workflow step"
        )
        assert simple_step.step_id == "simple_step_1"
        assert simple_step.step_type == "simple_step"
        assert simple_step.name == "Simple Step"
        assert simple_step.description == "Simple workflow step"
        assert len(simple_step.inputs) == 0
        assert len(simple_step.outputs) == 0
        assert len(simple_step.parameters) == 0
        
        # Test step with inputs
        input_step = WorkflowStep.create_input_step(
            step_id="input_step_1",
            step_type="input_step",
            name="Input Step",
            description="Step with inputs",
            inputs={
                "input1": {
                    "type": "string",
                    "value": "test input"
                }
            }
        )
        assert input_step.step_id == "input_step_1"
        assert input_step.step_type == "input_step"
        assert input_step.name == "Input Step"
        assert input_step.description == "Step with inputs"
        assert len(input_step.inputs) == 1
        assert input_step.inputs["input1"]["type"] == "string"
        assert input_step.inputs["input1"]["value"] == "test input"
        
        # Test step with outputs
        output_step = WorkflowStep.create_output_step(
            step_id="output_step_1",
            step_type="output_step",
            name="Output Step",
            description="Step with outputs",
            outputs={
                "output1": {
                    "type": "string"
                }
            }
        )
        assert output_step.step_id == "output_step_1"
        assert output_step.step_type == "output_step"
        assert output_step.name == "Output Step"
        assert output_step.description == "Step with outputs"
        assert len(output_step.outputs) == 1
        assert output_step.outputs["output1"]["type"] == "string"
        
        # Test step with parameters
        parameter_step = WorkflowStep.create_parameter_step(
            step_id="parameter_step_1",
            step_type="parameter_step",
            name="Parameter Step",
            description="Step with parameters",
            parameters={
                "param1": {
                    "type": "number",
                    "value": 42
                }
            }
        )
        assert parameter_step.step_id == "parameter_step_1"
        assert parameter_step.step_type == "parameter_step"
        assert parameter_step.name == "Parameter Step"
        assert parameter_step.description == "Step with parameters"
        assert len(parameter_step.parameters) == 1
        assert parameter_step.parameters["param1"]["type"] == "number"
        assert parameter_step.parameters["param1"]["value"] == 42
    
    def test_step_serialization(self):
        """Test serializing step to dictionary."""
        step = WorkflowStep(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step",
            inputs={
                "input1": {
                    "type": "string",
                    "value": "test input"
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
                    "value": 42
                }
            },
            metadata={
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        )
        
        serialized = step.to_dict()
        assert serialized["step_id"] == "test_step_1"
        assert serialized["step_type"] == "test_step"
        assert serialized["name"] == "Test Step"
        assert serialized["description"] == "Test workflow step"
        assert serialized["inputs"]["input1"]["type"] == "string"
        assert serialized["inputs"]["input1"]["value"] == "test input"
        assert serialized["outputs"]["output1"]["type"] == "string"
        assert serialized["parameters"]["param1"]["type"] == "number"
        assert serialized["parameters"]["param1"]["value"] == 42
        assert serialized["metadata"]["author"] == "Test Author"
        assert serialized["metadata"]["tags"] == ["test", "example"]
    
    def test_step_deserialization(self):
        """Test deserializing step from dictionary."""
        data = {
            "step_id": "test_step_1",
            "step_type": "test_step",
            "name": "Test Step",
            "description": "Test workflow step",
            "inputs": {
                "input1": {
                    "type": "string",
                    "value": "test input"
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
                    "value": 42
                }
            },
            "metadata": {
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        }
        
        step = WorkflowStep.from_dict(data)
        assert step.step_id == "test_step_1"
        assert step.step_type == "test_step"
        assert step.name == "Test Step"
        assert step.description == "Test workflow step"
        assert step.inputs["input1"]["type"] == "string"
        assert step.inputs["input1"]["value"] == "test input"
        assert step.outputs["output1"]["type"] == "string"
        assert step.parameters["param1"]["type"] == "number"
        assert step.parameters["param1"]["value"] == 42
        assert step.metadata["author"] == "Test Author"
        assert step.metadata["tags"] == ["test", "example"]

class TestWorkflowStepManager:
    """Test suite for WorkflowStepManager."""
    
    def test_initialization(self):
        """Test proper initialization of step manager."""
        manager = WorkflowStepManager()
        assert manager is not None
        assert manager.steps is not None
    
    def test_add_step(self):
        """Test adding step."""
        manager = WorkflowStepManager()
        
        # Add step
        step = WorkflowStep.create_simple_step(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step"
        )
        manager.add_step(step)
        
        # Verify step was added
        added_step = manager.get_step("test_step_1")
        assert added_step.step_id == "test_step_1"
        assert added_step.step_type == "test_step"
        assert added_step.name == "Test Step"
        assert added_step.description == "Test workflow step"
    
    def test_get_step(self):
        """Test retrieving step."""
        manager = WorkflowStepManager()
        
        # Add step
        step = WorkflowStep.create_simple_step(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step"
        )
        manager.add_step(step)
        
        # Get step
        retrieved_step = manager.get_step("test_step_1")
        assert retrieved_step.step_id == "test_step_1"
        assert retrieved_step.step_type == "test_step"
        assert retrieved_step.name == "Test Step"
        assert retrieved_step.description == "Test workflow step"
    
    def test_get_unknown_step(self):
        """Test retrieving unknown step."""
        manager = WorkflowStepManager()
        
        with pytest.raises(KeyError):
            manager.get_step("unknown_step")
    
    def test_get_steps_by_type(self):
        """Test retrieving steps by type."""
        manager = WorkflowStepManager()
        
        # Add steps of different types
        step1 = WorkflowStep.create_simple_step(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step 1",
            description="Test workflow step 1"
        )
        step2 = WorkflowStep.create_simple_step(
            step_id="test_step_2",
            step_type="test_step",
            name="Test Step 2",
            description="Test workflow step 2"
        )
        step3 = WorkflowStep.create_simple_step(
            step_id="other_step_1",
            step_type="other_step",
            name="Other Step",
            description="Other workflow step"
        )
        
        manager.add_step(step1)
        manager.add_step(step2)
        manager.add_step(step3)
        
        # Get steps by type
        test_steps = manager.get_steps_by_type("test_step")
        assert len(test_steps) == 2
        assert test_steps["test_step_1"].name == "Test Step 1"
        assert test_steps["test_step_2"].name == "Test Step 2"
        
        other_steps = manager.get_steps_by_type("other_step")
        assert len(other_steps) == 1
        assert other_steps["other_step_1"].name == "Other Step"
    
    def test_get_all_steps(self):
        """Test retrieving all steps."""
        manager = WorkflowStepManager()
        
        # Add steps
        step1 = WorkflowStep.create_simple_step(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step 1",
            description="Test workflow step 1"
        )
        step2 = WorkflowStep.create_simple_step(
            step_id="test_step_2",
            step_type="test_step",
            name="Test Step 2",
            description="Test workflow step 2"
        )
        
        manager.add_step(step1)
        manager.add_step(step2)
        
        # Get all steps
        all_steps = manager.get_all_steps()
        assert len(all_steps) == 2
        assert all_steps["test_step_1"].name == "Test Step 1"
        assert all_steps["test_step_2"].name == "Test Step 2"
    
    def test_remove_step(self):
        """Test removing step."""
        manager = WorkflowStepManager()
        
        # Add step
        step = WorkflowStep.create_simple_step(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step"
        )
        manager.add_step(step)
        
        # Remove step
        manager.remove_step("test_step_1")
        
        # Verify step was removed
        with pytest.raises(KeyError):
            manager.get_step("test_step_1")

class TestWorkflowStepValidator:
    """Test suite for WorkflowStepValidator."""
    
    def test_initialization(self):
        """Test proper initialization of step validator."""
        validator = WorkflowStepValidator()
        assert validator is not None
    
    def test_validate_step(self):
        """Test validating step."""
        validator = WorkflowStepValidator()
        
        # Test valid step
        step = WorkflowStep(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step",
            inputs={
                "input1": {
                    "type": "string",
                    "value": "test input"
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
                    "value": 42
                }
            }
        )
        
        result = validator.validate_step(step)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid step (missing required fields)
        invalid_step = WorkflowStep(
            step_id="test_step_1",
            step_type="",
            name="",
            description=""
        )
        
        result = validator.validate_step(invalid_step)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("step_type" in error.message for error in result.errors)
        assert any("name" in error.message for error in result.errors)
        assert any("description" in error.message for error in result.errors)
    
    def test_validate_step_inputs(self):
        """Test validating step inputs."""
        validator = WorkflowStepValidator()
        
        # Test valid inputs
        step = WorkflowStep(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step",
            inputs={
                "input1": {
                    "type": "string",
                    "value": "test input"
                },
                "input2": {
                    "type": "number",
                    "value": 42
                }
            }
        )
        
        result = validator.validate_step_inputs(step)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid inputs (missing required fields)
        invalid_step = WorkflowStep(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step",
            inputs={
                "input1": {
                    "type": "string"
                }
            }
        )
        
        result = validator.validate_step_inputs(invalid_step)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("value" in error.message for error in result.errors)
    
    def test_validate_step_outputs(self):
        """Test validating step outputs."""
        validator = WorkflowStepValidator()
        
        # Test valid outputs
        step = WorkflowStep(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step",
            outputs={
                "output1": {
                    "type": "string"
                },
                "output2": {
                    "type": "number"
                }
            }
        )
        
        result = validator.validate_step_outputs(step)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid outputs (missing type)
        invalid_step = WorkflowStep(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step",
            outputs={
                "output1": {}
            }
        )
        
        result = validator.validate_step_outputs(invalid_step)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("type" in error.message for error in result.errors)
    
    def test_validate_step_parameters(self):
        """Test validating step parameters."""
        validator = WorkflowStepValidator()
        
        # Test valid parameters
        step = WorkflowStep(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step",
            parameters={
                "param1": {
                    "type": "string",
                    "value": "test value"
                },
                "param2": {
                    "type": "number",
                    "value": 42
                }
            }
        )
        
        result = validator.validate_step_parameters(step)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid parameters (missing required fields)
        invalid_step = WorkflowStep(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step",
            parameters={
                "param1": {
                    "type": "string"
                }
            }
        )
        
        result = validator.validate_step_parameters(invalid_step)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("value" in error.message for error in result.errors) 