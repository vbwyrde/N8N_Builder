"""
AG-UI Server Implementation for N8N Workflow Builder.

This module provides a proper AG-UI server that handles RunAgentInput requests
and streams back AG-UI events for workflow generation, validation, and other operations.
"""

import asyncio
import logging
from typing import AsyncGenerator, Dict, Any, Optional, List
from datetime import datetime
import uuid
import json

# FastAPI imports
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# AG-UI imports
from ag_ui.core import (
    RunAgentInput,
    Event as AGUIEvent,
    EventType as AGUIEventType,
    RunStartedEvent,
    RunFinishedEvent,
    RunErrorEvent
)

# N8N Builder imports
from .agents.base_agent import (
    AgentConfig,
    WorkflowGeneratorAgent,
    ValidationAgent,
    OrchestratorAgent
)
from .agents.integration import (
    StateManager,
    MessageBroker,
    WorkflowEvent,
    WorkflowEventType
)


class AGUIServer:
    """
    AG-UI compatible server for N8N Workflow Builder.
    
    This server implements the AG-UI protocol for workflow generation,
    providing proper event streaming and state management.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the AG-UI server."""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize FastAPI app
        self.app = FastAPI(
            title="N8N Workflow Builder AG-UI Server",
            description="AG-UI compatible server for N8N workflow generation",
            version="1.0.0"
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.get("allowed_origins", ["*"]),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Initialize components
        self.state_manager: Optional[StateManager] = None
        self.message_broker: Optional[MessageBroker] = None
        self.agents: Dict[str, Any] = {}
        
        # Setup routes
        self._setup_routes()
        
        # Server state
        self._running = False
        self._active_runs: Dict[str, Dict[str, Any]] = {}
    
    def _setup_routes(self):
        """Setup FastAPI routes for AG-UI endpoints."""
        
        @self.app.post("/run-agent")
        async def run_agent(request: RunAgentInput) -> StreamingResponse:
            """
            Main AG-UI endpoint for running agents.
            
            This endpoint accepts RunAgentInput and streams back AG-UI events.
            """
            return StreamingResponse(
                self._stream_agent_run(request),
                media_type="text/plain",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no"  # Disable nginx buffering
                }
            )
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {
                "status": "healthy" if self._running else "stopped",
                "timestamp": datetime.now().isoformat(),
                "active_runs": len(self._active_runs),
                "agents": list(self.agents.keys())
            }
        
        @self.app.get("/status")
        async def server_status():
            """Get detailed server status."""
            agent_status = {}
            for name, agent in self.agents.items():
                if hasattr(agent, 'get_status'):
                    agent_status[name] = agent.get_status()
            
            return {
                "server": {
                    "running": self._running,
                    "active_runs": len(self._active_runs),
                    "uptime": "N/A"  # TODO: Add uptime tracking
                },
                "agents": agent_status,
                "config": {
                    "allowed_origins": self.config.get("allowed_origins", ["*"]),
                    "ag_ui_version": "1.0.0"
                }
            }
        
        @self.app.post("/workflow/generate")
        async def generate_workflow_legacy(request: Request):
            """Legacy endpoint that redirects to AG-UI."""
            body = await request.json()
            description = body.get("description", "Generate a workflow")
            
            # Convert to RunAgentInput
            run_input = RunAgentInput(
                thread_id=str(uuid.uuid4()),
                run_id=str(uuid.uuid4()),
                forwarded_props={},
                messages=[],
                context=[{"description": "Legacy workflow request", "value": description}],
                tools=[],
                state=None
            )
            
            return StreamingResponse(
                self._stream_agent_run(run_input),
                media_type="text/plain"
            )
    
    async def _stream_agent_run(self, input_data: RunAgentInput) -> AsyncGenerator[str, None]:
        """
        Stream AG-UI events from agent execution.
        
        This is the core method that handles AG-UI protocol streaming.
        """
        run_id = getattr(input_data, 'run_id', None) or getattr(input_data, 'runId', None) or str(uuid.uuid4())
        thread_id = getattr(input_data, 'thread_id', None) or getattr(input_data, 'threadId', None) or str(uuid.uuid4())
        
        try:
            # Track the run
            self._active_runs[run_id] = {
                "thread_id": thread_id,
                "start_time": datetime.now(),
                "status": "running"
            }
            
            # Determine which agent to use based on context
            agent = await self._select_agent(input_data)
            
            # Stream events from the agent
            async for event in agent.run_agent(input_data):
                # Convert event to AG-UI format and stream
                event_data = self._format_event_for_streaming(event)
                yield f"data: {event_data}\n\n"
            
            # Update run status
            self._active_runs[run_id]["status"] = "completed"
            self._active_runs[run_id]["end_time"] = datetime.now()
            
        except Exception as e:
            self.logger.error(f"Error in agent run {run_id}: {e}")
            
            # Send error event
            error_event = RunErrorEvent(
                type=AGUIEventType.RUN_ERROR,
                message=str(e),
                code=type(e).__name__,
                timestamp=int(datetime.now().timestamp())
            )
            
            error_data = self._format_event_for_streaming(error_event)
            yield f"data: {error_data}\n\n"
            
            # Update run status
            if run_id in self._active_runs:
                self._active_runs[run_id]["status"] = "failed"
                self._active_runs[run_id]["error"] = str(e)
        
        finally:
            # Clean up completed runs after some time
            asyncio.create_task(self._cleanup_run(run_id, delay=300))  # 5 minutes
    
    async def _select_agent(self, input_data: RunAgentInput) -> Any:
        """
        Select the appropriate agent based on the input data.
        
        This implements intelligent agent selection based on the request context.
        """
        # Check context for hints about what type of operation is needed
        context_text = ""
        if input_data.context:
            for ctx in input_data.context:
                if hasattr(ctx, 'content'):
                    context_text += str(ctx.content) + " "
        
        # Check messages for operation type
        message_text = ""
        if input_data.messages:
            for msg in input_data.messages:
                if hasattr(msg, 'content'):
                    message_text += str(msg.content) + " "
        
        combined_text = (context_text + message_text).lower()
        
        # Agent selection logic
        if any(word in combined_text for word in ["validate", "validation", "check", "verify"]):
            return self.agents.get("validator", self.agents["generator"])
        elif any(word in combined_text for word in ["generate", "create", "build", "workflow"]):
            return self.agents["generator"]
        elif any(word in combined_text for word in ["orchestrate", "manage", "coordinate"]):
            return self.agents.get("orchestrator", self.agents["generator"])
        else:
            # Default to workflow generator
            return self.agents["generator"]
    
    def _format_event_for_streaming(self, event: AGUIEvent) -> str:
        """
        Format an AG-UI event for Server-Sent Events streaming.
        
        This converts AG-UI events to the proper streaming format.
        """
        try:
            # Convert event to dictionary
            if hasattr(event, 'model_dump'):
                event_dict = event.model_dump()
            elif hasattr(event, 'dict'):
                event_dict = event.dict()
            else:
                # Fallback for basic events
                event_dict = {
                    "type": str(event.type),
                    "timestamp": getattr(event, 'timestamp', int(datetime.now().timestamp()))
                }
                
                # Add event-specific fields
                for attr in ['message', 'delta', 'snapshot', 'step_name', 'message_id', 'role']:
                    if hasattr(event, attr):
                        event_dict[attr] = getattr(event, attr)
            
            return json.dumps(event_dict)
            
        except Exception as e:
            self.logger.error(f"Error formatting event for streaming: {e}")
            # Return a basic error event
            return json.dumps({
                "type": "ERROR",
                "message": f"Event formatting error: {e}",
                "timestamp": int(datetime.now().timestamp())
            })
    
    async def _cleanup_run(self, run_id: str, delay: int = 300):
        """Clean up completed run data after a delay."""
        await asyncio.sleep(delay)
        if run_id in self._active_runs:
            run_data = self._active_runs[run_id]
            if run_data.get("status") in ["completed", "failed"]:
                del self._active_runs[run_id]
                self.logger.debug(f"Cleaned up run {run_id}")
    
    async def start(self):
        """Start the AG-UI server and initialize all components."""
        self.logger.info("Starting AG-UI Server...")
        
        # Initialize state manager
        self.state_manager = StateManager()
        
        # Initialize message broker
        self.message_broker = MessageBroker()
        await self.message_broker.start()
        
        # Initialize agents
        await self._initialize_agents()
        
        self._running = True
        self.logger.info("AG-UI Server started successfully")
    
    async def _initialize_agents(self):
        """Initialize all AG-UI compatible agents."""
        # Create agent configurations
        base_config = AgentConfig(
            name="agui_agent",
            capabilities={
                "workflow_generation": True,
                "workflow_validation": True,
                "ag_ui_protocol": True
            }
        )
        
        # Initialize workflow generator agent
        generator_config = AgentConfig(
            name="workflow_generator",
            capabilities=base_config.capabilities
        )
        self.agents["generator"] = WorkflowGeneratorAgent(generator_config)
        await self.agents["generator"].start()
        
        # Initialize validation agent
        validator_config = AgentConfig(
            name="workflow_validator", 
            capabilities=base_config.capabilities
        )
        self.agents["validator"] = ValidationAgent(validator_config)
        await self.agents["validator"].start()
        
        # Initialize orchestrator agent
        orchestrator_config = AgentConfig(
            name="workflow_orchestrator",
            capabilities=base_config.capabilities
        )
        self.agents["orchestrator"] = OrchestratorAgent(orchestrator_config)
        await self.agents["orchestrator"].start()
        
        self.logger.info(f"Initialized {len(self.agents)} AG-UI compatible agents")
    
    async def stop(self):
        """Stop the AG-UI server and clean up resources."""
        self.logger.info("Stopping AG-UI Server...")
        
        self._running = False
        
        # Stop all agents
        for agent in self.agents.values():
            await agent.stop()
        
        # Stop message broker
        if self.message_broker:
            await self.message_broker.stop()
        
        # Clear active runs
        self._active_runs.clear()
        
        self.logger.info("AG-UI Server stopped")
    
    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance."""
        return self.app


# Global server instance
_agui_server: Optional[AGUIServer] = None


def get_agui_server(config: Optional[Dict[str, Any]] = None) -> AGUIServer:
    """Get or create the global AG-UI server instance."""
    global _agui_server
    if _agui_server is None:
        _agui_server = AGUIServer(config)
    return _agui_server


async def start_agui_server(config: Optional[Dict[str, Any]] = None) -> AGUIServer:
    """Start the AG-UI server."""
    server = get_agui_server(config)
    await server.start()
    return server


__all__ = [
    'AGUIServer',
    'get_agui_server', 
    'start_agui_server'
]
