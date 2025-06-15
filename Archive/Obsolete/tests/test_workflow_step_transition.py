import pytest
from typing import Dict, Any, List

from ..agents.integration.workflow_step_transition import (
    WorkflowStepTransition,
    WorkflowStepTransitionType,
    WorkflowStepTransitionManager
)

class TestWorkflowStepTransition:
    """Test suite for WorkflowStepTransition."""
    
    def test_initialization(self):
        """Test proper initialization of step transition."""
        transition = WorkflowStepTransition(
            from_step_id="step1",
            to_step_id="step2",
            transition_type=WorkflowStepTransitionType.SUCCESS,
            condition="result.status == 'success'",
            metadata={
                "priority": 1,
                "description": "Transition on success"
            }
        )
        
        assert transition.from_step_id == "step1"
        assert transition.to_step_id == "step2"
        assert transition.transition_type == WorkflowStepTransitionType.SUCCESS
        assert transition.condition == "result.status == 'success'"
        assert transition.metadata["priority"] == 1
        assert transition.metadata["description"] == "Transition on success"
    
    def test_transition_creation(self):
        """Test creating transitions with different types."""
        # Test success transition
        success_transition = WorkflowStepTransition.create_success_transition(
            from_step_id="step1",
            to_step_id="step2",
            condition="result.status == 'success'"
        )
        assert success_transition.from_step_id == "step1"
        assert success_transition.to_step_id == "step2"
        assert success_transition.transition_type == WorkflowStepTransitionType.SUCCESS
        assert success_transition.condition == "result.status == 'success'"
        
        # Test error transition
        error_transition = WorkflowStepTransition.create_error_transition(
            from_step_id="step1",
            to_step_id="error_handler",
            condition="result.error is not None"
        )
        assert error_transition.from_step_id == "step1"
        assert error_transition.to_step_id == "error_handler"
        assert error_transition.transition_type == WorkflowStepTransitionType.ERROR
        assert error_transition.condition == "result.error is not None"
        
        # Test timeout transition
        timeout_transition = WorkflowStepTransition.create_timeout_transition(
            from_step_id="step1",
            to_step_id="timeout_handler",
            condition="result.timeout == True"
        )
        assert timeout_transition.from_step_id == "step1"
        assert timeout_transition.to_step_id == "timeout_handler"
        assert timeout_transition.transition_type == WorkflowStepTransitionType.TIMEOUT
        assert timeout_transition.condition == "result.timeout == True"
        
        # Test conditional transition
        conditional_transition = WorkflowStepTransition.create_conditional_transition(
            from_step_id="step1",
            to_step_id="step2",
            condition="result.value > 100"
        )
        assert conditional_transition.from_step_id == "step1"
        assert conditional_transition.to_step_id == "step2"
        assert conditional_transition.transition_type == WorkflowStepTransitionType.CONDITIONAL
        assert conditional_transition.condition == "result.value > 100"
    
    def test_transition_serialization(self):
        """Test serializing transition to dictionary."""
        transition = WorkflowStepTransition(
            from_step_id="step1",
            to_step_id="step2",
            transition_type=WorkflowStepTransitionType.SUCCESS,
            condition="result.status == 'success'",
            metadata={
                "priority": 1,
                "description": "Transition on success"
            }
        )
        
        serialized = transition.to_dict()
        assert serialized["from_step_id"] == "step1"
        assert serialized["to_step_id"] == "step2"
        assert serialized["transition_type"] == "SUCCESS"
        assert serialized["condition"] == "result.status == 'success'"
        assert serialized["metadata"]["priority"] == 1
        assert serialized["metadata"]["description"] == "Transition on success"
    
    def test_transition_deserialization(self):
        """Test deserializing transition from dictionary."""
        data = {
            "from_step_id": "step1",
            "to_step_id": "step2",
            "transition_type": "SUCCESS",
            "condition": "result.status == 'success'",
            "metadata": {
                "priority": 1,
                "description": "Transition on success"
            }
        }
        
        transition = WorkflowStepTransition.from_dict(data)
        assert transition.from_step_id == "step1"
        assert transition.to_step_id == "step2"
        assert transition.transition_type == WorkflowStepTransitionType.SUCCESS
        assert transition.condition == "result.status == 'success'"
        assert transition.metadata["priority"] == 1
        assert transition.metadata["description"] == "Transition on success"

