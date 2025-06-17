"""
AG-UI Compatible Base Agent Classes for N8N Workflow Builder.

This module provides the foundation for creating AG-UI compatible agents
that can participate in the N8N workflow generation process while emitting
proper AG-UI events and managing state according to the protocol.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, AsyncGenerator, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    pass
from dataclasses import dataclass, field
from datetime import datetime
import logging
import uuid
import asyncio

# Import AG-UI core types
from ag_ui.core import (
    Event as AGUIEvent,
    EventType as AGUIEventType,
    RunAgentInput,
    RunStartedEvent,
    RunFinishedEvent,
    RunErrorEvent,
    TextMessageStartEvent,
    TextMessageContentEvent,
    TextMessageEndEvent,
    StateSnapshotEvent,
    StateDeltaEvent,
    StepStartedEvent,
    StepFinishedEvent,
    Message,
    State
)

# Import our AG-UI integration components
from .integration.event_types import WorkflowEvent, WorkflowEventType, EventPriority
from .integration.message_protocol import WorkflowRequest, WorkflowResponse, MessageType


@dataclass
class AgentConfig:
    """Configuration for an agent."""
    name: str
    capabilities: Dict[str, bool] = field(default_factory=dict)
    max_concurrent_workflows: int = 5
    timeout: int = 300
    security: Dict[str, Any] = field(default_factory=dict)
    error_recovery: Dict[str, Any] = field(default_factory=dict)
    monitoring: Dict[str, Any] = field(default_factory=dict)
    resource_limits: Dict[str, Any] = field(default_factory=dict)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return getattr(self, key, default)


@dataclass
class AgentResult:
    """Result from an agent operation."""
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    agent_id: Optional[str] = None
    operation_id: Optional[str] = None


class BaseAgent(ABC):
    """
    AG-UI compatible base class for all agents in the system.

    This class implements the AG-UI protocol for agent communication,
    including proper event emission and state management.
    """

    def __init__(self, config: AgentConfig):
        """Initialize the AG-UI compatible base agent."""
        self.config = config
        self.name = config.name
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
        self.agent_id = str(uuid.uuid4())
        self._running = False
        self._capabilities = config.capabilities

        # AG-UI specific properties
        self._current_state: Dict[str, Any] = {}
        self._event_subscribers: List[Callable] = []
        self._active_runs: Dict[str, Dict[str, Any]] = {}

    @abstractmethod
    async def process_ag_ui_request(self, input_data: RunAgentInput) -> AsyncGenerator[AGUIEvent, None]:
        """
        Process an AG-UI request and yield events.

        This is the main AG-UI compatible method that agents must implement.
        It should yield a stream of AG-UI events during processing.
        """
        pass

    async def run_agent(self, input_data: RunAgentInput) -> AsyncGenerator[AGUIEvent, None]:
        """
        Main AG-UI entry point for running the agent.

        This method handles the AG-UI protocol lifecycle and delegates
        to the agent-specific processing logic.
        """
        run_id = str(uuid.uuid4())
        thread_id = str(uuid.uuid4())

        try:
            # Emit run started event
            yield RunStartedEvent(
                type=AGUIEventType.RUN_STARTED,
                thread_id=thread_id,
                run_id=run_id,
                timestamp=int(datetime.now().timestamp())
            )

            # Track the active run
            self._active_runs[run_id] = {
                'thread_id': thread_id,
                'start_time': datetime.now(),
                'status': 'running'
            }

            # Process the request and yield events
            async for event in self.process_ag_ui_request(input_data):
                yield event

            # Emit run finished event
            yield RunFinishedEvent(
                type=AGUIEventType.RUN_FINISHED,
                thread_id=thread_id,
                run_id=run_id,
                timestamp=int(datetime.now().timestamp())
            )

            # Update run status
            self._active_runs[run_id]['status'] = 'completed'

        except Exception as e:
            # Emit run error event
            yield RunErrorEvent(
                type=AGUIEventType.RUN_ERROR,
                message=str(e),
                code=type(e).__name__,
                timestamp=int(datetime.now().timestamp())
            )

            # Update run status
            if run_id in self._active_runs:
                self._active_runs[run_id]['status'] = 'failed'
                self._active_runs[run_id]['error'] = str(e)

            self.logger.error(f"Agent {self.name} run failed: {e}")

        finally:
            # Clean up completed runs
            if run_id in self._active_runs:
                self._active_runs[run_id]['end_time'] = datetime.now()

    async def emit_text_message(self, content: str, message_id: Optional[str] = None) -> AsyncGenerator[AGUIEvent, None]:
        """Emit a text message as AG-UI events."""
        if not message_id:
            message_id = str(uuid.uuid4())

        # Start message
        yield TextMessageStartEvent(
            type=AGUIEventType.TEXT_MESSAGE_START,
            message_id=message_id,
            role="assistant",
            timestamp=int(datetime.now().timestamp())
        )

        # Content (could be chunked for streaming)
        yield TextMessageContentEvent(
            type=AGUIEventType.TEXT_MESSAGE_CONTENT,
            message_id=message_id,
            delta=content,
            timestamp=int(datetime.now().timestamp())
        )

        # End message
        yield TextMessageEndEvent(
            type=AGUIEventType.TEXT_MESSAGE_END,
            message_id=message_id,
            timestamp=int(datetime.now().timestamp())
        )

    async def emit_state_update(self, state_updates: Dict[str, Any]) -> StateSnapshotEvent:
        """Emit a state update as AG-UI event."""
        self._current_state.update(state_updates)

        return StateSnapshotEvent(
            type=AGUIEventType.STATE_SNAPSHOT,
            snapshot=State(**self._current_state),
            timestamp=int(datetime.now().timestamp())
        )

    async def emit_step_events(self, step_name: str) -> AsyncGenerator[AGUIEvent, None]:
        """Emit step start and end events."""
        # Step started
        yield StepStartedEvent(
            type=AGUIEventType.STEP_STARTED,
            step_name=step_name,
            timestamp=int(datetime.now().timestamp())
        )

        # Yield control back to caller for step processing
        yield

        # Step finished
        yield StepFinishedEvent(
            type=AGUIEventType.STEP_FINISHED,
            step_name=step_name,
            timestamp=int(datetime.now().timestamp())
        )

    # Legacy compatibility methods
    async def process(self, request: Dict[str, Any]) -> AgentResult:
        """Legacy process method for backward compatibility."""
        return AgentResult(
            success=True,
            data={'message': f'{self.name} processed request'},
            agent_id=self.agent_id
        )

    async def start(self) -> None:
        """Start the agent."""
        self._running = True
        self.logger.info(f"AG-UI compatible agent {self.name} started")

    async def stop(self) -> None:
        """Stop the agent."""
        self._running = False
        self.logger.info(f"AG-UI compatible agent {self.name} stopped")

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent."""
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'running': self._running,
            'capabilities': self._capabilities,
            'active_runs': len(self._active_runs),
            'current_state': self._current_state,
            'ag_ui_compatible': True,
            'timestamp': datetime.now().isoformat()
        }

    async def close(self) -> None:
        """Close the agent and clean up resources."""
        await self.stop()
        self._active_runs.clear()
        self._event_subscribers.clear()


