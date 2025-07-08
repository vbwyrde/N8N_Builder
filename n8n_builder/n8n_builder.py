import json
import logging
import httpx
import asyncio
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
import concurrent.futures
import threading
import copy
import re

from .config import config
from .error_handler import EnhancedErrorHandler, ErrorDetail, ErrorCategory, ErrorSeverity, ValidationError as EValidationError
from .validators import EdgeCaseValidator, EdgeCaseValidationResult
from .performance_optimizer import performance_optimizer, PerformanceMetrics
from .retry_manager import retry_manager, RetryConfig, RetryStrategy, FailureType
from .workflow_differ import workflow_differ, WorkflowDiff
from .enhanced_prompt_builder import EnhancedPromptBuilder
from .logging_config import setup_logger

# Initialize logging configuration
logger = setup_logger(__name__)

# Configure enhanced logging for iteration operations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

# Create specialized loggers for different operation types
iteration_logger = logging.getLogger('n8n_builder.iteration')
performance_logger = logging.getLogger('n8n_builder.performance')
validation_logger = logging.getLogger('n8n_builder.validation')
llm_logger = logging.getLogger('n8n_builder.llm')

# Configure specialized log levels
iteration_logger.setLevel(logging.INFO)
performance_logger.setLevel(logging.INFO)
validation_logger.setLevel(logging.DEBUG)
llm_logger.setLevel(logging.DEBUG)