class TestWorkflowStepTransitionManager:
    """Test suite for WorkflowStepTransitionManager."""
    
    def test_initialization(self):
        """Test proper initialization of transition manager."""
        manager = WorkflowStepTransitionManager()
        assert manager is not None
        assert manager.transitions is not None
    
    def test_add_transition(self):
        """Test adding step transition."""
        manager = WorkflowStepTransitionManager()
        
        # Add transition
        transition = WorkflowStepTransition.create_success_transition(
            from_step_id="step1",
            to_step_id="step2",
            condition="result.status == 'success'"
        )
        manager.add_transition(transition)
        
        # Verify transition was added
        transitions = manager.get_transitions("step1")
        assert len(transitions) == 1
        assert transitions[0].to_step_id == "step2"
        assert transitions[0].transition_type == WorkflowStepTransitionType.SUCCESS
    
    def test_get_transitions(self):
        """Test retrieving step transitions."""
        manager = WorkflowStepTransitionManager()
        
        # Add transitions
        transition1 = WorkflowStepTransition.create_success_transition(
            from_step_id="step1",
            to_step_id="step2",
            condition="result.status == 'success'"
        )
        transition2 = WorkflowStepTransition.create_error_transition(
            from_step_id="step1",
            to_step_id="error_handler",
            condition="result.error is not None"
        )
        
        manager.add_transition(transition1)
        manager.add_transition(transition2)
        
        # Get transitions
        transitions = manager.get_transitions("step1")
        assert len(transitions) == 2
        assert transitions[0].to_step_id == "step2"
        assert transitions[1].to_step_id == "error_handler"
    
    def test_get_unknown_transitions(self):
        """Test retrieving unknown step transitions."""
        manager = WorkflowStepTransitionManager()
        
        transitions = manager.get_transitions("unknown_step")
        assert len(transitions) == 0
    
    def test_get_transitions_by_type(self):
        """Test retrieving step transitions by type."""
        manager = WorkflowStepTransitionManager()
        
        # Add transitions with different types
        transition1 = WorkflowStepTransition.create_success_transition(
            from_step_id="step1",
            to_step_id="step2",
            condition="result.status == 'success'"
        )
        transition2 = WorkflowStepTransition.create_error_transition(
            from_step_id="step1",
            to_step_id="error_handler",
            condition="result.error is not None"
        )
        transition3 = WorkflowStepTransition.create_success_transition(
            from_step_id="step1",
            to_step_id="step3",
            condition="result.status == 'success' and result.value > 100"
        )
        
        manager.add_transition(transition1)
        manager.add_transition(transition2)
        manager.add_transition(transition3)
        
        # Get transitions by type
        success_transitions = manager.get_transitions_by_type(
            "step1",
            WorkflowStepTransitionType.SUCCESS
        )
        assert len(success_transitions) == 2
        assert success_transitions[0].to_step_id == "step2"
        assert success_transitions[1].to_step_id == "step3"
        
        error_transitions = manager.get_transitions_by_type(
            "step1",
            WorkflowStepTransitionType.ERROR
        )
        assert len(error_transitions) == 1
        assert error_transitions[0].to_step_id == "error_handler"
    
    def test_remove_transition(self):
        """Test removing step transition."""
        manager = WorkflowStepTransitionManager()
        
        # Add transition
        transition = WorkflowStepTransition.create_success_transition(
            from_step_id="step1",
            to_step_id="step2",
            condition="result.status == 'success'"
        )
        manager.add_transition(transition)
        
        # Remove transition
        manager.remove_transition("step1", "step2")
        
        # Verify transition was removed
        transitions = manager.get_transitions("step1")
        assert len(transitions) == 0
    
    def test_clear_transitions(self):
        """Test clearing all step transitions."""
        manager = WorkflowStepTransitionManager()
        
        # Add transitions
        transition1 = WorkflowStepTransition.create_success_transition(
            from_step_id="step1",
            to_step_id="step2",
            condition="result.status == 'success'"
        )
        transition2 = WorkflowStepTransition.create_error_transition(
            from_step_id="step1",
            to_step_id="error_handler",
            condition="result.error is not None"
        )
        
        manager.add_transition(transition1)
        manager.add_transition(transition2)
        
        # Clear transitions
        manager.clear_transitions("step1")
        
        # Verify transitions were cleared
        transitions = manager.get_transitions("step1")
        assert len(transitions) == 0
    
    def test_get_all_transitions(self):
        """Test retrieving all step transitions."""
        manager = WorkflowStepTransitionManager()
        
        # Add transitions for multiple steps
        transition1 = WorkflowStepTransition.create_success_transition(
            from_step_id="step1",
            to_step_id="step2",
            condition="result.status == 'success'"
        )
        transition2 = WorkflowStepTransition.create_success_transition(
            from_step_id="step2",
            to_step_id="step3",
            condition="result.status == 'success'"
        )
        
        manager.add_transition(transition1)
        manager.add_transition(transition2)
        
        # Get all transitions
        all_transitions = manager.get_all_transitions()
        assert len(all_transitions) == 2
        assert all_transitions["step1"][0].to_step_id == "step2"
        assert all_transitions["step2"][0].to_step_id == "step3" 