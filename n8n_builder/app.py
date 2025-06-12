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

# Get the static directory path - point to root level static directory
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
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
    yield "data: " + json.dumps({
        "type": "RUN_STARTED",
        "workflow_id": workflow_id,
        "thread_id": thread_id,
        "run_id": run_id,
        "timestamp": datetime.now().isoformat()
    }) + "\n\n"
    
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
        yield "data: " + json.dumps({
            "type": "WORKFLOW_GENERATED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "data": response.dict()
        }) + "\n\n"
        
        # Finish event
        yield "data: " + json.dumps({
            "type": "RUN_FINISHED",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }) + "\n\n"
        
    except Exception as e:
        # Error event
        yield "data: " + json.dumps({
            "type": "RUN_ERROR",
            "workflow_id": workflow_id,
            "thread_id": thread_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }) + "\n\n"

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
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

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
        logger.error(f"Failed to list projects: {str(e)}")
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
        logger.error(f"Failed to get project stats: {str(e)}")
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
        logger.error(f"Failed to create project '{name}': {str(e)}")
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
        logger.error(f"Failed to get project '{name}': {str(e)}")
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
        logger.error(f"Failed to list workflows for project '{name}': {str(e)}")
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
        logger.error(f"Failed to get workflow '{filename}' from project '{name}': {str(e)}")
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
            create_backup=request.create_backup
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
        logger.error(f"Failed to save workflow '{filename}' to project '{name}': {str(e)}")
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
        logger.error(f"Failed to delete project '{name}': {str(e)}")
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
        logger.error(f"Failed to list versions for workflow '{filename}' in project '{name}': {str(e)}")
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
        logger.error(f"Failed to get version info for '{version_filename}': {str(e)}")
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
        logger.error(f"Failed to get version content for '{version_filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get version content: {str(e)}")

@app.post("/projects/{name}/workflows/{filename}/versions/{version_filename}/restore")
async def restore_workflow_version(name: str, filename: str, version_filename: str, request: VersionRestoreRequest):
    """Restore a workflow from a specific version."""
    try:
        success = filesystem_utils.restore_workflow_version(
            name, 
            filename, 
            version_filename,
            create_backup=request.create_backup
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
        logger.error(f"Failed to restore workflow from version '{version_filename}': {str(e)}")
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
        logger.error(f"Failed to compare workflow versions: {str(e)}")
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
        logger.error(f"Failed to delete version '{version_filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete workflow version: {str(e)}")

@app.post("/projects/{name}/workflows/{filename}/cleanup-versions")
async def cleanup_workflow_versions(name: str, filename: str, request: VersionCleanupRequest):
    """Clean up old versions of a workflow, keeping only the specified number."""
    try:
        deleted_count = filesystem_utils.cleanup_old_versions(name, filename, request.keep_versions)
        
        return {
            "message": f"Cleaned up old versions for workflow '{filename}'",
            "project_name": name,
            "workflow_filename": filename,
            "versions_deleted": deleted_count,
            "versions_kept": request.keep_versions
        }
        
    except Exception as e:
        logger.error(f"Failed to cleanup versions for workflow '{filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to cleanup workflow versions: {str(e)}") 