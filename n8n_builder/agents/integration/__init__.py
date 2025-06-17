"""
AG-UI Integration Module for N8N Workflow Builder.

This module provides AG-UI compatible components for the N8N Workflow Builder,
enabling proper integration with the AG-UI protocol while maintaining
N8N workflow-specific functionality.
"""

# Import AG-UI core components
from .event_types import (
    EventPriority,
    WorkflowEventType,
    WorkflowEvent,
    Event,
    EventType,
    # Re-export AG-UI types
    AGUIEvent,
    AGUIEventType,
    AGUIBaseEvent,
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

from .message_protocol import (
    MessageType,
    WorkflowRequest,
    WorkflowResponse,
    StatusUpdate,
    ToolCallRequest,
    ToolCallResponse,
    WorkflowTools,
    # Re-export AG-UI types
    RunAgentInput,
    Message,
    Context,
    Tool,
    State
)

from .state_manager import StateManager
from .message_broker import MessageBroker

# Import existing components
from .event_stream_manager import EventStreamManager
# from .agent_integration_manager import AgentIntegrationManager  # Temporarily disabled - needs refactoring
from .ui_controller import AgentUIController
from .monitoring import MonitoringManager
from .security import SecurityManager
from .error_recovery import ErrorRecoveryManager

__version__ = "0.1.0"

__all__ = [
    # Event types
    'EventPriority',
    'WorkflowEventType', 
    'WorkflowEvent',
    'Event',
    'EventType',
    
    # AG-UI event types
    'AGUIEvent',
    'AGUIEventType',
    'AGUIBaseEvent',
    'RunStartedEvent',
    'RunFinishedEvent',
    'RunErrorEvent',
    'TextMessageStartEvent',
    'TextMessageContentEvent',
    'TextMessageEndEvent',
    'ToolCallStartEvent',
    'ToolCallArgsEvent',
    'ToolCallEndEvent',
    'StateSnapshotEvent',
    'StateDeltaEvent',
    'MessagesSnapshotEvent',
    'StepStartedEvent',
    'StepFinishedEvent',
    'RawEvent',
    'CustomEvent',
    
    # Message protocol
    'MessageType',
    'WorkflowRequest',
    'WorkflowResponse',
    'StatusUpdate',
    'ToolCallRequest',
    'ToolCallResponse',
    'WorkflowTools',
    
    # AG-UI message types
    'RunAgentInput',
    'Message',
    'Context',
    'Tool',
    'State',
    
    # Core managers
    'StateManager',
    'MessageBroker',
    'EventStreamManager',
    # 'AgentIntegrationManager',  # Temporarily disabled
    'AgentUIController',
    
    # Support managers
    'MonitoringManager',
    'SecurityManager',
    'ErrorRecoveryManager'
]
