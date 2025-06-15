import pytest
from typing import Dict, Any, List

from ..agents.integration.workflow_execution_manager import (
    WorkflowExecutionManager,
    WorkflowExecution,
    WorkflowExecutionResult,
    WorkflowExecutionError
)

class TestWorkflowExecutionManager:
    """Test suite for WorkflowExecutionManager."""
    
    def test_initialization(self):
        """Test proper initialization of execution manager."""
        manager = WorkflowExecutionManager()
        assert manager is not None
        assert manager.executions is not None
        assert manager.results is not None
    
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
    
    def test_add_result(self):
        """Test adding execution result."""
        manager = WorkflowExecutionManager()
        
        # Add result
        result = WorkflowExecutionResult.create_success_result(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:30Z",
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    },
                    "outputs": {
                        "output1": {
                            "type": "string",
                            "value": "test output"
                        }
                    }
                }
            }
        )
        manager.add_result(result)
        
        # Verify result was added
        added_result = manager.get_result("test_execution_1")
        assert added_result.execution_id == "test_execution_1"
        assert added_result.workflow_id == "test_workflow_1"
        assert added_result.status == "completed"
        assert added_result.start_time == "2024-01-01T00:00:00Z"
        assert added_result.end_time == "2024-01-01T00:01:00Z"
        assert len(added_result.steps) == 1
        assert added_result.steps["step1"]["status"] == "completed"
        assert added_result.steps["step1"]["outputs"]["output1"]["value"] == "test output"
    
    def test_get_result(self):
        """Test retrieving execution result."""
        manager = WorkflowExecutionManager()
        
        # Add result
        result = WorkflowExecutionResult.create_success_result(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:30Z",
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    },
                    "outputs": {
                        "output1": {
                            "type": "string",
                            "value": "test output"
                        }
                    }
                }
            }
        )
        manager.add_result(result)
        
        # Get result
        retrieved_result = manager.get_result("test_execution_1")
        assert retrieved_result.execution_id == "test_execution_1"
        assert retrieved_result.workflow_id == "test_workflow_1"
        assert retrieved_result.status == "completed"
        assert retrieved_result.start_time == "2024-01-01T00:00:00Z"
        assert retrieved_result.end_time == "2024-01-01T00:01:00Z"
        assert len(retrieved_result.steps) == 1
        assert retrieved_result.steps["step1"]["status"] == "completed"
        assert retrieved_result.steps["step1"]["outputs"]["output1"]["value"] == "test output"
    
    def test_get_unknown_result(self):
        """Test retrieving unknown execution result."""
        manager = WorkflowExecutionManager()
        
        with pytest.raises(KeyError):
            manager.get_result("unknown_execution")
    
    def test_get_results_by_workflow(self):
        """Test retrieving execution results by workflow."""
        manager = WorkflowExecutionManager()
        
        # Add results for different workflows
        result1 = WorkflowExecutionResult.create_success_result(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:30Z",
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    },
                    "outputs": {
                        "output1": {
                            "type": "string",
                            "value": "test output"
                        }
                    }
                }
            }
        )
        result2 = WorkflowExecutionResult.create_success_result(
            execution_id="test_execution_2",
            workflow_id="test_workflow_1",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:30Z",
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    },
                    "outputs": {
                        "output1": {
                            "type": "string",
                            "value": "test output"
                        }
                    }
                }
            }
        )
        result3 = WorkflowExecutionResult.create_success_result(
            execution_id="other_execution_1",
            workflow_id="other_workflow_1",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:30Z",
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    },
                    "outputs": {
                        "output1": {
                            "type": "string",
                            "value": "test output"
                        }
                    }
                }
            }
        )
        
        manager.add_result(result1)
        manager.add_result(result2)
        manager.add_result(result3)
        
        # Get results by workflow
        test_results = manager.get_results_by_workflow("test_workflow_1")
        assert len(test_results) == 2
        assert test_results["test_execution_1"].execution_id == "test_execution_1"
        assert test_results["test_execution_2"].execution_id == "test_execution_2"
        
        other_results = manager.get_results_by_workflow("other_workflow_1")
        assert len(other_results) == 1
        assert other_results["other_execution_1"].execution_id == "other_execution_1"
    
    def test_get_all_results(self):
        """Test retrieving all execution results."""
        manager = WorkflowExecutionManager()
        
        # Add results
        result1 = WorkflowExecutionResult.create_success_result(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:30Z",
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    },
                    "outputs": {
                        "output1": {
                            "type": "string",
                            "value": "test output"
                        }
                    }
                }
            }
        )
        result2 = WorkflowExecutionResult.create_success_result(
            execution_id="test_execution_2",
            workflow_id="test_workflow_1",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:30Z",
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    },
                    "outputs": {
                        "output1": {
                            "type": "string",
                            "value": "test output"
                        }
                    }
                }
            }
        )
        
        manager.add_result(result1)
        manager.add_result(result2)
        
        # Get all results
        all_results = manager.get_all_results()
        assert len(all_results) == 2
        assert all_results["test_execution_1"].execution_id == "test_execution_1"
        assert all_results["test_execution_2"].execution_id == "test_execution_2"
    
    def test_remove_result(self):
        """Test removing execution result."""
        manager = WorkflowExecutionManager()
        
        # Add result
        result = WorkflowExecutionResult.create_success_result(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1",
            start_time="2024-01-01T00:00:00Z",
            end_time="2024-01-01T00:01:00Z",
            steps={
                "step1": {
                    "step_id": "step1",
                    "status": "completed",
                    "start_time": "2024-01-01T00:00:00Z",
                    "end_time": "2024-01-01T00:00:30Z",
                    "inputs": {
                        "input1": {
                            "type": "string",
                            "value": "test input"
                        }
                    },
                    "outputs": {
                        "output1": {
                            "type": "string",
                            "value": "test output"
                        }
                    }
                }
            }
        )
        manager.add_result(result)
        
        # Remove result
        manager.remove_result("test_execution_1")
        
        # Verify result was removed
        with pytest.raises(KeyError):
            manager.get_result("test_execution_1")
    
    def test_update_execution_status(self):
        """Test updating execution status."""
        manager = WorkflowExecutionManager()
        
        # Add execution
        execution = WorkflowExecution.create_simple_execution(
            execution_id="test_execution_1",
            workflow_id="test_workflow_1"
        )
        manager.add_execution(execution)
        
        # Update status
        manager.update_execution_status("test_execution_1", "running")
        
        # Verify status was updated
        updated_execution = manager.get_execution("test_execution_1")
        assert updated_execution.status == "running"
    
    def test_update_execution_step_status(self):
        """Test updating execution step status."""
        manager = WorkflowExecutionManager()
        
        # Add execution with step
        execution = WorkflowExecution.create_step_execution(
            execution_id="test_execution_1",
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
        manager.add_execution(execution)
        
        # Update step status
        manager.update_execution_step_status("test_execution_1", "step1", "running")
        
        # Verify step status was updated
        updated_execution = manager.get_execution("test_execution_1")
        assert updated_execution.steps["step1"]["status"] == "running"
    
    def test_update_execution_step_output(self):
        """Test updating execution step output."""
        manager = WorkflowExecutionManager()
        
        # Add execution with step
        execution = WorkflowExecution.create_step_execution(
            execution_id="test_execution_1",
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
                    },
                    "outputs": {
                        "output1": {
                            "type": "string"
                        }
                    }
                }
            }
        )
        manager.add_execution(execution)
        
        # Update step output
        manager.update_execution_step_output("test_execution_1", "step1", "output1", "test output")
        
        # Verify step output was updated
        updated_execution = manager.get_execution("test_execution_1")
        assert updated_execution.steps["step1"]["outputs"]["output1"]["value"] == "test output"
    
    def test_update_execution_step_error(self):
        """Test updating execution step error."""
        manager = WorkflowExecutionManager()
        
        # Add execution with step
        execution = WorkflowExecution.create_step_execution(
            execution_id="test_execution_1",
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
        manager.add_execution(execution)
        
        # Update step error
        error = WorkflowExecutionError(
            code="execution_failed",
            message="Step execution failed",
            details={
                "reason": "Timeout exceeded"
            }
        )
        manager.update_execution_step_error("test_execution_1", "step1", error)
        
        # Verify step error was updated
        updated_execution = manager.get_execution("test_execution_1")
        assert updated_execution.steps["step1"]["error"]["code"] == "execution_failed"
        assert updated_execution.steps["step1"]["error"]["message"] == "Step execution failed"
        assert updated_execution.steps["step1"]["error"]["details"]["reason"] == "Timeout exceeded" 