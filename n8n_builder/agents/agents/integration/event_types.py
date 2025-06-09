from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, List

class EventType(Enum):
    """Types of events that can be emitted by the system."""
    # Workflow Events
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_ERROR = "workflow_error"
    WORKFLOW_PROGRESS = "workflow_progress"
    
    # Agent Events
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_ERROR = "agent_error"
    
    # System Events
    SYSTEM_STARTED = "system_started"
    SYSTEM_STOPPED = "system_stopped"
    SYSTEM_ERROR = "system_error"
    
    # Resource Events
    RESOURCE_ALLOCATED = "resource_allocated"
    RESOURCE_RELEASED = "resource_released"
    RESOURCE_LIMIT_EXCEEDED = "resource_limit_exceeded"

@dataclass
class Event:
    """Base class for all events in the system."""
    event_type: EventType
    timestamp: datetime
    source: str
    correlation_id: Optional[str] = None
    parent_event_id: Optional[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class WorkflowEvent(Event):
    """Events related to workflow processing."""
    workflow_id: str
    workflow_status: str
    progress: Optional[float] = None
    error_message: Optional[str] = None

@dataclass
class AgentEvent(Event):
    """Events related to agent operations."""
    agent_id: str
    agent_status: str
    operation: str
    result: Optional[Any] = None
    error_message: Optional[str] = None

@dataclass
class ResourceEvent(Event):
    """Events related to resource management."""
    resource_type: str
    resource_id: str
    action: str
    current_usage: float
    limit: float
    details: Optional[Dict[str, Any]] = None

@dataclass
class SystemEvent(Event):
    """Events related to system operations."""
    component: str
    status: str
    details: Optional[Dict[str, Any]] = None 