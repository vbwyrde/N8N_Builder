from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime

class EventType(Enum):
    """Types of events that can be emitted in the system."""
    WORKFLOW_STARTED = "workflow.started"
    WORKFLOW_COMPLETED = "workflow.completed"
    WORKFLOW_FAILED = "workflow.failed"
    STEP_STARTED = "step.started"
    STEP_COMPLETED = "step.completed"
    STEP_FAILED = "step.failed"
    AGENT_STARTED = "agent.started"
    AGENT_STOPPED = "agent.stopped"
    AGENT_ERROR = "agent.error"
    SYSTEM_ERROR = "system.error"
    SYSTEM_STARTED = "system.started"
    SYSTEM_STOPPED = "system.stopped"
    RESOURCE_WARNING = "resource.warning"
    RESOURCE_LIMIT_REACHED = "resource.limit_reached"
    SECURITY_ALERT = "security.alert"

class EventPriority(Enum):
    """Priority levels for events."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

class Event:
    """Represents an event in the system."""
    def __init__(
        self,
        type: EventType,
        data: Dict[str, Any],
        priority: EventPriority = EventPriority.NORMAL,
        source: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ):
        self.type = type
        self.data = data
        self.priority = priority
        self.source = source
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary format."""
        return {
            "type": self.type.value,
            "data": self.data,
            "priority": self.priority.value,
            "source": self.source,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Event':
        """Create event from dictionary format."""
        return cls(
            type=EventType(data["type"]),
            data=data["data"],
            priority=EventPriority(data["priority"]),
            source=data.get("source"),
            timestamp=datetime.fromisoformat(data["timestamp"])
        )

class WorkflowEvent(Event):
    """Event specific to workflow operations."""
    def __init__(
        self,
        type: EventType,
        workflow_id: str,
        status: str,
        progress: Optional[float] = None,
        error_message: Optional[str] = None,
        priority: EventPriority = EventPriority.NORMAL,
        timestamp: Optional[datetime] = None
    ):
        data = {
            'workflow_id': workflow_id,
            'status': status,
            'progress': progress,
            'error_message': error_message
        }
        super().__init__(type, data, priority, 'workflow', timestamp)

class AgentEvent(Event):
    """Event specific to agent operations."""
    def __init__(
        self,
        type: EventType,
        agent_id: str,
        status: str,
        operation: str,
        result: Optional[Any] = None,
        error_message: Optional[str] = None,
        priority: EventPriority = EventPriority.NORMAL,
        timestamp: Optional[datetime] = None
    ):
        data = {
            'agent_id': agent_id,
            'status': status,
            'operation': operation,
            'result': result,
            'error_message': error_message
        }
        super().__init__(type, data, priority, 'agent', timestamp)

class ResourceEvent(Event):
    """Event specific to resource monitoring."""
    def __init__(
        self,
        type: EventType,
        resource_type: str,
        resource_id: str,
        action: str,
        current_usage: float,
        limit: float,
        details: Optional[Dict[str, Any]] = None,
        priority: EventPriority = EventPriority.NORMAL,
        timestamp: Optional[datetime] = None
    ):
        data = {
            'resource_type': resource_type,
            'resource_id': resource_id,
            'action': action,
            'current_usage': current_usage,
            'limit': limit,
            'details': details or {}
        }
        super().__init__(type, data, priority, 'resource', timestamp)

class SystemEvent(Event):
    """Event specific to system operations."""
    def __init__(
        self,
        type: EventType,
        component: str,
        status: str,
        details: Optional[Dict[str, Any]] = None,
        priority: EventPriority = EventPriority.NORMAL,
        timestamp: Optional[datetime] = None
    ):
        data = {
            'component': component,
            'status': status,
            'details': details or {}
        }
        super().__init__(type, data, priority, 'system', timestamp) 