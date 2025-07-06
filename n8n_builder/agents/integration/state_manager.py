"""
AG-UI compatible state manager for N8N Workflow Builder.

This module provides state management that is compatible with AG-UI's state
management events while handling N8N workflow-specific state.
"""

import json
import asyncio
import logging
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from pathlib import Path
import uuid

# Import AG-UI core types
from ag_ui.core import (
    State,
    StateSnapshotEvent,
    StateDeltaEvent,
    EventType as AGUIEventType
)

from .event_types import WorkflowEvent, EventPriority, WorkflowEventType


class StateManager:
    """
    AG-UI compatible state manager for workflow operations.
    
    Manages workflow state using AG-UI patterns with state snapshots and deltas.
    """
    
    def __init__(self, state_file: Optional[str] = None):
        """Initialize the state manager."""
        self.logger = logging.getLogger(__name__)
        self.state_file = Path(state_file) if state_file else None
        
        # Current state
        self._current_state: Dict[str, Any] = {}
        self._state_history: List[Dict[str, Any]] = []
        self._state_subscribers: List[Callable] = []
        
        # Workflow-specific state
        self._active_workflows: Dict[str, Dict[str, Any]] = {}
        self._workflow_history: Dict[str, List[Dict[str, Any]]] = {}
        
        # State management
        self._lock = asyncio.Lock()
        self._auto_save = True
        self._max_history_size = 100
        
        # Load existing state if file exists
        if self.state_file and self.state_file.exists():
            self._load_state()
    
    async def get_current_state(self) -> State:
        """Get the current state as AG-UI State object."""
        async with self._lock:
            return State(**self._current_state)
    
    async def update_state(self, updates: Dict[str, Any], workflow_id: Optional[str] = None) -> StateSnapshotEvent:
        """Update state and return AG-UI StateSnapshotEvent."""
        async with self._lock:
            # Update current state
            self._current_state.update(updates)
            
            # Update workflow-specific state if provided
            if workflow_id:
                if workflow_id not in self._active_workflows:
                    self._active_workflows[workflow_id] = {}
                self._active_workflows[workflow_id].update(updates)
            
            # Add to history
            state_snapshot = {
                "timestamp": datetime.now().isoformat(),
                "state": self._current_state.copy(),
                "workflow_id": workflow_id,
                "updates": updates
            }
            self._state_history.append(state_snapshot)
            
            # Trim history if needed
            if len(self._state_history) > self._max_history_size:
                self._state_history = self._state_history[-self._max_history_size:]
            
            # Auto-save if enabled
            if self._auto_save:
                await self._save_state()
            
            # Create AG-UI StateSnapshotEvent
            ag_ui_state = State(**self._current_state)
            event = StateSnapshotEvent(
                type=AGUIEventType.STATE_SNAPSHOT,
                snapshot=ag_ui_state,
                timestamp=int(datetime.now().timestamp())
            )
            
            # Notify subscribers
            await self._notify_subscribers(event)
            
            return event
    
    async def create_state_delta(self, changes: List[Dict[str, Any]], workflow_id: Optional[str] = None) -> StateDeltaEvent:
        """Create a state delta using JSON Patch format."""
        async with self._lock:
            # Apply changes to current state
            for change in changes:
                if change.get("op") == "replace":
                    path_parts = change.get("path", "").strip("/").split("/")
                    if path_parts and path_parts[0]:
                        self._set_nested_value(self._current_state, path_parts, change.get("value"))
                elif change.get("op") == "add":
                    path_parts = change.get("path", "").strip("/").split("/")
                    if path_parts and path_parts[0]:
                        self._set_nested_value(self._current_state, path_parts, change.get("value"))
                elif change.get("op") == "remove":
                    path_parts = change.get("path", "").strip("/").split("/")
                    if path_parts and path_parts[0]:
                        self._remove_nested_value(self._current_state, path_parts)
            
            # Update workflow state if provided
            if workflow_id:
                if workflow_id not in self._active_workflows:
                    self._active_workflows[workflow_id] = {}
                # Apply same changes to workflow state
                for change in changes:
                    if change.get("op") == "replace":
                        path_parts = change.get("path", "").strip("/").split("/")
                        if path_parts and path_parts[0]:
                            self._set_nested_value(self._active_workflows[workflow_id], path_parts, change.get("value"))
            
            # Create AG-UI StateDeltaEvent
            event = StateDeltaEvent(
                type=AGUIEventType.STATE_DELTA,
                delta=changes,
                timestamp=int(datetime.now().timestamp())
            )
            
            # Auto-save if enabled
            if self._auto_save:
                await self._save_state()
            
            # Notify subscribers
            await self._notify_subscribers(event)
            
            return event
    
    async def get_workflow_state(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get state for a specific workflow."""
        async with self._lock:
            return self._active_workflows.get(workflow_id, {}).copy()
    
    async def set_workflow_state(self, workflow_id: str, state: Dict[str, Any]) -> None:
        """Set state for a specific workflow."""
        async with self._lock:
            self._active_workflows[workflow_id] = state.copy()
            
            # Add to workflow history
            if workflow_id not in self._workflow_history:
                self._workflow_history[workflow_id] = []
            
            self._workflow_history[workflow_id].append({
                "timestamp": datetime.now().isoformat(),
                "state": state.copy()
            })
            
            # Trim workflow history
            if len(self._workflow_history[workflow_id]) > self._max_history_size:
                self._workflow_history[workflow_id] = self._workflow_history[workflow_id][-self._max_history_size:]
            
            # Auto-save if enabled
            if self._auto_save:
                await self._save_state()
    
    async def remove_workflow_state(self, workflow_id: str) -> None:
        """Remove state for a specific workflow."""
        async with self._lock:
            if workflow_id in self._active_workflows:
                del self._active_workflows[workflow_id]
            
            # Auto-save if enabled
            if self._auto_save:
                await self._save_state()
    
    async def subscribe_to_state_changes(self, callback: Callable) -> None:
        """Subscribe to state change notifications."""
        self._state_subscribers.append(callback)
    
    async def unsubscribe_from_state_changes(self, callback: Callable) -> None:
        """Unsubscribe from state change notifications."""
        if callback in self._state_subscribers:
            self._state_subscribers.remove(callback)
    
    async def get_state_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get state change history."""
        async with self._lock:
            history = self._state_history.copy()
            if limit:
                history = history[-limit:]
            return history
    
    async def get_workflow_history(self, workflow_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get state history for a specific workflow."""
        async with self._lock:
            history = self._workflow_history.get(workflow_id, []).copy()
            if limit:
                history = history[-limit:]
            return history
    
    async def clear_state(self) -> None:
        """Clear all state data."""
        async with self._lock:
            self._current_state.clear()
            self._active_workflows.clear()
            self._state_history.clear()
            self._workflow_history.clear()
            
            if self._auto_save:
                await self._save_state()
    
    async def close(self) -> None:
        """Close the state manager and save state."""
        if self._auto_save:
            await self._save_state()
        self._state_subscribers.clear()
    
    def _set_nested_value(self, obj: Dict[str, Any], path: List[str], value: Any) -> None:
        """Set a nested value in a dictionary using a path."""
        current = obj
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[path[-1]] = value
    
    def _remove_nested_value(self, obj: Dict[str, Any], path: List[str]) -> None:
        """Remove a nested value from a dictionary using a path."""
        current = obj
        for key in path[:-1]:
            if key not in current:
                return
            current = current[key]
        if path[-1] in current:
            del current[path[-1]]
    
    async def _notify_subscribers(self, event) -> None:
        """Notify all subscribers of state changes."""
        for callback in self._state_subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                self.logger.error(f"Error notifying state subscriber: {e}")
    
    def _load_state(self) -> None:
        """Load state from file."""
        try:
            if self.state_file and self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    self._current_state = data.get('current_state', {})
                    self._active_workflows = data.get('active_workflows', {})
                    self._state_history = data.get('state_history', [])
                    self._workflow_history = data.get('workflow_history', {})
                self.logger.info(f"Loaded state from {self.state_file}")
        except Exception as e:
            self.logger.error(f"Error loading state from {self.state_file}: {e}")
    
    async def _save_state(self) -> None:
        """Save state to file."""
        try:
            if self.state_file:
                data = {
                    'current_state': self._current_state,
                    'active_workflows': self._active_workflows,
                    'state_history': self._state_history,
                    'workflow_history': self._workflow_history,
                    'saved_at': datetime.now().isoformat()
                }
                
                # Ensure directory exists
                self.state_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(self.state_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                self.logger.debug(f"Saved state to {self.state_file}")
        except Exception as e:
            self.logger.error(f"Error saving state to {self.state_file}: {e}")


__all__ = ['StateManager']
