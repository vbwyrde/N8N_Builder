import pytest
from typing import Dict, Any, List

from n8n_builder.agents.integration.workflow import (
    Workflow,
    WorkflowManager,
    WorkflowValidator
)

class TestWorkflow:
    """Test suite for Workflow."""
    
    def test_initialization(self):
        """Test proper initialization of workflow."""
        workflow = Workflow(
            workflow_id="test_workflow_1",
            name="Test Workflow",
            description="Test workflow",
            steps={
                "step1": {
                    "step_id": "step1",
                    "step_type": "test_step",
                    "name": "Test Step 1",
                    "description": "Test workflow step 1"
                },
                "step2": {
                    "step_id": "step2",
                    "step_type": "test_step",
                    "name": "Test Step 2",
                    "description": "Test workflow step 2"
                }
            },
            metadata={
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        )
        
        assert workflow.workflow_id == "test_workflow_1"
        assert workflow.name == "Test Workflow"
        assert workflow.description == "Test workflow"
        assert len(workflow.steps) == 2
        assert workflow.steps["step1"]["step_id"] == "step1"
        assert workflow.steps["step1"]["step_type"] == "test_step"
        assert workflow.steps["step1"]["name"] == "Test Step 1"
        assert workflow.steps["step1"]["description"] == "Test workflow step 1"
        assert workflow.steps["step2"]["step_id"] == "step2"
        assert workflow.steps["step2"]["step_type"] == "test_step"
        assert workflow.steps["step2"]["name"] == "Test Step 2"
        assert workflow.steps["step2"]["description"] == "Test workflow step 2"
        assert workflow.metadata["author"] == "Test Author"
        assert workflow.metadata["tags"] == ["test", "example"]
    
    def test_workflow_creation(self):
        """Test creating workflows with different configurations."""
        # Test simple workflow
        simple_workflow = Workflow.create_simple_workflow(
            workflow_id="simple_workflow_1",
            name="Simple Workflow",
            description="Simple workflow"
        )
        assert simple_workflow.workflow_id == "simple_workflow_1"
        assert simple_workflow.name == "Simple Workflow"
        assert simple_workflow.description == "Simple workflow"
        assert len(simple_workflow.steps) == 0
        
        # Test workflow with steps
        step_workflow = Workflow.create_step_workflow(
            workflow_id="step_workflow_1",
            name="Step Workflow",
            description="Workflow with steps",
            steps={
                "step1": {
                    "step_id": "step1",
                    "step_type": "test_step",
                    "name": "Test Step 1",
                    "description": "Test workflow step 1"
                }
            }
        )
        assert step_workflow.workflow_id == "step_workflow_1"
        assert step_workflow.name == "Step Workflow"
        assert step_workflow.description == "Workflow with steps"
        assert len(step_workflow.steps) == 1
        assert step_workflow.steps["step1"]["step_id"] == "step1"
        assert step_workflow.steps["step1"]["step_type"] == "test_step"
        assert step_workflow.steps["step1"]["name"] == "Test Step 1"
        assert step_workflow.steps["step1"]["description"] == "Test workflow step 1"
    
    def test_workflow_serialization(self):
        """Test serializing workflow to dictionary."""
        workflow = Workflow(
            workflow_id="test_workflow_1",
            name="Test Workflow",
            description="Test workflow",
            steps={
                "step1": {
                    "step_id": "step1",
                    "step_type": "test_step",
                    "name": "Test Step 1",
                    "description": "Test workflow step 1"
                },
                "step2": {
                    "step_id": "step2",
                    "step_type": "test_step",
                    "name": "Test Step 2",
                    "description": "Test workflow step 2"
                }
            },
            metadata={
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        )
        
        serialized = workflow.to_dict()
        assert serialized["workflow_id"] == "test_workflow_1"
        assert serialized["name"] == "Test Workflow"
        assert serialized["description"] == "Test workflow"
        assert len(serialized["steps"]) == 2
        assert serialized["steps"]["step1"]["step_id"] == "step1"
        assert serialized["steps"]["step1"]["step_type"] == "test_step"
        assert serialized["steps"]["step1"]["name"] == "Test Step 1"
        assert serialized["steps"]["step1"]["description"] == "Test workflow step 1"
        assert serialized["steps"]["step2"]["step_id"] == "step2"
        assert serialized["steps"]["step2"]["step_type"] == "test_step"
        assert serialized["steps"]["step2"]["name"] == "Test Step 2"
        assert serialized["steps"]["step2"]["description"] == "Test workflow step 2"
        assert serialized["metadata"]["author"] == "Test Author"
        assert serialized["metadata"]["tags"] == ["test", "example"]
    
    def test_workflow_deserialization(self):
        """Test deserializing workflow from dictionary."""
        data = {
            "workflow_id": "test_workflow_1",
            "name": "Test Workflow",
            "description": "Test workflow",
            "steps": {
                "step1": {
                    "step_id": "step1",
                    "step_type": "test_step",
                    "name": "Test Step 1",
                    "description": "Test workflow step 1"
                },
                "step2": {
                    "step_id": "step2",
                    "step_type": "test_step",
                    "name": "Test Step 2",
                    "description": "Test workflow step 2"
                }
            },
            "metadata": {
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        }
        
        workflow = Workflow.from_dict(data)
        assert workflow.workflow_id == "test_workflow_1"
        assert workflow.name == "Test Workflow"
        assert workflow.description == "Test workflow"
        assert len(workflow.steps) == 2
        assert workflow.steps["step1"]["step_id"] == "step1"
        assert workflow.steps["step1"]["step_type"] == "test_step"
        assert workflow.steps["step1"]["name"] == "Test Step 1"
        assert workflow.steps["step1"]["description"] == "Test workflow step 1"
        assert workflow.steps["step2"]["step_id"] == "step2"
        assert workflow.steps["step2"]["step_type"] == "test_step"
        assert workflow.steps["step2"]["name"] == "Test Step 2"
        assert workflow.steps["step2"]["description"] == "Test workflow step 2"
        assert workflow.metadata["author"] == "Test Author"
        assert workflow.metadata["tags"] == ["test", "example"]

class TestWorkflowManager:
    """Test suite for WorkflowManager."""
    
    def test_initialization(self):
        """Test proper initialization of workflow manager."""
        manager = WorkflowManager()
        assert manager is not None
        assert manager.workflows is not None
    
    def test_add_workflow(self):
        """Test adding workflow."""
        manager = WorkflowManager()
        
        # Add workflow
        workflow = Workflow.create_simple_workflow(
            workflow_id="test_workflow_1",
            name="Test Workflow",
            description="Test workflow"
        )
        manager.add_workflow(workflow)
        
        # Verify workflow was added
        added_workflow = manager.get_workflow("test_workflow_1")
        assert added_workflow.workflow_id == "test_workflow_1"
        assert added_workflow.name == "Test Workflow"
        assert added_workflow.description == "Test workflow"
    
    def test_get_workflow(self):
        """Test retrieving workflow."""
        manager = WorkflowManager()
        
        # Add workflow
        workflow = Workflow.create_simple_workflow(
            workflow_id="test_workflow_1",
            name="Test Workflow",
            description="Test workflow"
        )
        manager.add_workflow(workflow)
        
        # Get workflow
        retrieved_workflow = manager.get_workflow("test_workflow_1")
        assert retrieved_workflow.workflow_id == "test_workflow_1"
        assert retrieved_workflow.name == "Test Workflow"
        assert retrieved_workflow.description == "Test workflow"
    
    def test_get_unknown_workflow(self):
        """Test retrieving unknown workflow."""
        manager = WorkflowManager()
        
        with pytest.raises(KeyError):
            manager.get_workflow("unknown_workflow")
    
    def test_get_all_workflows(self):
        """Test retrieving all workflows."""
        manager = WorkflowManager()
        
        # Add workflows
        workflow1 = Workflow.create_simple_workflow(
            workflow_id="test_workflow_1",
            name="Test Workflow 1",
            description="Test workflow 1"
        )
        workflow2 = Workflow.create_simple_workflow(
            workflow_id="test_workflow_2",
            name="Test Workflow 2",
            description="Test workflow 2"
        )
        
        manager.add_workflow(workflow1)
        manager.add_workflow(workflow2)
        
        # Get all workflows
        all_workflows = manager.get_all_workflows()
        assert len(all_workflows) == 2
        assert all_workflows["test_workflow_1"].name == "Test Workflow 1"
        assert all_workflows["test_workflow_2"].name == "Test Workflow 2"
    
    def test_remove_workflow(self):
        """Test removing workflow."""
        manager = WorkflowManager()
        
        # Add workflow
        workflow = Workflow.create_simple_workflow(
            workflow_id="test_workflow_1",
            name="Test Workflow",
            description="Test workflow"
        )
        manager.add_workflow(workflow)
        
        # Remove workflow
        manager.remove_workflow("test_workflow_1")
        
        # Verify workflow was removed
        with pytest.raises(KeyError):
            manager.get_workflow("test_workflow_1")

class TestWorkflowValidator:
    """Test suite for WorkflowValidator."""
    
    def test_initialization(self):
        """Test proper initialization of workflow validator."""
        validator = WorkflowValidator()
        assert validator is not None
    
    def test_validate_workflow(self):
        """Test validating workflow."""
        validator = WorkflowValidator()
        
        # Test valid workflow
        workflow = Workflow(
            workflow_id="test_workflow_1",
            name="Test Workflow",
            description="Test workflow",
            steps={
                "step1": {
                    "step_id": "step1",
                    "step_type": "test_step",
                    "name": "Test Step 1",
                    "description": "Test workflow step 1"
                }
            }
        )
        
        result = validator.validate_workflow(workflow)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid workflow (missing required fields)
        invalid_workflow = Workflow(
            workflow_id="test_workflow_1",
            name="",
            description=""
        )
        
        result = validator.validate_workflow(invalid_workflow)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("name" in error.message for error in result.errors)
        assert any("description" in error.message for error in result.errors)
    
    def test_validate_workflow_steps(self):
        """Test validating workflow steps."""
        validator = WorkflowValidator()
        
        # Test valid steps
        workflow = Workflow(
            workflow_id="test_workflow_1",
            name="Test Workflow",
            description="Test workflow",
            steps={
                "step1": {
                    "step_id": "step1",
                    "step_type": "test_step",
                    "name": "Test Step 1",
                    "description": "Test workflow step 1"
                },
                "step2": {
                    "step_id": "step2",
                    "step_type": "test_step",
                    "name": "Test Step 2",
                    "description": "Test workflow step 2"
                }
            }
        )
        
        result = validator.validate_workflow_steps(workflow)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid steps (missing required fields)
        invalid_workflow = Workflow(
            workflow_id="test_workflow_1",
            name="Test Workflow",
            description="Test workflow",
            steps={
                "step1": {
                    "step_id": "step1",
                    "step_type": "",
                    "name": "",
                    "description": ""
                }
            }
        )
        
        result = validator.validate_workflow_steps(invalid_workflow)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("step_type" in error.message for error in result.errors)
        assert any("name" in error.message for error in result.errors)
        assert any("description" in error.message for error in result.errors) 