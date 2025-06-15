"""
Base agent class for the N8N Builder system.
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class AgentConfig:
    """Configuration for agent initialization."""
    name: str
    capabilities: Dict[str, Any]
    max_concurrent_workflows: int = 5
    timeout: int = 300
    security: Dict[str, Any] = None
    error_recovery: Dict[str, Any] = None
    monitoring: Dict[str, Any] = None
    resource_limits: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.security is None:
            self.security = {}
        if self.error_recovery is None:
            self.error_recovery = {}
        if self.monitoring is None:
            self.monitoring = {}
        if self.resource_limits is None:
            self.resource_limits = {}
    
    def get(self, key: str, default=None):
        """Get configuration value by key."""
        return getattr(self, key, default)

@dataclass 
class AgentResult:
    """Result from agent processing."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}
        if self.metadata is None:
            self.metadata = {}

class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.name = config.name
        
    @abstractmethod
    async def process(self, request: Dict[str, Any]) -> AgentResult:
        """Process a request and return results."""
        pass
    
    async def start(self):
        """Start the agent."""
        self.logger.info(f"Starting {self.name}")
    
    async def stop(self):
        """Stop the agent."""
        self.logger.info(f"Stopping {self.name}")
    
    async def get_status(self) -> Dict[str, Any]:
        """Get agent status."""
        return {
            'name': self.name,
            'status': 'active',
            'capabilities': self.config.capabilities
        }
    
    async def close(self):
        """Close the agent and clean up resources."""
        self.logger.info(f"Closing {self.name}")
        # Subclasses can override this for cleanup 