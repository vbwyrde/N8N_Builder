import pytest
from typing import Dict, Any, List

from ..agents.integration.workflow_execution import (
    WorkflowExecution,
    WorkflowExecutionManager,
    WorkflowExecutionValidator
)

class TestWorkflowExecution:
    """Test suite for WorkflowExecution."""
    
    def test_initialization(self):
        """Test proper initialization of workflow execution."""
        execution = WorkflowExecution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            status="running",
            start_time="2024-01-01T00:00:00Z",
            end_time=None,
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "running",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": None,
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
                    }
                }
            },
            metadata={
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        )
        
        assert execution.execution_id == "test_execution_1"
        assert execution.workflow_id == "test_workflow_1"
        assert execution.status == "running"
        assert execution.start_time == "2024-01-01T00:00:00Z"
        assert execution.end_time is None
        assert len(execution.steps) == 1
        assert execution.steps["step1"]["step_id"] == "step1"
        assert execution.steps["step1"]["status"] == "running"
        assert execution.steps["step1"]["start_time"] == "2024-01-01T00:00:00Z"
        assert execution.steps["step1"]["end_time"] is None
        assert execution.steps["step1"]["inputs"]["input1"]["type"] == "string"
        assert execution.steps["step1"]["inputs"]["input1"]["value"] == "test input"
        assert execution.steps["step1"]["outputs"]["output1"]["type"] == "string"
        assert execution.steps["step1"]["parameters"]["param1"]["type"] == "number"
        assert execution.steps["step1"]["parameters"]["param1"]["value"] == 42
        assert execution.metadata["author"] == "Test Author"
        assert execution.metadata["tags"] == ["test", "example"]
    
    def test_execution_creation(self):
        """Test creating executions with different configurations."""
        # Test simple execution
        simple_execution = WorkflowExecution.create_simple_execution(
            execution_id="simple_execution_1",
            workflow_id="test_workflow_1"
        )
        assert simple_execution.execution_id == "simple_execution_1"
        assert simple_execution.workflow_id == "test_workflow_1"
        assert simple_execution.status == "pending"
        assert simple_execution.start_time is not None
        assert simple_execution.end_time is None
        assert len(simple_execution.steps) == 0
        
        # Test execution with steps
        step_execution = WorkflowExecution.create_step_execution(
            execution_id="step_execution_1",
            workflow_id="test_workflow_1",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "pending",
                    "start_time": None,
                    "end_time": None,
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    }
                }
            }
        )
        assert step_execution.execution_id == "step_execution_1"
        assert step_execution.workflow_id == "test_workflow_1"
        assert step_execution.status == "pending"
        assert step_execution.start_time is not None
        assert step_execution.end_time is None
        assert len(step_execution.steps) == 1
        assert step_execution.steps["step1"]["step_id"] == "step1"
        assert step_execution.steps["step1"]["status"] == "pending"
        assert step_execution.steps["step1"]["start_time"] is None
        assert step_execution.steps["step1"]["end_time"] is None
        assert step_execution.steps["step1"]["inputs"]["input1"]["type"] == "string"
        assert step_execution.steps["step1"]["inputs"]["input1"]["value"] == "test input"
    
    def test_execution_serialization(self):
        """Test serializing execution to dictionary."""
        execution = WorkflowExecution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            status="running",
            start_time="2024-01-01T00:00:00Z",
            end_time=None,
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "running",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": None,
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
                    }
                }
            },
            metadata={
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        )
        
        serialized = execution.to_dict()
        assert serialized["execution_id"] == "test_execution_1"
        assert serialized["workflow_id"] == "test_workflow_1"
        assert serialized["status"] == "running"
        assert serialized["start_time"] == "2024-01-01T00:00:00Z"
        assert serialized["end_time"] is None
        assert len(serialized["steps"]) == 1
        assert serialized["steps"]["step1"]["step_id"] == "step1"
        assert serialized["steps"]["step1"]["status"] == "running"
        assert serialized["steps"]["step1"]["start_time"] == "2024-01-01T00:00:00Z"
        assert serialized["steps"]["step1"]["end_time"] is None
        assert serialized["steps"]["step1"]["inputs"]["input1"]["type"] == "string"
        assert serialized["steps"]["step1"]["inputs"]["input1"]["value"] == "test input"
        assert serialized["steps"]["step1"]["outputs"]["output1"]["type"] == "string"
        assert serialized["steps"]["step1"]["parameters"]["param1"]["type"] == "number"
        assert serialized["steps"]["step1"]["parameters"]["param1"]["value"] == 42
        assert serialized["metadata"]["author"] == "Test Author"
        assert serialized["metadata"]["tags"] == ["test", "example"]
    
    def test_execution_deserialization(self):
        """Test deserializing execution from dictionary."""
        data = {
            "execution_id": "test_execution_1",
            "workflow_id": "test_workflow_1",
            "status": "running",
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": None,
            "steps": {
                "step1": {
                    "step_id": "step1",
                    "status": "running",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": None,
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
                    }
                }
            },
            "metadata": {
                "author": "Test Author",
                "tags": ["test", "example"]
            }
        }
        
        execution = WorkflowExecution.from_dict(data)
        assert execution.execution_id == "test_execution_1"
        assert execution.workflow_id == "test_workflow_1"
        assert execution.status == "running"
        assert execution.start_time == "2024-01-01T00:00:00Z"
        assert execution.end_time is None
        assert len(execution.steps) == 1
        assert execution.steps["step1"]["step_id"] == "step1"
        assert execution.steps["step1"]["status"] == "running"
        assert execution.steps["step1"]["start_time"] == "2024-01-01T00:00:00Z"
        assert execution.steps["step1"]["end_time"] is None
        assert execution.steps["step1"]["inputs"]["input1"]["type"] == "string"
        assert execution.steps["step1"]["inputs"]["input1"]["value"] == "test input"
        assert execution.steps["step1"]["outputs"]["output1"]["type"] == "string"
        assert execution.steps["step1"]["parameters"]["param1"]["type"] == "number"
        assert execution.steps["step1"]["parameters"]["param1"]["value"] == 42
        assert execution.metadata["author"] == "Test Author"
        assert execution.metadata["tags"] == ["test", "example"]

