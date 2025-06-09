import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any

from ..agents.integration.workflow_executor import (
    WorkflowExecutor,
    Workflow,
    WorkflowStep,
    WorkflowStatus,
    WorkflowPriority
)

pytestmark = pytest.mark.asyncio

class TestWorkflowExecutor:
    """Test suite for WorkflowExecutor."""
    
    async def test_initialization(self, workflow_executor):
        """Test proper initialization of the executor."""
        assert workflow_executor is not None
        assert workflow_executor.workflows is not None
        assert workflow_executor.execution_queue is not None
        assert workflow_executor.config is not None
    
    async def test_workflow_registration(self, workflow_executor):
        """Test workflow registration functionality."""
        # Create a test workflow
        workflow = Workflow(
            id="test_workflow",
            name="Test Workflow",
            steps=[
                WorkflowStep(
                    id="step1",
                    type="action",
                    config={"action": "test_action"}
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        
        # Register workflow
        await workflow_executor.register_workflow(workflow)
        
        # Verify workflow was registered
        retrieved_workflow = await workflow_executor.get_workflow("test_workflow")
        assert retrieved_workflow is not None
        assert retrieved_workflow.id == "test_workflow"
        assert retrieved_workflow.name == "Test Workflow"
        assert len(retrieved_workflow.steps) == 1
    
    async def test_workflow_execution(self, workflow_executor):
        """Test workflow execution functionality."""
        # Create and register a test workflow
        workflow = Workflow(
            id="test_workflow",
            name="Test Workflow",
            steps=[
                WorkflowStep(
                    id="step1",
                    type="action",
                    config={"action": "test_action"}
                ),
                WorkflowStep(
                    id="step2",
                    type="action",
                    config={"action": "test_action"}
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        await workflow_executor.register_workflow(workflow)
        
        # Execute workflow
        execution_id = await workflow_executor.execute_workflow("test_workflow")
        
        # Wait for execution
        await asyncio.sleep(0.1)
        
        # Verify execution
        status = await workflow_executor.get_workflow_status(execution_id)
        assert status == WorkflowStatus.COMPLETED
    
    async def test_workflow_priority(self, workflow_executor):
        """Test workflow priority handling."""
        # Create test workflows with different priorities
        high_priority_workflow = Workflow(
            id="high_priority",
            name="High Priority Workflow",
            steps=[WorkflowStep(id="step1", type="action", config={})],
            priority=WorkflowPriority.HIGH
        )
        normal_priority_workflow = Workflow(
            id="normal_priority",
            name="Normal Priority Workflow",
            steps=[WorkflowStep(id="step1", type="action", config={})],
            priority=WorkflowPriority.NORMAL
        )
        low_priority_workflow = Workflow(
            id="low_priority",
            name="Low Priority Workflow",
            steps=[WorkflowStep(id="step1", type="action", config={})],
            priority=WorkflowPriority.LOW
        )
        
        # Register workflows
        await workflow_executor.register_workflow(high_priority_workflow)
        await workflow_executor.register_workflow(normal_priority_workflow)
        await workflow_executor.register_workflow(low_priority_workflow)
        
        # Execute workflows in reverse priority order
        low_execution = await workflow_executor.execute_workflow("low_priority")
        normal_execution = await workflow_executor.execute_workflow("normal_priority")
        high_execution = await workflow_executor.execute_workflow("high_priority")
        
        # Wait for executions
        await asyncio.sleep(0.1)
        
        # Verify execution order
        executions = await workflow_executor.get_execution_history()
        assert len(executions) == 3
        assert executions[0]["workflow_id"] == "high_priority"
        assert executions[1]["workflow_id"] == "normal_priority"
        assert executions[2]["workflow_id"] == "low_priority"
    
    async def test_workflow_error_handling(self, workflow_executor):
        """Test workflow error handling."""
        # Create a workflow with a failing step
        workflow = Workflow(
            id="error_workflow",
            name="Error Workflow",
            steps=[
                WorkflowStep(
                    id="failing_step",
                    type="action",
                    config={"action": "failing_action"}
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        await workflow_executor.register_workflow(workflow)
        
        # Execute workflow
        execution_id = await workflow_executor.execute_workflow("error_workflow")
        
        # Wait for execution
        await asyncio.sleep(0.1)
        
        # Verify error handling
        status = await workflow_executor.get_workflow_status(execution_id)
        assert status == WorkflowStatus.FAILED
        
        # Verify error details
        execution = await workflow_executor.get_execution_details(execution_id)
        assert "error" in execution
        assert execution["error_step"] == "failing_step"
    
    async def test_workflow_pause_resume(self, workflow_executor):
        """Test workflow pause and resume functionality."""
        # Create a long-running workflow
        workflow = Workflow(
            id="long_workflow",
            name="Long Running Workflow",
            steps=[
                WorkflowStep(
                    id="step1",
                    type="action",
                    config={"action": "long_action"}
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        await workflow_executor.register_workflow(workflow)
        
        # Execute workflow
        execution_id = await workflow_executor.execute_workflow("long_workflow")
        
        # Pause workflow
        await workflow_executor.pause_workflow(execution_id)
        
        # Verify workflow is paused
        status = await workflow_executor.get_workflow_status(execution_id)
        assert status == WorkflowStatus.PAUSED
        
        # Resume workflow
        await workflow_executor.resume_workflow(execution_id)
        
        # Wait for completion
        await asyncio.sleep(0.1)
        
        # Verify workflow completed
        final_status = await workflow_executor.get_workflow_status(execution_id)
        assert final_status == WorkflowStatus.COMPLETED
    
    async def test_workflow_cancellation(self, workflow_executor):
        """Test workflow cancellation functionality."""
        # Create a long-running workflow
        workflow = Workflow(
            id="cancellable_workflow",
            name="Cancellable Workflow",
            steps=[
                WorkflowStep(
                    id="step1",
                    type="action",
                    config={"action": "long_action"}
                )
            ],
            priority=WorkflowPriority.NORMAL
        )
        await workflow_executor.register_workflow(workflow)
        
        # Execute workflow
        execution_id = await workflow_executor.execute_workflow("cancellable_workflow")
        
        # Cancel workflow
        await workflow_executor.cancel_workflow(execution_id)
        
        # Verify workflow is cancelled
        status = await workflow_executor.get_workflow_status(execution_id)
        assert status == WorkflowStatus.CANCELLED
    
    async def test_workflow_validation(self, workflow_executor):
        """Test workflow validation functionality."""
        # Create invalid workflow (missing required field)
        invalid_workflow = Workflow(
            id="invalid_workflow",
            name="Invalid Workflow",
            steps=[],  # Missing steps
            priority=WorkflowPriority.NORMAL
        )
        
        # Verify workflow validation fails
        with pytest.raises(Exception):
            await workflow_executor.register_workflow(invalid_workflow)
    
    async def test_workflow_cleanup(self, workflow_executor):
        """Test workflow cleanup functionality."""
        # Create and register test workflows
        workflow1 = Workflow(
            id="workflow1",
            name="Workflow 1",
            steps=[WorkflowStep(id="step1", type="action", config={})],
            priority=WorkflowPriority.NORMAL
        )
        workflow2 = Workflow(
            id="workflow2",
            name="Workflow 2",
            steps=[WorkflowStep(id="step1", type="action", config={})],
            priority=WorkflowPriority.NORMAL
        )
        
        await workflow_executor.register_workflow(workflow1)
        await workflow_executor.register_workflow(workflow2)
        
        # Remove workflow
        await workflow_executor.remove_workflow("workflow1")
        
        # Verify workflow was removed
        with pytest.raises(Exception):
            await workflow_executor.get_workflow("workflow1")
        
        # Verify other workflow remains
        assert await workflow_executor.get_workflow("workflow2") is not None
    
    async def test_start_stop(self, workflow_executor):
        """Test starting and stopping the workflow executor."""
        # Stop the executor
        await workflow_executor.stop()
        
        # Verify executor is stopped
        assert not workflow_executor._running
        
        # Start the executor
        await workflow_executor.start()
        
        # Verify executor is running
        assert workflow_executor._running
        
        # Test workflow operations after restart
        workflow = Workflow(
            id="test_workflow",
            name="Test Workflow",
            steps=[WorkflowStep(id="step1", type="action", config={})],
            priority=WorkflowPriority.NORMAL
        )
        await workflow_executor.register_workflow(workflow)
        
        retrieved_workflow = await workflow_executor.get_workflow("test_workflow")
        assert retrieved_workflow is not None
        assert retrieved_workflow.id == "test_workflow" 