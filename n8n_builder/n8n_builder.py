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

from .config import config
from .error_handler import EnhancedErrorHandler, ErrorDetail, ValidationError as EValidationError
from .validators import EdgeCaseValidator, EdgeCaseValidationResult
from .performance_optimizer import performance_optimizer, PerformanceMetrics

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
validation_logger.setLevel(logging.INFO)
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
        """Initialize N8N Builder with enhanced error handling and performance optimization."""
        self.documentation_path = Path("NN_Builder.md")
        self.node_types: Dict[str, NodeTypeInfo] = {}
        self.workflow_patterns: Dict[str, WorkflowPattern] = {}
        self.feedback_log: List[WorkflowFeedback] = []
        self.llm_config = config.mimo_llm
        logger.info(f"N8N Builder LLM Config: endpoint={self.llm_config.endpoint}, is_local={self.llm_config.is_local}, model={self.llm_config.model}")
        self.iteration_history = {}
        
        # Initialize enhanced error handling
        self.error_handler = EnhancedErrorHandler()
        
        # Initialize edge case validator
        self.edge_case_validator = EdgeCaseValidator()
        
        # Initialize performance optimizer (global instance)
        self.performance_optimizer = performance_optimizer
        logger.info("Performance optimizer initialized for large workflow processing")
        
        try:
            self.initialize_builder()
        except Exception as e:
            error_detail = self.error_handler.categorize_error(e, {"context": "initialization"})
            logger.error(f"Error initializing N8N Builder: {error_detail.title} - {error_detail.message}")
            if error_detail.fix_suggestions:
                logger.info(f"Suggestions: {'; '.join(error_detail.fix_suggestions)}")

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

            # 4. Validate connections
            if not isinstance(workflow.get("connections"), dict):
                validation_errors.append("Connections must be a dictionary")
            else:
                connection_errors = self._validate_connections(workflow["connections"], node_ids)
                validation_errors.extend(connection_errors)

            # 5. Validate settings (optional but should be dict if present)
            if "settings" in workflow and not isinstance(workflow["settings"], dict):
                validation_errors.append("Settings must be a dictionary")

            # 6. Validate version (optional but should be number if present)
            if "version" in workflow:
                if not isinstance(workflow["version"], (int, float)):
                    validation_errors.append("Version must be a number")

            # 7. Check workflow logic
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

    def _validate_connections(self, connections: Dict[str, Any], valid_node_ids: set) -> List[str]:
        """Validate workflow connections."""
        errors = []
        
        # Build a set of valid node identifiers (both IDs and names)
        valid_node_identifiers = valid_node_ids.copy()
        
        for source_node, connection_data in connections.items():
            # N8N connections can use either node IDs or node names
            # So we need to be more flexible in validation
            if not isinstance(connection_data, dict):
                errors.append(f"Connection data for '{source_node}' must be a dictionary")
                continue
            
            for connection_type, target_lists in connection_data.items():
                if not isinstance(target_lists, list):
                    errors.append(f"Connection type '{connection_type}' for '{source_node}' must be a list")
                    continue
                
                for i, target_list in enumerate(target_lists):
                    if not isinstance(target_list, list):
                        errors.append(f"Target list {i} for '{source_node}' must be a list")
                        continue
                    
                    for j, target in enumerate(target_list):
                        if not isinstance(target, dict):
                            errors.append(f"Target {j} in list {i} for '{source_node}' must be a dictionary")
                            continue
                        
                        if "node" not in target:
                            errors.append(f"Target {j} in list {i} for '{source_node}' missing 'node' field")
                            continue
                        
                        # Note: We're not validating node existence here since N8N can use names or IDs
                        # and the structure varies. This is a structural validation, not a semantic one.
        
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
            if any(trigger_word in node_type for trigger_word in ["trigger", "webhook", "schedule"]):
                trigger_nodes.append(node)
        
        if not trigger_nodes:
            errors.append("Workflow should have at least one trigger node")
        
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
        
        if isolated_nodes and len(nodes) > 1:
            errors.append(f"Isolated nodes found (not connected): {', '.join(isolated_nodes)}")
        
        return errors

    def _log_validation_errors(self, validation_errors: List[str]) -> bool:
        """Log validation errors with detailed information."""
        if validation_errors:
            validation_logger.error(f"Workflow validation error: {validation_errors[0]}")
            validation_logger.error(f"Total validation errors: {len(validation_errors)}")
            
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
        
        iteration_logger.info(f"Starting workflow modification [ID: {metrics.operation_id}]", extra={
            'operation_id': metrics.operation_id,
            'workflow_id': metrics.workflow_id,
            'modification_description': modification_description[:100] + '...' if len(modification_description) > 100 else modification_description
        })
        
        # Enhanced input validation with detailed feedback
        validation_start = time.time()
        
        # Validate workflow JSON
        workflow_validation_errors = self.error_handler.validate_workflow_input(existing_workflow_json)
        if workflow_validation_errors:
            validation_error_detail = self.error_handler.create_validation_error_summary(workflow_validation_errors)
            metrics.finish(success=False, error_message=validation_error_detail.message)
            
            iteration_logger.error(f"Workflow validation failed [ID: {metrics.operation_id}]: {validation_error_detail.title}")
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
            
            iteration_logger.error(f"Description validation failed [ID: {metrics.operation_id}]: {description_error_detail.title}")
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
                
                iteration_logger.error(f"Edge case validation failed [ID: {metrics.operation_id}]: {len(edge_case_result.errors)} errors detected")
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
            iteration_logger.warning(f"Edge case validation encountered an error [ID: {metrics.operation_id}]: {str(e)}")
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
                    category="workflow_structure",
                    severity="error",
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
                iteration_logger.error(f"Workflow structure validation failed [ID: {metrics.operation_id}]: {error_detail.title}")
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
                
                iteration_logger.warning(f"LLM failed, using mock response [ID: {metrics.operation_id}]")
                modifications_response = self._mock_workflow_modification(existing_workflow, modification_description)
                metrics.llm_calls_count = 0
                metrics.llm_total_time = llm_error_time

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
            
            iteration_logger.error(f"Workflow modification failed [ID: {metrics.operation_id}]: {error_detail.title}")
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
            
            iteration_logger.error(f"Workflow validation failed [ID: {metrics.operation_id}]: {validation_error_detail.title}")
            iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {validation_error_detail.user_guidance}")
            if validation_error_detail.fix_suggestions:
                iteration_logger.info(f"Fix suggestions [ID: {metrics.operation_id}]: {'; '.join(validation_error_detail.fix_suggestions)}")
            
            performance_logger.info(f"Iterate operation failed due to workflow validation", extra=metrics.to_dict())
            return existing_workflow_json
        
        # Validate feedback from testing
        if not feedback_from_testing or not feedback_from_testing.strip():
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
            metrics.finish(success=False, error_message=error_detail.message)
            iteration_logger.error(f"Feedback validation failed [ID: {metrics.operation_id}]: {error_detail.title}")
            iteration_logger.info(f"User guidance [ID: {metrics.operation_id}]: {error_detail.user_guidance}")
            performance_logger.info(f"Iterate operation failed due to feedback validation", extra=metrics.to_dict())
            return existing_workflow_json
        
        # Validate feedback length and quality
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
                
                iteration_logger.error(f"Edge case validation failed [ID: {metrics.operation_id}]: {len(edge_case_result.errors)} errors detected")
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
            iteration_logger.warning(f"Edge case validation encountered an error [ID: {metrics.operation_id}]: {str(e)}")
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
                
                iteration_logger.error(f"Iteration modification failed [ID: {metrics.operation_id}]: {error_detail.title}")
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
            
            iteration_logger.error(f"Workflow iteration failed [ID: {metrics.operation_id}]: {error_detail.title}")
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
        
        # Analyze nodes
        for node in workflow.get("nodes", []):
            node_type = node.get("type", "unknown")
            analysis["node_types"].append(node_type)
            
            # Categorize nodes
            if "trigger" in node_type.lower() or "webhook" in node_type.lower() or node_type.endswith("Trigger"):
                analysis["triggers"].append(node)
            else:
                analysis["actions"].append(node)
        
        # Analyze data flow
        for source_node, connections in analysis["connections"].items():
            if isinstance(connections, dict):
                for connection_type, targets in connections.items():
                    if isinstance(targets, list):
                        for target_list in targets:
                            if isinstance(target_list, list):
                                for target in target_list:
                                    if isinstance(target, dict):
                                        analysis["data_flow"].append({
                                            "from": source_node,
                                            "to": target.get("node"),
                                            "type": connection_type
                                        })
        
        return analysis

    def _build_modification_prompt(self, existing_workflow: Dict[str, Any], 
                                 analysis: Dict[str, Any], modification_description: str) -> str:
        """Build a prompt for modifying an existing workflow."""
        return f"""You are an n8n workflow modification assistant. 

IMPORTANT: Respond ONLY with valid JSON modification instructions. Do not include explanations, thinking processes, or any text outside the JSON.

EXISTING WORKFLOW ANALYSIS:
- Node count: {analysis['node_count']}
- Node types: {', '.join(analysis['node_types'])}
- Triggers: {len(analysis['triggers'])}
- Actions: {len(analysis['actions'])}
- Data flow connections: {len(analysis['data_flow'])}

CURRENT WORKFLOW JSON:
{json.dumps(existing_workflow, indent=2)}

MODIFICATION REQUEST:
{modification_description}

OUTPUT FORMAT: Return ONLY a JSON array of modification objects with this exact structure:
[
  {{
    "action": "add_node",
    "details": {{
      "node_id": "3",
      "name": "Database Log",
      "node_type": "n8n-nodes-base.postgres",
      "parameters": {{
        "operation": "insert",
        "table": "email_logs"
      }},
      "position": [680, 300]
    }},
    "reasoning": "Adds database logging as requested"
  }}
]

Valid actions: add_node, modify_node, remove_node, add_connection, modify_connection, remove_connection

CRITICAL: Return ONLY the JSON array, no other text, no thinking tags, no explanations."""

    def _apply_workflow_modifications(self, workflow: Dict[str, Any], modifications_response: str) -> Dict[str, Any]:
        """Apply modifications to a workflow based on LLM response with enhanced error handling."""
        try:
            logger.debug(f"Attempting to parse modifications response: {modifications_response[:200]}...")
            
            # First, try to clean and extract JSON from the response
            cleaned_response = self._extract_json_from_response(modifications_response)
            if not cleaned_response:
                logger.warning("No valid JSON found in LLM response, returning original workflow")
                return workflow
            
            # Parse modification instructions
            modifications = json.loads(cleaned_response)
            if not isinstance(modifications, list):
                modifications = [modifications]
            
            # Validate modifications structure
            valid_modifications = []
            for i, mod in enumerate(modifications):
                if self._validate_modification_structure(mod):
                    valid_modifications.append(mod)
                else:
                    logger.warning(f"Skipping invalid modification {i}: {mod}")
            
            if not valid_modifications:
                logger.warning("No valid modifications found, returning original workflow")
                return workflow
            
            # Apply modifications to a deep copy of the workflow
            modified_workflow = json.loads(json.dumps(workflow))  # Deep copy
            
            modifications_applied = 0
            for mod in valid_modifications:
                try:
                    action = mod.get("action")
                    details = mod.get("details", {})
                    
                    if action == "add_node":
                        self._add_node_to_workflow(modified_workflow, details)
                        modifications_applied += 1
                    elif action == "modify_node":
                        self._modify_node_in_workflow(modified_workflow, details)
                        modifications_applied += 1
                    elif action == "remove_node":
                        self._remove_node_from_workflow(modified_workflow, details)
                        modifications_applied += 1
                    elif action == "add_connection":
                        self._add_connection_to_workflow(modified_workflow, details)
                        modifications_applied += 1
                    elif action == "modify_connection":
                        self._modify_connection_in_workflow(modified_workflow, details)
                        modifications_applied += 1
                    elif action == "remove_connection":
                        self._remove_connection_from_workflow(modified_workflow, details)
                        modifications_applied += 1
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

    def _extract_json_from_response(self, response: str) -> str:
        """Extract valid JSON from LLM response with multiple strategies."""
        if not response or response.strip() == "":
            return ""
        
        response = response.strip()
        
        # Strategy 0: Remove thinking tags if present
        import re
        
        # Remove <think>...</think> blocks completely
        think_pattern = r'<think>.*?</think>'
        response_no_think = re.sub(think_pattern, '', response, flags=re.DOTALL | re.IGNORECASE)
        response_no_think = response_no_think.strip()
        
        if response_no_think:
            response = response_no_think
        
        # Strategy 1: Response is already valid JSON
        try:
            json.loads(response)
            return response
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Look for JSON between ```json and ``` blocks
        json_block_pattern = r'```(?:json)?\s*(.*?)\s*```'
        matches = re.findall(json_block_pattern, response, re.DOTALL | re.IGNORECASE)
        for match in matches:
            try:
                json.loads(match.strip())
                return match.strip()
            except json.JSONDecodeError:
                continue
        
        # Strategy 3: Look for JSON-like content between curly braces
        brace_pattern = r'\{.*\}'
        matches = re.findall(brace_pattern, response, re.DOTALL)
        for match in matches:
            try:
                json.loads(match)
                return match
            except json.JSONDecodeError:
                continue
        
        # Strategy 4: Look for array-like content between square brackets
        bracket_pattern = r'\[.*\]'
        matches = re.findall(bracket_pattern, response, re.DOTALL)
        for match in matches:
            try:
                json.loads(match)
                return match
            except json.JSONDecodeError:
                continue
        
        # Strategy 5: Try to find JSON after any text - look for first { or [
        for start_char in ['{', '[']:
            start_pos = response.find(start_char)
            if start_pos >= 0:
                # Find the matching closing bracket
                if start_char == '{':
                    end_char = '}'
                else:
                    end_char = ']'
                
                bracket_count = 0
                for i, char in enumerate(response[start_pos:], start_pos):
                    if char == start_char:
                        bracket_count += 1
                    elif char == end_char:
                        bracket_count -= 1
                        if bracket_count == 0:
                            potential_json = response[start_pos:i+1]
                            try:
                                json.loads(potential_json)
                                return potential_json
                            except json.JSONDecodeError:
                                break
        
        logger.warning(f"Could not extract valid JSON from response: {response[:200]}...")
        return ""

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
        
        if source not in workflow["connections"]:
            workflow["connections"][source] = {}
        if connection_type not in workflow["connections"][source]:
            workflow["connections"][source][connection_type] = [[]]
        
        workflow["connections"][source][connection_type][0].append({
            "node": target,
            "type": connection_type,
            "index": details.get("index", 0)
        })

    def _modify_connection_in_workflow(self, workflow: Dict[str, Any], details: Dict[str, Any]):
        """Modify an existing connection."""
        # Implementation for modifying connections
        pass

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
        """Summarize the changes between two workflow versions."""
        try:
            orig_workflow = json.loads(original)
            mod_workflow = json.loads(modified)
            
            return {
                "nodes_added": len(mod_workflow["nodes"]) - len(orig_workflow["nodes"]),
                "connections_changed": len(mod_workflow["connections"]) != len(orig_workflow["connections"]),
                "parameters_modified": True  # Simplified for now
            }
        except:
            return {"error": "Could not analyze changes"}

    def _mock_workflow_modification(self, workflow: Dict[str, Any], description: str) -> str:
        """Generate mock modification instructions for testing."""
        if "email" in description.lower():
            return json.dumps([{
                "action": "add_node",
                "details": {
                    "node_id": str(len(workflow["nodes"]) + 1),
                    "name": "Send Email",
                    "node_type": "n8n-nodes-base.emailSend",
                    "parameters": {
                        "to": "user@example.com",
                        "subject": "Workflow Update",
                        "text": "Workflow has been updated"
                    }
                }
            }])
        else:
            return json.dumps([{
                "action": "add_node", 
                "details": {
                    "node_id": str(len(workflow["nodes"]) + 1),
                    "name": "No Op",
                    "node_type": "n8n-nodes-base.noOp",
                    "parameters": {}
                }
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

The workflow should:
1. Use appropriate n8n nodes for the task
2. Follow n8n best practices
3. Include proper error handling
4. Be well-documented with comments

Return only the workflow JSON, no additional text or explanation."""

    async def _call_mimo_vl7b(self, prompt: str, max_retries: int = 3) -> str:
        """Call the Mimo VL 7B API with enhanced error handling."""
        retry_count = 0
        last_error = None
        
        llm_logger.info(f"Starting LLM call", extra={
            'endpoint': self.llm_config.endpoint,
            'model': self.llm_config.model,
            'is_local': self.llm_config.is_local,
            'max_retries': max_retries,
            'prompt_length': len(prompt)
        })
        
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
                                    {"role": "system", "content": "You are an n8n workflow generation assistant. Always respond with valid JSON only."},
                                    {"role": "user", "content": prompt}
                                ],
                                "temperature": self.llm_config.temperature,
                                "max_tokens": self.llm_config.max_tokens
                            }
                        )
                        response.raise_for_status()
                        
                        # Enhanced response validation
                        response_data = response.json()
                        if not response_data or "choices" not in response_data:
                            raise ValueError("Invalid response structure from LLM API")
                        
                        if not response_data["choices"] or len(response_data["choices"]) == 0:
                            raise ValueError("No choices returned from LLM API")
                        
                        content = response_data["choices"][0]["message"]["content"]
                        if not content or content.strip() == "":
                            raise ValueError("Empty response content from LLM API")
                        
                        attempt_time = time.time() - attempt_start
                        llm_logger.info(f"LLM call successful", extra={
                            'attempt': retry_count + 1,
                            'response_time': attempt_time,
                            'response_length': len(content),
                            'response_preview': content[:100] + '...' if len(content) > 100 else content
                        })
                        
                        logger.debug(f"LLM Response (first 200 chars): {content[:200]}...")
                        logger.info("Successfully received response from LLM")
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
                                    {"role": "system", "content": "You are an n8n workflow generation assistant. Always respond with valid JSON only."},
                                    {"role": "user", "content": prompt}
                                ],
                                "temperature": self.llm_config.temperature,
                                "max_tokens": self.llm_config.max_tokens
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
                        llm_logger.info(f"LLM call successful", extra={
                            'attempt': retry_count + 1,
                            'response_time': attempt_time,
                            'response_length': len(content),
                            'endpoint_type': 'external'
                        })
                        
                        return content.strip()
                    
            except httpx.TimeoutException as e:
                attempt_time = time.time() - attempt_start
                last_error = e
                retry_count += 1
                
                llm_logger.warning(f"LLM call timeout", extra={
                    'attempt': retry_count,
                    'attempt_time': attempt_time,
                    'error': str(e),
                    'retrying': retry_count < max_retries
                })
                
                if retry_count < max_retries:
                    logger.warning(f"Timeout on attempt {retry_count}, retrying...")
                    await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                continue
            except httpx.HTTPStatusError as e:
                attempt_time = time.time() - attempt_start
                
                llm_logger.error(f"LLM HTTP error", extra={
                    'attempt': retry_count + 1,
                    'attempt_time': attempt_time,
                    'status_code': e.response.status_code,
                    'response_text': e.response.text[:200],
                    'retrying': retry_count + 1 < max_retries
                })
                
                logger.error(f"HTTP error on attempt {retry_count + 1}: {e.response.status_code} - {e.response.text}")
                last_error = e
                retry_count += 1
                if retry_count < max_retries:
                    await asyncio.sleep(2)
                continue
            except ValueError as e:
                attempt_time = time.time() - attempt_start
                
                llm_logger.error(f"LLM response validation error", extra={
                    'attempt': retry_count + 1,
                    'attempt_time': attempt_time,
                    'error': str(e),
                    'retrying': retry_count + 1 < max_retries
                })
                
                logger.error(f"Response validation error on attempt {retry_count + 1}: {str(e)}")
                last_error = e
                retry_count += 1
                if retry_count < max_retries:
                    await asyncio.sleep(1)
                continue
            except Exception as e:
                attempt_time = time.time() - attempt_start
                
                llm_logger.error(f"LLM unexpected error", extra={
                    'attempt': retry_count + 1,
                    'attempt_time': attempt_time,
                    'error_type': type(e).__name__,
                    'error': str(e),
                    'retrying': retry_count + 1 < max_retries
                })
                
                logger.error(f"Unexpected error on attempt {retry_count + 1}: {str(e)}", exc_info=True)
                last_error = e
                retry_count += 1
                if retry_count < max_retries:
                    await asyncio.sleep(1)
                continue
        
        # If we get here, all retries failed
        error_message = f"Failed to get valid response from LLM after {max_retries} attempts. Last error: {str(last_error)}"
        
        llm_logger.error(f"LLM call failed completely", extra={
            'max_retries': max_retries,
            'final_error': str(last_error),
            'total_attempts': retry_count
        })
        
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