# AG-UI Compatible Agent Implementations
class OrchestratorAgent(BaseAgent):
    """AG-UI compatible orchestrator agent for managing workflow operations."""

    async def process_ag_ui_request(self, input_data: RunAgentInput) -> AsyncGenerator[AGUIEvent, None]:
        """Process orchestration requests using AG-UI protocol."""
        async for event in self.emit_text_message("Orchestrator agent processing request..."):
            yield event

        state_event = await self.emit_state_update({
            'current_step': 'orchestration',
            'status': 'completed'
        })
        yield state_event

    async def process(self, request: Dict[str, Any]) -> AgentResult:
        """Legacy process method for backward compatibility."""
        return AgentResult(
            success=True,
            data={'message': 'Orchestrator agent - use AG-UI interface'},
            agent_id=self.agent_id
        )


class WorkflowGeneratorAgent(BaseAgent):
    """AG-UI compatible agent for generating N8N workflows."""

    async def process_ag_ui_request(self, input_data: RunAgentInput) -> AsyncGenerator[AGUIEvent, None]:
        """Process workflow generation using AG-UI protocol."""
        # Extract description from messages
        description = ""
        if input_data.messages:
            for message in input_data.messages:
                if hasattr(message, 'content') and message.content:
                    description = message.content
                    break

        if not description:
            description = "Generate a basic N8N workflow"

        # Emit step: Starting workflow generation
        yield StepStartedEvent(
            type=AGUIEventType.STEP_STARTED,
            step_name="workflow_generation",
            timestamp=int(datetime.now().timestamp())
        )

        # Emit progress message
        async for event in self.emit_text_message(f"Starting workflow generation for: {description}"):
            yield event

        # Emit state update
        state_event = await self.emit_state_update({
            'current_step': 'workflow_generation',
            'description': description,
            'progress': 0.2
        })
        yield state_event

        # Simulate workflow generation process
        async for event in self.emit_text_message("Analyzing requirements and generating workflow structure..."):
            yield event

        # Update progress
        state_event = await self.emit_state_update({
            'progress': 0.6,
            'current_step': 'generating_nodes'
        })
        yield state_event

        # Generate workflow result
        workflow_result = {
            "name": "Generated Workflow",
            "nodes": [
                {
                    "id": "webhook",
                    "name": "Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "position": [250, 300]
                },
                {
                    "id": "function",
                    "name": "Process Data",
                    "type": "n8n-nodes-base.function",
                    "position": [500, 300]
                }
            ],
            "connections": {
                "webhook": {
                    "main": [
                        [{"node": "function", "type": "main", "index": 0}]
                    ]
                }
            },
            "active": True,
            "settings": {},
            "version": 1
        }

        # Emit completion message with workflow
        async for event in self.emit_text_message(f"Workflow generated successfully! Created {len(workflow_result['nodes'])} nodes."):
            yield event

        # Final state update
        state_event = await self.emit_state_update({
            'progress': 1.0,
            'current_step': 'completed',
            'workflow_result': workflow_result,
            'status': 'success'
        })
        yield state_event

        # Emit step completion
        yield StepFinishedEvent(
            type=AGUIEventType.STEP_FINISHED,
            step_name="workflow_generation",
            timestamp=int(datetime.now().timestamp())
        )

    async def process(self, request: Dict[str, Any]) -> AgentResult:
        """Legacy process method for backward compatibility."""
        return AgentResult(
            success=True,
            data={'message': 'Workflow generator agent - use AG-UI interface'},
            agent_id=self.agent_id
        )


