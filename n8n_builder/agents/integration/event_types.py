"""
AG-UI compatible event types for N8N Workflow Builder.

This module provides event types that are compatible with the AG-UI protocol
while extending them for N8N workflow-specific functionality.
"""

from typing import Dict, Any, Optional, List, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid

# Import AG-UI core types
from ag_ui.core import (
    Event as AGUIEvent,
    EventType as AGUIEventType,
    BaseEvent as AGUIBaseEvent,
    RunStartedEvent,
    RunFinishedEvent,
    RunErrorEvent,
    TextMessageStartEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
    ToolCallStartEvent,
    ToolCallArgsEvent,
    ToolCallEndEvent,
    StateSnapshotEvent,
    StateDeltaEvent,
    MessagesSnapshotEvent,
    StepStartedEvent,
    StepFinishedEvent,
    RawEvent,
    CustomEvent
)


class EventPriority(Enum):
    """Event priority levels for internal event management."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class WorkflowEventType(Enum):
    """Extended event types specific to N8N workflow operations."""
    # Workflow lifecycle events
    WORKFLOW_GENERATION_STARTED = "WORKFLOW_GENERATION_STARTED"
    WORKFLOW_GENERATION_PROGRESS = "WORKFLOW_GENERATION_PROGRESS"
    WORKFLOW_GENERATION_COMPLETED = "WORKFLOW_GENERATION_COMPLETED"
    WORKFLOW_GENERATION_FAILED = "WORKFLOW_GENERATION_FAILED"
    
    # Workflow modification events
    WORKFLOW_MODIFICATION_STARTED = "WORKFLOW_MODIFICATION_STARTED"
    WORKFLOW_MODIFICATION_COMPLETED = "WORKFLOW_MODIFICATION_COMPLETED"
    WORKFLOW_MODIFICATION_FAILED = "WORKFLOW_MODIFICATION_FAILED"
    
    # Workflow validation events
    WORKFLOW_VALIDATION_STARTED = "WORKFLOW_VALIDATION_STARTED"
    WORKFLOW_VALIDATION_COMPLETED = "WORKFLOW_VALIDATION_COMPLETED"
    WORKFLOW_VALIDATION_FAILED = "WORKFLOW_VALIDATION_FAILED"
    
    # LLM interaction events
    LLM_REQUEST_STARTED = "LLM_REQUEST_STARTED"
    LLM_REQUEST_COMPLETED = "LLM_REQUEST_COMPLETED"
    LLM_REQUEST_FAILED = "LLM_REQUEST_FAILED"
    
    # Node operation events
    NODE_ADDED = "NODE_ADDED"
    NODE_MODIFIED = "NODE_MODIFIED"
    NODE_REMOVED = "NODE_REMOVED"
    CONNECTION_ADDED = "CONNECTION_ADDED"
    CONNECTION_MODIFIED = "CONNECTION_MODIFIED"
    CONNECTION_REMOVED = "CONNECTION_REMOVED"


@dataclass
class WorkflowEvent:
    """
    Extended event class that wraps AG-UI events with workflow-specific metadata.
    """
    # AG-UI compatible fields
    ag_ui_event: Optional[AGUIEvent] = None
    
    # Workflow-specific fields
    type: Union[AGUIEventType, WorkflowEventType] = field(default=WorkflowEventType.WORKFLOW_GENERATION_STARTED)
    workflow_id: Optional[str] = None
    thread_id: Optional[str] = None
    run_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    priority: EventPriority = EventPriority.NORMAL
    source: str = "n8n_workflow_builder"
    
    # Event data
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Error information
    error: Optional[str] = None
    error_code: Optional[str] = None
    
    def to_ag_ui_event(self) -> AGUIEvent:
        """Convert this workflow event to a standard AG-UI event."""
        if self.ag_ui_event:
            return self.ag_ui_event
            
        # Map workflow events to AG-UI events
        if self.type == WorkflowEventType.WORKFLOW_GENERATION_STARTED:
            return RunStartedEvent(
                type=AGUIEventType.RUN_STARTED,
                thread_id=self.thread_id or str(uuid.uuid4()),
                run_id=self.run_id or str(uuid.uuid4()),
                timestamp=int(self.timestamp.timestamp())
            )
        elif self.type == WorkflowEventType.WORKFLOW_GENERATION_COMPLETED:
            return RunFinishedEvent(
                type=AGUIEventType.RUN_FINISHED,
                thread_id=self.thread_id or str(uuid.uuid4()),
                run_id=self.run_id or str(uuid.uuid4()),
                timestamp=int(self.timestamp.timestamp())
            )
        elif self.type == WorkflowEventType.WORKFLOW_GENERATION_FAILED:
            return RunErrorEvent(
                type=AGUIEventType.RUN_ERROR,
                message=self.error or "Workflow generation failed",
                code=self.error_code,
                timestamp=int(self.timestamp.timestamp())
            )
        else:
            # Use custom event for workflow-specific events
            return CustomEvent(
                type=AGUIEventType.CUSTOM,
                name=self.type.value if isinstance(self.type, WorkflowEventType) else str(self.type),
                value={
                    "workflow_id": self.workflow_id,
                    "data": self.data,
                    "metadata": self.metadata
                },
                timestamp=int(self.timestamp.timestamp())
            )
    
    @classmethod
    def from_ag_ui_event(cls, ag_ui_event: AGUIEvent, workflow_id: Optional[str] = None) -> 'WorkflowEvent':
        """Create a WorkflowEvent from an AG-UI event."""
        return cls(
            ag_ui_event=ag_ui_event,
            type=ag_ui_event.type,
            workflow_id=workflow_id,
            thread_id=getattr(ag_ui_event, 'thread_id', None),
            run_id=getattr(ag_ui_event, 'run_id', None),
            timestamp=datetime.fromtimestamp(ag_ui_event.timestamp) if ag_ui_event.timestamp else datetime.now(),
            data=getattr(ag_ui_event, 'value', {}) if hasattr(ag_ui_event, 'value') else {},
            error=getattr(ag_ui_event, 'message', None) if hasattr(ag_ui_event, 'message') else None,
            error_code=getattr(ag_ui_event, 'code', None) if hasattr(ag_ui_event, 'code') else None
        )


# Type aliases for compatibility
Event = WorkflowEvent
EventType = Union[AGUIEventType, WorkflowEventType]

# Export AG-UI event types for direct use
__all__ = [
    # AG-UI event types
    'AGUIEvent', 'AGUIEventType', 'AGUIBaseEvent',
    'RunStartedEvent', 'RunFinishedEvent', 'RunErrorEvent',
    'TextMessageStartEvent', 'TextMessageContentEvent', 'TextMessageEndEvent',
    'ToolCallStartEvent', 'ToolCallArgsEvent', 'ToolCallEndEvent',
    'StateSnapshotEvent', 'StateDeltaEvent', 'MessagesSnapshotEvent',
    'StepStartedEvent', 'StepFinishedEvent',
    'RawEvent', 'CustomEvent',
    
    # Extended workflow types
    'EventPriority', 'WorkflowEventType', 'WorkflowEvent',
    'Event', 'EventType'
]
