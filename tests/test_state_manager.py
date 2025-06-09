import pytest
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any

from n8n_builder.agents.integration.state_manager import (
    StateManager,
    State,
    StateType,
    StateTransition
)

pytestmark = pytest.mark.asyncio

class TestStateManager:
    """Test suite for StateManager."""
    
    async def test_initialization(self, state_manager):
        """Test proper initialization of the manager."""
        assert state_manager is not None
        assert state_manager.states is not None
        assert state_manager.transitions is not None
        assert state_manager.config is not None
    
    async def test_state_creation(self, state_manager):
        """Test state creation functionality."""
        # Create a test state
        state = State(
            id="test_state",
            type=StateType.WORKFLOW,
            data={"workflow_id": "test_workflow"},
            created_at=datetime.now()
        )
        
        # Add state
        await state_manager.add_state(state)
        
        # Verify state was added
        retrieved_state = await state_manager.get_state("test_state")
        assert retrieved_state is not None
        assert retrieved_state.id == "test_state"
        assert retrieved_state.type == StateType.WORKFLOW
        assert retrieved_state.data["workflow_id"] == "test_workflow"
    
    async def test_state_transition(self, state_manager):
        """Test state transition functionality."""
        # Create initial state
        initial_state = State(
            id="initial_state",
            type=StateType.WORKFLOW,
            data={"workflow_id": "test_workflow"},
            created_at=datetime.now()
        )
        await state_manager.add_state(initial_state)
        
        # Create target state
        target_state = State(
            id="target_state",
            type=StateType.WORKFLOW,
            data={"workflow_id": "test_workflow", "status": "completed"},
            created_at=datetime.now()
        )
        await state_manager.add_state(target_state)
        
        # Create transition
        transition = StateTransition(
            from_state="initial_state",
            to_state="target_state",
            timestamp=datetime.now(),
            metadata={"reason": "workflow_completed"}
        )
        
        # Execute transition
        await state_manager.transition_state(transition)
        
        # Verify transition
        current_state = await state_manager.get_current_state("test_workflow")
        assert current_state.id == "target_state"
        assert current_state.data["status"] == "completed"
    
    async def test_state_history(self, state_manager):
        """Test state history retrieval."""
        # Create multiple states
        states = [
            State(
                id=f"state_{i}",
                type=StateType.WORKFLOW,
                data={"workflow_id": "test_workflow", "step": i},
                created_at=datetime.now()
            )
            for i in range(3)
        ]
        
        # Add states and transitions
        for i, state in enumerate(states):
            await state_manager.add_state(state)
            if i > 0:
                transition = StateTransition(
                    from_state=states[i-1].id,
                    to_state=state.id,
                    timestamp=datetime.now(),
                    metadata={"step": i}
                )
                await state_manager.transition_state(transition)
        
        # Get state history
        history = await state_manager.get_state_history("test_workflow")
        assert len(history) == 3
        
        # Verify history order
        for i, state in enumerate(history):
            assert state.data["step"] == i
    
    async def test_state_validation(self, state_manager):
        """Test state validation functionality."""
        # Create invalid state (missing required field)
        invalid_state = State(
            id="invalid_state",
            type=StateType.WORKFLOW,
            data={},  # Missing workflow_id
            created_at=datetime.now()
        )
        
        # Verify state validation fails
        with pytest.raises(Exception):
            await state_manager.add_state(invalid_state)
    
    async def test_state_cleanup(self, state_manager):
        """Test state cleanup functionality."""
        # Create old state
        old_state = State(
            id="old_state",
            type=StateType.WORKFLOW,
            data={"workflow_id": "test_workflow"},
            created_at=datetime.now() - timedelta(days=2)
        )
        await state_manager.add_state(old_state)
        
        # Create new state
        new_state = State(
            id="new_state",
            type=StateType.WORKFLOW,
            data={"workflow_id": "test_workflow"},
            created_at=datetime.now()
        )
        await state_manager.add_state(new_state)
        
        # Run cleanup
        await state_manager.cleanup_old_states(timedelta(days=1))
        
        # Verify old state was removed
        with pytest.raises(Exception):
            await state_manager.get_state("old_state")
        
        # Verify new state remains
        assert await state_manager.get_state("new_state") is not None
    
    async def test_state_querying(self, state_manager):
        """Test state querying functionality."""
        # Create multiple states
        states = [
            State(
                id=f"state_{i}",
                type=StateType.WORKFLOW,
                data={
                    "workflow_id": "test_workflow",
                    "status": "active" if i % 2 == 0 else "completed"
                },
                created_at=datetime.now()
            )
            for i in range(5)
        ]
        
        # Add states
        for state in states:
            await state_manager.add_state(state)
        
        # Query active states
        active_states = await state_manager.query_states(
            type=StateType.WORKFLOW,
            filters={"status": "active"}
        )
        assert len(active_states) == 3
        
        # Query completed states
        completed_states = await state_manager.query_states(
            type=StateType.WORKFLOW,
            filters={"status": "completed"}
        )
        assert len(completed_states) == 2
    
    async def test_state_locking(self, state_manager):
        """Test state locking functionality."""
        # Create a test state
        state = State(
            id="test_state",
            type=StateType.WORKFLOW,
            data={"workflow_id": "test_workflow"},
            created_at=datetime.now()
        )
        await state_manager.add_state(state)
        
        # Lock state
        await state_manager.lock_state("test_state", "test_lock")
        
        # Verify state is locked
        assert await state_manager.is_state_locked("test_state")
        
        # Try to lock again
        with pytest.raises(Exception):
            await state_manager.lock_state("test_state", "another_lock")
        
        # Unlock state
        await state_manager.unlock_state("test_state", "test_lock")
        
        # Verify state is unlocked
        assert not await state_manager.is_state_locked("test_state")
    
    async def test_state_events(self, state_manager):
        """Test state event handling."""
        # Create event handlers
        state_events = []
        transition_events = []
        
        async def on_state_change(state: State):
            state_events.append(state)
        
        async def on_transition(transition: StateTransition):
            transition_events.append(transition)
        
        # Register event handlers
        state_manager.on_state_change(on_state_change)
        state_manager.on_transition(on_transition)
        
        # Create and add state
        state = State(
            id="test_state",
            type=StateType.WORKFLOW,
            data={"workflow_id": "test_workflow"},
            created_at=datetime.now()
        )
        await state_manager.add_state(state)
        
        # Create and execute transition
        target_state = State(
            id="target_state",
            type=StateType.WORKFLOW,
            data={"workflow_id": "test_workflow", "status": "completed"},
            created_at=datetime.now()
        )
        await state_manager.add_state(target_state)
        
        transition = StateTransition(
            from_state="test_state",
            to_state="target_state",
            timestamp=datetime.now(),
            metadata={"reason": "test"}
        )
        await state_manager.transition_state(transition)
        
        # Verify events were triggered
        assert len(state_events) == 2  # Initial state and target state
        assert len(transition_events) == 1
    
    async def test_start_stop(self, state_manager):
        """Test starting and stopping the state manager."""
        # Stop the manager
        await state_manager.stop()
        
        # Verify manager is stopped
        assert not state_manager._running
        
        # Start the manager
        await state_manager.start()
        
        # Verify manager is running
        assert state_manager._running
        
        # Test state operations after restart
        state = State(
            id="test_state",
            type=StateType.WORKFLOW,
            data={"workflow_id": "test_workflow"},
            created_at=datetime.now()
        )
        await state_manager.add_state(state)
        
        retrieved_state = await state_manager.get_state("test_state")
        assert retrieved_state is not None
        assert retrieved_state.id == "test_state" 