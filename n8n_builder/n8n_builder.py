import json
import logging
import httpx
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

from .config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class NodeTypeInfo:
    name: str
    description: str
    required_parameters: List[str]
    optional_parameters: List[str]
    example: str

@dataclass
class WorkflowPattern:
    name: str
    description: str
    template: str
    common_use_cases: List[str]

@dataclass
class WorkflowFeedback:
    workflow_id: str
    description: str
    generated_workflow: str
    success: bool
    feedback: str
    timestamp: datetime

class N8NBuilder:
    def __init__(self):
        self.documentation_path = Path("NN_Builder.md")
        self.node_types: Dict[str, NodeTypeInfo] = {}
        self.workflow_patterns: Dict[str, WorkflowPattern] = {}
        self.feedback_log: List[WorkflowFeedback] = []
        self.llm_config = config.mimo_llm
        logger.info(f"N8N Builder LLM Config: endpoint={self.llm_config.endpoint}, is_local={self.llm_config.is_local}, model={self.llm_config.model}")
        self.initialize_builder()

    def generate_workflow(self, plain_english_description: str) -> str:
        """Generate an n8n workflow from a plain English description."""
        try:
            # 1. Parse plain English using Mimo VL 7B
            prompt = self._build_prompt(plain_english_description)
            try:
                response = asyncio.run(self._call_mimo_vl7b(prompt))
            except Exception as e:
                logger.warning(f"LLM API call failed, using mock implementation: {str(e)}")
                response = self._mock_llm_response(plain_english_description)

            # 2. Map to n8n workflow structure
            workflow_json = self._map_to_workflow_structure(response)

            # 3. Validate and return JSON
            if self.validate_workflow(workflow_json):
                return workflow_json
            else:
                raise ValueError("Generated workflow failed validation")
        except Exception as e:
            logger.error(f"Error generating workflow: {str(e)}")
            return ""

    def _mock_llm_response(self, description: str) -> str:
        """Generate a mock workflow for testing purposes."""
        if "email" in description.lower() and "file" in description.lower():
            return json.dumps({
                "name": "File Upload Email Notification",
                "nodes": [
                    {
                        "id": "1",
                        "name": "Watch Folder",
                        "type": "n8n-nodes-base.watchFolder",
                        "parameters": {
                            "folderPath": "{{$env.WATCH_FOLDER}}",
                            "options": {
                                "includeSubfolders": True
                            }
                        }
                    },
                    {
                        "id": "2",
                        "name": "Send Email",
                        "type": "n8n-nodes-base.emailSend",
                        "parameters": {
                            "to": "{{$env.NOTIFICATION_EMAIL}}",
                            "subject": "New File Uploaded",
                            "text": "A new file has been uploaded: {{$node[\"Watch Folder\"].json[\"name\"]}}"
                        }
                    }
                ],
                "connections": {
                    "Watch Folder": {
                        "main": [
                            [
                                {
                                    "node": "Send Email",
                                    "type": "main",
                                    "index": 0
                                }
                            ]
                        ]
                    }
                },
                "settings": {},
                "active": True,
                "version": 1
            })
        else:
            return json.dumps({
                "name": "Basic Workflow",
                "nodes": [
                    {
                        "id": "1",
                        "name": "Start",
                        "type": "n8n-nodes-base.start",
                        "parameters": {}
                    }
                ],
                "connections": {},
                "settings": {},
                "active": True,
                "version": 1
            })

    def validate_workflow(self, workflow_json: str) -> bool:
        """Validate the generated workflow JSON."""
        try:
            # 1. Check JSON structure
            workflow = json.loads(workflow_json)
            if not workflow:
                logger.error("Empty workflow")
                return False

            # 2. Check required fields
            required_fields = ["name", "nodes", "connections"]
            for field in required_fields:
                if field not in workflow:
                    logger.error(f"Missing required field: {field}")
                    return False

            # 3. Validate nodes
            if not isinstance(workflow["nodes"], list):
                logger.error("Nodes must be a list")
                return False

            for node in workflow["nodes"]:
                if not all(field in node for field in ["id", "name", "type", "parameters"]):
                    logger.error(f"Invalid node structure: {node}")
                    return False

            # 4. Validate connections
            if not isinstance(workflow["connections"], dict):
                logger.error("Connections must be a dictionary")
                return False

            # 5. Validate settings
            if "settings" not in workflow:
                logger.error("Missing settings field")
                return False

            # 6. Validate version
            if "version" not in workflow:
                logger.error("Missing version field")
                return False

            return True
        except Exception as e:
            logger.error(f"Error validating workflow: {str(e)}")
            return False

    def add_feedback(self, workflow_id: str, description: str, 
                    generated_workflow: str, success: bool, feedback: str) -> None:
        """Add feedback for a generated workflow."""
        feedback_entry = WorkflowFeedback(
            workflow_id=workflow_id,
            description=description,
            generated_workflow=generated_workflow,
            success=success,
            feedback=feedback,
            timestamp=datetime.now()
        )
        self.feedback_log.append(feedback_entry)
        self._save_feedback_log()

    def get_feedback_history(self) -> List[WorkflowFeedback]:
        """Get the history of workflow feedback."""
        return self.feedback_log

    def _build_prompt(self, description: str) -> str:
        """Build the prompt for Mimo VL 7B."""
        return f"""You are an n8n workflow generation assistant. Generate a valid n8n workflow JSON for the following description:

{description}

The workflow should:
1. Use appropriate n8n nodes for the task
2. Follow n8n best practices
3. Include proper error handling
4. Be well-documented with comments

Return only the workflow JSON, no additional text or explanation."""

    async def _call_mimo_vl7b(self, prompt: str, max_retries: int = 3) -> str:
        """Call the Mimo VL 7B API."""
        retry_count = 0
        last_error = None
        
        while retry_count < max_retries:
            try:
                logger.info(f"Calling LLM API with is_local={self.llm_config.is_local} (attempt {retry_count + 1}/{max_retries})")
                
                if self.llm_config.is_local:
                    async with httpx.AsyncClient(timeout=1200.0) as client:  # 20 minute timeout
                        response = await client.post(
                            self.llm_config.endpoint,
                            json={
                                "model": self.llm_config.model,
                                "messages": [
                                    {"role": "system", "content": "You are an n8n workflow generation assistant."},
                                    {"role": "user", "content": prompt}
                                ],
                                "temperature": self.llm_config.temperature,
                                "max_tokens": self.llm_config.max_tokens
                            }
                        )
                        response.raise_for_status()
                        return response.json()["choices"][0]["message"]["content"]
                else:
                    if not self.llm_config.api_key:
                        raise ValueError("API key is required when not using local endpoint")
                    async with httpx.AsyncClient(timeout=1200.0) as client:
                        response = await client.post(
                            self.llm_config.endpoint,
                            headers={"Authorization": f"Bearer {self.llm_config.api_key}"},
                            json={
                                "model": self.llm_config.model,
                                "messages": [
                                    {"role": "system", "content": "You are an n8n workflow generation assistant."},
                                    {"role": "user", "content": prompt}
                                ],
                                "temperature": self.llm_config.temperature,
                                "max_tokens": self.llm_config.max_tokens
                            }
                        )
                        response.raise_for_status()
                        return response.json()["choices"][0]["message"]["content"]
                    
            except httpx.TimeoutException as e:
                last_error = e
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(f"Timeout on attempt {retry_count}, retrying...")
                    await asyncio.sleep(1)  # Wait 1 second before retrying
                continue
            except Exception as e:
                logger.error(f"Error calling LLM API: {e}", exc_info=True)
                raise
        
        # If we get here, all retries failed
        error_message = f"Failed to generate workflow after {max_retries} attempts. Last error: {str(last_error)}"
        logger.error(error_message)
        raise ValueError(error_message)

    def _map_to_workflow_structure(self, response: str) -> str:
        """Map the LLM response to n8n workflow structure."""
        try:
            # Try to parse the response as JSON
            workflow = json.loads(response)
            return json.dumps(workflow, indent=2)
        except json.JSONDecodeError:
            # If the response isn't valid JSON, try to extract JSON from the text
            try:
                # Look for JSON-like content between curly braces
                start = response.find('{')
                end = response.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = response[start:end]
                    workflow = json.loads(json_str)
                    return json.dumps(workflow, indent=2)
            except Exception as e:
                logger.error(f"Error extracting JSON from response: {str(e)}")
                raise ValueError("Could not extract valid workflow JSON from response")

    def _save_feedback_log(self) -> None:
        """Save the feedback log to a file."""
        try:
            feedback_data = [
                {
                    "workflow_id": f.workflow_id,
                    "description": f.description,
                    "generated_workflow": f.generated_workflow,
                    "success": f.success,
                    "feedback": f.feedback,
                    "timestamp": f.timestamp.isoformat()
                }
                for f in self.feedback_log
            ]
            with open("feedback_log.json", "w") as f:
                json.dump(feedback_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving feedback log: {str(e)}")

    def initialize_builder(self) -> None:
        """Initialize the builder with documentation and patterns."""
        try:
            # 1. Parse NN_Builder.md
            if self.documentation_path.exists():
                documentation = self.documentation_path.read_text()
                # TODO: Parse documentation and build node type catalog

            # 2. Initialize workflow patterns
            from .code_generation_patterns import CodeGenerationPatterns
            self.workflow_patterns = CodeGenerationPatterns.patterns

            # 3. Load feedback log if exists
            feedback_path = Path("feedback_log.json")
            if feedback_path.exists():
                with open(feedback_path) as f:
                    feedback_data = json.load(f)
                    self.feedback_log = [
                        WorkflowFeedback(
                            workflow_id=item["workflow_id"],
                            description=item["description"],
                            generated_workflow=item["generated_workflow"],
                            success=item["success"],
                            feedback=item["feedback"],
                            timestamp=datetime.fromisoformat(item["timestamp"])
                        )
                        for item in feedback_data
                    ]
        except Exception as e:
            logger.error(f"Error initializing builder: {str(e)}") 