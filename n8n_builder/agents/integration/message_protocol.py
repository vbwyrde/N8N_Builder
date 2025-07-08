"""
AG-UI compatible message protocol for N8N Workflow Builder.

This module defines message types and protocols that are compatible with AG-UI
while providing N8N workflow-specific functionality.
"""

from typing import Dict, Any, Optional, List, Union
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid

# Import AG-UI core types
from ag_ui.core import (
    RunAgentInput,
    Message,
    Context,
    Tool,
    State
)


class MessageType(Enum):
    """Message types for workflow operations."""
    # Request types
    WORKFLOW_GENERATION_REQUEST = "workflow_generation_request"
    WORKFLOW_MODIFICATION_REQUEST = "workflow_modification_request"
    WORKFLOW_VALIDATION_REQUEST = "workflow_validation_request"
    WORKFLOW_ITERATION_REQUEST = "workflow_iteration_request"
    
    # Response types
    WORKFLOW_GENERATION_RESPONSE = "workflow_generation_response"
    WORKFLOW_MODIFICATION_RESPONSE = "workflow_modification_response"
    WORKFLOW_VALIDATION_RESPONSE = "workflow_validation_response"
    WORKFLOW_ITERATION_RESPONSE = "workflow_iteration_response"
    
    # Status updates
    STATUS_UPDATE = "status_update"
    PROGRESS_UPDATE = "progress_update"
    ERROR_NOTIFICATION = "error_notification"
    
    # Tool calls
    TOOL_CALL_REQUEST = "tool_call_request"
    TOOL_CALL_RESPONSE = "tool_call_response"


@dataclass
class WorkflowRequest:
    """
    AG-UI compatible workflow request that extends RunAgentInput.
    """
    # Core AG-UI fields
    description: str
    thread_id: Optional[str] = None
    run_id: Optional[str] = None
    messages: List[Message] = field(default_factory=list)
    context: List[Context] = field(default_factory=list)
    tools: List[Tool] = field(default_factory=list)
    state: Optional[State] = None
    
    # N8N workflow specific fields
    workflow_id: Optional[str] = None
    existing_workflow: Optional[Dict[str, Any]] = None
    modification_type: Optional[str] = None
    validation_rules: Optional[Dict[str, Any]] = None
    iteration_feedback: Optional[str] = None
    
    # Request metadata
    request_type: MessageType = MessageType.WORKFLOW_GENERATION_REQUEST
    timestamp: datetime = field(default_factory=datetime.now)
    client_id: Optional[str] = None
    session_id: Optional[str] = None
    
    def to_run_agent_input(self) -> RunAgentInput:
        """Convert to standard AG-UI RunAgentInput."""
        return RunAgentInput(
            messages=self.messages,
            context=self.context,
            tools=self.tools,
            state=self.state
        )
    
    @classmethod
    def from_run_agent_input(cls, input_data: RunAgentInput, description: str, **kwargs) -> 'WorkflowRequest':
        """Create WorkflowRequest from AG-UI RunAgentInput."""
        return cls(
            description=description,
            messages=input_data.messages,
            context=input_data.context,
            tools=input_data.tools,
            state=input_data.state,
            **kwargs
        )


@dataclass
class WorkflowResponse:
    """Response message for workflow operations."""
    # Response identification
    request_id: str
    response_type: MessageType
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Response data
    success: bool = True
    workflow_json: Optional[Dict[str, Any]] = None
    validation_result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    
    # Metadata
    processing_time: Optional[float] = None
    llm_tokens_used: Optional[int] = None
    workflow_complexity: Optional[str] = None
    
    # AG-UI state information
    final_state: Optional[State] = None
    generated_messages: List[Message] = field(default_factory=list)


@dataclass
class StatusUpdate:
    """Status update message for ongoing operations."""
    operation_id: str
    status: str
    progress_percentage: Optional[float] = None
    current_step: Optional[str] = None
    estimated_completion: Optional[datetime] = None
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ToolCallRequest:
    """Request for tool execution."""
    tool_name: str
    tool_id: str
    arguments: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None
    timeout: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ToolCallResponse:
    """Response from tool execution."""
    tool_id: str
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)


class WorkflowTools:
    """Standard tools available for workflow operations."""
    
    @staticmethod
    def get_workflow_validation_tool() -> Tool:
        """Get the workflow validation tool definition."""
        return Tool(
            name="validate_workflow",
            description="Validate an N8N workflow for correctness and best practices",
            parameters={
                "type": "object",
                "properties": {
                    "workflow_json": {
                        "type": "object",
                        "description": "The N8N workflow JSON to validate"
                    },
                    "validation_level": {
                        "type": "string",
                        "enum": ["basic", "strict", "comprehensive"],
                        "description": "Level of validation to perform"
                    }
                },
                "required": ["workflow_json"]
            }
        )
    
    @staticmethod
    def get_workflow_modification_tool() -> Tool:
        """Get the workflow modification tool definition."""
        return Tool(
            name="modify_workflow",
            description="Modify an existing N8N workflow based on instructions",
            parameters={
                "type": "object",
                "properties": {
                    "existing_workflow": {
                        "type": "object",
                        "description": "The existing N8N workflow JSON"
                    },
                    "modification_instructions": {
                        "type": "string",
                        "description": "Instructions for how to modify the workflow"
                    },
                    "preserve_data": {
                        "type": "boolean",
                        "description": "Whether to preserve existing data connections"
                    }
                },
                "required": ["existing_workflow", "modification_instructions"]
            }
        )
    
    @staticmethod
    def get_workflow_optimization_tool() -> Tool:
        """Get the workflow optimization tool definition."""
        return Tool(
            name="optimize_workflow",
            description="Optimize an N8N workflow for performance and best practices",
            parameters={
                "type": "object",
                "properties": {
                    "workflow_json": {
                        "type": "object",
                        "description": "The N8N workflow JSON to optimize"
                    },
                    "optimization_goals": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optimization goals (performance, readability, maintainability)"
                    }
                },
                "required": ["workflow_json"]
            }
        )
    
    @classmethod
    def get_all_tools(cls) -> List[Tool]:
        """Get all available workflow tools."""
        return [
            cls.get_workflow_validation_tool(),
            cls.get_workflow_modification_tool(),
            cls.get_workflow_optimization_tool()
        ]


# Export all message types and utilities
__all__ = [
    'MessageType',
    'WorkflowRequest',
    'WorkflowResponse', 
    'StatusUpdate',
    'ToolCallRequest',
    'ToolCallResponse',
    'WorkflowTools',
    # Re-export AG-UI types
    'RunAgentInput',
    'Message',
    'Context',
    'Tool',
    'State'
]
