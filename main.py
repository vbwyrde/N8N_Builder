from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import json
import logging
import asyncio
from llm_integration import LLMClient, LLMConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize LLM client
llm_client = None

@app.on_event("startup")
async def startup_event():
    global llm_client
    llm_client = LLMClient()

@app.on_event("shutdown")
async def shutdown_event():
    global llm_client
    if llm_client:
        await llm_client.close()

class WorkflowRequest(BaseModel):
    description: str

@app.post("/generate-workflow")
async def generate_workflow(request: WorkflowRequest) -> Dict[str, Any]:
    """Generate an N8N workflow from a description."""
    try:
        logger.info(f"Received workflow generation request: {request.description}")
        if not llm_client:
            raise HTTPException(status_code=500, detail="LLM client not initialized")
        
        workflow = await llm_client.generate_workflow(request.description)
        return workflow
    except Exception as e:
        logger.error(f"Error generating workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Serve the main page."""
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    # Use port 8080 instead of 8002
    uvicorn.run(app, host="127.0.0.1", port=8080) 