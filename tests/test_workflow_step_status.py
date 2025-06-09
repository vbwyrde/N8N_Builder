import pytest
from enum import Enum
from typing import Dict, Any, List

from ..agents.integration.workflow_step_status import (
    WorkflowStepStatus,
    WorkflowStepStatusType,
    WorkflowStepStatusManager
)

class TestWorkflowStepStatus:
    """Test suite for WorkflowStepStatus."""
    
    def test_initialization(self):
        """Test proper initialization of step status."""
        status = WorkflowStepStatus(
            step_id="step1",
            status_type=WorkflowStepStatusType.RUNNING,
            message="Test status message",
            progress=50,
            metadata={
                "start_time": 1234567890,
                "end_time": None
            }
        )
        
        assert status.step_id == "step1"
        assert status.status_type == WorkflowStepStatusType.RUNNING
        assert status.message == "Test status message"
        assert status.progress == 50
        assert status.metadata["start_time"] == 1234567890
        assert status.metadata["end_time"] is None
    
    def test_status_creation(self):
        """Test creating statuses with different types."""
        # Test pending status
        pending_status = WorkflowStepStatus.create_pending_status(
            step_id="step1",
            message="Waiting to start"
        )
        assert pending_status.step_id == "step1"
        assert pending_status.status_type == WorkflowStepStatusType.PENDING
        assert pending_status.message == "Waiting to start"
        assert pending_status.progress == 0
        
        # Test running status
        running_status = WorkflowStepStatus.create_running_status(
            step_id="step1",
            message="Processing",
            progress=50
        )
        assert running_status.step_id == "step1"
        assert running_status.status_type == WorkflowStepStatusType.RUNNING
        assert running_status.message == "Processing"
        assert running_status.progress == 50
        
        # Test completed status
        completed_status = WorkflowStepStatus.create_completed_status(
            step_id="step1",
            message="Successfully completed"
        )
        assert completed_status.step_id == "step1"
        assert completed_status.status_type == WorkflowStepStatusType.COMPLETED
        assert completed_status.message == "Successfully completed"
        assert completed_status.progress == 100
        
        # Test failed status
        failed_status = WorkflowStepStatus.create_failed_status(
            step_id="step1",
            message="Operation failed",
            error="Test error"
        )
        assert failed_status.step_id == "step1"
        assert failed_status.status_type == WorkflowStepStatusType.FAILED
        assert failed_status.message == "Operation failed"
        assert failed_status.metadata["error"] == "Test error"
        
        # Test cancelled status
        cancelled_status = WorkflowStepStatus.create_cancelled_status(
            step_id="step1",
            message="Operation cancelled"
        )
        assert cancelled_status.step_id == "step1"
        assert cancelled_status.status_type == WorkflowStepStatusType.CANCELLED
        assert cancelled_status.message == "Operation cancelled"
    
    def test_status_serialization(self):
        """Test serializing status to dictionary."""
        status = WorkflowStepStatus(
            step_id="step1",
            status_type=WorkflowStepStatusType.RUNNING,
            message="Test status message",
            progress=50,
            metadata={
                "start_time": 1234567890,
                "end_time": None
            }
        )
        
        serialized = status.to_dict()
        assert serialized["step_id"] == "step1"
        assert serialized["status_type"] == "RUNNING"
        assert serialized["message"] == "Test status message"
        assert serialized["progress"] == 50
        assert serialized["metadata"]["start_time"] == 1234567890
        assert serialized["metadata"]["end_time"] is None
    
    def test_status_deserialization(self):
        """Test deserializing status from dictionary."""
        data = {
            "step_id": "step1",
            "status_type": "RUNNING",
            "message": "Test status message",
            "progress": 50,
            "metadata": {
                "start_time": 1234567890,
                "end_time": None
            }
        }
        
        status = WorkflowStepStatus.from_dict(data)
        assert status.step_id == "step1"
        assert status.status_type == WorkflowStepStatusType.RUNNING
        assert status.message == "Test status message"
        assert status.progress == 50
        assert status.metadata["start_time"] == 1234567890
        assert status.metadata["end_time"] is None