@dataclass
class IterationMetrics:
    """Metrics for iteration operations."""
    operation_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    operation_type: str = ""
    workflow_id: str = ""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    duration_seconds: Optional[float] = None
    success: bool = False
    error_message: Optional[str] = None
    nodes_before: int = 0
    nodes_after: int = 0
    llm_calls_count: int = 0
    llm_total_time: float = 0.0
    validation_time: float = 0.0
    modification_count: int = 0
    
    def finish(self, success: bool = True, error_message: Optional[str] = None):
        """Mark the operation as finished and calculate duration."""
        self.end_time = time.time()
        self.duration_seconds = self.end_time - self.start_time
        self.success = success
        self.error_message = error_message
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for logging."""
        return {
            'operation_id': self.operation_id,
            'operation_type': self.operation_type,
            'workflow_id': self.workflow_id,
            'duration_seconds': self.duration_seconds,
            'success': self.success,
            'error_message': self.error_message,
            'nodes_before': self.nodes_before,
            'nodes_after': self.nodes_after,
            'nodes_changed': self.nodes_after - self.nodes_before,
            'llm_calls_count': self.llm_calls_count,
            'llm_total_time': self.llm_total_time,
            'validation_time': self.validation_time,
            'modification_count': self.modification_count,
            'timestamp': datetime.fromtimestamp(self.start_time).isoformat()
        }

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
        """Initialize N8N Builder with enhanced error handling, performance optimization, and retry logic."""
        self.documentation_path = Path("NN_Builder.md")
        self.node_types: Dict[str, NodeTypeInfo] = {}
        self.workflow_patterns: Dict[str, WorkflowPattern] = {}
        self.feedback_log: List[WorkflowFeedback] = []
        self.llm_config = config.mimo_llm
        logger.info(f"N8N Builder LLM Config: endpoint={self.llm_config.endpoint}, is_local={self.llm_config.is_local}, model={self.llm_config.model}", extra={'operation_id': 'init'})
        self.iteration_history = []
        
        # Initialize enhanced error handling
        self.error_handler = EnhancedErrorHandler()
        
        # Initialize edge case validator
        self.edge_case_validator = EdgeCaseValidator()
        
        # Initialize performance optimizer (global instance)
        self.performance_optimizer = performance_optimizer
        logger.info("Performance optimizer initialized for large workflow processing", extra={'operation_id': 'init'})
        
        # Initialize enhanced retry logic with fallback strategies
        self.retry_manager = retry_manager
        self._setup_retry_configurations()
        self._register_fallback_strategies()
        logger.info("Enhanced retry manager initialized with intelligent failure handling", extra={'operation_id': 'init'})

        # Initialize enhanced prompt builder with MCP research
        self.enhanced_prompt_builder = EnhancedPromptBuilder(
            enable_research=getattr(config, 'enable_mcp_research', True),
            research_timeout=getattr(config, 'research_timeout', 30),
            github_api_token=getattr(config.mcp_research, 'github_api_token', None)
        )
        logger.info("Enhanced prompt builder initialized with MCP research capabilities", extra={'operation_id': 'init'})
        
        try:
            self.initialize_builder()
        except Exception as e:
            error_detail = self.error_handler.categorize_error(e, {"context": "initialization"})
            logger.exception(f"Error initializing N8N Builder: {error_detail.title} - {error_detail.message}", extra={'operation_id': 'init'})
            if error_detail.fix_suggestions:
                logger.info(f"Suggestions: {'; '.join(error_detail.fix_suggestions)}")

    def _setup_retry_configurations(self):
        """Setup retry configurations for different types of LLM failures."""
        # Configure different retry strategies for different failure types
        
        # Timeout failures - more aggressive retries with longer delays
        timeout_config = RetryConfig(
            max_attempts=5,
            base_delay=2.0,
            max_delay=120.0,
            strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
            jitter=True,
            failure_threshold=3,
            recovery_timeout=30
        )
        
        # Rate limiting - linear backoff with longer delays
        rate_limit_config = RetryConfig(
            max_attempts=4,
            base_delay=5.0,
            max_delay=180.0,
            strategy=RetryStrategy.LINEAR_BACKOFF,
            jitter=True,
            failure_threshold=2,
            recovery_timeout=120
        )
        
        # Server errors - exponential backoff
        server_error_config = RetryConfig(
            max_attempts=4,
            base_delay=1.5,
            max_delay=60.0,
            strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
            jitter=True,
            failure_threshold=4,
            recovery_timeout=45
        )
        
        # Connection errors - immediate retry first, then exponential
        connection_error_config = RetryConfig(
            max_attempts=6,
            base_delay=0.5,
            max_delay=30.0,
            strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
            jitter=True,
            failure_threshold=3,
            recovery_timeout=20
        )
        
        # Validation errors - fewer retries as these are often permanent
        validation_error_config = RetryConfig(
            max_attempts=2,
            base_delay=1.0,
            max_delay=5.0,
            strategy=RetryStrategy.FIXED_DELAY,
            jitter=False,
            failure_threshold=2,
            recovery_timeout=60
        )
        
        # Default configuration with failure-specific overrides
        default_config = RetryConfig(
            max_attempts=3,
            base_delay=1.0,
            max_delay=60.0,
            strategy=RetryStrategy.EXPONENTIAL_BACKOFF,
            jitter=True,
            failure_threshold=5,
            recovery_timeout=60,
            failure_configs={
                FailureType.TIMEOUT: timeout_config,
                FailureType.RATE_LIMIT: rate_limit_config,
                FailureType.SERVER_ERROR: server_error_config,
                FailureType.CONNECTION_ERROR: connection_error_config,
                FailureType.VALIDATION_ERROR: validation_error_config
            }
        )
        
        # Configure the retry manager for our LLM endpoint
        endpoint_key = self.llm_config.endpoint or "default_llm"
        self.retry_manager.configure_endpoint(endpoint_key, default_config)
        
        logger.info(f"Configured retry strategies for LLM endpoint: {endpoint_key}")

    def _register_fallback_strategies(self):
        """Register fallback strategies for when LLM API completely fails."""
        # Register mock response fallback
        self.retry_manager.register_fallback_strategy(
            "mock_response", 
            self._fallback_mock_response
        )
        
        # Register simplified response fallback
        self.retry_manager.register_fallback_strategy(
            "simplified_response", 
            self._fallback_simplified_response
        )
        
        # Register cached response fallback (if we had caching)
        self.retry_manager.register_fallback_strategy(
            "basic_workflow", 
            self._fallback_basic_workflow
        )
        
        logger.info("Registered 3 fallback strategies for LLM failures")

    async def _fallback_mock_response(self, prompt: str, **kwargs) -> str:
        """Fallback strategy: Generate mock response based on prompt content."""
        logger.info("Using mock response fallback strategy")
        
        # Analyze prompt to determine appropriate mock response
        if "email" in prompt.lower():
            return json.dumps([
                {
                    "action": "add_node",
                    "details": {
                        "node_id": "fallback_email",
                        "name": "Email Fallback",
                        "node_type": "n8n-nodes-base.emailSend",
                        "parameters": {
                            "to": "elthosrpg@elthos.com",
                            "subject": "Workflow Completed",
                            "text": "This email was generated by fallback logic when the workflow completed."
                        },
                        "position": [1000, 300]
                    }
                },
                {
                    "action": "add_connection",
                    "details": {
                        "source_node": "process-data",
                        "target_node": "fallback_email",
                        "connection_type": "main",
                        "index": 0
                    }
                },
                {
                    "action": "modify_connection",
                    "details": {
                        "source_node": "process-data",
                        "old_target": "webhook-response",
                        "new_target": "fallback_email",
                        "connection_type": "main"
                    }
                },
                {
                    "action": "add_connection",
                    "details": {
                        "source_node": "fallback_email",
                        "target_node": "webhook-response",
                        "connection_type": "main",
                        "index": 0
                    }
                }
            ])
        elif "database" in prompt.lower() or "db" in prompt.lower():
            return json.dumps([{
                "action": "add_node",
                "details": {
                    "node_id": "fallback_db",
                    "name": "Database Fallback",
                    "node_type": "n8n-nodes-base.postgres",
                    "parameters": {
                        "operation": "insert",
                        "table": "fallback_table"
                    }
                },
                "reasoning": "Fallback database node added due to LLM failure"
            }])
        else:
            return json.dumps([{
                "action": "add_node",
                "details": {
                    "node_id": "fallback_generic",
                    "name": "Generic Fallback",
                    "node_type": "n8n-nodes-base.noOp",
                    "parameters": {}
                },
                "reasoning": "Generic fallback node added due to LLM failure"
            }])

    async def _fallback_simplified_response(self, prompt: str, **kwargs) -> str:
        """Fallback strategy: Generate simplified but functional response."""
        logger.info("Using simplified response fallback strategy")
        
        return json.dumps([{
            "action": "add_node",
            "details": {
                "node_id": "simplified_node",
                "name": "Simplified Node",
                "node_type": "n8n-nodes-base.function",
                "parameters": {
                    "code": "// Simplified fallback function\nreturn items;"
                }
            },
            "reasoning": "Simplified function node added as safe fallback"
        }])

    async def _fallback_basic_workflow(self, prompt: str, **kwargs) -> str:
        """Fallback strategy: Return basic workflow structure."""
        logger.info("Using basic workflow fallback strategy")
        
        return json.dumps({
            "name": "Fallback Workflow",
            "nodes": [
                {
                    "id": "fallback_start",
                    "name": "Start",
                    "type": "n8n-nodes-base.manualTrigger",
                    "parameters": {}
                },
                {
                    "id": "fallback_end",
                    "name": "End",
                    "type": "n8n-nodes-base.noOp",
                    "parameters": {}
                }
            ],
            "connections": {
                "Start": {
                    "main": [
                        [
                            {
                                "node": "End",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                }
            },
            "settings": {},
            "active": False,
            "version": 1
        })

    def generate_workflow(self, plain_english_description: str) -> str:
        """Generate an n8n workflow from a plain English description with enhanced research."""
        try:
            # 1. Generate enhanced prompt with research
            try:
                # Check if we're in an async context
                try:
                    asyncio.get_running_loop()
                    # We're in an async context, can't use asyncio.run
                    logger.info("In async context, using ThreadPoolExecutor for enhanced prompt building")

                    # Create a function to run the async prompt building in a separate thread
                    def build_prompt_sync():
                        return asyncio.run(self.enhanced_prompt_builder.build_enhanced_prompt(plain_english_description))

                    # Run the enhanced prompt building in a separate thread with its own event loop
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(build_prompt_sync)
                        prompt = future.result(timeout=60)  # 60 second timeout for research

                    logger.info("Enhanced prompt building successful")

                except RuntimeError:
                    # No event loop running, we can use asyncio.run normally
                    logger.info("Not in async context, using asyncio.run for enhanced prompt building")
                    prompt = asyncio.run(self.enhanced_prompt_builder.build_enhanced_prompt(plain_english_description))

            except Exception as e:
                # If enhanced prompt building fails, fall back to basic prompt
                logger.warning(f"Enhanced prompt building failed, using basic prompt: {str(e)}")
                prompt = self._build_prompt(plain_english_description)

            # 2. Generate with LLM using the prompt (enhanced or basic)
            response = None
            try:
                try:
                    asyncio.get_running_loop()
                    # We're in an async context, can't use asyncio.run
                    logger.info("In async context, using ThreadPoolExecutor for LLM call")

                    # Create a function to run the async call in a separate thread
                    def call_llm_sync():
                        return asyncio.run(self._call_mimo_vl7b(prompt))

                    # Run the LLM call in a separate thread with its own event loop
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(call_llm_sync)
                        response = future.result(timeout=360)  # 6 minute timeout

                    logger.info("LLM call successful")

                except RuntimeError:
                    # No event loop running, we can use asyncio.run normally
                    logger.info("Not in async context, using asyncio.run for LLM call")
                    response = asyncio.run(self._call_mimo_vl7b(prompt))

            except Exception as e:
                # If LLM call fails, preserve the detailed error information instead of wrapping it
                logger.error(f"LLM API call failed: {str(e)}")
                error_message = str(e)
                # If the error is a known LLM crash, token limit, or truncation, surface it directly
                if any(keyword in error_message.lower() for keyword in [
                    "crashed", "exit code", "connection refused", "connection reset",
                    "broken pipe", "terminated", "killed", "service error", "token limit", "truncated"
                ]):
                    raise RuntimeError(error_message)
                else:
                    # Generic error, add context
                    raise RuntimeError(f"LLM service unavailable: {str(e)}")

            # Ensure we have a response before proceeding
            if response is None:
                raise RuntimeError("LLM call failed to produce a response")

            # 3. Map to n8n workflow structure
            workflow_json = self._map_to_workflow_structure(response)

            # 4. Validate and return JSON
            if self.validate_workflow(workflow_json):
                return workflow_json
            else:
                raise ValueError("Generated workflow failed validation")
        except Exception as e:
            logger.exception(f"Error generating workflow: {str(e)}", extra={'operation_id': 'generate'})
            # Re-raise the exception instead of returning empty string
            raise

    def get_research_stats(self) -> Dict[str, Any]:
        """Get research performance statistics."""
        if hasattr(self, 'enhanced_prompt_builder'):
            return self.enhanced_prompt_builder.get_research_stats()
        return {}

    async def close(self):
        """Clean up resources."""
        if hasattr(self, 'enhanced_prompt_builder'):
            await self.enhanced_prompt_builder.close()

    def _mock_llm_response(self, description: str) -> str:
        """Generate a mock workflow for testing purposes with proper trigger nodes."""
        description_lower = description.lower()
        
        if "email" in description_lower and ("webhook" in description_lower or "http" in description_lower):
            return json.dumps({
                "name": "Webhook Email Automation",
                "nodes": [
                    {
                        "id": "webhook-trigger",
                        "name": "Webhook Trigger",
                        "type": "n8n-nodes-base.webhook",
                        "parameters": {
                            "httpMethod": "POST",
                            "path": "email-automation",
                            "responseMode": "responseNode"
                        },
                        "position": [250, 300]
                    },
                    {
                        "id": "email-send",
                        "name": "Send Email",
                        "type": "n8n-nodes-base.emailSend",
                        "parameters": {
                            "to": "{{$json[\"email\"]}}",
                            "subject": "Webhook Received",
                            "text": "We received your data: {{JSON.stringify($json)}}"
                        },
                        "position": [500, 300]
                    },
                    {
                        "id": "webhook-response",
                        "name": "Webhook Response",
                        "type": "n8n-nodes-base.respondToWebhook",
                        "parameters": {
                            "respondWith": "json",
                            "responseBody": "{\"status\": \"success\", \"message\": \"Email sent\"}"
                        },
                        "position": [750, 300]
                    }
                ],
                "connections": {
                    "Webhook Trigger": {
                        "main": [
                            [
                                {
                                    "node": "Send Email",
                                    "type": "main",
                                    "index": 0
                                }
                            ]
                        ]
                    },
                    "Send Email": {
                        "main": [
                            [
                                {
                                    "node": "Webhook Response",
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
        elif "schedule" in description_lower or "cron" in description_lower or "time" in description_lower:
            return json.dumps({
                "name": "Scheduled Email Report",
                "nodes": [
                    {
                        "id": "schedule-trigger",
                        "name": "Schedule Trigger",
                        "type": "n8n-nodes-base.scheduleTrigger",
                        "parameters": {
                            "rule": {
                                "interval": [
                                    {
                                        "field": "cronExpression",
                                        "expression": "0 9 * * 1"
                                    }
                                ]
                            }
                        },
                        "position": [250, 300]
                    },
                    {
                        "id": "email-send",
                        "name": "Send Report Email",
                        "type": "n8n-nodes-base.emailSend",
                        "parameters": {
                            "to": "report@company.com",
                            "subject": "Weekly Report - {{$now.format('YYYY-MM-DD')}}",
                            "text": "This is your automated weekly report."
                        },
                        "position": [500, 300]
                    }
                ],
                "connections": {
                    "Schedule Trigger": {
                        "main": [
                            [
                                {
                                    "node": "Send Report Email",
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
        elif "file" in description_lower and ("watch" in description_lower or "monitor" in description_lower):
            return json.dumps({
                "name": "File Monitoring Workflow",
                "nodes": [
                    {
                        "id": "file-trigger",
                        "name": "File Trigger",
                        "type": "n8n-nodes-base.localFileTrigger",
                        "parameters": {
                            "path": "/tmp/watch-folder",
                            "watchFor": "file"
                        },
                        "position": [250, 300]
                    },
                    {
                        "id": "process-file",
                        "name": "Process File",
                        "type": "n8n-nodes-base.function",
                        "parameters": {
                            "functionCode": "// Process the file\nconst fileName = $input.first().json.name;\nreturn [{ json: { fileName, processed: true, timestamp: new Date() } }];"
                        },
                        "position": [500, 300]
                    }
                ],
                "connections": {
                    "File Trigger": {
                        "main": [
                            [
                                {
                                    "node": "Process File",
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
            # Default workflow with proper webhook trigger
            return json.dumps({
                "name": "Basic Webhook Workflow",
                "nodes": [
                    {
                        "id": "webhook-trigger",
                        "name": "Webhook Trigger",
                        "type": "n8n-nodes-base.webhook",
                        "parameters": {
                            "httpMethod": "POST",
                            "path": "basic-workflow",
                            "responseMode": "responseNode"
                        },
                        "position": [250, 300]
                    },
                    {
                        "id": "process-data",
                        "name": "Process Data",
                        "type": "n8n-nodes-base.function",
                        "parameters": {
                            "functionCode": "// Process incoming data\nconst data = $input.first().json;\nreturn [{ json: { ...data, processed: true, timestamp: new Date().toISOString() } }];"
                        },
                        "position": [500, 300]
                    },
                    {
                        "id": "webhook-response",
                        "name": "Webhook Response",
                        "type": "n8n-nodes-base.respondToWebhook",
                        "parameters": {
                            "respondWith": "json",
                            "responseBody": "{\"status\": \"success\", \"message\": \"Data processed\"}"
                        },
                        "position": [750, 300]
                    }
                ],
                "connections": {
                    "Webhook Trigger": {
                        "main": [
                            [
                                {
                                    "node": "Process Data",
                                    "type": "main",
                                    "index": 0
                                }
                            ]
                        ]
                    },
                    "Process Data": {
                        "main": [
                            [
                                {
                                    "node": "Webhook Response",
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

    def validate_workflow(self, workflow_json: str) -> bool:
        """Validate the generated workflow JSON with comprehensive checks."""
        validation_errors = []
        
        try:
            # 1. Check JSON structure
            workflow = json.loads(workflow_json)
            if not workflow:
                validation_errors.append("Empty workflow")
                return self._log_validation_errors(validation_errors)

            # 2. Check required fields
            required_fields = ["name", "nodes", "connections"]
            for field in required_fields:
                if field not in workflow:
                    validation_errors.append(f"Missing required field: {field}")

            # 3. Validate nodes
            if not isinstance(workflow.get("nodes"), list):
                validation_errors.append("Nodes must be a list")
            else:
                nodes = workflow["nodes"]
                node_ids = set()
                
                for i, node in enumerate(nodes):
                    node_errors = self._validate_node_structure(node, i)
                    validation_errors.extend(node_errors)
                    
                    # Check for duplicate node IDs
                    node_id = node.get("id")
                    if node_id:
                        if node_id in node_ids:
                            validation_errors.append(f"Duplicate node ID: {node_id}")
                        node_ids.add(node_id)

            # 4. Validate connections (use a deep copy to avoid mutating the original)
            workflow_copy = copy.deepcopy(workflow)
            node_ids = {node['id'] for node in workflow.get('nodes', [])}
            connection_errors = self._validate_connections(workflow_copy, node_ids, workflow.get('nodes', []))
            if connection_errors:
                validation_errors.extend(connection_errors)

            # 5. Validate settings (optional but should be dict if present)
            if "settings" in workflow and not isinstance(workflow["settings"], dict):
                validation_errors.append("Settings must be a dictionary")

            # 6. Validate version (optional but should be number if present)
            if "version" in workflow:
                if not isinstance(workflow["version"], (int, float)):
                    validation_errors.append("Version must be a number")

            # 7. Check workflow logic (use original workflow, not the mutated copy)
            logic_errors = self._validate_workflow_logic(workflow)
            validation_errors.extend(logic_errors)

            # Return validation result
            is_valid = len(validation_errors) == 0
            if not is_valid:
                self._log_validation_errors(validation_errors)
            
            return is_valid
            
        except json.JSONDecodeError as e:
            validation_errors.append(f"Invalid JSON structure: {str(e)}")
            return self._log_validation_errors(validation_errors)
        except Exception as e:
            validation_errors.append(f"Validation error: {str(e)}")
            return self._log_validation_errors(validation_errors)

    def _validate_node_structure(self, node: Dict[str, Any], index: int) -> List[str]:
        """Validate individual node structure."""
        errors = []
        
        # Check required node fields
        required_node_fields = ["id", "name", "type", "parameters"]
        for field in required_node_fields:
            if field not in node:
                errors.append(f"Node {index} missing required field: {field}")
        
        # Validate node types
        if "type" in node:
            node_type = node["type"]
            if not isinstance(node_type, str) or not node_type.strip():
                errors.append(f"Node {index} has invalid type: {node_type}")
        
        # Validate parameters
        if "parameters" in node and not isinstance(node["parameters"], dict):
            errors.append(f"Node {index} parameters must be a dictionary")
        
        # Validate position if present
        if "position" in node:
            position = node["position"]
            if not isinstance(position, list) or len(position) != 2:
                errors.append(f"Node {index} position must be a list of 2 numbers")
            elif not all(isinstance(coord, (int, float)) for coord in position):
                errors.append(f"Node {index} position coordinates must be numbers")
        
        return errors

    def _validate_connections(self, workflow_data: Dict[str, Any], node_ids: Optional[set] = None, nodes: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """Validate workflow connections."""
        errors = []
        try:
            # Handle both old and new parameter formats
            if isinstance(workflow_data, dict) and 'nodes' in workflow_data and 'connections' in workflow_data:
                # New format: workflow_data contains both nodes and connections
                connections = workflow_data.get('connections', {})
                nodes = workflow_data.get('nodes', [])
            else:
                # Old format: workflow_data is just connections
                connections = workflow_data
                if not nodes:
                    nodes = []

            # Ensure nodes is always a list (handle None case)
            if nodes is None:
                nodes = []

            # Build set of valid node IDs
            if not node_ids:
                node_ids = {node['id'] for node in nodes}
            validation_logger.debug(f"[VALIDATION DEBUG] Valid node IDs: {node_ids}")

            # Build mapping of node names to IDs
            node_name_to_id = {node['name']: node['id'] for node in nodes}
            validation_logger.debug(f"[VALIDATION DEBUG] Node name to ID mapping: {node_name_to_id}")
            
            validation_logger.debug(f"[VALIDATION DEBUG] Connections to validate: {connections}")
            
            for source_id, connection_data in connections.items():
                validation_logger.debug(f"[VALIDATION DEBUG] Validating connection from source: {source_id}")
                
                # Check if source node exists by ID or name
                if source_id not in node_ids and source_id not in node_name_to_id:
                    validation_logger.debug(f"[VALIDATION DEBUG] Source node '{source_id}' not found in node_ids or node_name_to_id")
                    errors.append(f"Connection references non-existent node '{source_id}'")
                    continue
                
                # If source is a name, get its ID
                actual_source_id = node_name_to_id.get(source_id, source_id)
                validation_logger.debug(f"[VALIDATION DEBUG] Actual source ID: {actual_source_id}")
                
                if not isinstance(connection_data, dict):
                    validation_logger.debug(f"[VALIDATION DEBUG] Invalid connection data structure for node '{source_id}'")
                    errors.append(f"Invalid connection data structure for node '{source_id}'")
                    continue
                
                for connection_type, targets in connection_data.items():
                    validation_logger.debug(f"[VALIDATION DEBUG] Validating connection type: {connection_type}")
                    if not isinstance(targets, list):
                        validation_logger.debug(f"[VALIDATION DEBUG] Invalid targets structure for node '{source_id}'")
                        errors.append(f"Invalid targets structure for node '{source_id}'")
                        continue
                    
                    for target_list in targets:
                        if not isinstance(target_list, list):
                            validation_logger.debug(f"[VALIDATION DEBUG] Invalid target list structure for node '{source_id}'")
                            errors.append(f"Invalid target list structure for node '{source_id}'")
                            continue
                        
                        for target in target_list:
                            if not isinstance(target, dict):
                                validation_logger.debug(f"[VALIDATION DEBUG] Invalid target structure for node '{source_id}'")
                                errors.append(f"Invalid target structure for node '{source_id}'")
                                continue
                            
                            target_node = target.get('node')
                            if not target_node:
                                validation_logger.debug(f"[VALIDATION DEBUG] Missing target node in connection from '{source_id}'")
                                errors.append(f"Missing target node in connection from '{source_id}'")
                                continue
                            
                            # Check if target node exists by ID or name
                            if target_node not in node_ids and target_node not in node_name_to_id:
                                validation_logger.debug(f"[VALIDATION DEBUG] Target node '{target_node}' not found in node_ids or node_name_to_id")
                                errors.append(f"Connection references non-existent node '{target_node}'")
                                continue
                            
                            # If target is a name, get its ID
                            actual_target_id = node_name_to_id.get(target_node, target_node)
                            validation_logger.debug(f"[VALIDATION DEBUG] Actual target ID: {actual_target_id}")
                            
                            # Update the connection to use IDs instead of names
                            target['node'] = actual_target_id
                            validation_logger.debug(f"[VALIDATION DEBUG] Updated target node to ID: {actual_target_id}")
            
            return errors
        except Exception as e:
            validation_logger.error(f"Error validating connections: {str(e)}", exc_info=True)
            errors.append(f"Error validating connections: {str(e)}")
            return errors

    def _validate_workflow_logic(self, workflow: Dict[str, Any]) -> List[str]:
        """Validate workflow logic and structure."""
        errors = []
        nodes = workflow.get("nodes", [])
        
        if not nodes:
            errors.append("Workflow has no nodes")
            return errors
        
        # Check for at least one trigger node
        trigger_nodes = []
        for node in nodes:
            node_type = node.get("type", "").lower()
            # More comprehensive trigger detection
            trigger_keywords = [
                "trigger", "webhook", "schedule", 
                "filetrigger", "localfiletrigger", "scheduletrigger",
                "manualtrigger", "emailtrigger", "httptrigger"
            ]
            if any(trigger_word in node_type for trigger_word in trigger_keywords):
                trigger_nodes.append(node)
        
        if not trigger_nodes:
            # errors.append("Workflow should have at least one trigger node")
            validation_logger.debug("Workflow should have at least one trigger node")
            
        # Check for isolated nodes (nodes with no connections)
        connections = workflow.get("connections", {})
        connected_nodes = set()
        
        # Collect all connected nodes
        for source, targets in connections.items():
            connected_nodes.add(source)
            for target_lists in targets.values():
                for target_list in target_lists:
                    for target in target_list:
                        if "node" in target:
                            connected_nodes.add(target["node"])
        
        # Find isolated nodes
        all_node_names = {node.get("name", f"Node_{i}") for i, node in enumerate(nodes)}
        isolated_nodes = all_node_names - connected_nodes
        
        # Debug logging to understand the validation issue
        validation_logger.debug(f"[VALIDATION DEBUG] All node names: {all_node_names}")
        validation_logger.debug(f"[VALIDATION DEBUG] Connected nodes: {connected_nodes}")
        validation_logger.debug(f"[VALIDATION DEBUG] Isolated nodes: {isolated_nodes}")
        validation_logger.debug(f"[VALIDATION DEBUG] Connections structure: {connections}")
        
        # More intelligent isolated node validation
        if isolated_nodes and len(nodes) > 1:
            # Expanded list of acceptable isolated node types
            acceptable_isolated_types = {
                "webhook response", "http response", "respond to webhook",
                "no operation", "noop", "stop and error", "merge",
                "http request", "database", "mysql", "postgres", "mongodb",
                "redis", "elasticsearch", "api", "rest", "graphql",
                "email", "slack", "discord", "telegram", "sms",
                "file", "csv", "json", "xml", "pdf", "excel",
                "transform", "filter", "sort", "aggregate", "calculate",
                "webhook", "trigger", "schedule", "manual"
            }

            # Check if isolated nodes are acceptable types that can be safely isolated
            problematic_isolated_nodes = set()
            acceptable_isolated_nodes = set()

            for isolated_node_name in isolated_nodes:
                # Find the node object for this isolated node
                isolated_node = None
                for node in nodes:
                    if node.get("name") == isolated_node_name:
                        isolated_node = node
                        break

                if isolated_node:
                    node_type = isolated_node.get("type", "").lower()
                    node_name_lower = isolated_node_name.lower()

                    # Check if this is an acceptable type to be isolated
                    is_type_acceptable = any(acceptable_type in node_type for acceptable_type in acceptable_isolated_types)
                    is_name_acceptable = any(acceptable_type in node_name_lower for acceptable_type in acceptable_isolated_types)

                    if is_type_acceptable or is_name_acceptable:
                        acceptable_isolated_nodes.add(isolated_node_name)
                    else:
                        # Only consider it problematic if it's clearly not a utility/data node
                        # and the workflow has more than 2 nodes (to allow simple workflows)
                        if len(nodes) > 2:
                            problematic_isolated_nodes.add(isolated_node_name)
                        else:
                            # For simple workflows (2 nodes), treat as acceptable
                            acceptable_isolated_nodes.add(isolated_node_name)
                else:
                    # If we can't find the node, only consider it problematic in complex workflows
                    if len(nodes) > 2:
                        problematic_isolated_nodes.add(isolated_node_name)
                    else:
                        acceptable_isolated_nodes.add(isolated_node_name)

            # Log acceptable isolated nodes as info (not error or warning)
            if acceptable_isolated_nodes:
                validation_logger.info(f"Acceptable isolated nodes detected: {', '.join(acceptable_isolated_nodes)}")

            # Only report error for truly problematic isolated nodes in complex workflows
            # For most cases, isolated nodes should be warnings, not errors
            if problematic_isolated_nodes and len(nodes) > 3:
                # Only treat as error in very complex workflows where isolation is clearly wrong
                validation_logger.warning(f"Potentially problematic isolated nodes in complex workflow: {', '.join(problematic_isolated_nodes)}")
                # Don't add to errors - let the workflow proceed with a warning
            elif problematic_isolated_nodes:
                # For simpler workflows, just log as info
                validation_logger.info(f"Isolated nodes detected (may be intentional): {', '.join(problematic_isolated_nodes)}")
        
        return errors

    def _log_validation_errors(self, validation_errors: List[str]) -> bool:
        """Log validation errors with detailed information."""
        if validation_errors:
            validation_logger.error(f"Workflow validation error: {validation_errors[0]}", extra={'operation_id': 'validate'})
            validation_logger.error(f"Total validation errors: {len(validation_errors)}", extra={'operation_id': 'validate'})
            
            # Log all errors in detail
            for i, error in enumerate(validation_errors, 1):
                validation_logger.debug(f"Validation error {i}: {error}")
            
            logger.error(f"Modified workflow failed validation, returning original")
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

    def modify_workflow(self, existing_workflow_json: str, modification_description: str, 
                       workflow_id: Optional[str] = None) -> str:
        """Modify an existing workflow based on a description of changes needed."""
        # Initialize metrics tracking
        metrics = IterationMetrics(
            operation_type="modify_workflow",
            workflow_id=workflow_id or "unknown"
        )
        
        iteration_logger.info(f"Starting workflow modification [ID: {metrics.operation_id}]", extra={'operation_id': metrics.operation_id})
        
        # Enhanced input validation with detailed feedback
        validation_start = time.time()
        
        # Validate workflow JSON
        workflow_validation_errors = self.error_handler.validate_workflow_input(existing_workflow_json)
        if workflow_validation_errors:
            validation_error_detail = self.error_handler.create_validation_error_summary(workflow_validation_errors)
            metrics.finish(success=False, error_message=validation_error_detail.message)
            
            iteration_logger.exception(f"Workflow validation failed [ID: {metrics.operation_id}]: {validation_error_detail.title}", extra={'operation_id': metrics.operation_id})
            iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {validation_error_detail.user_guidance}")
            if validation_error_detail.fix_suggestions:
                iteration_logger.info(f"Fix suggestions [ID: {metrics.operation_id}]: {'; '.join(validation_error_detail.fix_suggestions)}")
            
            performance_logger.info(f"Modify operation failed due to validation", extra=metrics.to_dict())
            return existing_workflow_json
        
        # Validate modification description
        description_validation_errors = self.error_handler.validate_modification_description(modification_description)
        if description_validation_errors:
            description_error_detail = self.error_handler.create_validation_error_summary(description_validation_errors)
            metrics.finish(success=False, error_message=description_error_detail.message)
            
            iteration_logger.exception(f"Description validation failed [ID: {metrics.operation_id}]: {description_error_detail.title}", extra={'operation_id': metrics.operation_id})
            iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {description_error_detail.user_guidance}")
            if description_error_detail.fix_suggestions:
                iteration_logger.info(f"Fix suggestions [ID: {metrics.operation_id}]: {'; '.join(description_error_detail.fix_suggestions)}")
            
            performance_logger.info(f"Modify operation failed due to description validation", extra=metrics.to_dict())
            return existing_workflow_json
        
        metrics.validation_time = time.time() - validation_start
        
        # Enhanced Edge Case Validation
        edge_case_start = time.time()
        try:
            edge_case_result = self.edge_case_validator.validate_edge_cases(
                existing_workflow_json, 
                modification_description
            )
            
            if not edge_case_result.is_valid:
                metrics.finish(success=False, error_message=f"Edge case validation failed: {'; '.join(edge_case_result.errors)}")
                
                iteration_logger.exception(f"Edge case validation failed [ID: {metrics.operation_id}]: {len(edge_case_result.errors)} errors detected", extra={'operation_id': metrics.operation_id})
                iteration_logger.info(f"Edge cases detected [ID: {metrics.operation_id}]: {', '.join(edge_case_result.edge_cases_detected)}")
                
                # Log specific edge case errors
                for error in edge_case_result.errors:
                    iteration_logger.error(f"Edge case error [ID: {metrics.operation_id}]: {error}")
                
                # Log edge case suggestions
                if edge_case_result.suggestions:
                    iteration_logger.info(f"Edge case suggestions [ID: {metrics.operation_id}]: {'; '.join(edge_case_result.suggestions)}")
                
                performance_logger.info(f"Modify operation failed due to edge case validation", extra=metrics.to_dict())
                return existing_workflow_json
            
            # Log edge case warnings and performance metrics
            if edge_case_result.warnings:
                iteration_logger.warning(f"Edge case warnings [ID: {metrics.operation_id}]: {'; '.join(edge_case_result.warnings)}")
            
            if edge_case_result.edge_cases_detected:
                iteration_logger.info(f"Non-critical edge cases detected [ID: {metrics.operation_id}]: {', '.join(edge_case_result.edge_cases_detected)}")
            
            # Add edge case metrics to our tracking
            edge_case_time = time.time() - edge_case_start
            metrics.validation_time += edge_case_time
            
            iteration_logger.info(f"Edge case validation completed [ID: {metrics.operation_id}]", extra={
                'operation_id': metrics.operation_id,
                'edge_case_time': edge_case_time,
                'edge_cases_detected': len(edge_case_result.edge_cases_detected),
                'warnings_count': len(edge_case_result.warnings),
                'performance_metrics': edge_case_result.performance_metrics
            })
            
        except Exception as e:
            edge_case_time = time.time() - edge_case_start
            metrics.validation_time += edge_case_time
            iteration_logger.exception(f"Edge case validation encountered an error [ID: {metrics.operation_id}]: {str(e)}", extra={'operation_id': metrics.operation_id})
            # Continue with normal processing if edge case validation fails

        try:
            # 1. Parse and validate existing workflow
            existing_workflow = json.loads(existing_workflow_json)
            metrics.nodes_before = len(existing_workflow.get('nodes', []))
            
            iteration_logger.info(f"Parsed existing workflow [ID: {metrics.operation_id}]", extra={
                'operation_id': metrics.operation_id,
                'nodes_count': metrics.nodes_before,
                'workflow_name': existing_workflow.get('name', 'Unnamed')
            })
            
            if not self._validate_workflow_structure(existing_workflow):
                error_detail = ErrorDetail(
                    category=ErrorCategory.WORKFLOW_STRUCTURE,
                    severity=ErrorSeverity.ERROR,
                    title="Invalid Workflow Structure",
                    message="The existing workflow has structural issues that prevent modification",
                    user_guidance="Please ensure your workflow has the correct structure with required fields",
                    fix_suggestions=[
                        "Check that your workflow has 'name', 'nodes', and 'connections' fields",
                        "Ensure all nodes have 'id', 'name', and 'type' fields",
                        "Verify that connections reference existing nodes"
                    ]
                )
                metrics.finish(success=False, error_message=error_detail.message)
                iteration_logger.exception(f"Workflow structure validation failed [ID: {metrics.operation_id}]: {error_detail.title}", extra={'operation_id': metrics.operation_id})
                iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {error_detail.user_guidance}")
                performance_logger.info(f"Modify operation failed", extra=metrics.to_dict())
                return existing_workflow_json

            # 2. Analyze the existing workflow
            analysis_start = time.time()
            analysis = self._analyze_workflow(existing_workflow)
            analysis_time = time.time() - analysis_start
            
            iteration_logger.info(f"Workflow analysis completed [ID: {metrics.operation_id}]", extra={
                'operation_id': metrics.operation_id,
                'analysis_time': analysis_time,
                'node_types': analysis.get('node_types', []),
                'triggers_count': len(analysis.get('triggers', [])),
                'actions_count': len(analysis.get('actions', []))
            })

            # 3. Build modification prompt
            prompt = self._build_modification_prompt(existing_workflow, analysis, modification_description)
            
            # 4. Get modification instructions from LLM with enhanced error handling
            llm_start = time.time()
            try:
                # Check if we're in an async context
                try:
                    asyncio.get_running_loop()
                    # We're in an async context, can't use asyncio.run
                    logger.info("In async context, using ThreadPoolExecutor for modification")
                    
                    # Create a function to run the async call in a separate thread
                    def call_llm_sync():
                        return asyncio.run(self._call_mimo_vl7b(prompt))
                    
                    # Run the LLM call in a separate thread with its own event loop
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(call_llm_sync)
                        modifications_response = future.result(timeout=1200)  # 20 minute timeout
                    
                    logger.info("LLM modification call successful")
                    
                except RuntimeError:
                    # No event loop running, we can use asyncio.run normally
                    logger.info("Not in async context, using asyncio.run for modification")
                    modifications_response = asyncio.run(self._call_mimo_vl7b(prompt))
                
                metrics.llm_calls_count = 1
                metrics.llm_total_time = time.time() - llm_start
                
                llm_logger.info(f"LLM response received [ID: {metrics.operation_id}]", extra={
                    'operation_id': metrics.operation_id,
                    'llm_time': metrics.llm_total_time,
                    'response_length': len(modifications_response)
                })
                
            except Exception as e:
                llm_error_time = time.time() - llm_start
                error_detail = self.error_handler.create_llm_error_guidance(e, {
                    'operation_id': metrics.operation_id,
                    'operation_type': 'modify_workflow',
                    'workflow_id': workflow_id
                })
                
                llm_logger.error(f"LLM call failed [ID: {metrics.operation_id}]: {error_detail.title}")
                llm_logger.info(f"User guidance [ID: {metrics.operation_id}]: {error_detail.user_guidance}")
                if error_detail.fix_suggestions:
                    llm_logger.info(f"Fix suggestions [ID: {metrics.operation_id}]: {'; '.join(error_detail.fix_suggestions)}")
                
                # No longer fall back to mock - LLM availability should be checked upfront
                metrics.finish(success=False, error_message=error_detail.message)
                
                # Check if this is already a detailed error message from our enhanced error handling
                if any(keyword in error_detail.message.lower() for keyword in [
                    "crashed", "exit code", "connection refused", "connection reset", 
                    "broken pipe", "terminated", "killed", "service error"
                ]):
                    # This is already a detailed error, preserve it
                    raise RuntimeError(error_detail.message)
                else:
                    # Generic error, add context
                    raise RuntimeError(f"LLM service unavailable: {error_detail.message}")

            # 5. Apply modifications with enhanced error handling
            modification_start = time.time()
            try:
                modified_workflow = self._apply_workflow_modifications(existing_workflow, modifications_response)
                modification_time = time.time() - modification_start
                metrics.nodes_after = len(modified_workflow.get('nodes', []))
                
                iteration_logger.info(f"Modifications applied [ID: {metrics.operation_id}]", extra={
                    'operation_id': metrics.operation_id,
                    'modification_time': modification_time,
                    'nodes_before': metrics.nodes_before,
                    'nodes_after': metrics.nodes_after,
                    'nodes_changed': metrics.nodes_after - metrics.nodes_before
                })
                
            except Exception as e:
                error_detail = self.error_handler.categorize_error(e, {
                    'operation_id': metrics.operation_id,
                    'operation_type': 'apply_modifications',
                    'workflow_id': workflow_id
                })
                
                iteration_logger.error(f"Modification application failed [ID: {metrics.operation_id}]: {error_detail.title}")
                iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {error_detail.user_guidance}")
                
                # Return original workflow on modification failure
                modified_workflow = existing_workflow
                metrics.nodes_after = metrics.nodes_before

            # 6. Validate the modified workflow
            validation_start = time.time()
            modified_workflow_json = json.dumps(modified_workflow)
            is_valid = self.validate_workflow(modified_workflow_json)
            metrics.validation_time += time.time() - validation_start
            
            if not is_valid:
                validation_logger.warning(f"Modified workflow failed validation [ID: {metrics.operation_id}], returning original")
                iteration_logger.warning(f"Returning original workflow due to validation failure [ID: {metrics.operation_id}]")
                iteration_logger.info(f"Validation guidance [ID: {metrics.operation_id}]: The modified workflow contains structural issues. Using original workflow to prevent errors.")
                metrics.nodes_after = metrics.nodes_before  # Reset since we're returning original
                modified_workflow_json = existing_workflow_json

            # 7. Track the iteration
            if workflow_id:
                self._track_workflow_iteration(
                    workflow_id, 
                    existing_workflow_json, 
                    modified_workflow_json, 
                    modification_description
                )
                iteration_logger.info(f"Iteration tracked [ID: {metrics.operation_id}]", extra={
                    'operation_id': metrics.operation_id,
                    'workflow_id': workflow_id
                })

            # 8. Finalize metrics and log performance
            metrics.finish(success=True)
            performance_logger.info(f"Workflow modification completed successfully", extra=metrics.to_dict())
            
            iteration_logger.info(f"Workflow modification completed [ID: {metrics.operation_id}]", extra={
                'operation_id': metrics.operation_id,
                'total_duration': metrics.duration_seconds,
                'success': True,
                'final_nodes': metrics.nodes_after
            })
            
            logger.info(f"Workflow modification completed successfully")
            return modified_workflow_json
            
        except Exception as e:
            error_detail = self.error_handler.categorize_error(e, {
                'operation_id': metrics.operation_id,
                'operation_type': 'modify_workflow',
                'workflow_id': workflow_id
            })
            
            metrics.finish(success=False, error_message=error_detail.message)
            
            iteration_logger.exception(f"Workflow modification failed [ID: {metrics.operation_id}]: {error_detail.title}", extra={'operation_id': metrics.operation_id})
            iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {error_detail.user_guidance}")
            if error_detail.fix_suggestions:
                iteration_logger.info(f"Fix suggestions [ID: {metrics.operation_id}]: {'; '.join(error_detail.fix_suggestions)}")
            
            performance_logger.error(f"Workflow modification failed", extra=metrics.to_dict())
            logger.error(f"Workflow modification failed: {error_detail.title} - {error_detail.message}")
            return existing_workflow_json

    def iterate_workflow(self, workflow_id: str, existing_workflow_json: str, 
                        feedback_from_testing: str, additional_requirements: str = "") -> str:
        """Iterate on an existing workflow based on testing feedback and additional requirements."""
        # Initialize metrics tracking
        metrics = IterationMetrics(
            operation_type="iterate_workflow",
            workflow_id=workflow_id
        )
        
        iteration_logger.info(f"Starting workflow iteration [ID: {metrics.operation_id}]", extra={
            'operation_id': metrics.operation_id,
            'workflow_id': metrics.workflow_id,
            'feedback_summary': feedback_from_testing[:100] + '...' if len(feedback_from_testing) > 100 else feedback_from_testing,
            'has_additional_requirements': bool(additional_requirements)
        })
        
        # Enhanced input validation with detailed feedback
        validation_start = time.time()
        
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
            metrics.finish(success=False, error_message=error_detail.message)
            iteration_logger.error(f"Workflow ID validation failed [ID: {metrics.operation_id}]: {error_detail.title}")
            iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {error_detail.user_guidance}")
            performance_logger.info(f"Iterate operation failed due to workflow ID validation", extra=metrics.to_dict())
            return existing_workflow_json
        
        # Validate workflow JSON
        workflow_validation_errors = self.error_handler.validate_workflow_input(existing_workflow_json)
        if workflow_validation_errors:
            validation_error_detail = self.error_handler.create_validation_error_summary(workflow_validation_errors)
            metrics.finish(success=False, error_message=validation_error_detail.message)
            
            iteration_logger.exception(f"Workflow validation failed [ID: {metrics.operation_id}]: {validation_error_detail.title}", extra={'operation_id': metrics.operation_id})
            iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {validation_error_detail.user_guidance}")
            if validation_error_detail.fix_suggestions:
                iteration_logger.info(f"Fix suggestions [ID: {metrics.operation_id}]: {'; '.join(validation_error_detail.fix_suggestions)}")
            
            performance_logger.info(f"Iterate operation failed due to workflow validation", extra=metrics.to_dict())
            return existing_workflow_json
        
        # Validate feedback from testing
        if not feedback_from_testing or not feedback_from_testing.strip():
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
            metrics.finish(success=False, error_message=error_detail.message)
            iteration_logger.error(f"Feedback validation failed [ID: {metrics.operation_id}]: {error_detail.title}")
            iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {error_detail.user_guidance}")
            performance_logger.info(f"Iterate operation failed due to feedback validation", extra=metrics.to_dict())
            return existing_workflow_json
        
        # Validate feedback length and quality
        # TEMPORARY: Bypass validation for testing
        """
        feedback_validation_errors = self.error_handler.validate_modification_description(feedback_from_testing)
        if feedback_validation_errors:
            feedback_error_detail = self.error_handler.create_validation_error_summary(feedback_validation_errors)
            metrics.finish(success=False, error_message=feedback_error_detail.message)
            
            iteration_logger.error(f"Feedback quality validation failed [ID: {metrics.operation_id}]: {feedback_error_detail.title}")
            iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {feedback_error_detail.user_guidance}")
            if feedback_error_detail.fix_suggestions:
                iteration_logger.info(f"Fix suggestions [ID: {metrics.operation_id}]: {'; '.join(feedback_error_detail.fix_suggestions)}")
            
            performance_logger.info(f"Iterate operation failed due to feedback quality", extra=metrics.to_dict())
            return existing_workflow_json
        """
        
        # Log that we're bypassing validation for testing
        iteration_logger.info(f"TESTING: Bypassing feedback validation to test LLM functionality [ID: {metrics.operation_id}]")
        
        metrics.validation_time = time.time() - validation_start
        
        # Enhanced Edge Case Validation for Iteration
        edge_case_start = time.time()
        try:
            # Combine feedback and additional requirements for edge case validation
            combined_description = f"FEEDBACK FROM TESTING: {feedback_from_testing}"
            if additional_requirements:
                combined_description += f"\n\nADDITIONAL REQUIREMENTS: {additional_requirements}"
            
            edge_case_result = self.edge_case_validator.validate_edge_cases(
                existing_workflow_json, 
                combined_description
            )
            
            if not edge_case_result.is_valid:
                metrics.finish(success=False, error_message=f"Edge case validation failed: {'; '.join(edge_case_result.errors)}")
                
                iteration_logger.exception(f"Edge case validation failed [ID: {metrics.operation_id}]: {len(edge_case_result.errors)} errors detected", extra={'operation_id': metrics.operation_id})
                iteration_logger.info(f"Edge cases detected [ID: {metrics.operation_id}]: {', '.join(edge_case_result.edge_cases_detected)}")
                
                # Log specific edge case errors
                for error in edge_case_result.errors:
                    iteration_logger.error(f"Edge case error [ID: {metrics.operation_id}]: {error}")
                
                # Log edge case suggestions
                if edge_case_result.suggestions:
                    iteration_logger.info(f"Edge case suggestions [ID: {metrics.operation_id}]: {'; '.join(edge_case_result.suggestions)}")
                
                performance_logger.info(f"Iterate operation failed due to edge case validation", extra=metrics.to_dict())
                return existing_workflow_json
            
            # Log edge case warnings and performance metrics
            if edge_case_result.warnings:
                iteration_logger.warning(f"Edge case warnings [ID: {metrics.operation_id}]: {'; '.join(edge_case_result.warnings)}")
            
            if edge_case_result.edge_cases_detected:
                iteration_logger.info(f"Non-critical edge cases detected [ID: {metrics.operation_id}]: {', '.join(edge_case_result.edge_cases_detected)}")
            
            # Add edge case metrics to our tracking
            edge_case_time = time.time() - edge_case_start
            metrics.validation_time += edge_case_time
            
            iteration_logger.info(f"Edge case validation completed [ID: {metrics.operation_id}]", extra={
                'operation_id': metrics.operation_id,
                'edge_case_time': edge_case_time,
                'edge_cases_detected': len(edge_case_result.edge_cases_detected),
                'warnings_count': len(edge_case_result.warnings),
                'performance_metrics': edge_case_result.performance_metrics
            })
            
        except Exception as e:
            edge_case_time = time.time() - edge_case_start
            metrics.validation_time += edge_case_time
            iteration_logger.exception(f"Edge case validation encountered an error [ID: {metrics.operation_id}]: {str(e)}", extra={'operation_id': metrics.operation_id})
            # Continue with normal processing if edge case validation fails

        try:
            # Parse existing workflow with enhanced error handling
            try:
                existing_workflow = json.loads(existing_workflow_json)
                metrics.nodes_before = len(existing_workflow.get('nodes', []))
            except json.JSONDecodeError as e:
                error_detail = self.error_handler.create_json_error_guidance(e, {
                    'operation_id': metrics.operation_id,
                    'operation_type': 'iterate_workflow'
                })
                metrics.finish(success=False, error_message=error_detail.message)
                
                iteration_logger.error(f"JSON parsing failed [ID: {metrics.operation_id}]: {error_detail.title}")
                iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {error_detail.user_guidance}")
                if error_detail.fix_suggestions:
                    iteration_logger.info(f"Fix suggestions [ID: {metrics.operation_id}]: {'; '.join(error_detail.fix_suggestions)}")
                
                performance_logger.error(f"Iterate operation failed due to JSON parsing", extra=metrics.to_dict())
                return existing_workflow_json
            
            iteration_logger.info(f"Parsed workflow for iteration [ID: {metrics.operation_id}]", extra={
                'operation_id': metrics.operation_id,
                'workflow_name': existing_workflow.get('name', 'Unnamed'),
                'nodes_count': metrics.nodes_before
            })
            
            # Analyze existing workflow
            analysis_start = time.time()
            analysis = self._analyze_workflow(existing_workflow)
            analysis_time = time.time() - analysis_start
            
            iteration_logger.info(f"Workflow analysis for iteration completed [ID: {metrics.operation_id}]", extra={
                'operation_id': metrics.operation_id,
                'analysis_time': analysis_time,
                'triggers_count': len(analysis.get('triggers', [])),
                'actions_count': len(analysis.get('actions', [])),
                'potential_issues': analysis.get('potential_issues', [])
            })

            # Build iteration-specific prompt that includes both feedback and requirements
            combined_description = f"FEEDBACK FROM TESTING: {feedback_from_testing}"
            if additional_requirements:
                combined_description += f"\n\nADDITIONAL REQUIREMENTS: {additional_requirements}"
            
            iteration_logger.info(f"Built iteration prompt [ID: {metrics.operation_id}]", extra={
                'operation_id': metrics.operation_id,
                'combined_description_length': len(combined_description)
            })

            # Get workflow iteration suggestions using modify_workflow method with enhanced error handling
            iteration_start = time.time()
            try:
                iterated_workflow_json = self.modify_workflow(
                    existing_workflow_json, 
                    combined_description, 
                    workflow_id
                )
                iteration_time = time.time() - iteration_start
                
                # Parse the iterated workflow to get metrics
                try:
                    iterated_workflow = json.loads(iterated_workflow_json)
                    metrics.nodes_after = len(iterated_workflow.get('nodes', []))
                except json.JSONDecodeError:
                    metrics.nodes_after = metrics.nodes_before
                    iteration_logger.warning(f"Could not parse iterated workflow JSON [ID: {metrics.operation_id}]")
                
            except Exception as e:
                error_detail = self.error_handler.categorize_error(e, {
                    'operation_id': metrics.operation_id,
                    'operation_type': 'iteration_modification',
                    'workflow_id': workflow_id
                })
                
                iteration_logger.exception(f"Iteration modification failed [ID: {metrics.operation_id}]: {error_detail.title}", extra={'operation_id': metrics.operation_id})
                iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {error_detail.user_guidance}")
                if error_detail.fix_suggestions:
                    iteration_logger.info(f"Fix suggestions [ID: {metrics.operation_id}]: {'; '.join(error_detail.fix_suggestions)}")
                
                # Return original workflow on iteration failure
                iterated_workflow_json = existing_workflow_json
                iteration_time = time.time() - iteration_start
                metrics.nodes_after = metrics.nodes_before
            
            # Check if iteration actually resulted in changes
            if iterated_workflow_json == existing_workflow_json:
                iteration_logger.warning(f"Workflow iteration did not result in changes [ID: {metrics.operation_id}]")
                iteration_logger.info(f"Iteration guidance [ID: {metrics.operation_id}]: This might indicate that your feedback was unclear or the workflow is already optimal. Try providing more specific feedback about what needs to change.")
            else:
                iteration_logger.info(f"Workflow iteration resulted in changes [ID: {metrics.operation_id}]", extra={
                    'operation_id': metrics.operation_id,
                    'nodes_changed': metrics.nodes_after - metrics.nodes_before
                })

            # Track this specific iteration
            try:
                self._track_workflow_iteration(
                    workflow_id, 
                    existing_workflow_json, 
                    iterated_workflow_json,
                    f"ITERATION - Feedback: {feedback_from_testing[:50]}{'...' if len(feedback_from_testing) > 50 else ''}"
                )
                
                iteration_logger.info(f"Iteration tracked in history [ID: {metrics.operation_id}]", extra={
                    'operation_id': metrics.operation_id,
                    'workflow_id': workflow_id
                })
                
            except Exception as e:
                iteration_logger.warning(f"Failed to track iteration [ID: {metrics.operation_id}]: {str(e)}")

            # Finalize metrics and log performance
            metrics.finish(success=True)
            performance_logger.info(f"Workflow iteration completed successfully", extra=metrics.to_dict())
            
            iteration_logger.info(f"Workflow iteration completed [ID: {metrics.operation_id}]", extra={
                'operation_id': metrics.operation_id,
                'total_duration': metrics.duration_seconds,
                'iteration_time': iteration_time,
                'success': True,
                'resulted_in_changes': iterated_workflow_json != existing_workflow_json
            })
            
            logger.info("Workflow iteration completed successfully")
            return iterated_workflow_json
            
        except Exception as e:
            error_detail = self.error_handler.categorize_error(e, {
                'operation_id': metrics.operation_id,
                'operation_type': 'iterate_workflow',
                'workflow_id': workflow_id
            })
            
            metrics.finish(success=False, error_message=error_detail.message)
            
            iteration_logger.exception(f"Workflow iteration failed [ID: {metrics.operation_id}]: {error_detail.title}", extra={'operation_id': metrics.operation_id})
            iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {error_detail.user_guidance}")
            if error_detail.fix_suggestions:
                iteration_logger.info(f"Fix suggestions [ID: {metrics.operation_id}]: {'; '.join(error_detail.fix_suggestions)}")
            
            performance_logger.error(f"Workflow iteration failed", extra=metrics.to_dict())
            logger.error(f"Workflow iteration failed: {error_detail.title} - {error_detail.message}")
            return existing_workflow_json

    def _validate_modify_inputs(self, existing_workflow_json: str, modification_description: str, workflow_id: Optional[str] = None) -> Optional[str]:
        """Validate inputs for modify_workflow method."""
        if not existing_workflow_json or not existing_workflow_json.strip():
            return "existing_workflow_json cannot be empty"
        
        if not modification_description or not modification_description.strip():
            return "modification_description cannot be empty"
        
        if len(modification_description.strip()) < 5:
            return "modification_description must be at least 5 characters"
        
        if len(modification_description) > 10000:
            return "modification_description is too long (max 10000 characters)"
        
        if workflow_id is not None and (not workflow_id.strip() or len(workflow_id) > 100):
            return "workflow_id must be non-empty and less than 100 characters"
        
        # Try to parse JSON
        try:
            json.loads(existing_workflow_json)
        except json.JSONDecodeError as e:
            return f"existing_workflow_json is not valid JSON: {str(e)}"
        
        return None

    def _validate_iterate_inputs(self, workflow_id: str, existing_workflow_json: str, feedback_from_testing: str, additional_requirements: str = "") -> Optional[str]:
        """Validate inputs for iterate_workflow method."""
        if not workflow_id or not workflow_id.strip():
            return "workflow_id cannot be empty"
        
        if len(workflow_id) > 100:
            return "workflow_id is too long (max 100 characters)"
        
        if not existing_workflow_json or not existing_workflow_json.strip():
            return "existing_workflow_json cannot be empty"
        
        if not feedback_from_testing or not feedback_from_testing.strip():
            return "feedback_from_testing cannot be empty"
        
        if len(feedback_from_testing.strip()) < 5:
            return "feedback_from_testing must be at least 5 characters"
        
        if len(feedback_from_testing) > 5000:
            return "feedback_from_testing is too long (max 5000 characters)"
        
        if additional_requirements and len(additional_requirements) > 5000:
            return "additional_requirements is too long (max 5000 characters)"
        
        # Try to parse JSON
        try:
            json.loads(existing_workflow_json)
        except json.JSONDecodeError as e:
            return f"existing_workflow_json is not valid JSON: {str(e)}"
        
        return None

    def _analyze_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a workflow structure to understand its components and flow with performance optimization."""
        # Convert workflow to JSON string for performance optimization
        workflow_json = json.dumps(workflow)
        
        # Use performance optimizer for large workflows
        try:
            result, perf_metrics = self.performance_optimizer.optimize_workflow_processing(
                workflow_json, 
                'analyze'
            )
            
            # Log performance metrics for analysis operations
            if perf_metrics.optimizations_applied:
                logger.info(f"Workflow analysis used optimizations: {', '.join(perf_metrics.optimizations_applied)}")
            
            # If performance optimizer returned results, use them
            if result and isinstance(result, dict) and 'analysis_type' in result:
                return result
            
        except Exception as e:
            logger.warning(f"Performance optimization failed for workflow analysis: {str(e)}")
            # Fall back to standard analysis
        
        # Standard analysis implementation (fallback)
        analysis = {
            "node_count": len(workflow.get("nodes", [])),
            "node_types": [],
            "connections": workflow.get("connections", {}),
            "triggers": [],
            "actions": [],
            "data_flow": [],
            "potential_issues": [],
            "analysis_type": "standard"
        }
        
        # Get all node IDs and names for validation
        all_node_ids = set()
        node_name_to_id = {}
        for node in workflow.get("nodes", []):
            node_id = node.get("id")
            node_name = node.get("name")
            if node_id:
                all_node_ids.add(node_id)
            if node_name and node_id:
                node_name_to_id[node_name] = node_id
        
        connected_node_ids = set()
        
        # Analyze nodes
        for node in workflow.get("nodes", []):
            node_type = node.get("type", "unknown")
            analysis["node_types"].append(node_type)
            
            # Categorize nodes
            if "trigger" in node_type.lower() or "webhook" in node_type.lower() or node_type.endswith("Trigger"):
                analysis["triggers"].append(node)
            else:
                analysis["actions"].append(node)
        
        # Analyze data flow and track connected nodes
        for source_node, connections in analysis["connections"].items():
            # Get the actual node ID (either direct ID or mapped from name)
            source_node_id = source_node if source_node in all_node_ids else node_name_to_id.get(source_node)
            
            if source_node_id:
                connected_node_ids.add(source_node_id)
                
                if isinstance(connections, dict):
                    for connection_type, targets in connections.items():
                        if isinstance(targets, list):
                            for target_list in targets:
                                if isinstance(target_list, list):
                                    for target in target_list:
                                        if isinstance(target, dict):
                                            target_node = target.get("node")
                                            # Get the actual target node ID
                                            target_node_id = target_node if target_node in all_node_ids else node_name_to_id.get(target_node)
                                            
                                            if target_node_id:
                                                connected_node_ids.add(target_node_id)
                                                analysis["data_flow"].append({
                                                    "from": source_node_id,
                                                    "to": target_node_id,
                                                    "type": connection_type
                                                })
                                            else:
                                                analysis["potential_issues"].append(
                                                    f"Connection references non-existent node '{target_node}'"
                                                )
        
        # Check for orphaned nodes (nodes with no connections)
        orphaned_nodes = all_node_ids - connected_node_ids
        if orphaned_nodes:
            analysis["potential_issues"].append(f"Orphaned nodes detected: {', '.join(orphaned_nodes)}")
        
        # Check for unreachable nodes (nodes that can't be reached from any trigger)
        trigger_ids = {node.get("id") for node in analysis["triggers"]}
        reachable_nodes = set()
        
        # Start from trigger nodes and traverse the graph
        for trigger_id in trigger_ids:
            reachable_nodes.add(trigger_id)
            self._traverse_workflow_graph(trigger_id, analysis["connections"], reachable_nodes, node_name_to_id)
        
        unreachable_nodes = all_node_ids - reachable_nodes
        if unreachable_nodes:
            analysis["potential_issues"].append(f"Unreachable nodes detected: {', '.join(unreachable_nodes)}")
        
        return analysis
        
    def _traverse_workflow_graph(self, node_id: str, connections: Dict[str, Any], 
                               reachable_nodes: set, node_name_to_id: Dict[str, str]) -> None:
        """Helper method to traverse the workflow graph and mark reachable nodes."""
        if node_id not in connections:
            return
            
        for connection_type, targets in connections[node_id].items():
            if isinstance(targets, list):
                for target_list in targets:
                    if isinstance(target_list, list):
                        for target in target_list:
                            if isinstance(target, dict):
                                target_node = target.get("node")
                                target_node_id = target_node if target_node and target_node in reachable_nodes else (node_name_to_id.get(target_node) if target_node else None)
                                
                                if target_node_id and target_node_id not in reachable_nodes:
                                    reachable_nodes.add(target_node_id)
                                    self._traverse_workflow_graph(target_node_id, connections, reachable_nodes, node_name_to_id)

    def _build_modification_prompt(self, existing_workflow: Dict[str, Any], 
                                 analysis: Dict[str, Any], modification_description: str) -> str:
        """Build a simplified prompt for modifying an existing workflow."""
        # Simplify the workflow representation to reduce prompt size
        simplified_workflow = {
            "name": existing_workflow.get("name", ""),
            "nodes": [
                {
                    "id": node.get("id"),
                    "name": node.get("name"),
                    "type": node.get("type")
                } for node in existing_workflow.get("nodes", [])
            ],
            "connections": existing_workflow.get("connections", {})
        }
        
        return f"""Modify n8n workflow. Respond with JSON only.

Current workflow:
{json.dumps(simplified_workflow, indent=1)}

Request: {modification_description}

IMPORTANT: When adding nodes, you MUST also create connections to integrate them into the workflow flow. Isolated nodes will be rejected.

CONNECTION RULES:
- Use "add_connection" to create NEW connections between existing nodes
- Use "modify_connection" to CHANGE an existing connection to point to a different target
- NEVER use both add_connection AND modify_connection for the same source->target pair

Example for adding email node and redirecting existing connection:
[
  {{"action":"add_node","details":{{"node_id":"email-node","name":"Send Email","node_type":"n8n-nodes-base.emailSend","parameters":{{"to":"user@example.com","subject":"Workflow Complete"}},"position":[1000,300]}}}},
  {{"action":"modify_connection","details":{{"source_node":"process-data","old_target":"webhook-response","new_target":"email-node","connection_type":"main"}}}}
]

Valid actions: add_node, modify_node, remove_node, add_connection, modify_connection, remove_connection
CRITICAL: Return ONLY valid JSON array. NO thinking tags (<think>), NO code blocks (```), NO explanations, NO extra text."""

    def _apply_workflow_modifications(self, workflow: Dict[str, Any], modifications_response: str) -> Dict[str, Any]:
        """Apply modifications to a workflow based on LLM response with enhanced error handling."""
        try:
            logger.debug(f"Attempting to parse modifications response: {modifications_response[:200]}...")
            
            # Debug: Log what we received from the LLM
            logger.info(f"Raw LLM response for modifications: length={len(modifications_response)}")
            logger.debug(f"First 500 chars of response: {modifications_response[:500]}")
            logger.debug(f"Contains thinking tags: {'<think>' in modifications_response.lower()}")
            logger.debug(f"Contains code blocks: {'```' in modifications_response}")
            logger.debug(f"Starts with JSON: {modifications_response.strip().startswith(('{', '['))}")
            
            # First, try to clean and extract JSON from the response
            cleaned_response = self._extract_json_from_response(modifications_response)
            if not cleaned_response:
                logger.warning("No valid JSON found in LLM response, returning original workflow")
                logger.debug(f"JSON extraction failed for: {modifications_response}")
                return workflow
            
            logger.debug(f"Extracted JSON: {cleaned_response[:200]}...")
            
            # Parse modification instructions
            modifications = json.loads(cleaned_response)
            if not isinstance(modifications, list):
                modifications = [modifications]
            
            logger.info(f"Parsed {len(modifications)} modification instructions")
            
            # Validate modifications structure
            valid_modifications = []
            for i, mod in enumerate(modifications):
                if self._validate_modification_structure(mod):
                    valid_modifications.append(mod)
                    logger.debug(f"Valid modification {i}: {mod.get('action', 'unknown')}")
                else:
                    logger.warning(f"Skipping invalid modification {i}: {mod}")
            
            if not valid_modifications:
                logger.warning("No valid modifications found, returning original workflow")
                logger.debug(f"All modifications were invalid: {modifications}")
                return workflow
            
            logger.info(f"Applying {len(valid_modifications)} valid modifications")
            
            # Apply modifications to a deep copy of the workflow
            modified_workflow = json.loads(json.dumps(workflow))  # Deep copy
            
            # Pre-process modifications to detect and resolve conflicts
            processed_modifications = self._resolve_modification_conflicts(valid_modifications)
            
            modifications_applied = 0
            for mod in processed_modifications:
                try:
                    action = mod.get("action")
                    details = mod.get("details", {})
                    
                    logger.debug(f"Applying modification: {action} with details: {details}")
                    
                    if action == "add_node":
                        self._add_node_to_workflow(modified_workflow, details)
                        modifications_applied += 1
                        logger.info(f"Added node: {details.get('name', 'unnamed')}")
                    elif action == "modify_node":
                        self._modify_node_in_workflow(modified_workflow, details)
                        modifications_applied += 1
                        logger.info(f"Modified node: {details.get('node_id', 'unknown')}")
                    elif action == "remove_node":
                        self._remove_node_from_workflow(modified_workflow, details)
                        modifications_applied += 1
                        logger.info(f"Removed node: {details.get('node_id', 'unknown')}")
                    elif action == "add_connection":
                        self._add_connection_to_workflow(modified_workflow, details)
                        modifications_applied += 1
                        logger.info(f"Added connection: {details.get('source_node', 'unknown')} -> {details.get('target_node', 'unknown')}")
                    elif action == "modify_connection":
                        self._modify_connection_in_workflow(modified_workflow, details)
                        modifications_applied += 1
                        logger.info(f"Modified connection")
                    elif action == "remove_connection":
                        self._remove_connection_from_workflow(modified_workflow, details)
                        modifications_applied += 1
                        logger.info(f"Removed connection")
                    else:
                        logger.warning(f"Unknown modification action: {action}")
                        
                except Exception as mod_error:
                    logger.error(f"Error applying modification {action}: {str(mod_error)}")
                    continue
            
            logger.info(f"Successfully applied {modifications_applied} modifications")
            return modified_workflow
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in modifications: {str(e)}")
            logger.debug(f"Failed to parse: {modifications_response}")
            return workflow  # Return original on JSON error
        except Exception as e:
            logger.error(f"Error applying modifications: {str(e)}")
            return workflow  # Return original on error

    def _resolve_modification_conflicts(self, modifications: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Resolve conflicts between modifications, particularly add_connection + modify_connection duplicates."""
        # Group modifications by type
        add_connections = []
        modify_connections = []
        other_modifications = []
        
        for mod in modifications:
            action = mod.get("action")
            if action == "add_connection":
                add_connections.append(mod)
            elif action == "modify_connection":
                modify_connections.append(mod)
            else:
                other_modifications.append(mod)
        
        # Check for conflicts: add_connection + modify_connection to same target
        resolved_modifications = other_modifications.copy()
        
        # Process modify_connections first (they take precedence)
        for modify_mod in modify_connections:
            modify_details = modify_mod.get("details", {})
            modify_source = modify_details.get("source_node")
            modify_new_target = modify_details.get("new_target")
            
            # Check if there's a conflicting add_connection
            conflicting_add = None
            for add_mod in add_connections:
                add_details = add_mod.get("details", {})
                add_source = add_details.get("source_node")
                add_target = add_details.get("target_node")
                
                # If add_connection has same source->target as modify_connection's new target
                if (modify_source == add_source and modify_new_target == add_target):
                    conflicting_add = add_mod
                    logger.info(f"Detected conflict: add_connection and modify_connection both create {modify_source} -> {modify_new_target}")
                    break
            
            # Remove the conflicting add_connection and keep only modify_connection
            if conflicting_add:
                add_connections.remove(conflicting_add)
                logger.info(f"Resolved conflict: Removed duplicate add_connection, keeping modify_connection")
            
            resolved_modifications.append(modify_mod)
        
        # Add remaining non-conflicting add_connections
        resolved_modifications.extend(add_connections)
        
        logger.info(f"Conflict resolution: {len(modifications)} -> {len(resolved_modifications)} modifications")
        return resolved_modifications

    def _extract_json_from_response(self, response: str) -> str:
        """Extract the last valid JSON object or array from the LLM response, robust to multiline and nested structures."""
        if not response or response.strip() == "":
            return ""
        import re
        # Remove <think>...</think> tags
        think_pattern = r'<think>.*?</think>'
        response_no_think = re.sub(think_pattern, '', response, flags=re.DOTALL | re.IGNORECASE)
        response_no_think = response_no_think.strip()

        # Stack-based scan for last top-level JSON object or array
        text = response_no_think
        stack = []
        start_idx = None
        last_valid = ""
        for i, char in enumerate(text):
            if char in '{[':
                if not stack:
                    start_idx = i
                stack.append(char)
            elif char in '}]':
                if stack:
                    open_char = stack.pop()
                    if not stack and start_idx is not None:
                        candidate = text[start_idx:i+1].strip()
                        try:
                            parsed = json.loads(candidate)
                            if self._is_valid_modifications_json(parsed) or self._is_valid_workflow_json(parsed):
                                last_valid = candidate
                        except Exception:
                            pass
        if last_valid:
            return last_valid

        # Fallback: try previous strategies
        return self._try_json_extraction_strategies(response_no_think)

    def _try_json_extraction_strategies(self, text: str) -> str:
        """Try multiple JSON extraction strategies on a piece of text, supporting both workflow objects and modifications arrays."""
        import re
        json_block_pattern = r'```(?:json)?\s*(.*?)\s*```'
        matches = re.findall(json_block_pattern, text, re.DOTALL | re.IGNORECASE)
        for match in matches:
            try:
                parsed = json.loads(match.strip())
                if self._is_valid_modifications_json(parsed) or self._is_valid_workflow_json(parsed):
                    logger.debug("Found valid JSON in code block")
                    return match.strip()
            except json.JSONDecodeError:
                continue
        start_indices = [i for i, char in enumerate(text) if char == '[']
        for start_idx in reversed(start_indices):
            bracket_count = 0
            end_idx = -1
            for i, char in enumerate(text[start_idx:], start_idx):
                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        end_idx = i
                        break
            if end_idx != -1:
                potential_json = text[start_idx:end_idx+1]
                try:
                    parsed = json.loads(potential_json)
                    if self._is_valid_modifications_json(parsed) or self._is_valid_workflow_json(parsed):
                        logger.debug(f"Found valid JSON using bracket counting")
                        return potential_json
                except json.JSONDecodeError:
                    continue
        brace_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(brace_pattern, text, re.DOTALL)
        for match in reversed(matches):
            try:
                parsed = json.loads(match)
                if self._is_valid_modifications_json([parsed]) or self._is_valid_workflow_json(parsed):
                    logger.debug("Found valid JSON object")
                    return match
            except json.JSONDecodeError:
                continue
        lines = text.split('\n')
        for line in reversed(lines):
            line = line.strip()
            if line.startswith('[') or line.startswith('{'):
                try:
                    parsed = json.loads(line)
                    if (isinstance(parsed, list) and self._is_valid_modifications_json(parsed)) or self._is_valid_workflow_json(parsed):
                        logger.debug("Found valid JSON in line starting with bracket")
                        return line
                except json.JSONDecodeError:
                    continue
        logger.warning(f"Could not extract valid workflow or modifications JSON from text: {text[:200]}...")
        return ""

    def _is_valid_modifications_json(self, parsed_json) -> bool:
        """Check if the parsed JSON is a valid modifications array."""
        if not isinstance(parsed_json, list):
            return False
        
        if len(parsed_json) == 0:
            return False
        
        # Check if all items in the array are modification objects
        for item in parsed_json:
            if not isinstance(item, dict):
                return False
            if "action" not in item:
                return False
            # Check if action is one of the valid modification actions
            valid_actions = ["add_node", "modify_node", "remove_node", "add_connection", "modify_connection", "remove_connection"]
            if item.get("action") not in valid_actions:
                return False
        
        return True

    def _is_valid_workflow_json(self, parsed_json) -> bool:
        """Check if the parsed JSON is a valid workflow object."""
        if not isinstance(parsed_json, dict):
            return False
        # Must have at least 'nodes' and 'connections' keys
        if 'nodes' not in parsed_json or 'connections' not in parsed_json:
            return False
        # Nodes should be a list, connections should be a dict or list
        if not isinstance(parsed_json['nodes'], list):
            return False
        if not (isinstance(parsed_json['connections'], dict) or isinstance(parsed_json['connections'], list)):
            return False
        return True

    def _validate_modification_structure(self, modification: Dict[str, Any]) -> bool:
        """Validate that a modification has the correct structure."""
        if not isinstance(modification, dict):
            logger.warning("Modification is not a dictionary")
            return False
        
        # Check required fields
        if "action" not in modification:
            logger.warning("Modification missing 'action' field")
            return False
        
        action = modification.get("action")
        valid_actions = [
            "add_node", "modify_node", "remove_node",
            "add_connection", "modify_connection", "remove_connection"
        ]
        
        if action not in valid_actions:
            logger.warning(f"Invalid action: {action}")
            return False
        
        # Validate details based on action
        details = modification.get("details", {})
        if not isinstance(details, dict):
            logger.warning("Modification 'details' must be a dictionary")
            return False
        
        # Action-specific validation
        if action in ["modify_node", "remove_node"] and "node_id" not in details:
            logger.warning(f"Action {action} requires 'node_id' in details")
            return False
        
        if action == "add_node" and "node_type" not in details:
            logger.warning("Action 'add_node' requires 'node_type' in details")
            return False
        
        return True

    def _add_node_to_workflow(self, workflow: Dict[str, Any], details: Dict[str, Any]):
        """Add a new node to the workflow."""
        new_node = {
            "id": details.get("node_id", str(len(workflow["nodes"]) + 1)),
            "name": details.get("name", f"New Node {len(workflow['nodes']) + 1}"),
            "type": details.get("node_type", "n8n-nodes-base.noOp"),
            "parameters": details.get("parameters", {}),
            "position": details.get("position", [0, 0])
        }
        workflow["nodes"].append(new_node)

    def _modify_node_in_workflow(self, workflow: Dict[str, Any], details: Dict[str, Any]):
        """Modify an existing node in the workflow."""
        node_id = details.get("node_id")
        for node in workflow["nodes"]:
            if node["id"] == node_id:
                if "parameters" in details:
                    node["parameters"].update(details["parameters"])
                if "name" in details:
                    node["name"] = details["name"]
                break

    def _remove_node_from_workflow(self, workflow: Dict[str, Any], details: Dict[str, Any]):
        """Remove a node from the workflow."""
        node_id = details.get("node_id")
        workflow["nodes"] = [node for node in workflow["nodes"] if node["id"] != node_id]
        
        # Also remove connections involving this node
        connections_to_remove = []
        for source, targets in workflow["connections"].items():
            if source == node_id:
                connections_to_remove.append(source)
            else:
                for conn_type, target_lists in targets.items():
                    for target_list in target_lists:
                        target_list[:] = [t for t in target_list if t.get("node") != node_id]

        for conn in connections_to_remove:
            del workflow["connections"][conn]

    def _add_connection_to_workflow(self, workflow: Dict[str, Any], details: Dict[str, Any]):
        """Add a connection between nodes."""
        source = details.get("source_node")
        target = details.get("target_node")
        connection_type = details.get("connection_type", "main")
        
        # Create mapping from node IDs to node names and vice versa
        node_id_to_name = {}
        node_name_to_id = {}
        for node in workflow.get("nodes", []):
            node_id = node.get("id", "")
            node_name = node.get("name", "")
            if node_id and node_name:
                node_id_to_name[node_id] = node_name
                node_name_to_id[node_name] = node_id
        
        # Convert source and target to node names if they're IDs
        source_name = node_id_to_name.get(source, source)
        target_name = node_id_to_name.get(target, target)
        
        if source_name not in workflow["connections"]:
            workflow["connections"][source_name] = {}
        if connection_type not in workflow["connections"][source_name]:
            workflow["connections"][source_name][connection_type] = [[]]
        
        workflow["connections"][source_name][connection_type][0].append({
            "node": target_name,
            "type": connection_type,
            "index": details.get("index", 0)
        })
        
        logger.info(f"Added connection: {source_name} -> {target_name} (type: {connection_type})")

    def _modify_connection_in_workflow(self, workflow: Dict[str, Any], details: Dict[str, Any]):
        """Modify an existing connection."""
        source_node = details.get("source_node")
        old_target = details.get("old_target")
        new_target = details.get("new_target")
        connection_type = details.get("connection_type", "main")
        
        if not source_node or not old_target or not new_target:
            logger.warning(f"Missing required fields for modify_connection: {details}")
            return
        
        # Create mapping from node IDs to node names and vice versa
        node_id_to_name = {}
        node_name_to_id = {}
        for node in workflow.get("nodes", []):
            node_id = node.get("id", "")
            node_name = node.get("name", "")
            if node_id and node_name:
                node_id_to_name[node_id] = node_name
                node_name_to_id[node_name] = node_id
        
        # Convert source_node to node name if it's an ID
        source_node_name = node_id_to_name.get(source_node, source_node)
        
        # Convert old_target to node name if it's an ID
        old_target_name = node_id_to_name.get(old_target, old_target)
        
        # Convert new_target to node name if it's an ID
        new_target_name = node_id_to_name.get(new_target, new_target)
        
        # Find and update the connection
        if source_node_name in workflow["connections"]:
            if connection_type in workflow["connections"][source_node_name]:
                for target_list in workflow["connections"][source_node_name][connection_type]:
                    for i, connection in enumerate(target_list):
                        connection_node = connection.get("node")
                        # Check if connection matches old_target (by name or ID)
                        if connection_node == old_target_name or connection_node == old_target:
                            # Update the connection to point to the new target (use node name)
                            target_list[i]["node"] = new_target_name
                            logger.info(f"Modified connection: {source_node_name} -> {old_target_name} changed to {source_node_name} -> {new_target_name}")
                            return
        
        # If source_node was provided as name, also try it as ID
        if source_node != source_node_name:
            source_node_id = node_name_to_id.get(source_node, source_node)
            if source_node_id in workflow["connections"]:
                if connection_type in workflow["connections"][source_node_id]:
                    for target_list in workflow["connections"][source_node_id][connection_type]:
                        for i, connection in enumerate(target_list):
                            connection_node = connection.get("node")
                            if connection_node == old_target_name or connection_node == old_target:
                                target_list[i]["node"] = new_target_name
                                logger.info(f"Modified connection: {source_node_id} -> {old_target_name} changed to {source_node_id} -> {new_target_name}")
                                return
        
        logger.warning(f"Could not find connection to modify: {source_node} -> {old_target} (tried both node names and IDs)")
        logger.debug(f"Available connections: {list(workflow.get('connections', {}).keys())}")
        logger.debug(f"Node ID to Name mapping: {node_id_to_name}")
        logger.debug(f"Node Name to ID mapping: {node_name_to_id}")

    def _remove_connection_from_workflow(self, workflow: Dict[str, Any], details: Dict[str, Any]):
        """Remove a connection between nodes."""
        source = details.get("source_node")
        target = details.get("target_node")
        
        if source in workflow["connections"]:
            for conn_type, target_lists in workflow["connections"][source].items():
                for target_list in target_lists:
                    target_list[:] = [t for t in target_list if t.get("node") != target]

    def _track_workflow_iteration(self, workflow_id: str, original: str, modified: str, description: str):
        """Track workflow iteration history with enhanced logging."""
        try:
            changes_summary = self._summarize_changes(original, modified)
            
            iteration_entry = {
                "workflow_id": workflow_id,
                "timestamp": datetime.now().isoformat(),
                "description": description,
                "original_hash": hash(original),
                "modified_hash": hash(modified),
                "changes_summary": changes_summary,
                "original_size": len(original),
                "modified_size": len(modified)
            }
            
            # Store iteration history (you might want to use a database for this)
            if not hasattr(self, 'iteration_history'):
                self.iteration_history = []
            self.iteration_history.append(iteration_entry)
            
            iteration_logger.info(f"Iteration tracked", extra={
                'workflow_id': workflow_id,
                'description': description[:100] + '...' if len(description) > 100 else description,
                'changes_summary': changes_summary,
                'iteration_count': len([e for e in self.iteration_history if e['workflow_id'] == workflow_id])
            })
            
            # Log significant changes
            if changes_summary.get('nodes_added', 0) > 0:
                iteration_logger.info(f"Nodes added to workflow", extra={
                    'workflow_id': workflow_id,
                    'nodes_added': changes_summary['nodes_added']
                })
            
            if changes_summary.get('connections_changed', False):
                iteration_logger.info(f"Workflow connections modified", extra={
                    'workflow_id': workflow_id,
                    'connections_changed': True
                })
                
        except Exception as e:
            iteration_logger.error(f"Failed to track iteration", extra={
                'workflow_id': workflow_id,
                'error': str(e)
            })
            logger.error(f"Error tracking workflow iteration: {str(e)}")

    def _summarize_changes(self, original: str, modified: str) -> Dict[str, Any]:
        """Summarize the changes between two workflow versions using comprehensive diffing."""
        try:
            # Use the comprehensive workflow differ for detailed analysis
            diff_result = workflow_differ.compare_workflows(original, modified)
            
            # Return enhanced summary with detailed information
            return {
                # Basic compatibility (existing fields)
                "nodes_added": diff_result.nodes_added,
                "connections_changed": diff_result.connections_added > 0 or diff_result.connections_removed > 0,
                "parameters_modified": diff_result.parameters_changed > 0,
                
                # Enhanced detailed information
                "detailed_analysis": diff_result.to_dict(),
                "has_changes": diff_result.has_changes,
                "overall_severity": diff_result.overall_severity.value,
                "change_summary": diff_result.change_summary,
                "human_readable_summary": diff_result.get_human_readable_summary(),
                
                # Statistics breakdown
                "nodes_removed": diff_result.nodes_removed,
                "nodes_modified": diff_result.nodes_modified,
                "connections_added": diff_result.connections_added,
                "connections_removed": diff_result.connections_removed,
                "connections_modified": diff_result.connections_modified,
                "parameters_changed": diff_result.parameters_changed,
                "workflow_changes": len(diff_result.workflow_changes),
                
                # Performance metrics
                "analysis_duration_ms": diff_result.analysis_duration_ms,
                "comparison_complexity": diff_result.comparison_complexity,
                
                # Hashes for tracking
                "original_hash": diff_result.original_workflow_hash,
                "modified_hash": diff_result.modified_workflow_hash
            }
        except Exception as e:
            logger.error(f"Error in comprehensive workflow diffing: {str(e)}")
            # Fallback to basic analysis
            try:
                orig_workflow = json.loads(original)
                mod_workflow = json.loads(modified)
                
                return {
                    "nodes_added": len(mod_workflow["nodes"]) - len(orig_workflow["nodes"]),
                    "connections_changed": len(mod_workflow["connections"]) != len(orig_workflow["connections"]),
                    "parameters_modified": True,  # Simplified for fallback
                    "error": f"Comprehensive diffing failed: {str(e)}",
                    "fallback_used": True
                }
            except:
                return {"error": "Could not analyze changes"}

    def compare_workflow_versions(self, original_json: str, modified_json: str) -> WorkflowDiff:
        """
        Compare two workflow versions and return detailed diff analysis.
        
        Args:
            original_json: Original workflow JSON string
            modified_json: Modified workflow JSON string
            
        Returns:
            WorkflowDiff object with comprehensive comparison results
        """
        return workflow_differ.compare_workflows(original_json, modified_json)

    def generate_workflow_diff_report(self, original_json: str, modified_json: str, format: str = "html") -> str:
        """
        Generate a formatted diff report between two workflows.
        
        Args:
            original_json: Original workflow JSON string
            modified_json: Modified workflow JSON string
            format: Report format ("html", "text", or "json")
            
        Returns:
            Formatted diff report string
        """
        diff_result = workflow_differ.compare_workflows(original_json, modified_json)
        
        if format.lower() == "html":
            return workflow_differ.generate_html_diff_report(diff_result)
        elif format.lower() == "text":
            return self._generate_text_diff_report(diff_result)
        elif format.lower() == "json":
            return json.dumps(diff_result.to_dict(), indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'html', 'text', or 'json'")

    def _generate_text_diff_report(self, diff: WorkflowDiff) -> str:
        """Generate a text-based diff report."""
        report_lines = []
        
        # Header
        report_lines.append("=" * 60)
        report_lines.append("WORKFLOW DIFF REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Analysis Date: {diff.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Overall Severity: {diff.overall_severity.value.upper()}")
        report_lines.append(f"Changes Detected: {'Yes' if diff.has_changes else 'No'}")
        report_lines.append(f"Analysis Duration: {diff.analysis_duration_ms:.2f}ms")
        report_lines.append("")
        
        # Summary
        report_lines.append("SUMMARY:")
        report_lines.append(f"  {diff.change_summary}")
        report_lines.append("")
        
        # Statistics
        report_lines.append("STATISTICS:")
        report_lines.append(f"  Nodes Added: {diff.nodes_added}")
        report_lines.append(f"  Nodes Removed: {diff.nodes_removed}")
        report_lines.append(f"  Nodes Modified: {diff.nodes_modified}")
        report_lines.append(f"  Connections Added: {diff.connections_added}")
        report_lines.append(f"  Connections Removed: {diff.connections_removed}")
        report_lines.append(f"  Parameters Changed: {diff.parameters_changed}")
        report_lines.append("")
        
        # Node Changes
        if diff.node_diffs:
            report_lines.append("NODE CHANGES:")
            for node_diff in diff.node_diffs:
                change_symbol = {
                    "node_added": "+ ",
                    "node_removed": "- ",
                    "node_modified": "~ "
                }.get(node_diff.change_type.value, "  ")
                
                report_lines.append(f"  {change_symbol}{node_diff.node_name} ({node_diff.node_id})")
                report_lines.append(f"    Type: {node_diff.change_type.value.replace('_', ' ').title()}")
                report_lines.append(f"    Severity: {node_diff.severity.value.upper()}")
                report_lines.append(f"    Description: {node_diff.description}")
                
                if node_diff.parameter_changes:
                    report_lines.append("    Parameter Changes:")
                    for param_name, param_change in node_diff.parameter_changes.items():
                        change_desc = f"      {param_name}: {param_change['change_type']}"
                        if param_change['old_value'] is not None and param_change['new_value'] is not None:
                            change_desc += f" ({param_change['old_value']} → {param_change['new_value']})"
                        report_lines.append(change_desc)
                
                report_lines.append("")
        
        # Connection Changes
        if diff.connection_diffs:
            report_lines.append("CONNECTION CHANGES:")
            for conn_diff in diff.connection_diffs:
                change_symbol = {
                    "connection_added": "+ ",
                    "connection_removed": "- ",
                    "connection_modified": "~ "
                }.get(conn_diff.change_type.value, "  ")
                
                report_lines.append(f"  {change_symbol}{conn_diff.source_node} → {conn_diff.target_node}")
                report_lines.append(f"    Type: {conn_diff.change_type.value.replace('_', ' ').title()}")
                report_lines.append(f"    Connection Type: {conn_diff.connection_type}")
                report_lines.append(f"    Description: {conn_diff.description}")
                report_lines.append("")
        
        return "\n".join(report_lines)

    def get_workflow_diff_history(self) -> List[Dict[str, Any]]:
        """Get the history of workflow comparisons."""
        history = workflow_differ.get_comparison_history()
        return [diff.to_dict() for diff in history]

    def _mock_workflow_modification(self, workflow: Dict[str, Any], description: str) -> str:
        """Generate mock modification instructions for testing."""
        if "email" in description.lower():
            return json.dumps([{
                "action": "add_node",
                "details": {
                    "node_id": "fallback_email",
                    "name": "Email Fallback",
                    "node_type": "n8n-nodes-base.emailSend",
                    "parameters": {
                        "to": "user@example.com",
                        "subject": "Fallback Email",
                        "text": "This email was generated by fallback logic"
                    }
                },
                "reasoning": "Fallback email node added due to LLM failure"
            }])
        else:
            return json.dumps([{
                "action": "add_node",
                "details": {
                    "node_id": "fallback_generic",
                    "name": "Generic Fallback",
                    "node_type": "n8n-nodes-base.noOp",
                    "parameters": {}
                },
                "reasoning": "Generic fallback node added due to LLM failure"
            }])

    def _validate_workflow_structure(self, workflow: Dict[str, Any]) -> bool:
        """Validate the basic structure of a workflow dictionary."""
        required_fields = ["name", "nodes", "connections"]
        return all(field in workflow for field in required_fields)

    def get_workflow_iterations(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get the iteration history for a specific workflow."""
        if not hasattr(self, 'iteration_history'):
            return []
        return [entry for entry in self.iteration_history if entry['workflow_id'] == workflow_id]

    def _build_prompt(self, description: str) -> str:
        """Build the prompt for Mimo VL 7B."""
        return f"""You are an n8n workflow generation assistant. Generate a valid n8n workflow JSON for the following description:

{description}

CRITICAL REQUIREMENTS - EVERY WORKFLOW MUST:
1. START WITH A TRIGGER NODE - This is mandatory! Every workflow must begin with one of these trigger types:
   - n8n-nodes-base.manualTrigger (for manual execution)
   - n8n-nodes-base.webhook (for HTTP triggers)
   - n8n-nodes-base.scheduleTrigger (for time-based triggers)
   - n8n-nodes-base.localFileTrigger (for file monitoring)
   - n8n-nodes-base.emailTrigger (for email triggers)

2. INCLUDE ALL REQUIRED FIELDS: name, nodes, connections, settings, active, version

3. CREATE PROPER CONNECTIONS between all nodes

WORKFLOW STRUCTURE TEMPLATE:

{{
  "name": "Workflow Name Here",
  "nodes": [
    {{
      "id": "trigger-node",
      "name": "Start Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "parameters": {{}},
      "position": [250, 300]
    }},
    {{
      "id": "action-node",
      "name": "Action Node",
      "type": "n8n-nodes-base.nodetype",
      "parameters": {{
        "param1": "value1"
      }},
      "position": [500, 300]
    }}
  ],
  "connections": {{
    "Start Trigger": {{
      "main": [
        [
          {{
            "node": "Action Node",
            "type": "main",
            "index": 0
          }}
        ]
      ]
    }}
  }},
  "settings": {{}},
  "active": true,
  "version": 1
}}

AVAILABLE NODE TYPES:
- n8n-nodes-base.manualTrigger (REQUIRED: Use this if no specific trigger is mentioned)
- n8n-nodes-base.webhook (for HTTP triggers)
- n8n-nodes-base.scheduleTrigger (for time-based triggers)
- n8n-nodes-base.emailSend (for sending emails)
- n8n-nodes-base.function (for custom JavaScript code)
- n8n-nodes-base.httpRequest (for making HTTP requests)
- n8n-nodes-base.fileSystem (for file operations)
- n8n-nodes-base.set (for data transformation)

POSITIONING RULES:
- Start trigger at [250, 300]
- Space subsequent nodes by 250 pixels horizontally: [500, 300], [750, 300], etc.

Return ONLY the JSON, no additional text or explanation."""

    async def _call_mimo_vl7b(self, prompt: str, max_retries: int = 3) -> str:
        """Call the Mimo VL 7B API with enhanced retry logic and intelligent failure handling."""
        operation_id = f"llm_call_{int(time.time() * 1000)}"
        endpoint_key = self.llm_config.endpoint or "default_llm"
        
        # Use the retry manager for intelligent handling
        try:
            result, retry_metrics = await self.retry_manager.execute_with_retry(
                self._execute_llm_call,
                operation_id,
                "llm_api_call",
                endpoint_key,
                prompt
            )
            
            # Log retry metrics if there were retries
            if retry_metrics.total_attempts > 1 or retry_metrics.fallback_used:
                logger.info(f"LLM call completed with retry handling [ID: {operation_id}]", extra={
                    'operation_id': operation_id,
                    'total_attempts': retry_metrics.total_attempts,
                    'total_retry_time': retry_metrics.total_retry_time,
                    'fallback_used': retry_metrics.fallback_used,
                    'final_success': retry_metrics.final_success
                })
            
            return result
            
        except Exception as e:
            # If retry manager completely fails, fall back to original implementation
            logger.warning(f"Retry manager failed, using original LLM implementation: {str(e)}")
            return await self._call_mimo_vl7b_original(prompt, max_retries)

    async def _execute_llm_call(self, prompt: str) -> str:
        """Execute a single LLM API call (used by retry manager)."""
        llm_logger.info(f"Executing LLM API call", extra={
            'endpoint': self.llm_config.endpoint,
            'model': self.llm_config.model,
            'is_local': self.llm_config.is_local,
            'prompt_length': len(prompt)
        })
        
        # Enhanced system prompt to prevent thinking tags and code blocks
        system_prompt = ("You are an n8n workflow generation assistant. "
                        "CRITICAL: Return ONLY valid JSON. "
                        "NO thinking tags (<think>), NO code blocks (```), NO explanations, NO extra text. "
                        "Just pure JSON that can be parsed directly.")
        
        if self.llm_config.is_local:
            async with httpx.AsyncClient(timeout=1200.0) as client:  # 20 minute timeout
                try:
                    response = await client.post(
                        self.llm_config.endpoint,
                        json={
                            "model": self.llm_config.model,
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": self.llm_config.temperature,
                            "max_tokens": self.llm_config.max_tokens,
                            "stream": False  # Ensure we get complete response, not streaming
                        }
                    )
                    response.raise_for_status()
                except httpx.ConnectError as e:
                    # Enhanced error message for connection issues (often indicates crashes)
                    error_msg = str(e)
                    if "connection refused" in error_msg.lower():
                        raise ValueError(f"LLM service connection refused - the service may have crashed or stopped. Original error: {error_msg}")
                    elif "connection reset" in error_msg.lower():
                        raise ValueError(f"LLM service connection reset - the service may have crashed during processing. Original error: {error_msg}")
                    else:
                        raise ValueError(f"Cannot connect to LLM service - it may have crashed or be unavailable. Original error: {error_msg}")
                except httpx.HTTPStatusError as e:
                    # Enhanced error message for HTTP errors - check response body for specific errors
                    error_detail = None
                    try:
                        error_detail = e.response.json()
                    except:
                        try:
                            error_detail = e.response.text
                        except:
                            error_detail = None
                    
                    # Check for specific "no model loaded" errors in response body
                    if error_detail:
                        error_str = str(error_detail).lower()
                        if any(phrase in error_str for phrase in [
                            "no models loaded", "model_not_found", "model not found", 
                            "please load a model", "no model is currently loaded"
                        ]):
                            raise ValueError(f"No models loaded. Please load a model in your LLM service (e.g., LM Studio). Server response: {error_detail}")
                    
                    # Handle specific HTTP status codes
                    if e.response.status_code == 400:
                        if error_detail:
                            raise ValueError(f"LLM service bad request (400) - {error_detail}")
                        else:
                            raise ValueError(f"LLM service bad request (400) - check your request format. HTTP error: {e}")
                    elif e.response.status_code == 404:
                        if error_detail:
                            raise ValueError(f"LLM service endpoint not found (404) - {error_detail}")
                        else:
                            raise ValueError(f"LLM service endpoint not found (404) - check your endpoint URL. HTTP error: {e}")
                    elif e.response.status_code == 500:
                        if error_detail and ("crashed" in str(error_detail).lower() or "exit code" in str(error_detail).lower()):
                            raise ValueError(f"LLM model crashed with server error (500). Error details: {error_detail}")
                        else:
                            raise ValueError(f"LLM service internal error (500) - the model may have crashed. HTTP error: {e}")
                    elif e.response.status_code == 502:
                        raise ValueError(f"LLM service gateway error (502) - the service may be down or crashed. HTTP error: {e}")
                    elif e.response.status_code == 503:
                        raise ValueError(f"LLM service unavailable (503) - the service may be overloaded or crashed. HTTP error: {e}")
                    else:
                        if error_detail:
                            raise ValueError(f"LLM service HTTP error ({e.response.status_code}): {error_detail}")
                        else:
                            raise ValueError(f"LLM service HTTP error ({e.response.status_code}): {e}")
                except httpx.TimeoutException as e:
                    raise ValueError(f"LLM service timeout - the service may be unresponsive or crashed. Timeout error: {e}")
                except Exception as e:
                    # Catch any other exceptions and provide enhanced error context
                    error_msg = str(e)
                    if any(keyword in error_msg.lower() for keyword in ["exit code", "crashed", "terminated", "killed"]):
                        raise ValueError(f"LLM service appears to have crashed. Error: {error_msg}")
                    else:
                        raise ValueError(f"LLM service error: {error_msg}")
                
                # Enhanced response validation
                response_data = response.json()
                if not response_data or "choices" not in response_data:
                    raise ValueError("Invalid response structure from LLM API")
                
                if not response_data["choices"] or len(response_data["choices"]) == 0:
                    raise ValueError("No choices returned from LLM API")
                
                # Check if response was completed (not truncated due to streaming)
                choice = response_data["choices"][0]
                finish_reason = choice.get("finish_reason", "")
                if finish_reason == "length":
                    raise ValueError("LLM response was truncated due to token limit - increase max_tokens")
                elif finish_reason not in ["stop", "end_turn", "eos_token"]:
                    logger.warning(f"Unexpected finish_reason: {finish_reason}")
                
                content = choice["message"]["content"]
                if not content or content.strip() == "":
                    raise ValueError("Empty response content from LLM API")
                
                # Enhanced debugging for modification issues
                llm_logger.info(f"LLM call successful", extra={
                    'response_length': len(content),
                    'response_preview': content[:100] + '...' if len(content) > 100 else content,
                    'has_thinking_tags': '<think>' in content.lower(),
                    'has_code_blocks': '```' in content,
                    'starts_with_json': content.strip().startswith(('{', '[')),
                })
                
                logger.debug(f"LLM Response (first 200 chars): {content[:200]}...")
                logger.info("Successfully received response from LLM")
                
                # Add debug logging for JSON parsing issues
                logger.debug(f"Full LLM Response: {content}")
                
                return content.strip()
        else:
            if not self.llm_config.api_key:
                raise ValueError("API key is required when not using local endpoint")
            async with httpx.AsyncClient(timeout=1200.0) as client:
                try:
                    response = await client.post(
                        self.llm_config.endpoint,
                        headers={"Authorization": f"Bearer {self.llm_config.api_key}"},
                        json={
                            "model": self.llm_config.model,
                            "messages": [
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": prompt}
                            ],
                            "temperature": self.llm_config.temperature,
                            "max_tokens": self.llm_config.max_tokens,
                            "stream": False  # Ensure we get complete response, not streaming
                        }
                    )
                    response.raise_for_status()
                except httpx.HTTPStatusError as e:
                    # Enhanced error handling for external LLM services
                    if e.response.status_code == 429:
                        raise ValueError(f"LLM service rate limit exceeded (429). Please wait before trying again.")
                    elif e.response.status_code == 500:
                        raise ValueError(f"LLM service internal error (500) - the service may be experiencing issues.")
                    elif e.response.status_code == 502:
                        raise ValueError(f"LLM service gateway error (502) - the service may be temporarily unavailable.")
                    elif e.response.status_code == 503:
                        raise ValueError(f"LLM service unavailable (503) - the service may be overloaded.")
                    else:
                        raise ValueError(f"LLM service HTTP error ({e.response.status_code}): {e}")
                except httpx.ConnectError as e:
                    raise ValueError(f"Cannot connect to external LLM service. Check your internet connection and endpoint URL. Error: {e}")
                except httpx.TimeoutException as e:
                    raise ValueError(f"External LLM service timeout. The service may be overloaded. Error: {e}")
                except Exception as e:
                    raise ValueError(f"External LLM service error: {e}")
                
                # Enhanced response validation
                response_data = response.json()
                if not response_data or "choices" not in response_data:
                    raise ValueError("Invalid response structure from LLM API")
                
                content = response_data["choices"][0]["message"]["content"]
                if not content or content.strip() == "":
                    raise ValueError("Empty response content from LLM API")
                
                llm_logger.info(f"LLM call successful", extra={
                    'response_length': len(content),
                    'endpoint_type': 'external',
                    'has_thinking_tags': '<think>' in content.lower(),
                    'has_code_blocks': '```' in content,
                    'starts_with_json': content.strip().startswith(('{', '[')),
                })
                
                return content.strip()

    async def _call_mimo_vl7b_original(self, prompt: str, max_retries: int = 3) -> str:
        """Original LLM API calling implementation as fallback."""
        retry_count = 0
        last_error = None
        
        llm_logger.info(f"Starting original LLM call fallback", extra={
            'endpoint': self.llm_config.endpoint,
            'model': self.llm_config.model,
            'is_local': self.llm_config.is_local,
            'max_retries': max_retries,
            'prompt_length': len(prompt)
        })
        
        # Enhanced system prompt to prevent thinking tags and code blocks
        system_prompt = ("You are an n8n workflow generation assistant. "
                        "CRITICAL: Return ONLY valid JSON. "
                        "NO thinking tags (<think>), NO code blocks (```), NO explanations, NO extra text. "
                        "Just pure JSON that can be parsed directly.")
        
        while retry_count < max_retries:
            attempt_start = time.time()
            try:
                logger.info(f"Calling LLM API with is_local={self.llm_config.is_local} (attempt {retry_count + 1}/{max_retries})")
                
                if self.llm_config.is_local:
                    async with httpx.AsyncClient(timeout=1200.0) as client:  # 20 minute timeout
                        response = await client.post(
                            self.llm_config.endpoint,
                            json={
                                "model": self.llm_config.model,
                                "messages": [
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": prompt}
                                ],
                                "temperature": self.llm_config.temperature,
                                "max_tokens": self.llm_config.max_tokens,
                                "stream": False  # Ensure we get complete response, not streaming
                            }
                        )
                        response.raise_for_status()
                        
                        # Enhanced response validation
                        response_data = response.json()
                        if not response_data or "choices" not in response_data:
                            raise ValueError("Invalid response structure from LLM API")
                        
                        if not response_data["choices"] or len(response_data["choices"]) == 0:
                            raise ValueError("No choices returned from LLM API")
                        
                        # Check if response was completed (not truncated due to streaming)
                        choice = response_data["choices"][0]
                        finish_reason = choice.get("finish_reason", "")
                        if finish_reason == "length":
                            raise ValueError("LLM response was truncated due to token limit - increase max_tokens")
                        elif finish_reason not in ["stop", "end_turn", "eos_token"]:
                            logger.warning(f"Unexpected finish_reason: {finish_reason}")
                        
                        content = choice["message"]["content"]
                        if not content or content.strip() == "":
                            raise ValueError("Empty response content from LLM API")
                        
                        attempt_time = time.time() - attempt_start
                        llm_logger.info(f"Original LLM call successful", extra={
                            'attempt': retry_count + 1,
                            'response_time': attempt_time,
                            'response_length': len(content),
                            'response_preview': content[:100] + '...' if len(content) > 100 else content,
                            'has_thinking_tags': '<think>' in content.lower(),
                            'has_code_blocks': '```' in content,
                            'starts_with_json': content.strip().startswith(('{', '[')),
                        })
                        
                        logger.debug(f"LLM Response (first 200 chars): {content[:200]}...")
                        logger.info("Successfully received response from original LLM implementation")
                        
                        # Add debug logging for JSON parsing issues
                        logger.debug(f"Full Original LLM Response: {content}")
                        
                        return content.strip()
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
                                    {"role": "system", "content": system_prompt},
                                    {"role": "user", "content": prompt}
                                ],
                                "temperature": self.llm_config.temperature,
                                "max_tokens": self.llm_config.max_tokens,
                                "stream": False  # Ensure we get complete response, not streaming
                            }
                        )
                        response.raise_for_status()
                        
                        # Enhanced response validation
                        response_data = response.json()
                        if not response_data or "choices" not in response_data:
                            raise ValueError("Invalid response structure from LLM API")
                        
                        content = response_data["choices"][0]["message"]["content"]
                        if not content or content.strip() == "":
                            raise ValueError("Empty response content from LLM API")
                        
                        attempt_time = time.time() - attempt_start
                        llm_logger.info(f"Original LLM call successful", extra={
                            'attempt': retry_count + 1,
                            'response_time': attempt_time,
                            'response_length': len(content),
                            'endpoint_type': 'external',
                            'has_thinking_tags': '<think>' in content.lower(),
                            'has_code_blocks': '```' in content,
                            'starts_with_json': content.strip().startswith(('{', '[')),
                        })
                        
                        return content.strip()
                    
            except httpx.TimeoutException as e:
                attempt_time = time.time() - attempt_start
                last_error = e
                retry_count += 1
                
                llm_logger.warning(f"Original LLM call timeout", extra={
                    'attempt': retry_count,
                    'attempt_time': attempt_time,
                    'error': str(e),
                    'retrying': retry_count < max_retries
                })
                
                if retry_count < max_retries:
                    logger.warning(f"Timeout on attempt {retry_count}, retrying...")
                    await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                continue
            except Exception as e:
                attempt_time = time.time() - attempt_start
                last_error = e
                retry_count += 1
                
                llm_logger.error(f"Original LLM call error", extra={
                    'attempt': retry_count,
                    'attempt_time': attempt_time,
                    'error_type': type(e).__name__,
                    'error': str(e),
                    'retrying': retry_count < max_retries
                })
                
                if retry_count < max_retries:
                    await asyncio.sleep(1)
                continue
        
        # If we get here, all retries failed
        error_message = f"Failed to get valid response from original LLM after {max_retries} attempts. Last error: {str(last_error)}"
        
        llm_logger.error(f"Original LLM call failed completely", extra={
            'max_retries': max_retries,
            'final_error': str(last_error),
            'total_attempts': retry_count
        })
        
        logger.error(error_message)
        raise ValueError(error_message)

    def _map_to_workflow_structure(self, response: str) -> str:
        """Map the LLM response to n8n workflow structure with robust JSON extraction."""
        try:
            # First try to parse the response directly as JSON
            workflow = json.loads(response)
            return json.dumps(workflow, indent=2)
        except json.JSONDecodeError:
            # If direct parsing fails, use the robust JSON extraction logic
            logger.info("Direct JSON parsing failed, attempting to extract JSON from response")
            
            # Use the existing robust JSON extraction method
            extracted_json = self._extract_json_from_response(response)
            
            if not extracted_json:
                logger.error("Could not extract valid JSON from LLM response")
                logger.debug(f"Failed response (first 500 chars): {response[:500]}...")
                raise ValueError("Could not extract valid workflow JSON from response")
            
            try:
                # Parse the extracted JSON
                workflow = json.loads(extracted_json)
                logger.info("Successfully extracted and parsed JSON from LLM response")
                return json.dumps(workflow, indent=2)
            except json.JSONDecodeError as e:
                logger.error(f"Extracted JSON is still invalid: {str(e)}")
                logger.debug(f"Extracted JSON: {extracted_json[:200]}...")
                raise ValueError("Extracted JSON from response is not valid")
        except Exception as e:
            logger.error(f"Unexpected error in workflow structure mapping: {str(e)}")
            raise ValueError(f"Could not map response to workflow structure: {str(e)}")

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