import pytest
from typing import Dict, Any, List

from n8n_builder.agents.integration.workflow import (
    Workflow,
    WorkflowManager,
    WorkflowValidator
)
from n8n_builder.agents.integration.workflow_step import (
    WorkflowStep,
    WorkflowStepManager,
    WorkflowStepValidator
)

class TestWorkflowCore:
    """Test suite for core workflow functionality."""
    
    def test_workflow_state_transitions(self):
        """Test workflow state transitions."""
        workflow = Workflow.create_simple_workflow(
            workflow_id="test_workflow_1",
            name="Test Workflow",
            description="Test workflow"
        )
        
        # Test initial state
        assert workflow.state == "created"
        
        # Test state transitions
        workflow.start()
        assert workflow.state == "running"
        
        workflow.complete()
        assert workflow.state == "completed"
        
        workflow.fail("Test error")
        assert workflow.state == "failed"
        assert workflow.error == "Test error"
    
    def test_workflow_step_dependencies(self):
        """Test workflow step dependencies."""
        workflow = Workflow.create_step_workflow(
            workflow_id="test_workflow_1",
            name="Test Workflow",
            description="Test workflow",
            steps={
                "step1": {
                    "step_id": "step1",
                    "step_type": "test_step",
                    "dependencies": []
                },
                "step2": {
                    "step_id": "step2",
                    "step_type": "test_step",
                    "dependencies": ["step1"]
                }
            }
        )
        
        assert len(workflow.steps["step1"]["dependencies"]) == 0
        assert workflow.steps["step2"]["dependencies"] == ["step1"]

class TestWorkflowStepCore:
    """Test suite for core workflow step functionality."""
    
    def test_step_execution(self):
        """Test basic step execution."""
        step = WorkflowStep.create_simple_step(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step"
        )
        
        # Test execution
        result = step.execute()
        assert result.success
        assert result.step_id == "test_step_1"
        assert result.status == "completed"
    
    def test_step_input_output_handling(self):
        """Test step input/output handling."""
        step = WorkflowStep.create_input_step(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            description="Test workflow step",
            inputs={
                "input1": {
                    "type": "string",
                    "value": "test input"
                }
            }
        )
        
        # Test input validation
        assert step.validate_inputs()
        
        # Test execution with inputs
        result = step.execute()
        assert result.success
        assert result.outputs["output1"]["value"] == "processed test input"

class TestWorkflowValidationCore:
    """Test suite for core workflow validation functionality."""
    
    def test_step_type_validation(self):
        """Test step type validation."""
        validator = WorkflowStepValidator()
        
        # Test valid step type
        step = WorkflowStep.create_simple_step(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step"
        )
        result = validator.validate_step_type(step)
        assert result.is_valid
        
        # Test invalid step type
        invalid_step = WorkflowStep.create_simple_step(
            step_id="test_step_1",
            step_type="invalid_type",
            name="Test Step"
        )
        result = validator.validate_step_type(invalid_step)
        assert not result.is_valid
        assert len(result.errors) > 0
    
    def test_input_output_validation(self):
        """Test input/output validation."""
        validator = WorkflowStepValidator()
        
        # Test valid inputs/outputs
        step = WorkflowStep.create_input_step(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
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
            }
        )
        
        result = validator.validate_step(step)
        assert result.is_valid
        
        # Test invalid inputs
        invalid_step = WorkflowStep.create_input_step(
            step_id="test_step_1",
            step_type="test_step",
            name="Test Step",
            inputs={
                "input1": {
                    "type": "invalid_type",
                    "value": "test input"
                }
            }
        )
        
        result = validator.validate_step(invalid_step)
        assert not result.is_valid
        assert len(result.errors) > 0 