class ValidationAgent(BaseAgent):
    """AG-UI compatible agent for validating N8N workflows."""

    async def process_ag_ui_request(self, input_data: RunAgentInput) -> AsyncGenerator[AGUIEvent, None]:
        """Process workflow validation using AG-UI protocol."""
        # Extract workflow data from context or state
        workflow_data = None
        if input_data.context:
            for context_item in input_data.context:
                if hasattr(context_item, 'content') and 'workflow' in str(context_item.content):
                    workflow_data = context_item.content
                    break

        # Emit step: Starting validation
        yield StepStartedEvent(
            type=AGUIEventType.STEP_STARTED,
            step_name="workflow_validation",
            timestamp=int(datetime.now().timestamp())
        )

        # Emit progress message
        async for event in self.emit_text_message("Starting workflow validation..."):
            yield event

        # Emit state update
        state_event = await self.emit_state_update({
            'current_step': 'workflow_validation',
            'progress': 0.3
        })
        yield state_event

        # Perform validation checks
        validation_results = {
            'structure_valid': True,
            'nodes_valid': True,
            'connections_valid': True,
            'warnings': [],
            'errors': []
        }

        if workflow_data:
            async for event in self.emit_text_message("Validating workflow structure and node configurations..."):
                yield event

            # Simulate validation logic
            if not isinstance(workflow_data, dict):
                validation_results['structure_valid'] = False
                validation_results['errors'].append("Workflow data must be a valid JSON object")
        else:
            validation_results['warnings'].append("No workflow data provided for validation")

        # Update progress
        state_event = await self.emit_state_update({
            'progress': 0.8,
            'validation_results': validation_results
        })
        yield state_event

        # Emit completion message
        if validation_results['errors']:
            async for event in self.emit_text_message(f"Validation completed with {len(validation_results['errors'])} errors"):
                yield event
        else:
            async for event in self.emit_text_message("Validation completed successfully!"):
                yield event

        # Final state update
        state_event = await self.emit_state_update({
            'progress': 1.0,
            'current_step': 'completed',
            'validation_results': validation_results,
            'status': 'success' if not validation_results['errors'] else 'failed'
        })
        yield state_event

        # Emit step completion
        yield StepFinishedEvent(
            type=AGUIEventType.STEP_FINISHED,
            step_name="workflow_validation",
            timestamp=int(datetime.now().timestamp())
        )

    async def process(self, request: Dict[str, Any]) -> AgentResult:
        """Legacy process method for backward compatibility."""
        return AgentResult(
            success=True,
            data={'message': 'Validation agent - use AG-UI interface'},
            agent_id=self.agent_id
        )