class TestWorkflowStepStatusManager:
    """Test suite for WorkflowStepStatusManager."""
    
    def test_initialization(self):
        """Test proper initialization of status manager."""
        manager = WorkflowStepStatusManager()
        assert manager is not None
        assert manager.statuses is not None
    
    def test_update_status(self):
        """Test updating step status."""
        manager = WorkflowStepStatusManager()
        
        # Update status
        status = WorkflowStepStatus.create_running_status(
            step_id="step1",
            message="Processing",
            progress=50
        )
        manager.update_status(status)
        
        # Verify status was updated
        current_status = manager.get_status("step1")
        assert current_status.step_id == "step1"
        assert current_status.status_type == WorkflowStepStatusType.RUNNING
        assert current_status.message == "Processing"
        assert current_status.progress == 50
    
    def test_get_status(self):
        """Test retrieving step status."""
        manager = WorkflowStepStatusManager()
        
        # Update status
        status = WorkflowStepStatus.create_running_status(
            step_id="step1",
            message="Processing",
            progress=50
        )
        manager.update_status(status)
        
        # Get status
        retrieved_status = manager.get_status("step1")
        assert retrieved_status.step_id == "step1"
        assert retrieved_status.status_type == WorkflowStepStatusType.RUNNING
        assert retrieved_status.message == "Processing"
        assert retrieved_status.progress == 50
    
    def test_get_unknown_status(self):
        """Test retrieving unknown step status."""
        manager = WorkflowStepStatusManager()
        
        with pytest.raises(KeyError):
            manager.get_status("unknown_step")
    
    def test_get_status_history(self):
        """Test retrieving step status history."""
        manager = WorkflowStepStatusManager()
        
        # Update status multiple times
        status1 = WorkflowStepStatus.create_pending_status(
            step_id="step1",
            message="Waiting to start"
        )
        status2 = WorkflowStepStatus.create_running_status(
            step_id="step1",
            message="Processing",
            progress=50
        )
        status3 = WorkflowStepStatus.create_completed_status(
            step_id="step1",
            message="Successfully completed"
        )
        
        manager.update_status(status1)
        manager.update_status(status2)
        manager.update_status(status3)
        
        # Get status history
        history = manager.get_status_history("step1")
        assert len(history) == 3
        assert history[0].status_type == WorkflowStepStatusType.PENDING
        assert history[1].status_type == WorkflowStepStatusType.RUNNING
        assert history[2].status_type == WorkflowStepStatusType.COMPLETED
    
    def test_get_unknown_status_history(self):
        """Test retrieving unknown step status history."""
        manager = WorkflowStepStatusManager()
        
        with pytest.raises(KeyError):
            manager.get_status_history("unknown_step")
    
    def test_clear_status(self):
        """Test clearing step status."""
        manager = WorkflowStepStatusManager()
        
        # Update status
        status = WorkflowStepStatus.create_running_status(
            step_id="step1",
            message="Processing",
            progress=50
        )
        manager.update_status(status)
        
        # Clear status
        manager.clear_status("step1")
        
        # Verify status was cleared
        with pytest.raises(KeyError):
            manager.get_status("step1")
    
    def test_get_all_statuses(self):
        """Test retrieving all step statuses."""
        manager = WorkflowStepStatusManager()
        
        # Update statuses for multiple steps
        status1 = WorkflowStepStatus.create_running_status(
            step_id="step1",
            message="Processing step 1",
            progress=50
        )
        status2 = WorkflowStepStatus.create_running_status(
            step_id="step2",
            message="Processing step 2",
            progress=75
        )
        
        manager.update_status(status1)
        manager.update_status(status2)
        
        # Get all statuses
        all_statuses = manager.get_all_statuses()
        assert len(all_statuses) == 2
        assert all_statuses["step1"].message == "Processing step 1"
        assert all_statuses["step2"].message == "Processing step 2"
    
    def test_get_statuses_by_type(self):
        """Test retrieving step statuses by type."""
        manager = WorkflowStepStatusManager()
        
        # Update statuses with different types
        status1 = WorkflowStepStatus.create_running_status(
            step_id="step1",
            message="Processing step 1",
            progress=50
        )
        status2 = WorkflowStepStatus.create_completed_status(
            step_id="step2",
            message="Completed step 2"
        )
        status3 = WorkflowStepStatus.create_running_status(
            step_id="step3",
            message="Processing step 3",
            progress=25
        )
        
        manager.update_status(status1)
        manager.update_status(status2)
        manager.update_status(status3)
        
        # Get statuses by type
        running_statuses = manager.get_statuses_by_type(WorkflowStepStatusType.RUNNING)
        assert len(running_statuses) == 2
        assert running_statuses["step1"].message == "Processing step 1"
        assert running_statuses["step3"].message == "Processing step 3"
        
        completed_statuses = manager.get_statuses_by_type(WorkflowStepStatusType.COMPLETED)
        assert len(completed_statuses) == 1
        assert completed_statuses["step2"].message == "Completed step 2" 