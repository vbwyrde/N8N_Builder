import asyncio
import json
import logging
from typing import Dict, Any, Optional, List, Set
from datetime import datetime
from .event_types import Event, EventType, WorkflowEvent, AgentEvent, ResourceEvent, SystemEvent
from .event_stream_manager import EventStreamManager

class AgentUIController:
    """Manages UI interactions and real-time updates."""
    
    def __init__(self, event_stream_manager: EventStreamManager):
        self.logger = logging.getLogger(__name__)
        self.event_stream_manager = event_stream_manager
        self.ui_sessions: Dict[str, Dict[str, Any]] = {}
        self.workflow_visualizations: Dict[str, Dict[str, Any]] = {}
        self._running = False
        self._event_processor = None
    
    async def start(self):
        """Start the UI controller."""
        if self._running:
            return
        
        self._running = True
        self._event_processor = asyncio.create_task(self._process_ui_events())
        self.logger.info("AgentUIController started")
    
    async def stop(self):
        """Stop the UI controller."""
        if not self._running:
            return
        
        self._running = False
        if self._event_processor:
            self._event_processor.cancel()
            try:
                await self._event_processor
            except asyncio.CancelledError:
                pass
        
        # Clear all sessions and visualizations
        self.ui_sessions.clear()
        self.workflow_visualizations.clear()
        
        self.logger.info("AgentUIController stopped")
    
    async def create_session(self, session_id: str, client_info: Dict[str, Any]) -> str:
        """Create a new UI session."""
        if session_id in self.ui_sessions:
            return session_id
        
        # Create event stream for the session
        stream = await self.event_stream_manager.create_stream(session_id)
        
        # Initialize session data
        self.ui_sessions[session_id] = {
            'client_info': client_info,
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'subscribed_events': set(),
            'active_workflows': set(),
            'stream': stream
        }
        
        # Subscribe to basic events
        await self.event_stream_manager.subscribe(
            session_id,
            {
                EventType.SYSTEM_STARTED,
                EventType.SYSTEM_STOPPED,
                EventType.SYSTEM_ERROR
            }
        )
        
        self.logger.info(f"Created UI session: {session_id}")
        return session_id
    
    async def remove_session(self, session_id: str):
        """Remove a UI session."""
        if session_id in self.ui_sessions:
            # Remove event stream
            await self.event_stream_manager.remove_stream(session_id)
            
            # Remove session data
            del self.ui_sessions[session_id]
            
            self.logger.info(f"Removed UI session: {session_id}")
    
    async def subscribe_to_workflow(self, session_id: str, workflow_id: str):
        """Subscribe a session to workflow events."""
        if session_id not in self.ui_sessions:
            raise ValueError(f"Session {session_id} does not exist")
        
        # Add workflow to active workflows
        self.ui_sessions[session_id]['active_workflows'].add(workflow_id)
        
        # Subscribe to workflow events
        await self.event_stream_manager.subscribe(
            session_id,
            {
                EventType.WORKFLOW_STARTED,
                EventType.WORKFLOW_COMPLETED,
                EventType.WORKFLOW_ERROR,
                EventType.WORKFLOW_PROGRESS
            }
        )
        
        # Create or update workflow visualization
        if workflow_id not in self.workflow_visualizations:
            self.workflow_visualizations[workflow_id] = {
                'nodes': [],
                'edges': [],
                'status': 'pending',
                'last_update': datetime.now()
            }
        
        self.logger.info(f"Session {session_id} subscribed to workflow {workflow_id}")
    
    async def unsubscribe_from_workflow(self, session_id: str, workflow_id: str):
        """Unsubscribe a session from workflow events."""
        if session_id not in self.ui_sessions:
            return
        
        # Remove workflow from active workflows
        self.ui_sessions[session_id]['active_workflows'].discard(workflow_id)
        
        # Unsubscribe from workflow events if no active workflows
        if not self.ui_sessions[session_id]['active_workflows']:
            await self.event_stream_manager.unsubscribe(
                session_id,
                {
                    EventType.WORKFLOW_STARTED,
                    EventType.WORKFLOW_COMPLETED,
                    EventType.WORKFLOW_ERROR,
                    EventType.WORKFLOW_PROGRESS
                }
            )
        
        self.logger.info(f"Session {session_id} unsubscribed from workflow {workflow_id}")
    
    async def update_workflow_visualization(self, workflow_id: str, 
                                         nodes: List[Dict[str, Any]],
                                         edges: List[Dict[str, Any]]):
        """Update the visualization data for a workflow."""
        if workflow_id not in self.workflow_visualizations:
            self.workflow_visualizations[workflow_id] = {
                'nodes': [],
                'edges': [],
                'status': 'pending',
                'last_update': datetime.now()
            }
        
        self.workflow_visualizations[workflow_id].update({
            'nodes': nodes,
            'edges': edges,
            'last_update': datetime.now()
        })
        
        # Emit visualization update event
        await self._emit_visualization_update(workflow_id)
    
    async def get_workflow_visualization(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get the current visualization data for a workflow."""
        return self.workflow_visualizations.get(workflow_id)
    
    async def _process_ui_events(self):
        """Process and handle UI-related events."""
        while self._running:
            try:
                # Process any pending events
                for session_id, session_data in self.ui_sessions.items():
                    stream = session_data['stream']
                    if not stream.empty():
                        event = await stream.get()
                        # Handle event based on type
                        await self._handle_ui_event(session_id, event)
                        stream.task_done()
                
                await asyncio.sleep(0.1)  # Prevent CPU spinning
            except Exception as e:
                self.logger.error(f"Error processing UI events: {str(e)}")
                await asyncio.sleep(1)  # Back off on error
    
    async def _handle_ui_event(self, session_id: str, event: Event):
        """Handle UI-related events."""
        try:
            # Update session activity
            self.ui_sessions[session_id]['last_activity'] = datetime.now()
            
            # Handle different event types
            if isinstance(event, WorkflowEvent):
                await self._handle_workflow_event(session_id, event)
            elif isinstance(event, AgentEvent):
                await self._handle_agent_event(session_id, event)
            elif isinstance(event, ResourceEvent):
                await self._handle_resource_event(session_id, event)
            elif isinstance(event, SystemEvent):
                await self._handle_system_event(session_id, event)
            
        except Exception as e:
            self.logger.error(f"Error handling UI event: {str(e)}")
    
    async def _handle_workflow_event(self, session_id: str, event: WorkflowEvent):
        """Handle workflow-related events."""
        workflow_id = event.workflow_id
        
        # Update workflow visualization status
        if workflow_id in self.workflow_visualizations:
            self.workflow_visualizations[workflow_id]['status'] = event.workflow_status
            
            # Emit visualization update
            await self._emit_visualization_update(workflow_id)
    
    async def _handle_agent_event(self, session_id: str, event: AgentEvent):
        """Handle agent-related events."""
        # Update agent status in relevant workflow visualizations
        for workflow_id, viz in self.workflow_visualizations.items():
            if event.agent_id in [node.get('agent_id') for node in viz['nodes']]:
                # Update node status
                for node in viz['nodes']:
                    if node.get('agent_id') == event.agent_id:
                        node['status'] = event.agent_status
                        node['last_update'] = datetime.now().isoformat()
                
                # Emit visualization update
                await self._emit_visualization_update(workflow_id)
    
    async def _handle_resource_event(self, session_id: str, event: ResourceEvent):
        """Handle resource-related events."""
        # Update resource usage in relevant workflow visualizations
        for workflow_id, viz in self.workflow_visualizations.items():
            if event.resource_id in [node.get('resource_id') for node in viz['nodes']]:
                # Update node resource usage
                for node in viz['nodes']:
                    if node.get('resource_id') == event.resource_id:
                        node['resource_usage'] = event.current_usage
                        node['resource_limit'] = event.limit
                        node['last_update'] = datetime.now().isoformat()
                
                # Emit visualization update
                await self._emit_visualization_update(workflow_id)
    
    async def _handle_system_event(self, session_id: str, event: SystemEvent):
        """Handle system-related events."""
        # Update system status in relevant workflow visualizations
        if event.component == 'system':
            for workflow_id, viz in self.workflow_visualizations.items():
                viz['system_status'] = event.status
                viz['last_update'] = datetime.now().isoformat()
                
                # Emit visualization update
                await self._emit_visualization_update(workflow_id)
    
    async def _emit_visualization_update(self, workflow_id: str):
        """Emit a visualization update event."""
        viz_data = self.workflow_visualizations.get(workflow_id)
        if not viz_data:
            return
        
        # Create visualization update event
        event = SystemEvent(
            event_type=EventType.SYSTEM_STARTED,  # Using system event for visualization updates
            timestamp=datetime.now(),
            source="ui_controller",
            component="visualization",
            status="updated",
            details={
                'workflow_id': workflow_id,
                'visualization': viz_data
            }
        )
        
        # Publish event
        await self.event_stream_manager.publish_event(event) 