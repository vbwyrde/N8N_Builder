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

from .n8n_builder import N8NBuilder
from .validators import BaseWorkflowValidator, ValidationResult
from .error_handler import EnhancedErrorHandler, ErrorDetail
from .project_manager import project_manager, filesystem_utils, ProjectInfo, WorkflowInfo

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get the static directory path
static_dir = os.path.join(os.path.dirname(__file__), "static")
logger.debug(f"Static directory path: {static_dir}")
logger.debug(f"Static directory exists: {os.path.exists(static_dir)}")
logger.debug(f"Static directory contents: {os.listdir(static_dir) if os.path.exists(static_dir) else 'Directory not found'}")

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

async def generate_workflow_events(request: WorkflowRequest):
    """Generate events for workflow creation process."""
    workflow_id = str(uuid.uuid4())
    thread_id = request.thread_id or str(uuid.uuid4())
    run_id = request.run_id or str(uuid.uuid4())
    
    # Start event
    yield json.dumps({
        "type": "RUN_STARTED",
        "workflow_id": workflow_id,
        "thread_id": thread_id,
        "run_id": run_id,
        "timestamp": datetime.now().isoformat()
    }) + "\n"
    
    try:
        # Generate workflow
        workflow_json = workflow_builder.generate_workflow(request.description)
        
        # Validate workflow
        validation_result = workflow_validator.validate_workflow(workflow_json)
        
        # Create response
        response = WorkflowResponse(
            workflow_id=workflow_id,
            workflow_json=workflow_json,
            validation_result=validation_result,
            timestamp=datetime.now()
        )
        
        # Success event
        yield json.dumps({
            "type": "WORKFLOW_GENERATED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "data": response.dict()
        }) + "\n"
        
        # Finish event
        yield json.dumps({
            "type": "RUN_FINISHED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }) + "\n"
        
    except Exception as e:
        # Error event
        yield json.dumps({
            "type": "RUN_ERROR",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }) + "\n"

@app.post("/generate")
async def generate_workflow(request: WorkflowRequest):
    """Generate an n8n workflow from a description."""
    return StreamingResponse(
        generate_workflow_events(request),
        media_type="text/event-stream"
    )

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
    yield json.dumps({
        "type": "MODIFICATION_STARTED",
        "workflow_id": workflow_id,
        "thread_id": thread_id,
        "run_id": run_id,
        "timestamp": datetime.now().isoformat()
    }) + "\n"
    
    try:
        # Pre-validate inputs with enhanced error handling
        yield json.dumps({
            "type": "VALIDATION_STARTED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Validating workflow and modification request..."
        }) + "\n"
        
        # Validate workflow JSON
        workflow_validation_errors = error_handler.validate_workflow_input(request.existing_workflow_json)
        if workflow_validation_errors:
            validation_error_detail = error_handler.create_validation_error_summary(workflow_validation_errors)
            
            yield json.dumps({
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
            }) + "\n"
            return
        
        # Validate modification description
        description_validation_errors = error_handler.validate_modification_description(request.modification_description)
        if description_validation_errors:
            description_error_detail = error_handler.create_validation_error_summary(description_validation_errors)
            
            yield json.dumps({
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
            }) + "\n"
            return
        
        # Validation passed
        yield json.dumps({
            "type": "VALIDATION_COMPLETED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Input validation completed successfully"
        }) + "\n"
        
        # Processing started
        yield json.dumps({
            "type": "PROCESSING_STARTED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Processing workflow modification..."
        }) + "\n"
        
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
        yield json.dumps({
            "type": "WORKFLOW_MODIFIED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "data": response.dict()
        }) + "\n"
        
        # Finish event
        yield json.dumps({
            "type": "MODIFICATION_FINISHED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }) + "\n"
        
    except Exception as e:
        # Enhanced error handling
        error_detail = error_handler.categorize_error(e, {
            'workflow_id': workflow_id,
            'operation_type': 'api_modify_workflow'
        })
        
        # Error event with detailed information
        yield json.dumps({
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
        }) + "\n"

async def iterate_workflow_events(request: WorkflowIterationRequest):
    """Generate events for workflow iteration process with enhanced error handling."""
    workflow_id = request.workflow_id
    thread_id = request.thread_id or str(uuid.uuid4())
    run_id = request.run_id or str(uuid.uuid4())
    
    # Start event
    yield json.dumps({
        "type": "ITERATION_STARTED",
        "workflow_id": workflow_id,
        "thread_id": thread_id,
        "run_id": run_id,
        "timestamp": datetime.now().isoformat()
    }) + "\n"
    
    try:
        # Pre-validate inputs with enhanced error handling
        yield json.dumps({
            "type": "VALIDATION_STARTED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Validating workflow and iteration request..."
        }) + "\n"
        
        # Validate workflow ID
        if not workflow_id or not workflow_id.strip():
            error_detail = ErrorDetail(
                category="input_validation",
                severity="error",
                title="Missing Workflow ID",
                message="Workflow ID is required for iteration tracking",
                user_guidance="Please provide a valid workflow ID to track iteration history",
                fix_suggestions=[
                    "Provide a unique workflow ID string",
                    "Use a descriptive name like 'my-email-workflow' or 'customer-onboarding'"
                ]
            )
            
            yield json.dumps({
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
            }) + "\n"
            return
        
        # Validate workflow JSON
        workflow_validation_errors = error_handler.validate_workflow_input(request.existing_workflow_json)
        if workflow_validation_errors:
            validation_error_detail = error_handler.create_validation_error_summary(workflow_validation_errors)
            
            yield json.dumps({
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
            }) + "\n"
            return
        
        # Validate feedback from testing
        if not request.feedback_from_testing or not request.feedback_from_testing.strip():
            error_detail = ErrorDetail(
                category="input_validation",
                severity="error",
                title="Missing Testing Feedback",
                message="Testing feedback is required for workflow iteration",
                user_guidance="Please provide feedback about how the workflow performed during testing",
                fix_suggestions=[
                    "Describe what worked well: 'The email sending works correctly'",
                    "Describe what needs improvement: 'The error handling needs to be more robust'",
                    "Provide specific issues: 'The workflow fails when the API is unavailable'"
                ]
            )
            
            yield json.dumps({
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
            }) + "\n"
            return
        
        # Validation passed
        yield json.dumps({
            "type": "VALIDATION_COMPLETED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Input validation completed successfully"
        }) + "\n"
        
        # Processing started
        yield json.dumps({
            "type": "PROCESSING_STARTED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "message": "Processing workflow iteration..."
        }) + "\n"
        
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
        yield json.dumps({
            "type": "WORKFLOW_ITERATED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "data": response.dict()
        }) + "\n"
        
        # Finish event
        yield json.dumps({
            "type": "ITERATION_FINISHED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }) + "\n"
        
    except Exception as e:
        # Enhanced error handling
        error_detail = error_handler.categorize_error(e, {
            'workflow_id': workflow_id,
            'operation_type': 'api_iterate_workflow'
        })
        
        # Error event with detailed information
        yield json.dumps({
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
        }) + "\n"

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
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()} 