import json
import asyncio
import logging
from typing import Dict, Any, Optional, Set
from datetime import datetime
from pathlib import Path

class StateManager:
    """Manages shared state between agents with persistence and synchronization."""
    
    def __init__(self, state_file: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.state_file = state_file
        self.state: Dict[str, Any] = {}
        self.state_locks: Dict[str, asyncio.Lock] = {}
        self.state_subscribers: Dict[str, Set[str]] = {}
        self.last_save = datetime.utcnow()
        self.save_interval = 300  # 5 minutes
        self.logger.info("StateManager initialized")
        
        # Load initial state if file exists
        if state_file and Path(state_file).exists():
            self._load_state()
    
    def _load_state(self):
        """Load state from file."""
        try:
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
            self.logger.info(f"State loaded from {self.state_file}")
        except Exception as e:
            self.logger.error(f"Error loading state: {str(e)}")
            self.state = {}
    
    async def _save_state(self):
        """Save state to file."""
        if not self.state_file:
            return
        
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            self.last_save = datetime.utcnow()
            self.logger.info(f"State saved to {self.state_file}")
        except Exception as e:
            self.logger.error(f"Error saving state: {str(e)}")
    
    async def get_state(self, key: str, default: Any = None) -> Any:
        """Get state value with optional default."""
        return self.state.get(key, default)
    
    async def set_state(self, key: str, value: Any, agent_id: str):
        """Set state value with synchronization."""
        # Get or create lock for this key
        if key not in self.state_locks:
            self.state_locks[key] = asyncio.Lock()
        
        async with self.state_locks[key]:
            self.state[key] = value
            self.logger.debug(f"State updated for key {key} by agent {agent_id}")
            
            # Notify subscribers
            if key in self.state_subscribers:
                for subscriber in self.state_subscribers[key]:
                    self.logger.debug(f"Notifying subscriber {subscriber} of state change for {key}")
            
            # Save state if enough time has passed
            if (datetime.utcnow() - self.last_save).total_seconds() > self.save_interval:
                await self._save_state()
    
    async def delete_state(self, key: str):
        """Delete state value."""
        if key in self.state:
            del self.state[key]
            if key in self.state_locks:
                del self.state_locks[key]
            if key in self.state_subscribers:
                del self.state_subscribers[key]
            await self._save_state()
    
    async def subscribe_to_state(self, key: str, agent_id: str):
        """Subscribe an agent to state changes for a key."""
        if key not in self.state_subscribers:
            self.state_subscribers[key] = set()
        self.state_subscribers[key].add(agent_id)
        self.logger.info(f"Agent {agent_id} subscribed to state changes for {key}")
    
    async def unsubscribe_from_state(self, key: str, agent_id: str):
        """Unsubscribe an agent from state changes for a key."""
        if key in self.state_subscribers:
            self.state_subscribers[key].discard(agent_id)
            self.logger.info(f"Agent {agent_id} unsubscribed from state changes for {key}")
    
    async def get_all_state(self) -> Dict[str, Any]:
        """Get all state values."""
        return self.state.copy()
    
    async def clear_state(self):
        """Clear all state."""
        self.state.clear()
        self.state_locks.clear()
        self.state_subscribers.clear()
        await self._save_state()
    
    async def get_state_keys(self) -> Set[str]:
        """Get all state keys."""
        return set(self.state.keys())
    
    async def has_state(self, key: str) -> bool:
        """Check if state exists for key."""
        return key in self.state
    
    async def get_state_metadata(self, key: str) -> Dict[str, Any]:
        """Get metadata about state value."""
        if key not in self.state:
            return {}
        
        return {
            "subscribers": list(self.state_subscribers.get(key, set())),
            "has_lock": key in self.state_locks,
            "value_type": type(self.state[key]).__name__
        }
    
    async def close(self):
        """Clean up and save final state."""
        await self._save_state()
        self.logger.info("StateManager closed") 