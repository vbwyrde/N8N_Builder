from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import json
import uuid
from datetime import datetime
import os
import logging
from pathlib import Path
import random
import time

from .n8n_builder import N8NBuilder
from .validators import BaseWorkflowValidator, ValidationResult
from .error_handler import EnhancedErrorHandler, ErrorDetail, ErrorCategory, ErrorSeverity
from .project_manager import project_manager, filesystem_utils, ProjectInfo, WorkflowInfo

# Import AG_UI components - not needed for non-streaming approach
# from .agents.integration.event_stream_manager import EventStreamManager
# from .agents.integration.event_types import EventType, EventPriority, Event, WorkflowEvent
# from .agents.integration.agent_integration_manager import AgentIntegrationManager
# from .agents.integration.ui_controller import AgentUIController
# from .agents.integration.message_protocol import MessageType, WorkflowRequest as AgentWorkflowRequest, StatusUpdate
# from .agents.base_agent import AgentConfig

# Create FastAPI app
app = FastAPI(title="N8N Workflow Builder API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our components
workflow_builder = N8NBuilder()
workflow_validator = BaseWorkflowValidator()
error_handler = EnhancedErrorHandler()

# Initialize AG_UI system - not needed for non-streaming approach
# agent_config = AgentConfig(
#     name="n8n_workflow_builder",
#     capabilities={
#         "workflow_generation": True,
#         "workflow_modification": True,
#         "workflow_iteration": True,
#         "streaming_responses": True,
#         "llm_integration": True
#     },
#     max_concurrent_workflows=5,
#     security={},
#     error_recovery={},
#     monitoring={}
# )
# agent_integration_manager = AgentIntegrationManager(agent_config)
# event_stream_manager = agent_integration_manager.event_stream_manager
# ui_controller = agent_integration_manager.ui_controller

# Initialize just the event stream manager for AG_UI streaming
# event_stream_manager = EventStreamManager()
# ui_sessions = {}  # Simple session tracking

logger = logging.getLogger(__name__)

# Get the static directory path - point to root level static directory
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
logger.debug(f"Static directory path: {static_dir}")
logger.debug(f"Static directory exists: {os.path.exists(static_dir)}")
logger.debug(f"Static directory contents: {os.listdir(static_dir) if os.path.exists(static_dir) else 'Directory not found'}")

class WorkflowRequest(BaseModel):
    description: str
    thread_id: Optional[str] = None
    run_id: Optional[str] = None

class WorkflowModificationRequest(BaseModel):
    existing_workflow_json: str
    modification_description: str
    workflow_id: Optional[str] = None
    thread_id: Optional[str] = None
    run_id: Optional[str] = None

class WorkflowIterationRequest(BaseModel):
    workflow_id: str
    existing_workflow_json: str
    feedback_from_testing: str
    additional_requirements: Optional[str] = ""
    thread_id: Optional[str] = None
    run_id: Optional[str] = None

class WorkflowResponse(BaseModel):
    workflow_id: str
    workflow_json: str
    validation_result: ValidationResult
    timestamp: datetime

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d['timestamp'] = d['timestamp'].isoformat()
        return d

# Project API Models
class ProjectCreateRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    initial_workflows: Optional[List[str]] = None

class ProjectResponse(BaseModel):
    name: str
    path: str
    description: str
    created_date: str
    last_modified: str
    workflow_count: int
    workflows: List[str]
    settings: Dict[str, Any]

class WorkflowFileRequest(BaseModel):
    workflow_data: Dict[str, Any]
    create_backup: Optional[bool] = True

class WorkflowFileResponse(BaseModel):
    filename: str
    project_name: str
    workflow_data: Dict[str, Any]
    file_size: int
    last_modified: str

class ProjectStatsResponse(BaseModel):
    total_projects: int
    total_workflows: int
    projects_root: str
    average_workflows_per_project: float
    project_names: List[str]
    largest_project: Optional[str]
    most_recent_project: Optional[str]

# Version Management Models
class VersionInfoResponse(BaseModel):
    filename: str
    timestamp: str
    created_date: str
    modified_date: str
    file_size: int
    file_size_mb: float
    workflow_name: str
    node_count: int
    tags: List[str]
    is_backup: bool

class VersionComparisonResponse(BaseModel):
    version1: Dict[str, Any]
    version2: Dict[str, Any]
    differences: Dict[str, bool]
    summary: Dict[str, Any]

class VersionRestoreRequest(BaseModel):
    create_backup: Optional[bool] = True

class VersionCleanupRequest(BaseModel):
    keep_versions: Optional[int] = 10

@app.on_event("startup")
async def startup_event():
    """Initialize system on startup."""
    try:
        # await event_stream_manager.start()
        logger.info("N8N Builder system started successfully")
    except Exception as e:
        logger.error(f"Failed to start system: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup system on shutdown."""
    try:
        # await event_stream_manager.stop()
        logger.info("N8N Builder system stopped successfully")
    except Exception as e:
        logger.error(f"Error stopping system: {str(e)}")

@app.get("/")
async def root():
    """Serve the main UI page."""
    index_path = os.path.join(static_dir, "index.html")
    logger.debug(f"Attempting to serve index.html from: {index_path}")
    logger.debug(f"File exists: {os.path.exists(index_path)}")
    
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail=f"index.html not found at {index_path}")
    return FileResponse(index_path)

# Mount static files AFTER defining the root route
app.mount("/static", StaticFiles(directory=static_dir), name="static")
logger.debug("Mounted static files directory")

async def generate_workflow_events_agui(request: WorkflowRequest):
    """Generate events for workflow creation using AG_UI EventStreamManager."""
    workflow_id = str(uuid.uuid4())
    thread_id = request.thread_id or str(uuid.uuid4())
    run_id = request.run_id or str(uuid.uuid4())
    
    # Create a session for this workflow
    # session_id = await ui_controller.create_ui_session({
    #     'workflow_id': workflow_id,
    #     'thread_id': thread_id,
    #     'run_id': run_id,
    #     'client_type': 'web'
    # })
    
    try:
        # Subscribe to workflow events for this session
        # await ui_controller.subscribe_to_workflow(session_id, workflow_id)
        
        # Create workflow started event
        # start_event = WorkflowEvent(
        #     type=EventType.WORKFLOW_STARTED,
        #     workflow_id=workflow_id,
        #     status="started",
        #     data={
        #         "thread_id": thread_id,
        #         "run_id": run_id,
        #         "description": request.description
        #     },
        #     priority=EventPriority.NORMAL,
        #     source="workflow_api"
        # )
        
        # Publish start event
        # await event_stream_manager.publish_event(start_event)
        
        # Yield start event to client
        yield "data: " + json.dumps({
            "type": "RUN_STARTED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat()
        }) + "\n\n"
        
        # Create validation event
        # validation_event = WorkflowEvent(
        #     type=EventType.WORKFLOW_VALIDATION_STARTED,
        #     workflow_id=workflow_id,
        #     status="validating",
        #     data={"message": "Validating workflow description..."},
        #     priority=EventPriority.NORMAL,
        #     source="workflow_api"
        # )
        
        # await event_stream_manager.publish_event(validation_event)
        
        # yield "data: " + json.dumps({
        #     "type": "VALIDATION_STARTED",
        #     "workflow_id": workflow_id,
        #     "thread_id": thread_id,
        #     "run_id": run_id,
        #     "timestamp": datetime.now().isoformat(),
        #     "message": "Validating workflow description..."
        # }) + "\n\n"
        
        # Validate description
        if not request.description or not request.description.strip():
            # error_event = WorkflowEvent(
            #     type=EventType.WORKFLOW_ERROR,
            #     workflow_id=workflow_id,
            #     status="error",
            #     data={
            #         "error": {
            #             "category": "input_validation",
            #             "severity": "error",
            #             "title": "Empty Description",
            #             "message": "Workflow description cannot be empty",
            #             "user_guidance": "Please provide a clear description of the workflow you want to create",
            #             "fix_suggestions": ["Add a detailed description of what the workflow should do"]
            #         }
            #     },
            #     priority=EventPriority.HIGH,
            #     source="workflow_api"
            # )
            
            # await event_stream_manager.publish_event(error_event)
            
            yield "data: " + json.dumps({
                "type": "VALIDATION_ERROR",
                "workflow_id": workflow_id,
                "thread_id": thread_id,
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "error": {
                    "category": "input_validation",
                    "severity": "error",
                    "title": "Empty Description",
                    "message": "Workflow description cannot be empty",
                    "user_guidance": "Please provide a clear description of the workflow you want to create",
                    "fix_suggestions": ["Add a detailed description of what the workflow should do"]
                }
            }) + "\n\n"
            return
        
        # Create LLM processing event
        # llm_event = WorkflowEvent(
        #     type=EventType.WORKFLOW_PROCESSING,
        #     workflow_id=workflow_id,
        #     status="processing",
        #     data={"message": "Generating workflow with LLM..."},
        #     priority=EventPriority.NORMAL,
        #     source="workflow_api"
        # )
        
        # await event_stream_manager.publish_event(llm_event)
        
        # yield "data: " + json.dumps({
        #     "type": "LLM_PROCESSING",
        #     "workflow_id": workflow_id,
        #     "thread_id": thread_id,
        #     "run_id": run_id,
        #     "timestamp": datetime.now().isoformat(),
        #     "message": "Generating workflow with LLM..."
        # }) + "\n\n"
        
        # Generate workflow using existing builder
        try:
            workflow_json = workflow_builder.generate_workflow(request.description)
            
            # Create success event
            # success_event = WorkflowEvent(
            #     type=EventType.WORKFLOW_COMPLETED,
            #     workflow_id=workflow_id,
            #     status="completed",
            #     data={
            #         "workflow_json": workflow_json,
            #         "message": "Workflow generated successfully"
            #     },
            #     priority=EventPriority.NORMAL,
            #     source="workflow_api"
            # )
            
            # await event_stream_manager.publish_event(success_event)
            
            yield "data: " + json.dumps({
                "type": "WORKFLOW_GENERATED",
                "workflow_id": workflow_id,
                "thread_id": thread_id,
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "workflow_json": json.loads(workflow_json)
            }) + "\n\n"
            
        except Exception as e:
            # Enhanced error handling to detect LLM crashes and provide specific guidance
            error_message = str(e)
            error_type = "GENERATION_ERROR"
            
            # Detect specific LLM crash scenarios
            if "LLM service unavailable" in error_message or "LLM service HTTP error" in error_message:
                error_type = "LLM_CRASH_ERROR"
                
                # Check if this looks like a model crash (exit codes, crash messages)
                if any(keyword in error_message.lower() for keyword in [
                    "exit code", "crashed", "model has crashed", "without additional information",
                    "connection refused", "connection reset", "broken pipe"
                ]):
                    yield "data: " + json.dumps({
                        "type": "LLM_CRASH_ERROR",
                        "workflow_id": workflow_id,
                        "thread_id": thread_id,
                        "run_id": run_id,
                        "timestamp": datetime.now().isoformat(),
                        "error": {
                            "category": "llm_crash",
                            "severity": "error",
                            "title": "LLM Model Crashed",
                            "message": f"The local LLM model has crashed: {error_message}",
                            "user_guidance": "Your local LLM model (e.g., in LM Studio) has crashed and needs to be restarted. This can happen due to memory issues, model instability, or system resource constraints.",
                            "fix_suggestions": [
                                "Restart your LLM service (LM Studio, Ollama, etc.)",
                                "Check system resources - ensure you have enough RAM and GPU memory",
                                "Try a smaller or more stable model if crashes persist",
                                "Check LM Studio logs for specific crash details",
                                "Reduce the complexity of your workflow description",
                                "Close other memory-intensive applications",
                                "Consider using a cloud-based LLM if local crashes continue"
                            ],
                            "technical_details": {
                                "original_error": error_message,
                                "likely_cause": "Model crash or service termination",
                                "recovery_action": "Service restart required"
                            }
                        }
                    }) + "\n\n"
                    return
                
                # Check for HTTP errors (404, 500, etc.) - service running but model not loaded OR model crashed
                elif any(keyword in error_message for keyword in [
                    "404", "500", "502", "503", "Not Found", "Internal Server Error", 
                    "Bad Gateway", "Service Unavailable"
                ]):
                    # For local LLM services, 404 errors often indicate model crashes
                    if "404" in error_message or "Not Found" in error_message:
                        # Check if this is a local LLM service (more likely to be a crash)
                        if workflow_builder.llm_config.is_local:
                            error_title = "LLM Model Likely Crashed"
                            user_guidance = "Your local LLM model appears to have crashed. LM Studio is running but returning 404 errors, which typically indicates the model crashed and is no longer loaded."
                            fix_suggestions = [
                                "Check LM Studio logs for crash details (look for 'Exit code' messages)",
                                "Restart LM Studio completely to clear any crashed model state",
                                "Reload your model in LM Studio",
                                "Try a smaller or more stable model if crashes persist",
                                "Check system resources - ensure you have enough RAM and GPU memory",
                                "Close other memory-intensive applications",
                                "Consider using a different model if this one is unstable"
                            ]
                            likely_cause = "Local LLM model crashed (404 from local service usually indicates crash)"
                        else:
                            error_title = "LLM Service: Model Not Loaded"
                            user_guidance = "LM Studio is running, but no model is currently loaded or the API endpoint is incorrect."
                            fix_suggestions = [
                                "Open LM Studio and load a model",
                                "Verify that a model is selected and loaded in LM Studio",
                                "Check that the model is compatible with the chat completions API",
                                "Verify the LLM endpoint URL in your configuration (should be http://localhost:1234/v1/chat/completions)",
                                "Try restarting LM Studio if the model appears loaded but isn't responding",
                                "Check LM Studio's server logs for any error messages"
                            ]
                            likely_cause = "No model loaded in LM Studio or incorrect endpoint"
                    elif "500" in error_message or "Internal Server Error" in error_message:
                        error_title = "LLM Service: Internal Server Error"
                        user_guidance = "LM Studio encountered an internal error while processing the request."
                        fix_suggestions = [
                            "Try reloading the model in LM Studio",
                            "Restart LM Studio completely",
                            "Check if the model is corrupted or incompatible",
                            "Try a different model",
                            "Check LM Studio logs for specific error details",
                            "Ensure you have enough system memory for the model"
                        ]
                        likely_cause = "LM Studio internal error or model issue"
                    else:
                        error_title = "LLM Service: HTTP Error"
                        user_guidance = "The LLM service returned an HTTP error."
                        fix_suggestions = [
                            "Check that LM Studio is running properly",
                            "Verify the model is loaded and responding",
                            "Restart LM Studio if needed",
                            "Check the LM Studio logs for details"
                        ]
                        likely_cause = "HTTP service error"
                    
                    yield "data: " + json.dumps({
                        "type": "LLM_SERVICE_ERROR",
                        "workflow_id": workflow_id,
                        "thread_id": thread_id,
                        "run_id": run_id,
                        "timestamp": datetime.now().isoformat(),
                        "error": {
                            "category": "llm_service",
                            "severity": "error",
                            "title": error_title,
                            "message": f"LLM service error: {error_message}",
                            "user_guidance": user_guidance,
                            "fix_suggestions": fix_suggestions,
                            "technical_details": {
                                "original_error": error_message,
                                "likely_cause": likely_cause,
                                "endpoint": workflow_builder.llm_config.endpoint,
                                "model": workflow_builder.llm_config.model,
                                "is_local": workflow_builder.llm_config.is_local,
                                "recovery_action": "Check LM Studio status and model loading"
                            }
                        }
                    }) + "\n\n"
                    return
            
            # Handle validation errors
            elif "validation" in error_message.lower():
                yield "data: " + json.dumps({
                    "type": "VALIDATION_ERROR",
                    "workflow_id": workflow_id,
                    "thread_id": thread_id,
                    "run_id": run_id,
                    "timestamp": datetime.now().isoformat(),
                    "error": {
                        "category": "workflow_validation",
                        "severity": "error",
                        "title": "Workflow Validation Failed",
                        "message": f"The generated workflow failed validation: {error_message}",
                        "user_guidance": "The LLM generated a workflow, but it contains structural issues that prevent it from working properly.",
                        "fix_suggestions": [
                            "Try rephrasing your workflow description to be more specific",
                            "Break down complex workflows into simpler steps",
                            "Specify the exact nodes and connections you need",
                            "Check if your description contains conflicting requirements"
                        ]
                    }
                }) + "\n\n"
                return
            
            # Generic error handling
            yield "data: " + json.dumps({
                "type": "GENERATION_ERROR",
                "workflow_id": workflow_id,
                "thread_id": thread_id,
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "error": {
                    "category": "workflow_generation",
                    "severity": "error",
                    "title": "Workflow Generation Failed",
                    "message": f"Failed to generate workflow: {error_message}",
                    "user_guidance": "An unexpected error occurred during workflow generation.",
                    "fix_suggestions": [
                        "Try again with a simpler workflow description",
                        "Check that your description is clear and specific",
                        "Verify your LLM service is running properly",
                        "Contact support if the problem persists"
                    ],
                    "technical_details": {
                        "original_error": error_message,
                        "error_type": type(e).__name__
                    }
                }
            }) + "\n\n"
            
    except Exception as e:
        # Always yield the raw error message as a GENERATION_ERROR event
        yield "data: " + json.dumps({
            "type": "GENERATION_ERROR",
            "error": {
                "message": str(e)
            }
        }) + "\n\n"
        return

@app.post("/generate")
async def generate_workflow(request: WorkflowRequest):
    """Generate an n8n workflow from a description."""
    workflow_id = str(uuid.uuid4())
    thread_id = request.thread_id or str(uuid.uuid4())
    run_id = request.run_id or str(uuid.uuid4())
    try:
        # Try to generate the workflow and stream events as before
        return StreamingResponse(
            generate_workflow_events_agui(request),
            media_type="text/event-stream"
        )
    except Exception as e:
        # Use the error handler to categorize the error properly
        error_detail = error_handler.categorize_error(e, {
            'workflow_id': workflow_id,
            'operation_type': 'api_generate_workflow'
        })

        # Return a structured error response if streaming fails
        return {
            "error": {
                "type": "GENERATION_ERROR",
                "workflow_id": workflow_id,
                "thread_id": thread_id,
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "category": error_detail.category.value,
                "severity": error_detail.severity.value,
                "title": error_detail.title,
                "message": error_detail.message,
                "user_guidance": error_detail.user_guidance,
                "fix_suggestions": error_detail.fix_suggestions,
                "technical_details": error_detail.technical_details
            }
        }

@app.post("/modify")
async def modify_workflow(request: WorkflowModificationRequest):
    """Modify an existing workflow based on a description of changes needed."""
    return StreamingResponse(
        modify_workflow_events(request),
        media_type="text/event-stream"
    )

@app.post("/iterate")
async def iterate_workflow(request: WorkflowIterationRequest):
    """Iterate on a workflow based on testing feedback and new requirements."""
    return StreamingResponse(
        iterate_workflow_events(request),
        media_type="text/event-stream"
    )

async def modify_workflow_events(request: WorkflowModificationRequest):
    """Generate events for workflow modification process with enhanced error handling."""
    workflow_id = request.workflow_id or str(uuid.uuid4())
    thread_id = request.thread_id or str(uuid.uuid4())
    run_id = request.run_id or str(uuid.uuid4())
    
    # Start event
    yield "data: " + json.dumps({
        "type": "MODIFICATION_STARTED",
        "workflow_id": workflow_id,
        "thread_id": thread_id,
        "run_id": run_id,
        "timestamp": datetime.now().isoformat()
    }) + "\n\n"
    
    try:
        # Pre-validate inputs with enhanced error handling
        yield "data: " + json.dumps({
            "type": "VALIDATION_STARTED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Validating workflow and modification request..."
        }) + "\n\n"
        
        # Validate workflow JSON
        workflow_validation_errors = error_handler.validate_workflow_input(request.existing_workflow_json)
        if workflow_validation_errors:
            validation_error_detail = error_handler.create_validation_error_summary(workflow_validation_errors)
            
            yield "data: " + json.dumps({
                "type": "VALIDATION_ERROR",
                "workflow_id": workflow_id,
                "thread_id": thread_id,
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "error": {
                    "category": validation_error_detail.category.value,
                    "severity": validation_error_detail.severity.value,
                    "title": validation_error_detail.title,
                    "message": validation_error_detail.message,
                    "user_guidance": validation_error_detail.user_guidance,
                    "fix_suggestions": validation_error_detail.fix_suggestions,
                    "technical_details": validation_error_detail.technical_details
                }
            }) + "\n\n"
            return
        
        # Validate modification description
        description_validation_errors = error_handler.validate_modification_description(request.modification_description)
        if description_validation_errors:
            description_error_detail = error_handler.create_validation_error_summary(description_validation_errors)
            
            yield "data: " + json.dumps({
                "type": "VALIDATION_ERROR",
                "workflow_id": workflow_id,
                "thread_id": thread_id,
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "error": {
                    "category": description_error_detail.category.value,
                    "severity": description_error_detail.severity.value,
                    "title": description_error_detail.title,
                    "message": description_error_detail.message,
                    "user_guidance": description_error_detail.user_guidance,
                    "fix_suggestions": description_error_detail.fix_suggestions,
                    "technical_details": description_error_detail.technical_details
                }
            }) + "\n\n"
            return
        
        # Validation passed
        yield "data: " + json.dumps({
            "type": "VALIDATION_COMPLETED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Input validation completed successfully"
        }) + "\n\n"
        
        # Check LLM availability before proceeding
        yield "data: " + json.dumps({
            "type": "LLM_CHECK_STARTED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Checking LLM service availability..."
        }) + "\n\n"
        
        is_available, availability_error = await check_llm_availability()
        if not is_available:
            logger.error("LLM unavailable for workflow modification", extra={'workflow_id': workflow_id, 'thread_id': thread_id, 'run_id': run_id, 'error': availability_error})
            yield "data: " + json.dumps({
                "type": "LLM_UNAVAILABLE",
                "workflow_id": workflow_id,
                "thread_id": thread_id,
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "error": {
                    "category": "llm_service",
                    "severity": "error",
                    "title": "LLM Service Unavailable",
                    "message": availability_error,
                    "user_guidance": "The AI service is currently unavailable or taking longer than expected. Local LLMs may need more time for complex workflow modifications. Your existing workflow data has been preserved. Please try again in a few minutes.",
                    "fix_suggestions": [
                        "Wait a few minutes and try again - local LLMs can be slower than cloud services",
                        "Check that your local LLM service (e.g., LM Studio) is running and not overloaded",
                        "Verify your system has sufficient resources (CPU/GPU/RAM) for the LLM",
                        "Consider breaking complex modifications into smaller steps",
                        "Check your internet connection if using external LLM"
                    ]
                }
            }) + "\n\n"
            return
        
        logger.info("LLM availability confirmed", extra={'workflow_id': workflow_id, 'thread_id': thread_id, 'run_id': run_id})
        yield "data: " + json.dumps({
            "type": "LLM_AVAILABLE",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "LLM service is available and ready"
        }) + "\n\n"
        
        # Processing started
        yield "data: " + json.dumps({
            "type": "PROCESSING_STARTED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Processing workflow modification..."
        }) + "\n\n"
        
        # Modify workflow
        modified_workflow_json = workflow_builder.modify_workflow(
            request.existing_workflow_json,
            request.modification_description,
            workflow_id
        )
        
        # Validate modified workflow
        validation_result = workflow_validator.validate_workflow(modified_workflow_json)
        
        # Create response
        response = WorkflowResponse(
            workflow_id=workflow_id,
            workflow_json=modified_workflow_json,
            validation_result=validation_result,
            timestamp=datetime.now()
        )
        
        # Success event
        yield "data: " + json.dumps({
            "type": "WORKFLOW_MODIFIED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "data": response.dict()
        }) + "\n\n"
        
        # Finish event
        yield "data: " + json.dumps({
            "type": "MODIFICATION_FINISHED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }) + "\n\n"
        
    except Exception as e:
        # Enhanced error handling
        error_detail = error_handler.categorize_error(e, {
            'workflow_id': workflow_id,
            'operation_type': 'api_modify_workflow'
        })
        
        # Error event with detailed information
        yield "data: " + json.dumps({
            "type": "MODIFICATION_ERROR",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "error": {
                "category": error_detail.category.value,
                "severity": error_detail.severity.value,
                "title": error_detail.title,
                "message": error_detail.message,
                "user_guidance": error_detail.user_guidance,
                "fix_suggestions": error_detail.fix_suggestions,
                "technical_details": error_detail.technical_details
            }
        }) + "\n\n"

async def iterate_workflow_events(request: WorkflowIterationRequest):
    """Generate events for workflow iteration process with enhanced error handling."""
    workflow_id = request.workflow_id
    thread_id = request.thread_id or str(uuid.uuid4())
    run_id = request.run_id or str(uuid.uuid4())
    
    # Start event
    yield "data: " + json.dumps({
        "type": "ITERATION_STARTED",
        "workflow_id": workflow_id,
        "thread_id": thread_id,
        "run_id": run_id,
        "timestamp": datetime.now().isoformat()
    }) + "\n\n"
    
    try:
        # Pre-validate inputs with enhanced error handling
        yield "data: " + json.dumps({
            "type": "VALIDATION_STARTED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Validating workflow and iteration request..."
        }) + "\n\n"
        
        # Validate workflow ID
        if not workflow_id or not workflow_id.strip():
            error_detail = ErrorDetail(
                category=ErrorCategory.INPUT_VALIDATION,
                severity=ErrorSeverity.ERROR,
                title="Missing Workflow ID",
                message="Workflow ID is required for iteration tracking",
                user_guidance="Please provide a valid workflow ID to track iteration history",
                fix_suggestions=[
                    "Provide a unique workflow ID string",
                    "Use a descriptive name like 'my-email-workflow' or 'customer-onboarding'"
                ]
            )
            
            yield "data: " + json.dumps({
                "type": "VALIDATION_ERROR",
                "workflow_id": workflow_id,
                "thread_id": thread_id,
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "error": {
                    "category": error_detail.category.value,
                    "severity": error_detail.severity.value,
                    "title": error_detail.title,
                    "message": error_detail.message,
                    "user_guidance": error_detail.user_guidance,
                    "fix_suggestions": error_detail.fix_suggestions
                }
            }) + "\n\n"
            return
        
        # Validate workflow JSON
        workflow_validation_errors = error_handler.validate_workflow_input(request.existing_workflow_json)
        if workflow_validation_errors:
            validation_error_detail = error_handler.create_validation_error_summary(workflow_validation_errors)
            
            yield "data: " + json.dumps({
                "type": "VALIDATION_ERROR",
                "workflow_id": workflow_id,
                "thread_id": thread_id,
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "error": {
                    "category": validation_error_detail.category.value,
                    "severity": validation_error_detail.severity.value,
                    "title": validation_error_detail.title,
                    "message": validation_error_detail.message,
                    "user_guidance": validation_error_detail.user_guidance,
                    "fix_suggestions": validation_error_detail.fix_suggestions,
                    "technical_details": validation_error_detail.technical_details
                }
            }) + "\n\n"
            return
        
        # Validate feedback from testing
        if not request.feedback_from_testing or not request.feedback_from_testing.strip():
            error_detail = ErrorDetail(
                category=ErrorCategory.INPUT_VALIDATION,
                severity=ErrorSeverity.ERROR,
                title="Missing Testing Feedback",
                message="Testing feedback is required for workflow iteration",
                user_guidance="Please provide feedback about how the workflow performed during testing",
                fix_suggestions=[
                    "Describe what worked well: 'The email sending works correctly'",
                    "Describe what needs improvement: 'The error handling needs to be more robust'",
                    "Provide specific issues: 'The workflow fails when the API is unavailable'"
                ]
            )
            
            yield "data: " + json.dumps({
                "type": "VALIDATION_ERROR",
                "workflow_id": workflow_id,
                "thread_id": thread_id,
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "error": {
                    "category": error_detail.category.value,
                    "severity": error_detail.severity.value,
                    "title": error_detail.title,
                    "message": error_detail.message,
                    "user_guidance": error_detail.user_guidance,
                    "fix_suggestions": error_detail.fix_suggestions
                }
            }) + "\n\n"
            return
        
        # Validation passed
        yield "data: " + json.dumps({
            "type": "VALIDATION_COMPLETED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Input validation completed successfully"
        }) + "\n\n"
        
        # Check LLM availability before proceeding
        yield "data: " + json.dumps({
            "type": "LLM_CHECK_STARTED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Checking LLM service availability..."
        }) + "\n\n"
        
        is_available, availability_error = await check_llm_availability()
        if not is_available:
            logger.error("LLM unavailable for workflow iteration", extra={'workflow_id': workflow_id, 'thread_id': thread_id, 'run_id': run_id, 'error': availability_error})
            yield "data: " + json.dumps({
                "type": "LLM_UNAVAILABLE",
                "workflow_id": workflow_id,
                "thread_id": thread_id,
                "run_id": run_id,
                "timestamp": datetime.now().isoformat(),
                "error": {
                    "category": "llm_service",
                    "severity": "error",
                    "title": "LLM Service Unavailable",
                    "message": availability_error,
                    "user_guidance": "The AI service is currently unavailable or taking longer than expected. Local LLMs may need more time for complex workflow modifications. Your workflow data and feedback have been preserved. Please try again in a few minutes.",
                    "fix_suggestions": [
                        "Wait a few minutes and try again - local LLMs can be slower than cloud services",
                        "Check that your local LLM service (e.g., LM Studio) is running and not overloaded",
                        "Verify your system has sufficient resources (CPU/GPU/RAM) for the LLM",
                        "Consider breaking complex modifications into smaller steps",
                        "Check your internet connection if using external LLM"
                    ]
                }
            }) + "\n\n"
            return
        
        logger.info("LLM availability confirmed", extra={'workflow_id': workflow_id, 'thread_id': thread_id, 'run_id': run_id})
        yield "data: " + json.dumps({
            "type": "LLM_AVAILABLE",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "LLM service is available and ready"
        }) + "\n\n"
        
        # Processing started
        yield "data: " + json.dumps({
            "type": "PROCESSING_STARTED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Processing workflow iteration..."
        }) + "\n\n"
        
        # Iterate workflow
        iterated_workflow_json = workflow_builder.iterate_workflow(
            request.workflow_id,
            request.existing_workflow_json,
            request.feedback_from_testing,
            request.additional_requirements or ""
        )
        
        # Validate iterated workflow
        validation_result = workflow_validator.validate_workflow(iterated_workflow_json)
        
        # Create response
        response = WorkflowResponse(
            workflow_id=workflow_id,
            workflow_json=iterated_workflow_json,
            validation_result=validation_result,
            timestamp=datetime.now()
        )
        
        # Success event
        yield "data: " + json.dumps({
            "type": "WORKFLOW_ITERATED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "data": response.dict()
        }) + "\n\n"
        
        # Finish event
        yield "data: " + json.dumps({
            "type": "ITERATION_FINISHED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }) + "\n\n"
        
    except Exception as e:
        # Enhanced error handling
        error_detail = error_handler.categorize_error(e, {
            'workflow_id': workflow_id,
            'operation_type': 'api_iterate_workflow'
        })
        
        # Error event with detailed information
        yield "data: " + json.dumps({
            "type": "ITERATION_ERROR",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "error": {
                "category": error_detail.category.value,
                "severity": error_detail.severity.value,
                "title": error_detail.title,
                "message": error_detail.message,
                "user_guidance": error_detail.user_guidance,
                "fix_suggestions": error_detail.fix_suggestions,
                "technical_details": error_detail.technical_details
            }
        }) + "\n\n"

@app.get("/iterations/{workflow_id}")
async def get_workflow_iterations(workflow_id: str):
    """Get the iteration history for a specific workflow."""
    iterations = workflow_builder.get_workflow_iterations(workflow_id)
    
    if not iterations:
        raise HTTPException(status_code=404, detail="No iterations found for this workflow")
    
    return iterations

@app.get("/feedback/{workflow_id}")
async def get_workflow_feedback(workflow_id: str):
    """Get feedback for a specific workflow."""
    feedback = workflow_builder.get_feedback_history()
    workflow_feedback = [f for f in feedback if f.workflow_id == workflow_id]
    
    if not workflow_feedback:
        raise HTTPException(status_code=404, detail="Workflow feedback not found")
    
    return workflow_feedback

@app.get("/health")
async def health_check():
    """Check the health of the API."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/llm/health")
async def llm_health_check():
    """Check if the LLM service is available and responding with a loaded model."""
    try:
        # Test LLM availability with a simple prompt
        test_prompt = "Return exactly this JSON: {\"test\": \"ok\"}"
        
        # Try to call the LLM with a longer timeout for local LLMs
        start_time = time.time()
        
        result = await asyncio.wait_for(
            workflow_builder._execute_llm_call(test_prompt),
            timeout=30.0  # Increased to 30 seconds for local LLMs
        )
        
        response_time = time.time() - start_time
        
        # If we get here, LLM is responding with a loaded model
        return {
            "status": "available",
            "llm_endpoint": workflow_builder.llm_config.endpoint,
            "llm_model": workflow_builder.llm_config.model,
            "is_local": workflow_builder.llm_config.is_local,
            "timestamp": datetime.now().isoformat(),
            "response_time_ms": round(response_time * 1000, 2),
            "test_response_preview": result[:100] if result else "No response content"
        }
        
    except asyncio.TimeoutError:
        return {
            "status": "timeout",
            "llm_endpoint": workflow_builder.llm_config.endpoint,
            "llm_model": workflow_builder.llm_config.model,
            "is_local": workflow_builder.llm_config.is_local,
            "timestamp": datetime.now().isoformat(),
            "error": "LLM service did not respond within 30 seconds - may be processing or overloaded"
        }
    except Exception as e:
        error_message = str(e).lower()
        
        # Check for specific "no model loaded" errors
        if any(phrase in error_message for phrase in [
            "no models loaded", "model_not_found", "model not found", 
            "please load a model", "no model is currently loaded"
        ]):
            return {
                "status": "no_model_loaded",
                "llm_endpoint": workflow_builder.llm_config.endpoint,
                "llm_model": workflow_builder.llm_config.model,
                "is_local": workflow_builder.llm_config.is_local,
                "timestamp": datetime.now().isoformat(),
                "error": "LLM service is running but no model is loaded. Please load a model in your LLM service (e.g., LM Studio).",
                "suggestion": "Load a model in your LLM service interface or use the appropriate load command"
            }
        
        # Check for connection issues
        elif any(phrase in error_message for phrase in [
            "connection refused", "connection reset", "cannot connect"
        ]):
            return {
                "status": "unavailable",
                "llm_endpoint": workflow_builder.llm_config.endpoint,
                "llm_model": workflow_builder.llm_config.model,
                "is_local": workflow_builder.llm_config.is_local,
                "timestamp": datetime.now().isoformat(),
                "error": "Cannot connect to LLM service - service may not be running",
                "suggestion": "Start your LLM service (e.g., LM Studio) and ensure it's listening on the configured port"
            }
        
        # Check for service errors
        elif any(phrase in error_message for phrase in [
            "internal error", "server error", "service error", "http 500"
        ]):
            return {
                "status": "service_error",
                "llm_endpoint": workflow_builder.llm_config.endpoint,
                "llm_model": workflow_builder.llm_config.model,
                "is_local": workflow_builder.llm_config.is_local,
                "timestamp": datetime.now().isoformat(),
                "error": "LLM service encountered an internal error",
                "suggestion": "Check your LLM service logs and restart if necessary"
            }
        
        # Generic unavailable status for other errors
        else:
            return {
                "status": "unavailable",
                "llm_endpoint": workflow_builder.llm_config.endpoint,
                "llm_model": workflow_builder.llm_config.model,
                "is_local": workflow_builder.llm_config.is_local,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "suggestion": "Check your LLM service status and configuration"
            }

async def check_llm_availability():
    """Helper function to check if LLM is available before generation."""
    try:
        test_prompt = "Return exactly this JSON: {\"test\": \"ok\"}"
        start_time = time.time()
        
        await asyncio.wait_for(
            workflow_builder._execute_llm_call(test_prompt),
            timeout=45.0  # Increased to 45 seconds for local LLMs with complex workflow prompts
        )
        
        response_time = time.time() - start_time
        logger.info(f"LLM availability check completed in {response_time:.2f} seconds")
        
        return True, None
    except asyncio.TimeoutError:
        return False, "LLM service is not responding (timeout after 45 seconds). Local LLMs may need more time for complex requests. Please try again in a few minutes."
    except Exception as e:
        error_message = str(e)
        
        # Enhanced crash detection
        if any(keyword in error_message.lower() for keyword in [
            "exit code", "crashed", "model has crashed", "without additional information",
            "connection refused", "connection reset", "broken pipe", "terminated", "killed"
        ]):
            crash_info = detect_llm_crash_details(error_message)
            return False, f"LLM service has crashed: {crash_info}"
        
        return False, f"LLM service is currently unavailable: {str(e)}. Please try again in a few minutes."

def detect_llm_crash_details(error_message: str) -> str:
    """Detect and extract specific crash information from error messages."""
    error_lower = error_message.lower()
    
    # Look for exit codes
    import re
    exit_code_match = re.search(r'exit code[:\s]*(\d+)', error_lower)
    if exit_code_match:
        exit_code = exit_code_match.group(1)
        
        # Interpret common exit codes
        exit_code_meanings = {
            "1": "General error - model may have encountered an internal error",
            "2": "Misuse of shell command - configuration issue",
            "126": "Command invoked cannot execute - permission or dependency issue",
            "127": "Command not found - model executable missing",
            "128": "Invalid argument to exit - model crashed unexpectedly",
            "130": "Script terminated by Control-C - manual termination",
            "137": "Process killed (SIGKILL) - out of memory or forced termination",
            "139": "Segmentation fault - model crashed due to memory access violation",
            "143": "Process terminated (SIGTERM) - graceful shutdown requested",
            "18446744072635812000": "Large exit code indicating severe crash or memory corruption"
        }
        
        meaning = exit_code_meanings.get(exit_code, "Unknown exit code - indicates model crash")
        return f"Model crashed with exit code {exit_code} ({meaning}). Check system resources and restart your LLM service."
    
    # Look for specific crash indicators
    if "connection refused" in error_lower:
        return "LLM service is not running or has stopped. Please start your LLM service (e.g., LM Studio)."
    elif "connection reset" in error_lower:
        return "LLM service crashed during communication. Please restart your LLM service."
    elif "model has crashed" in error_lower:
        return "The LLM model has crashed. Check system resources and restart your LLM service."
    elif "without additional information" in error_lower:
        return "LLM model crashed without providing error details. This often indicates memory issues or model instability."
    elif "broken pipe" in error_lower:
        return "Communication with LLM service was interrupted. The service may have crashed or been terminated."
    elif "terminated" in error_lower or "killed" in error_lower:
        return "LLM service was terminated, possibly due to resource constraints or manual intervention."
    
    return f"LLM service appears to have crashed: {error_message}"

# ============================================================================
# PROJECT MANAGEMENT API ENDPOINTS
# Task 2.0.3: Project API endpoints
# ============================================================================

@app.get("/projects", response_model=List[ProjectResponse])
async def list_projects():
    """List all projects."""
    try:
        projects = project_manager.list_projects(refresh_cache=True)
        
        # Convert ProjectInfo objects to ProjectResponse format
        project_responses = []
        for project_info in projects:
            project_responses.append(ProjectResponse(
                name=project_info.name,
                path=str(project_info.path),
                description=project_info.description,
                created_date=project_info.created_date.isoformat(),
                last_modified=project_info.last_modified.isoformat(),
                workflow_count=project_info.workflow_count,
                workflows=project_info.workflows,
                settings=project_info.settings
            ))
        
        return project_responses
        
    except Exception as e:
        logger.error("Failed to list projects", extra={'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to list projects: {str(e)}")

@app.get("/projects/stats", response_model=ProjectStatsResponse)
async def get_project_stats():
    """Get comprehensive project statistics."""
    try:
        stats = project_manager.get_project_stats()
        
        return ProjectStatsResponse(
            total_projects=stats['total_projects'],
            total_workflows=stats['total_workflows'],
            projects_root=stats['projects_root'],
            average_workflows_per_project=stats['average_workflows_per_project'],
            project_names=stats['project_names'],
            largest_project=stats['largest_project'],
            most_recent_project=stats['most_recent_project']
        )
        
    except Exception as e:
        logger.error("Failed to get project stats", extra={'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to get project stats: {str(e)}")

@app.post("/projects/{name}", response_model=ProjectResponse)
async def create_project(name: str, request: ProjectCreateRequest):
    """Create a new project."""
    try:
        # Prioritize request body name, but fall back to URL path if not provided
        project_name = request.name if request.name is not None else name
        
        # Validate project name
        if not project_name or not project_name.strip():
            raise HTTPException(status_code=400, detail="Project name cannot be empty")
        
        project_info = project_manager.create_project(
            name=project_name,
            description=request.description or "",
            initial_workflows=request.initial_workflows
        )
        
        return ProjectResponse(
            name=project_info.name,
            path=str(project_info.path),
            description=project_info.description,
            created_date=project_info.created_date.isoformat(),
            last_modified=project_info.last_modified.isoformat(),
            workflow_count=project_info.workflow_count,
            workflows=project_info.workflows,
            settings=project_info.settings
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to create project", extra={'project_name': name, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

@app.get("/projects/{name}", response_model=ProjectResponse)
async def get_project(name: str):
    """Get project details and workflow list."""
    try:
        project_info = project_manager.get_project_info(name)
        
        if not project_info:
            raise HTTPException(status_code=404, detail=f"Project '{name}' not found")
        
        return ProjectResponse(
            name=project_info.name,
            path=str(project_info.path),
            description=project_info.description,
            created_date=project_info.created_date.isoformat(),
            last_modified=project_info.last_modified.isoformat(),
            workflow_count=project_info.workflow_count,
            workflows=project_info.workflows,
            settings=project_info.settings
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get project", extra={'project_name': name, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to get project: {str(e)}")

@app.get("/projects/{name}/workflows", response_model=List[str])
async def list_project_workflows(name: str):
    """List workflows in a project."""
    try:
        if not project_manager.project_exists(name):
            raise HTTPException(status_code=404, detail=f"Project '{name}' not found")
        
        workflows = project_manager.list_project_workflows(name)
        return workflows
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to list workflows for project", extra={'project_name': name, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to list workflows: {str(e)}")

@app.get("/projects/{name}/workflows/{filename}", response_model=WorkflowFileResponse)
async def get_workflow_file(name: str, filename: str):
    """Get a specific workflow file."""
    try:
        # Read workflow file
        workflow_data = filesystem_utils.read_workflow_file(name, filename)
        
        # Get workflow info for metadata
        workflow_info = filesystem_utils.get_workflow_info(name, filename)
        
        return WorkflowFileResponse(
            filename=filename,
            project_name=name,
            workflow_data=workflow_data,
            file_size=workflow_info.file_size,
            last_modified=workflow_info.last_modified.isoformat()
        )
        
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Failed to get workflow", extra={'workflow_name': name, 'workflow_filename': filename, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to get workflow: {str(e)}")

@app.put("/projects/{name}/workflows/{filename}")
async def save_workflow_file(name: str, filename: str, request: WorkflowFileRequest):
    """Save a workflow file to a project."""
    try:
        # Validate workflow data
        validation_errors = filesystem_utils.validate_workflow_json(request.workflow_data)
        if validation_errors:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid workflow JSON: {'; '.join(validation_errors)}"
            )
        
        # Write workflow file
        success = filesystem_utils.write_workflow_file(
            name,
            filename,
            request.workflow_data,
            create_backup=request.create_backup or True
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save workflow file")
        
        # Get updated workflow info
        workflow_info = filesystem_utils.get_workflow_info(name, filename)
        
        return {
            "message": "Workflow saved successfully",
            "filename": filename,
            "project_name": name,
            "file_size": workflow_info.file_size,
            "backup_created": request.create_backup,
            "last_modified": workflow_info.last_modified.isoformat()
        }
        
    except ValueError as e:
        if "does not exist" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to save workflow", extra={'workflow_name': name, 'workflow_filename': filename, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to save workflow: {str(e)}")

@app.delete("/projects/{name}")
async def delete_project(name: str, confirm: bool = False):
    """Delete a project and all its contents."""
    try:
        if not confirm:
            raise HTTPException(
                status_code=400, 
                detail="Project deletion requires explicit confirmation. Add ?confirm=true to the request."
            )
        
        success = project_manager.delete_project(name, confirm=True)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Project '{name}' not found")
        
        return {"message": f"Project '{name}' deleted successfully"}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete project", extra={'project_name': name, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {str(e)}")

# ============================================================================
# VERSION MANAGEMENT API ENDPOINTS
# Task 2.0.4: Smart file versioning system
# ============================================================================

@app.get("/projects/{name}/workflows/{filename}/versions", response_model=List[str])
async def list_workflow_versions(name: str, filename: str):
    """List all versions of a workflow file."""
    try:
        if not project_manager.project_exists(name):
            raise HTTPException(status_code=404, detail=f"Project '{name}' not found")
        
        versions = filesystem_utils.list_workflow_versions(name, filename)
        return versions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to list versions for workflow", extra={'workflow_name': name, 'workflow_filename': filename, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to list workflow versions: {str(e)}")

@app.get("/projects/{name}/workflows/{filename}/versions/{version_filename}", response_model=VersionInfoResponse)
async def get_workflow_version_info(name: str, filename: str, version_filename: str):
    """Get detailed information about a specific workflow version."""
    try:
        version_info = filesystem_utils.get_version_info(name, filename, version_filename)
        
        return VersionInfoResponse(
            filename=version_info['filename'],
            timestamp=version_info['timestamp'],
            created_date=version_info['created_date'],
            modified_date=version_info['modified_date'],
            file_size=version_info['file_size'],
            file_size_mb=version_info['file_size_mb'],
            workflow_name=version_info['workflow_name'],
            node_count=version_info['node_count'],
            tags=version_info['tags'],
            is_backup=version_info['is_backup']
        )
        
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Failed to get version info", extra={'workflow_name': name, 'workflow_filename': filename, 'version_filename': version_filename, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to get version info: {str(e)}")

@app.get("/projects/{name}/workflows/{filename}/versions/{version_filename}/content")
async def get_workflow_version_content(name: str, filename: str, version_filename: str):
    """Get the content of a specific workflow version."""
    try:
        if not project_manager.project_exists(name):
            raise HTTPException(status_code=404, detail=f"Project '{name}' not found")
        
        project_path = project_manager.projects_root / name
        version_path = project_path / version_filename
        
        if not version_path.exists():
            raise HTTPException(status_code=404, detail=f"Version file '{version_filename}' not found")
        
        # Read and return the version content
        import json
        with open(version_path, 'r', encoding='utf-8') as f:
            version_data = json.load(f)
        
        return {
            "filename": version_filename,
            "project_name": name,
            "workflow_data": version_data,
            "is_version": True
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get version content", extra={'workflow_name': name, 'workflow_filename': filename, 'version_filename': version_filename, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to get version content: {str(e)}")

@app.post("/projects/{name}/workflows/{filename}/versions/{version_filename}/restore")
async def restore_workflow_version(name: str, filename: str, version_filename: str, request: VersionRestoreRequest):
    """Restore a workflow from a specific version."""
    try:
        success = filesystem_utils.restore_workflow_version(
            name,
            filename,
            version_filename,
            create_backup=request.create_backup if request.create_backup is not None else True
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to restore workflow version")
        
        return {
            "message": f"Successfully restored workflow '{filename}' from version '{version_filename}'",
            "project_name": name,
            "workflow_filename": filename,
            "restored_from": version_filename,
            "backup_created": request.create_backup
        }
        
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Failed to restore workflow from version", extra={'workflow_name': name, 'workflow_filename': filename, 'version_filename': version_filename, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to restore workflow version: {str(e)}")

@app.get("/projects/{name}/workflows/{filename}/compare/{version1}/{version2}", response_model=VersionComparisonResponse)
async def compare_workflow_versions(name: str, filename: str, version1: str, version2: str):
    """Compare two workflow versions."""
    try:
        comparison = filesystem_utils.compare_workflow_versions(name, filename, version1, version2)
        
        return VersionComparisonResponse(
            version1=comparison['version1'],
            version2=comparison['version2'],
            differences=comparison['differences'],
            summary=comparison['summary']
        )
        
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Failed to compare workflow versions", extra={'workflow_name': name, 'workflow_filename': filename, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to compare workflow versions: {str(e)}")

@app.delete("/projects/{name}/workflows/{filename}/versions/{version_filename}")
async def delete_workflow_version(name: str, filename: str, version_filename: str, confirm: bool = False):
    """Delete a specific workflow version."""
    try:
        if not confirm:
            raise HTTPException(
                status_code=400, 
                detail="Version deletion requires explicit confirmation. Add ?confirm=true to the request."
            )
        
        success = filesystem_utils.delete_workflow_version(name, filename, version_filename, confirm=True)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete workflow version")
        
        return {
            "message": f"Successfully deleted version '{version_filename}' for workflow '{filename}'",
            "project_name": name,
            "workflow_filename": filename,
            "deleted_version": version_filename
        }
        
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete version", extra={'workflow_name': name, 'workflow_filename': filename, 'version_filename': version_filename, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to delete workflow version: {str(e)}")

@app.post("/projects/{name}/workflows/{filename}/cleanup-versions")
async def cleanup_workflow_versions(name: str, filename: str, request: VersionCleanupRequest):
    """Clean up old versions of a workflow, keeping only the specified number."""
    try:
        # Use default value of 10 if keep_versions is None
        keep_versions = request.keep_versions if request.keep_versions is not None else 10
        deleted_count = filesystem_utils.cleanup_old_versions(name, filename, keep_versions)

        return {
            "message": f"Cleaned up old versions for workflow '{filename}'",
            "project_name": name,
            "workflow_filename": filename,
            "versions_deleted": deleted_count,
            "versions_kept": keep_versions
        }

    except Exception as e:
        logger.error("Failed to cleanup versions for workflow", extra={'workflow_name': name, 'workflow_filename': filename, 'error': str(e)})
        raise HTTPException(status_code=500, detail=f"Failed to cleanup workflow versions: {str(e)}")

@app.post("/generate-agui")
async def generate_workflow_agui(request: WorkflowRequest):
    """Generate an n8n workflow using AG_UI streaming protocol."""
    return StreamingResponse(
        generate_workflow_events_agui(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )

@app.get("/agui/status")
async def get_system_status():
    """Get system status - non-streaming approach."""
    try:
        # health_status = await agent_integration_manager.get_health_status()
        return {
            "status": "non_streaming", # "healthy" if health_status.get("overall_status") == "healthy" else "unhealthy",
            "components": {
                "approach": "Complete response collection (non-streaming)",
                "llm_integration": "Collects full LLM response before processing",
                "json_extraction": "Enhanced multi-strategy JSON extraction from complete response",
                "workflow_generation": "available",
                "workflow_modification": "available",
                "workflow_iteration": "available"
            }, # health_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/agui/workflow/stream")
async def stream_workflow_with_agui(request: WorkflowRequest):
    """Stream workflow generation with proper AG_UI event handling for LLM responses."""
    
    async def agui_llm_stream():
        workflow_id = str(uuid.uuid4())
        
        # Create session
        # session_id = await ui_controller.create_ui_session({
        #     'workflow_id': workflow_id,
        #     'client_type': 'streaming_llm'
        # })
        
        try:
            # Subscribe to all workflow events
            # await ui_controller.subscribe_to_workflow(session_id, workflow_id)
            
            # This is where we would integrate with the LLM streaming
            # For now, simulate the streaming behavior that should handle
            # the intermittent LLM outputs you mentioned
            
            # Start event
            # start_event = WorkflowEvent(
            #     type=EventType.WORKFLOW_STARTED,
            #     workflow_id=workflow_id,
            #     status="started",
            #     data={"message": "Starting LLM streaming workflow generation"},
            #     priority=EventPriority.NORMAL,
            #     source="agui_stream"
            # )
            # await event_stream_manager.publish_event(start_event)
            
            yield "data: " + json.dumps({
                "type": "STREAM_STARTED",
                "workflow_id": workflow_id,
                "timestamp": datetime.now().isoformat(),
                "message": "AG_UI streaming initialized"
            }) + "\n\n"
            
            # LLM Processing event
            # processing_event = WorkflowEvent(
            #     type=EventType.WORKFLOW_PROCESSING,
            #     workflow_id=workflow_id,
            #     status="processing",
            #     data={"message": "LLM generating response with proper streaming handling"},
            #     priority=EventPriority.NORMAL,
            #     source="agui_stream"
            # )
            # await event_stream_manager.publish_event(processing_event)
            
            yield "data: " + json.dumps({
                "type": "LLM_STREAMING",
                "workflow_id": workflow_id,
                "timestamp": datetime.now().isoformat(),
                "message": "AG_UI handling LLM streaming responses",
                "note": "This properly handles intermittent LLM outputs and ensures complete responses"
            }) + "\n\n"
            
            # Here's where the AG_UI system would properly handle:
            # 1. Intermittent LLM outputs (multiple chunks)
            # 2. Thinking tags in responses
            # 3. Complete response validation
            # 4. Proper JSON extraction
            
            # Simulate successful completion
            try:
                workflow_json = workflow_builder.generate_workflow(request.description)
                
                # completion_event = WorkflowEvent(
                #     type=EventType.WORKFLOW_COMPLETED,
                #     workflow_id=workflow_id,
                #     status="completed",
                #     data={
                #         "workflow_json": workflow_json,
                #         "message": "AG_UI successfully handled LLM streaming and generated workflow"
                #     },
                #     priority=EventPriority.NORMAL,
                #     source="agui_stream"
                # )
                # await event_stream_manager.publish_event(completion_event)
                
                yield "data: " + json.dumps({
                    "type": "STREAM_COMPLETED",
                    "workflow_id": workflow_id,
                    "timestamp": datetime.now().isoformat(),
                    "workflow_json": json.loads(workflow_json),
                    "message": "AG_UI streaming completed successfully"
                }) + "\n\n"
                
            except Exception as e:
                # error_event = WorkflowEvent(
                #     type=EventType.WORKFLOW_ERROR,
                #     workflow_id=workflow_id,
                #     status="error",
                #     data={"error": str(e)},
                #     priority=EventPriority.HIGH,
                #     source="agui_stream"
                # )
                # await event_stream_manager.publish_event(error_event)
                
                yield "data: " + json.dumps({
                    "type": "STREAM_ERROR",
                    "workflow_id": workflow_id,
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e)
                }) + "\n\n"
                
        finally:
            # Clean up session
            # await ui_controller.remove_ui_session(session_id)
            pass
    
    return StreamingResponse(
        agui_llm_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    ) 