class TestWorkflowExecutionManager:
    """Test suite for WorkflowExecutionManager."""
    
    def test_initialization(self):
        """Test proper initialization of execution manager."""
        manager = WorkflowExecutionManager()
        assert manager is not None
        assert manager.executions is not None
    
    def test_add_execution(self):
        """Test adding execution."""
        manager = WorkflowExecutionManager()
        
        # Add execution
        execution = WorkflowExecution.create_simple_execution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1"
        )
        manager.add_execution(execution)
        
        # Verify execution was added
        added_execution = manager.get_execution("test_execution_1")
        assert added_execution.execution_id == "test_execution_1"
        assert added_execution.workflow_id == "test_workflow_1"
        assert added_execution.status == "pending"
    
    def test_get_execution(self):
        """Test retrieving execution."""
        manager = WorkflowExecutionManager()
        
        # Add execution
        execution = WorkflowExecution.create_simple_execution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1"
        )
        manager.add_execution(execution)
        
        # Get execution
        retrieved_execution = manager.get_execution("test_execution_1")
        assert retrieved_execution.execution_id == "test_execution_1"
        assert retrieved_execution.workflow_id == "test_workflow_1"
        assert retrieved_execution.status == "pending"
    
    def test_get_unknown_execution(self):
        """Test retrieving unknown execution."""
        manager = WorkflowExecutionManager()
        
        with pytest.raises(KeyError):
            manager.get_execution("unknown_execution")
    
    def test_get_executions_by_workflow(self):
        """Test retrieving executions by workflow."""
        manager = WorkflowExecutionManager()
        
        # Add executions for different workflows
        execution1 = WorkflowExecution.create_simple_execution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1"
        )
        execution2 = WorkflowExecution.create_simple_execution(
            execution_id="test_execution_2",
            workflow_id="test_workflow_1"
        )
        execution3 = WorkflowExecution.create_simple_execution(
            execution_id="other_execution_1",
            workflow_id="other_workflow_1"
        )
        
        manager.add_execution(execution1)
        manager.add_execution(execution2)
        manager.add_execution(execution3)
        
        # Get executions by workflow
        test_executions = manager.get_executions_by_workflow("test_workflow_1")
        assert len(test_executions) == 2
        assert test_executions["test_execution_1"].execution_id == "test_execution_1"
        assert test_executions["test_execution_2"].execution_id == "test_execution_2"
        
        other_executions = manager.get_executions_by_workflow("other_workflow_1")
        assert len(other_executions) == 1
        assert other_executions["other_execution_1"].execution_id == "other_execution_1"
    
    def test_get_all_executions(self):
        """Test retrieving all executions."""
        manager = WorkflowExecutionManager()
        
        # Add executions
        execution1 = WorkflowExecution.create_simple_execution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1"
        )
        execution2 = WorkflowExecution.create_simple_execution(
            execution_id="test_execution_2",
            workflow_id="test_workflow_1"
        )
        
        manager.add_execution(execution1)
        manager.add_execution(execution2)
        
        # Get all executions
        all_executions = manager.get_all_executions()
        assert len(all_executions) == 2
        assert all_executions["test_execution_1"].execution_id == "test_execution_1"
        assert all_executions["test_execution_2"].execution_id == "test_execution_2"
    
    def test_remove_execution(self):
        """Test removing execution."""
        manager = WorkflowExecutionManager()
        
        # Add execution
        execution = WorkflowExecution.create_simple_execution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1"
        )
        manager.add_execution(execution)
        
        # Remove execution
        manager.remove_execution("test_execution_1")
        
        # Verify execution was removed
        with pytest.raises(KeyError):
            manager.get_execution("test_execution_1")

