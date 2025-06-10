from typing import Dict, Any, Optional, List, Callable
import asyncio
import logging
from datetime import datetime
from .event_types import Event, EventType, EventPriority

class AgentUIController:
    """Manages UI state and interactions."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.ui_state: Dict[str, Any] = {}
        self.callbacks: Dict[str, List[Callable]] = {}
        self.logger = logging.getLogger(__name__)
        self._running = False
        self._tasks: List[asyncio.Task] = []

    async def start(self):
        """Start the UI controller."""
        if self._running:
            return

        self._running = True
        self._tasks = [
            asyncio.create_task(self._process_ui_updates())
        ]
        self.logger.info("UI Controller started")

    async def stop(self):
        """Stop the UI controller."""
        if not self._running:
            return

        self._running = False
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks = []
        self.logger.info("UI Controller stopped")

    async def update_ui_state(self, component_id: str, state: Dict[str, Any]):
        """Update the state of a UI component."""
        if not self._running:
            raise RuntimeError("UI Controller is not running")

        self.ui_state[component_id] = {
            **self.ui_state.get(component_id, {}),
            **state,
            "last_updated": datetime.now().isoformat()
        }
        self.logger.debug(f"Updated UI state for component: {component_id}")

    async def get_ui_state(self, component_id: str) -> Dict[str, Any]:
        """Get the current state of a UI component."""
        return self.ui_state.get(component_id, {})

    async def register_callback(self, component_id: str, callback: Callable):
        """Register a callback for UI state changes."""
        if component_id not in self.callbacks:
            self.callbacks[component_id] = []
        self.callbacks[component_id].append(callback)
        self.logger.debug(f"Registered callback for component: {component_id}")

    async def unregister_callback(self, component_id: str, callback: Callable):
        """Unregister a callback for UI state changes."""
        if component_id in self.callbacks:
            self.callbacks[component_id].remove(callback)
            if not self.callbacks[component_id]:
                del self.callbacks[component_id]
            self.logger.debug(f"Unregistered callback for component: {component_id}")

    async def _process_ui_updates(self):
        """Process UI state updates and notify callbacks."""
        while self._running:
            try:
                # Process any pending UI updates
                for component_id, callbacks in self.callbacks.items():
                    if component_id in self.ui_state:
                        state = self.ui_state[component_id]
                        for callback in callbacks:
                            try:
                                await callback(state)
                            except Exception as e:
                                self.logger.error(f"Error in UI callback: {str(e)}")
                
                await asyncio.sleep(0.1)  # Prevent CPU spinning
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error processing UI updates: {str(e)}")
                await asyncio.sleep(1)  # Back off on error

    async def handle_user_action(self, component_id: str, action: str, data: Dict[str, Any]):
        """Handle a user action from a UI component."""
        try:
            # Create an event for the user action
            event = Event(
                type=EventType.USER_ACTION,
                data={
                    "component_id": component_id,
                    "action": action,
                    "data": data
                },
                priority=EventPriority.NORMAL,
                source="ui_controller"
            )
            
            # Update UI state based on action
            await self.update_ui_state(component_id, {
                "last_action": action,
                "action_data": data,
                "action_time": datetime.now().isoformat()
            })
            
            return event
            
        except Exception as e:
            self.logger.error(f"Error handling user action: {str(e)}")
            return None

    async def get_component_history(self, component_id: str) -> List[Dict[str, Any]]:
        """Get the history of state changes for a component."""
        # This would typically query a database or storage system
        # For now, return an empty list as this is a placeholder
        return [] 