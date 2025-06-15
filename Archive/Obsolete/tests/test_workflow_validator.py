import pytest
from typing import Dict, Any

from ..agents.integration.workflow_validator import (
    WorkflowValidator,
    Workflow,
    WorkflowStep,
    WorkflowPriority
)

class TestWorkflowValidator:
    """Test suite for WorkflowValidator."""
    
    def test_initialization(self, workflow_validator):
        """Test proper initialization of the validator."""
        assert workflow_validator is not None
        assert workflow_validator.config is not None
    
    def test_valid_workflow(self, workflow_validator):
        """Test validation of a valid workflow."""
        # Create a valid workflow
        workflow = Workflow(
            id="valid_workflow",
            name="Valid Workflow",
            steps=[
                WorkflowStep(
                    id="step1",
                    type="action",
                    config={"action": "test_action"}
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        
        # Validate workflow
        is_valid, errors = workflow_validator.validate_workflow(workflow)
        assert is_valid
        assert not errors
    
    def test_invalid_workflow_missing_id(self, workflow_validator):
        """Test validation of a workflow with missing ID."""
        # Create an invalid workflow (missing ID)
        workflow = Workflow(
            id="",  # Empty ID
            name="Invalid Workflow",
            steps=[
                WorkflowStep(
                    id="step1",
                    type="action",
                    config={"action": "test_action"}
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        
        # Validate workflow
        is_valid, errors = workflow_validator.validate_workflow(workflow)
        assert not is_valid
        assert "id" in errors
    
    def test_invalid_workflow_missing_name(self, workflow_validator):
        """Test validation of a workflow with missing name."""
        # Create an invalid workflow (missing name)
        workflow = Workflow(
            id="invalid_workflow",
            name="",  # Empty name
            steps=[
                WorkflowStep(
                    id="step1",
                    type="action",
                    config={"action": "test_action"}
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        
        # Validate workflow
        is_valid, errors = workflow_validator.validate_workflow(workflow)
        assert not is_valid
        assert "name" in errors
    
    def test_invalid_workflow_missing_steps(self, workflow_validator):
        """Test validation of a workflow with missing steps."""
        # Create an invalid workflow (missing steps)
        workflow = Workflow(
            id="invalid_workflow",
            name="Invalid Workflow",
            steps=[],  # Empty steps
            priority=WorkflowPriority.NORMAL
        )
        
        # Validate workflow
        is_valid, errors = workflow_validator.validate_workflow(workflow)
        assert not is_valid
        assert "steps" in errors
    
    def test_invalid_workflow_step_missing_id(self, workflow_validator):
        """Test validation of a workflow step with missing ID."""
        # Create a workflow with an invalid step (missing ID)
        workflow = Workflow(
            id="invalid_workflow",
            name="Invalid Workflow",
            steps=[
                WorkflowStep(
                    id="",  # Empty ID
                    type="action",
                    config={"action": "test_action"}
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        
        # Validate workflow
        is_valid, errors = workflow_validator.validate_workflow(workflow)
        assert not is_valid
        assert "steps" in errors
        assert "id" in errors["steps"][0]
    
    def test_invalid_workflow_step_missing_type(self, workflow_validator):
        """Test validation of a workflow step with missing type."""
        # Create a workflow with an invalid step (missing type)
        workflow = Workflow(
            id="invalid_workflow",
            name="Invalid Workflow",
            steps=[
                WorkflowStep(
                    id="step1",
                    type="",  # Empty type
                    config={"action": "test_action"}
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        
        # Validate workflow
        is_valid, errors = workflow_validator.validate_workflow(workflow)
        assert not is_valid
        assert "steps" in errors
        assert "type" in errors["steps"][0]
    
    def test_invalid_workflow_step_missing_config(self, workflow_validator):
        """Test validation of a workflow step with missing config."""
        # Create a workflow with an invalid step (missing config)
        workflow = Workflow(
            id="invalid_workflow",
            name="Invalid Workflow",
            steps=[
                WorkflowStep(
                    id="step1",
                    type="action",
                    config={}  # Empty config
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        
        # Validate workflow
        is_valid, errors = workflow_validator.validate_workflow(workflow)
        assert not is_valid
        assert "steps" in errors
        assert "config" in errors["steps"][0]
    
    def test_invalid_workflow_priority(self, workflow_validator):
        """Test validation of a workflow with invalid priority."""
        # Create a workflow with an invalid priority
        workflow = Workflow(
            id="invalid_workflow",
            name="Invalid Workflow",
            steps=[
                WorkflowStep(
                    id="step1",
                    type="action",
                    config={"action": "test_action"}
                )
            ],
            priority="INVALID"  # Invalid priority
        )
        
        # Validate workflow
        is_valid, errors = workflow_validator.validate_workflow(workflow)
        assert not is_valid
        assert "priority" in errors
    
    def test_workflow_step_type_validation(self, workflow_validator):
        """Test validation of workflow step types."""
        # Create a workflow with an invalid step type
        workflow = Workflow(
            id="invalid_workflow",
            name="Invalid Workflow",
            steps=[
                WorkflowStep(
                    id="step1",
                    type="invalid_type",  # Invalid type
                    config={"action": "test_action"}
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        
        # Validate workflow
        is_valid, errors = workflow_validator.validate_workflow(workflow)
        assert not is_valid
        assert "steps" in errors
        assert "type" in errors["steps"][0]
    
    def test_workflow_step_config_validation(self, workflow_validator):
        """Test validation of workflow step configuration."""
        # Create a workflow with an invalid step config
        workflow = Workflow(
            id="invalid_workflow",
            name="Invalid Workflow",
            steps=[
                WorkflowStep(
                    id="step1",
                    type="action",
                    config={"invalid_key": "value"}  # Invalid config
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        
        # Validate workflow
        is_valid, errors = workflow_validator.validate_workflow(workflow)
        assert not is_valid
        assert "steps" in errors
        assert "config" in errors["steps"][0]
    
    def test_workflow_duplicate_step_ids(self, workflow_validator):
        """Test validation of workflow with duplicate step IDs."""
        # Create a workflow with duplicate step IDs
        workflow = Workflow(
            id="invalid_workflow",
            name="Invalid Workflow",
            steps=[
                WorkflowStep(
                    id="step1",
                    type="action",
                    config={"action": "test_action"}
                ),
                WorkflowStep(
                    id="step1",  # Duplicate ID
                    type="action",
                    config={"action": "test_action"}
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        
        # Validate workflow
        is_valid, errors = workflow_validator.validate_workflow(workflow)
        assert not is_valid
        assert "steps" in errors
        assert "duplicate" in errors["steps"] 