class TestWorkflowExecutionValidator:
    """Test suite for WorkflowExecutionValidator."""
    
    def test_initialization(self):
        """Test proper initialization of execution validator."""
        validator = WorkflowExecutionValidator()
        assert validator is not None
    
    def test_validate_execution(self):
        """Test validating execution."""
        validator = WorkflowExecutionValidator()
        
        # Test valid execution
        execution = WorkflowExecution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            status="running",
            start_time="2024-01-01T00:00:00Z",
            end_time=None,
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "running",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": None,
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    }
                }
            }
        )
        
        result = validator.validate_execution(execution)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid execution (missing required fields)
        invalid_execution = WorkflowExecution(
            execution_id="test_execution_1",
            workflow_id="",
            status="",
            start_time=None
        )
        
        result = validator.validate_execution(invalid_execution)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("workflow_id" in error.message for error in result.errors)
        assert any("status" in error.message for error in result.errors)
        assert any("start_time" in error.message for error in result.errors)
    
    def test_validate_execution_steps(self):
        """Test validating execution steps."""
        validator = WorkflowExecutionValidator()
        
        # Test valid steps
        execution = WorkflowExecution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            status="running",
            start_time="2024-01-01T00:00:00Z",
            end_time=None,
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "running",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": None,
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    }
                },
                "step2": {
                    "step_id": "step2",
                    "status": "pending",
                    "start_time": None,
                    "end_time": None,
                    "inputs": {
                        "input2": {
                            "type": "number",
                            "value": 42
                        }
                    }
                }
            }
        )
        
        result = validator.validate_execution_steps(execution)
        assert result.is_valid
        assert len(result.errors) == 0
        
        # Test invalid steps (missing required fields)
        invalid_execution = WorkflowExecution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            status="running",
            start_time="2024-01-01T00:00:00Z",
            end_time=None,
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "",
                    "start_time": None,
                    "end_time": None,
                    "inputs": {}
                }
            }
        )
        
        result = validator.validate_execution_steps(invalid_execution)
        assert not result.is_valid
        assert len(result.errors) > 0
        assert any("status" in error.message for error in result.errors)
        assert any("start_time" in error.message for error in result.errors) 