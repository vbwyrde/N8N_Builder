"""
Agent Integration Manager for N8N Builder.

This module provides the integration layer between the AG-UI protocol
and the N8N Builder agent system.
"""

import logging
import asyncio
import time
from typing import Dict, Any, List, Optional, Set, Callable, Awaitable
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid

from .message_protocol import (
    Message,
    MessageType,
    WorkflowRequest,
    WorkflowResponse,
    StatusUpdate
)
from .event_types import (
    EventType,
    Event,
    WorkflowEvent,
    WorkflowEventType,
    EventPriority
)
from .message_broker import MessageBroker
from .state_manager import StateManager

from ..base_agent import (
    BaseAgent,
    AgentConfig,
    AgentResult,
    OrchestratorAgent,
    WorkflowGeneratorAgent,
    ValidationAgent,
    WorkflowExecutorAgent,
    ErrorRecoveryAgent,
    WorkflowOptimizerAgent,
    WorkflowDocumentationAgent,
    WorkflowTestingAgent
)

class AgentIntegrationManager:
    """
    Manages the integration between AG-UI protocol and N8N Builder agents.
    
    This class is responsible for:
    1. Creating and managing agent instances
    2. Routing messages between AG-UI and agents
    3. Managing workflow state
    4. Handling events from agents and publishing to AG-UI
    """
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize core components
        self.message_broker = MessageBroker()
        self.state_manager = StateManager()
        
        # Initialize agent registry
        self.agents: Dict[str, BaseAgent] = {}
        self.orchestrator: Optional[OrchestratorAgent] = None
        
        # Initialize event stream
        self.event_handlers: Dict[EventType, List[Callable[[Event], Awaitable[None]]]] = {}
        
        # Track active workflows
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        
        # Setup is_running flag for clean shutdown
        self.is_running = False
        self._shutdown_event = asyncio.Event()
    
    async def start(self) -> None:
        """Start the integration manager and initialize all components."""
        self.logger.info("Starting Agent Integration Manager")
        self.is_running = True
        
        # Initialize message broker
        await self.message_broker.start()
        
        # Initialize state manager
        await self.state_manager.initialize()
        
        # Create and initialize agents
        await self._initialize_agents()
        
        # Register message handlers
        self._register_message_handlers()
        
        self.logger.info("Agent Integration Manager started successfully")
    
    async def _initialize_agents(self) -> None:
        """Initialize all agent instances."""
        # Create orchestrator agent
        orchestrator_config = AgentConfig(
            name="workflow_orchestrator",
            capabilities=self.config.capabilities,
            parameters=self.config.parameters
        )
        self.orchestrator = OrchestratorAgent(orchestrator_config)
        await self.orchestrator.initialize()
        self.agents["orchestrator"] = self.orchestrator
        
        # Create and register other agents
        agent_types = {
            "generator": WorkflowGeneratorAgent,
            "validator": ValidationAgent,
            "executor": WorkflowExecutorAgent,
            "error_recovery": ErrorRecoveryAgent,
            "optimizer": WorkflowOptimizerAgent,
            "documenter": WorkflowDocumentationAgent,
            "tester": WorkflowTestingAgent
        }
        
        for agent_type, agent_class in agent_types.items():
            agent_config = AgentConfig(
                name=f"workflow_{agent_type}",
                capabilities=self.config.capabilities,
                parameters=self.config.parameters
            )
            agent = agent_class(agent_config)
            await agent.initialize()
            self.agents[agent_type] = agent
            
            # Register with orchestrator
            if self.orchestrator:
                await self.orchestrator.register_agent(agent_type, agent)
            
            # Register state change handler
            agent.register_event_handler("state_changed", 
                lambda data, agent=agent, agent_type=agent_type: 
                    self._handle_agent_state_change(agent, agent_type, data)
            )
    
    async def _handle_agent_state_change(self, agent: BaseAgent, agent_type: str, data: Dict[str, Any]) -> None:
        """Handle state changes from agents and publish events."""
        old_state = data.get("old_state")
        new_state = data.get("new_state")
        
        event = AgentEvent(
            event_type=EventType.AGENT_STATE_CHANGED,
            timestamp=datetime.now(),
            source=agent_type,
            agent_id=agent.agent_id,
            agent_name=agent.config.name,
            old_state=str(old_state) if old_state else None,
            new_state=str(new_state) if new_state else None
        )
        
        await self.publish_event(event)
    
    def _register_message_handlers(self) -> None:
        """Register message handlers for the message broker."""
        self.message_broker.register_handler(
            MessageType.WORKFLOW_REQUEST,
            self._handle_workflow_request
        )
        self.message_broker.register_handler(
            MessageType.STATUS_UPDATE,
            self._handle_status_update
        )
        self.message_broker.register_handler(
            MessageType.ERROR,
            self._handle_error
        )
    
    async def _handle_workflow_request(self, message: WorkflowRequest) -> None:
        """Handle incoming workflow requests."""
        try:
            # Forward the request to the orchestrator
            if self.orchestrator:
                await self.orchestrator.process(message.content['workflow_data'])
        except Exception as e:
            self.logger.error(f"Error handling workflow request: {str(e)}")
            await self._handle_error(message, str(e))
    
    async def _handle_status_update(self, message: StatusUpdate) -> None:
        """Handle status updates from agents."""
        try:
            # Forward the status update to the orchestrator
            if self.orchestrator:
                await self.orchestrator.handle_status_update(message)
        except Exception as e:
            self.logger.error(f"Error handling status update: {str(e)}")
            await self._handle_error(message, str(e))
    
    async def _handle_error(self, message: Message, error: str) -> None:
        """Handle errors from agents."""
        error_message = ErrorMessage(
            sender=message.sender,
            recipient=message.recipient,
            error=error,
            error_type='agent_error',
            details={'message_id': message.message_id},
            correlation_id=message.correlation_id,
            parent_message_id=message.message_id
        )
        await self.message_broker.publish(error_message)
    
    async def stop(self) -> None:
        """Stop the integration manager and clean up resources."""
        self.logger.info("Stopping Agent Integration Manager")
        self.is_running = False
        self._shutdown_event.set()
        
        # Cancel background tasks
        await self._cancel_background_tasks()
        
        # Close message broker
        await self.message_broker.stop()
        
        # Close state manager
        await self.state_manager.close()
        
        # Close all agents
        for agent in self.agents.values():
            await agent.close()
        
        self.logger.info("Agent Integration Manager stopped successfully")
    
    async def _cancel_background_tasks(self) -> None:
        """Cancel all background tasks."""
        for agent in self.agents.values():
            await agent.cancel_background_tasks()
    
    async def process_workflow(self, workflow_data: Dict[str, Any], token: Optional[str] = None) -> AgentResult:
        """Process a workflow through the agent pipeline."""
        start_time = time.time()
        try:
            # Validate authentication if token provided
            user = None
            if token:
                user = await self.security_manager.validate_token(token)
                if not await self.security_manager.check_permission(user, PermissionLevel.WRITE):
                    raise AuthorizationError("Insufficient permissions to process workflow")
            
            # Validate workflow data
            is_valid, error = await self.security_manager.validate_workflow_data(workflow_data)
            if not is_valid:
                raise ValidationError(f"Invalid workflow data: {error}")
            
            # Check rate limit
            client_id = user.user_id if user else 'anonymous'
            await self.security_manager.check_rate_limit(client_id, 'workflow')
            
            workflow_id = workflow_data.get('workflow_id', 'default')
            self.logger.info(f"Starting workflow processing for ID: {workflow_id}")
            
            # Record workflow start metric
            await self.monitoring_manager.record_metric(
                'workflow.started',
                1,
                MetricType.COUNTER,
                {'workflow_id': workflow_id}
            )
            
            # Initialize workflow state
            await self.state_manager.set_state(
                f"workflow_{workflow_id}",
                {
                    'status': 'processing',
                    'current_agent': None,
                    'start_time': asyncio.get_event_loop().time(),
                    'agents_used': set(),
                    'errors': [],
                    'user_id': user.user_id if user else None
                },
                'integration_manager'
            )
            
            # Create workflow request with error recovery
            async def execute_workflow():
                request = WorkflowRequest(
                    sender='integration_manager',
                    recipient='generator',
                    workflow_data=workflow_data
                )
                await self.message_broker.publish(request)
                return await self._wait_for_workflow_response(workflow_id)
            
            # Execute with circuit breaker and retry
            result = await self.error_recovery_manager.execute_with_circuit_breaker(
                'workflow_executor',
                lambda: self.error_recovery_manager.execute_with_retry(
                    'workflow_processing',
                    execute_workflow
                )
            )
            
            # Record workflow completion metric
            processing_time = time.time() - start_time
            await self.monitoring_manager.record_metric(
                'workflow.completed',
                1,
                MetricType.COUNTER,
                {
                    'workflow_id': workflow_id,
                    'success': str(result.success).lower()
                }
            )
            await self.monitoring_manager.record_metric(
                'workflow.processing_time',
                processing_time,
                MetricType.HISTOGRAM,
                {'workflow_id': workflow_id}
            )
            
            return result
            
        except SecurityError as e:
            # Record security error metric
            await self.monitoring_manager.record_metric(
                'workflow.security_error',
                1,
                MetricType.COUNTER,
                {'error_type': type(e).__name__}
            )
            return await self._handle_workflow_error(workflow_id, AgentResult(
                success=False,
                error=str(e)
            ))
        except Exception as e:
            # Track error
            self.error_recovery_manager.track_error(
                'workflow_executor',
                e,
                {'workflow_id': workflow_id, 'user_id': user.user_id if user else None}
            )
            # Record error metric
            await self.monitoring_manager.record_metric(
                'workflow.error',
                1,
                MetricType.COUNTER,
                {
                    'workflow_id': workflow_id,
                    'error_type': type(e).__name__
                }
            )
            return await self._handle_workflow_error(workflow_id, AgentResult(
                success=False,
                error=str(e)
            ))
    
    async def _handle_workflow_request(self, message: WorkflowRequest):
        """Handle incoming workflow requests."""
        try:
            agent_name = message.recipient
            if agent_name not in self.agents:
                raise ValueError(f"Unknown agent: {agent_name}")
            
            # Update agent state
            self.agent_states[agent_name]['status'] = 'processing'
            self.agent_states[agent_name]['last_activity'] = asyncio.get_event_loop().time()
            
            # Process workflow
            result = await self.agents[agent_name].process(message.content['workflow_data'])
            
            # Create response
            response = WorkflowResponse(
                sender=agent_name,
                recipient=message.sender,
                workflow_result=result.data if result.success else None,
                success=result.success,
                error=result.error,
                correlation_id=message.correlation_id,
                parent_message_id=message.message_id
            )
            
            # Publish response
            await self.message_broker.publish(response)
            
            # Update agent state
            self.agent_states[agent_name]['status'] = 'idle'
            if result.success:
                self.agent_states[agent_name]['success_count'] += 1
            else:
                self.agent_states[agent_name]['error_count'] += 1
            
        except Exception as e:
            # Send error message
            error_msg = ErrorMessage(
                sender=agent_name,
                recipient=message.sender,
                error=str(e),
                error_type='workflow_processing_error',
                details={'message_id': message.message_id},
                correlation_id=message.correlation_id,
                parent_message_id=message.message_id
            )
            await self.message_broker.publish(error_msg)
    
    async def _wait_for_workflow_response(self, workflow_id: str, timeout: int = 300) -> AgentResult:
        """Wait for workflow processing response."""
        try:
            start_time = asyncio.get_event_loop().time()
            while True:
                # Check timeout
                if asyncio.get_event_loop().time() - start_time > timeout:
                    raise TimeoutError(f"Workflow processing timed out after {timeout} seconds")
                
                # Get workflow state
                state = await self.state_manager.get_state(f"workflow_{workflow_id}")
                if not state:
                    raise ValueError(f"Workflow state not found for ID: {workflow_id}")
                
                # Check if processing is complete
                if state['status'] in ['completed', 'failed']:
                    return AgentResult(
                        success=state['status'] == 'completed',
                        data=state.get('result'),
                        error=state.get('error'),
                        metadata={
                            'workflow_id': workflow_id,
                            'processing_time': state.get('end_time', 0) - state.get('start_time', 0),
                            'agents_used': list(state.get('agents_used', set()))
                        }
                    )
                
                # Wait before checking again
                await asyncio.sleep(1)
                
        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e)
            )
    
    async def _handle_workflow_error(self, workflow_id: str, error_result: AgentResult) -> AgentResult:
        """Handle workflow errors and update workflow state."""
        try:
            # Update workflow state
            await self.state_manager.set_state(
                f"workflow_{workflow_id}",
                {
                    'status': 'failed',
                    'error': error_result.error,
                    'end_time': asyncio.get_event_loop().time()
                },
                'integration_manager'
            )
            
            # Send error message with graceful degradation
            async def send_error_message():
                error_msg = ErrorMessage(
                    sender='integration_manager',
                    recipient='',  # Broadcast to all
                    error=error_result.error,
                    error_type='workflow_error',
                    details={'workflow_id': workflow_id}
                )
                await self.message_broker.publish(error_msg)
            
            async def fallback_error_handling():
                self.logger.error(f"Failed to send error message for workflow {workflow_id}: {error_result.error}")
                # Store error locally for later retry
                await self.state_manager.set_state(
                    f"error_retry_{workflow_id}",
                    {
                        'error': error_result.error,
                        'timestamp': datetime.now().isoformat(),
                        'retry_count': 0
                    },
                    'integration_manager'
                )
            
            await self.error_recovery_manager.execute_with_graceful_degradation(
                send_error_message,
                fallback_error_handling
            )
            
        except Exception as e:
            self.logger.error(f"Error handling workflow error: {str(e)}")
        
        return error_result
    
    async def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        """Get the current status of an agent."""
        return self.agent_states.get(agent_name, {})
    
    async def get_workflow_status(self, workflow_id: str, token: Optional[str] = None) -> Dict[str, Any]:
        """Get the current status of a workflow."""
        try:
            # Validate authentication if token provided
            if token:
                user = await self.security_manager.validate_token(token)
                if not await self.security_manager.check_permission(user, PermissionLevel.READ):
                    raise AuthorizationError("Insufficient permissions to view workflow status")
            
            # Check rate limit
            client_id = user.user_id if token else 'anonymous'
            await self.security_manager.check_rate_limit(client_id)
            
            # Get status with error recovery
            async def get_status():
                task = self.workflow_tasks.get(workflow_id)
                if not task:
                    return await super().get_workflow_status(workflow_id)
                
                return {
                    'workflow_id': task.workflow_id,
                    'status': task.status,
                    'priority': task.priority.name,
                    'assigned_agent': task.assigned_agent,
                    'retry_count': task.retry_count,
                    'created_at': task.created_at.isoformat(),
                    'dependencies': list(task.dependencies) if task.dependencies else []
                }
            
            return await self.error_recovery_manager.execute_with_retry(
                'get_workflow_status',
                get_status
            )
            
        except SecurityError as e:
            raise
        except Exception as e:
            self.logger.error(f"Error getting workflow status: {str(e)}")
            raise
    
    async def get_error_stats(self, service_id: str) -> Dict[str, Any]:
        """Get error statistics for a service."""
        return await self.error_recovery_manager.get_error_stats(service_id)

    async def reset_circuit_breaker(self, service_id: str):
        """Reset a circuit breaker for a service."""
        await self.error_recovery_manager.reset_circuit_breaker(service_id)

    async def cleanup_old_errors(self):
        """Clean up old error records."""
        await self.error_recovery_manager.cleanup_old_errors()

    async def close(self):
        """Clean up resources and close all components."""
        await self.stop()

    def _start_background_tasks(self):
        """Start background tasks for parallel processing."""
        self.workflow_processor = asyncio.create_task(self._process_workflow_queue())
        self.resource_monitor = asyncio.create_task(self._monitor_resources())

    async def _process_workflow_queue(self):
        """Process workflows from the queue based on priority."""
        while True:
            try:
                # Process workflows in priority order
                for priority in sorted(WorkflowPriority, reverse=True):
                    if self.workflow_queue[priority]:
                        task = self.workflow_queue[priority][0]
                        if await self._can_process_task(task):
                            async with self.processing_semaphore:
                                await self._execute_workflow_task(task)
                                self.workflow_queue[priority].pop(0)
                
                await asyncio.sleep(0.1)  # Prevent CPU spinning
            except Exception as e:
                self.logger.error(f"Error in workflow queue processor: {str(e)}")
                await asyncio.sleep(1)  # Back off on error

    async def _monitor_resources(self):
        """Monitor and manage resource usage."""
        while True:
            try:
                for agent, limit in self.resource_limits.items():
                    if self.current_resources[agent] > limit:
                        self.logger.warning(f"Resource limit exceeded for agent {agent}")
                        # Implement resource management strategy
                await asyncio.sleep(5)  # Check every 5 seconds
            except Exception as e:
                self.logger.error(f"Error in resource monitor: {str(e)}")
                await asyncio.sleep(5)

    async def _can_process_task(self, task: WorkflowTask) -> bool:
        """Check if a task can be processed based on dependencies and resources."""
        if task.dependencies:
            for dep_id in task.dependencies:
                dep_task = self.workflow_tasks.get(dep_id)
                if not dep_task or dep_task.status != 'completed':
                    return False
        
        # Check resource availability
        for agent, limit in self.resource_limits.items():
            if self.current_resources[agent] >= limit:
                return False
        
        return True

    async def _execute_workflow_task(self, task: WorkflowTask):
        """Execute a workflow task."""
        try:
            # Update task status
            task.status = 'processing'
            task.assigned_agent = 'generator'  # Initial agent
            
            # Emit workflow started event
            await self._emit_workflow_event(
                EventType.WORKFLOW_STARTED,
                task.workflow_id,
                'processing'
            )
            
            # Update resource usage
            self.current_resources[task.assigned_agent] += 1
            await self._emit_resource_event(
                EventType.RESOURCE_ALLOCATED,
                'agent',
                task.assigned_agent,
                'allocate',
                self.current_resources[task.assigned_agent],
                self.resource_limits[task.assigned_agent]
            )
            
            # Process workflow
            result = await self.process_workflow(task.workflow_data)
            
            # Update task status
            task.status = 'completed' if result.success else 'failed'
            
            # Emit workflow completed/error event
            if result.success:
                await self._emit_workflow_event(
                    EventType.WORKFLOW_COMPLETED,
                    task.workflow_id,
                    'completed',
                    progress=100.0
                )
            else:
                await self._emit_workflow_event(
                    EventType.WORKFLOW_ERROR,
                    task.workflow_id,
                    'failed',
                    error_message=result.error
                )
            
            # Update resource usage
            self.current_resources[task.assigned_agent] -= 1
            await self._emit_resource_event(
                EventType.RESOURCE_RELEASED,
                'agent',
                task.assigned_agent,
                'release',
                self.current_resources[task.assigned_agent],
                self.resource_limits[task.assigned_agent]
            )
            
            # Handle retries if needed
            if not result.success and task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = 'pending'
                self.workflow_queue[task.priority].append(task)
                
                # Emit retry event
                await self._emit_workflow_event(
                    EventType.WORKFLOW_PROGRESS,
                    task.workflow_id,
                    'retrying',
                    progress=0.0,
                    error_message=f"Retry attempt {task.retry_count} of {task.max_retries}"
                )
            
        except Exception as e:
            self.logger.error(f"Error executing workflow task {task.workflow_id}: {str(e)}")
            task.status = 'failed'
            self.current_resources[task.assigned_agent] -= 1
            
            # Emit error event
            await self._emit_workflow_event(
                EventType.WORKFLOW_ERROR,
                task.workflow_id,
                'failed',
                error_message=str(e)
            )

    async def process_workflow_parallel(self, workflow_data: Dict[str, Any], 
                                      priority: WorkflowPriority = WorkflowPriority.NORMAL,
                                      dependencies: Optional[Set[str]] = None) -> str:
        """Process a workflow in parallel with priority and dependencies."""
        workflow_id = workflow_data.get('workflow_id', f"wf_{datetime.now().timestamp()}")
        
        # Create workflow task
        task = WorkflowTask(
            workflow_id=workflow_id,
            priority=priority,
            workflow_data=workflow_data,
            created_at=datetime.now(),
            dependencies=dependencies
        )
        
        # Add to workflow tracking
        self.workflow_tasks[workflow_id] = task
        
        # Add to priority queue
        self.workflow_queue[priority].append(task)

    async def _emit_workflow_event(self, event_type: EventType, workflow_id: str, 
                                 status: str, progress: Optional[float] = None,
                                 error_message: Optional[str] = None):
        """Emit a workflow-related event."""
        event = WorkflowEvent(
            event_type=event_type,
            timestamp=datetime.now(),
            source="integration_manager",
            workflow_id=workflow_id,
            workflow_status=status,
            progress=progress,
            error_message=error_message
        )
        await self.event_stream_manager.publish_event(event)

    async def _emit_agent_event(self, event_type: EventType, agent_id: str,
                              status: str, operation: str,
                              result: Optional[Any] = None,
                              error_message: Optional[str] = None):
        """Emit an agent-related event."""
        event = AgentEvent(
            event_type=event_type,
            timestamp=datetime.now(),
            source="integration_manager",
            agent_id=agent_id,
            agent_status=status,
            operation=operation,
            result=result,
            error_message=error_message
        )
        await self.event_stream_manager.publish_event(event)

    async def _emit_resource_event(self, event_type: EventType, resource_type: str,
                                 resource_id: str, action: str,
                                 current_usage: float, limit: float,
                                 details: Optional[Dict[str, Any]] = None):
        """Emit a resource-related event."""
        event = ResourceEvent(
            event_type=event_type,
            timestamp=datetime.now(),
            source="integration_manager",
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            current_usage=current_usage,
            limit=limit,
            details=details
        )
        await self.event_stream_manager.publish_event(event)

    async def _emit_system_event(self, event_type: EventType, component: str,
                               status: str, details: Optional[Dict[str, Any]] = None):
        """Emit a system-related event."""
        event = SystemEvent(
            type=event_type,
            component=component,
            status=status,
            details=details,
            priority=EventPriority.NORMAL,
            timestamp=datetime.now()
        )
        await self.event_stream_manager.publish_event(event)

    async def create_ui_session(self, client_info: Dict[str, Any], token: Optional[str] = None) -> str:
        """Create a new UI session."""
        try:
            # Validate authentication if token provided
            user = None
            if token:
                user = await self.security_manager.validate_token(token)
                if not await self.security_manager.check_permission(user, PermissionLevel.READ):
                    raise AuthorizationError("Insufficient permissions to create UI session")
            
            # Check rate limit
            client_id = user.user_id if user else client_info.get('ip_address', 'unknown')
            await self.security_manager.check_rate_limit(client_id)
            
            return await self.ui_controller.create_session(
                f"session_{datetime.now().timestamp()}",
                client_info
            )
            
        except SecurityError as e:
            raise
        except Exception as e:
            self.logger.error(f"Error creating UI session: {str(e)}")
            raise

    async def remove_ui_session(self, session_id: str, token: Optional[str] = None):
        """Remove a UI session."""
        try:
            # Validate authentication if token provided
            if token:
                user = await self.security_manager.validate_token(token)
                if not await self.security_manager.check_permission(user, PermissionLevel.WRITE):
                    raise AuthorizationError("Insufficient permissions to remove UI session")
            
            await self.ui_controller.remove_session(session_id)
            
        except SecurityError as e:
            raise
        except Exception as e:
            self.logger.error(f"Error removing UI session: {str(e)}")
            raise

    async def subscribe_to_workflow(self, session_id: str, workflow_id: str, token: Optional[str] = None):
        """Subscribe a UI session to workflow events."""
        try:
            # Validate authentication if token provided
            if token:
                user = await self.security_manager.validate_token(token)
                if not await self.security_manager.check_permission(user, PermissionLevel.READ):
                    raise AuthorizationError("Insufficient permissions to subscribe to workflow")
            
            # Check rate limit
            client_id = user.user_id if token else session_id
            await self.security_manager.check_rate_limit(client_id)
            
            await self.ui_controller.subscribe_to_workflow(session_id, workflow_id)
            
        except SecurityError as e:
            raise
        except Exception as e:
            self.logger.error(f"Error subscribing to workflow: {str(e)}")
            raise

    async def get_workflow_visualization(self, workflow_id: str, token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get the current visualization data for a workflow."""
        try:
            # Validate authentication if token provided
            if token:
                user = await self.security_manager.validate_token(token)
                if not await self.security_manager.check_permission(user, PermissionLevel.READ):
                    raise AuthorizationError("Insufficient permissions to view workflow visualization")
            
            # Check rate limit
            client_id = user.user_id if token else 'anonymous'
            await self.security_manager.check_rate_limit(client_id)
            
            return await self.ui_controller.get_workflow_visualization(workflow_id)
            
        except SecurityError as e:
            raise
        except Exception as e:
            self.logger.error(f"Error getting workflow visualization: {str(e)}")
            raise

    async def update_workflow_visualization(self, workflow_id: str,
                                         nodes: List[Dict[str, Any]],
                                         edges: List[Dict[str, Any]],
                                         token: Optional[str] = None):
        """Update the visualization data for a workflow."""
        try:
            # Validate authentication if token provided
            if token:
                user = await self.security_manager.validate_token(token)
                if not await self.security_manager.check_permission(user, PermissionLevel.WRITE):
                    raise AuthorizationError("Insufficient permissions to update workflow visualization")
            
            # Check rate limit
            client_id = user.user_id if token else 'anonymous'
            await self.security_manager.check_rate_limit(client_id)
            
            await self.ui_controller.update_workflow_visualization(workflow_id, nodes, edges)
            
        except SecurityError as e:
            raise
        except Exception as e:
            self.logger.error(f"Error updating workflow visualization: {str(e)}")
            raise

    async def get_health_status(self) -> Dict[str, Any]:
        """Get the health status of the integration manager and its components."""
        try:
            # Get system health
            system_health = await self.monitoring_manager.get_health_status()
            
            # Get agent health
            agent_health = {}
            for agent_name, agent in self.agents.items():
                try:
                    status = await agent.get_status()
                    agent_health[agent_name] = {
                        'status': status.get('status', 'unknown'),
                        'last_activity': status.get('last_activity'),
                        'error_count': status.get('error_count', 0),
                        'success_count': status.get('success_count', 0)
                    }
                except Exception as e:
                    agent_health[agent_name] = {
                        'status': 'error',
                        'error': str(e)
                    }
            
            # Get workflow health
            workflow_health = {
                'active_workflows': len(self.active_workflows),
                'queued_workflows': sum(len(queue) for queue in self.workflow_queue.values()),
                'failed_workflows': sum(1 for task in self.workflow_tasks.values() if task.status == 'failed')
            }
            
            return {
                'system': system_health,
                'agents': agent_health,
                'workflows': workflow_health,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting health status: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def get_metrics(self, metric_name: Optional[str] = None,
                         start_time: Optional[datetime] = None,
                         end_time: Optional[datetime] = None) -> Dict[str, Any]:
        """Get metrics for the integration manager."""
        try:
            if metric_name:
                metrics = await self.monitoring_manager.get_metric_history(
                    metric_name,
                    start_time,
                    end_time
                )
                return {
                    metric_name: [
                        {
                            'value': m.value,
                            'timestamp': m.timestamp.isoformat(),
                            'labels': m.labels
                        }
                        for m in metrics
                    ]
                }
            
            # Get all metrics
            all_metrics = {}
            for name in self.monitoring_manager.metrics:
                metrics = await self.monitoring_manager.get_metric_history(
                    name,
                    start_time,
                    end_time
                )
                all_metrics[name] = [
                    {
                        'value': m.value,
                        'timestamp': m.timestamp.isoformat(),
                        'labels': m.labels
                    }
                    for m in metrics
                ]
            
            return all_metrics
            
        except Exception as e:
            self.logger.error(f"Error getting metrics: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            } 