class WorkflowExecutorAgent(BaseAgent):
    """Agent for executing workflows."""
    
    async def process(self, request: Dict[str, Any]) -> AgentResult:
        """Process execution requests."""
        return AgentResult(
            success=True,
            data={'message': 'Workflow executor agent placeholder'},
            agent_id=self.agent_id
        )


class ErrorRecoveryAgent(BaseAgent):
    """Agent for handling error recovery."""
    
    async def process(self, request: Dict[str, Any]) -> AgentResult:
        """Process error recovery requests."""
        return AgentResult(
            success=True,
            data={'message': 'Error recovery agent placeholder'},
            agent_id=self.agent_id
        )


class WorkflowOptimizerAgent(BaseAgent):
    """Agent for optimizing workflows."""
    
    async def process(self, request: Dict[str, Any]) -> AgentResult:
        """Process optimization requests."""
        return AgentResult(
            success=True,
            data={'message': 'Workflow optimizer agent placeholder'},
            agent_id=self.agent_id
        )


class WorkflowDocumentationAgent(BaseAgent):
    """Agent for generating workflow documentation."""
    
    async def process(self, request: Dict[str, Any]) -> AgentResult:
        """Process documentation requests."""
        return AgentResult(
            success=True,
            data={'message': 'Documentation agent placeholder'},
            agent_id=self.agent_id
        )


class WorkflowTestingAgent(BaseAgent):
    """Agent for testing workflows."""
    
    async def process(self, request: Dict[str, Any]) -> AgentResult:
        """Process testing requests."""
        return AgentResult(
            success=True,
            data={'message': 'Testing agent placeholder'},
            agent_id=self.agent_id
        )


__all__ = [
    'AgentConfig',
    'AgentResult', 
    'BaseAgent',
    'OrchestratorAgent',
    'WorkflowGeneratorAgent',
    'ValidationAgent',
    'WorkflowExecutorAgent',
    'ErrorRecoveryAgent',
    'WorkflowOptimizerAgent',
    'WorkflowDocumentationAgent',
    'WorkflowTestingAgent'
]
