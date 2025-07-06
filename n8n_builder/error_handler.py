#!/usr/bin/env python3
"""
Enhanced Error Handling System for N8N Builder
Provides detailed error categorization, user-friendly messages, and actionable guidance.

Task 1.1.3: Improve Error Messages and User Feedback
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union, Callable
from enum import Enum
import json
import re
import logging

logger = logging.getLogger(__name__)

class ErrorCategory(Enum):
    """Categories of errors for better user understanding."""
    INPUT_VALIDATION = "input_validation"
    WORKFLOW_STRUCTURE = "workflow_structure"
    LLM_COMMUNICATION = "llm_communication"
    JSON_PARSING = "json_parsing"
    NODE_CONFIGURATION = "node_configuration"
    CONNECTION_VALIDATION = "connection_validation"
    PERFORMANCE = "performance"
    SYSTEM = "system"

class ErrorSeverity(Enum):
    """Error severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ErrorDetail:
    """Detailed error information with user guidance."""
    category: ErrorCategory
    severity: ErrorSeverity
    title: str
    message: str
    user_guidance: str
    technical_details: Optional[str] = None
    fix_suggestions: Optional[List[str]] = None
    documentation_links: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None

@dataclass
class ValidationError:
    """Enhanced validation errors with specific guidance."""
    field: str
    issue: str
    current_value: Any
    expected_format: str
    fix_instruction: str
    example: Optional[str] = None

class EnhancedErrorHandler:
    """Enhanced error handling with user-friendly messages and guidance."""
    
    def __init__(self):
        self.error_patterns = self._initialize_error_patterns()
        self.validation_rules = self._initialize_validation_rules()
    
    def categorize_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> ErrorDetail:
        """Categorize an error and provide user-friendly guidance."""
        error_str = str(error).lower()
        error_type = type(error).__name__
        context = context or {}
        logger.debug(f"Categorizing error: {error_type} - {error_str}", extra={'operation_id': context.get('operation_id', 'unknown'), 'error_type': error_type})
        # Check for specific error patterns
        for pattern, handler in self.error_patterns.items():
            if pattern in error_str or pattern in error_type.lower():
                return handler(error, context)
        # Default fallback
        return self._create_generic_error(error, context)
    
    def validate_workflow_input(self, workflow_json: str, context: Optional[Dict[str, Any]] = None) -> List[ValidationError]:
        """Validate workflow input with detailed feedback."""
        errors = []
        context = context or {}
        # Check if it's valid JSON
        try:
            workflow = json.loads(workflow_json)
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON format in workflow input", extra={'operation_id': context.get('operation_id', 'unknown'), 'field': 'workflow_json', 'error_type': 'JSONDecodeError'})
            errors.append(ValidationError(
                field="workflow_json",
                issue="Invalid JSON format",
                current_value=workflow_json[:100] + "..." if len(workflow_json) > 100 else workflow_json,
                expected_format="Valid JSON object",
                fix_instruction="Check for missing quotes, commas, or brackets. Use a JSON validator.",
                example='{"name": "My Workflow", "nodes": [], "connections": {}}'
            ))
            return errors
        # Validate required fields
        required_fields = {
            'name': 'string',
            'nodes': 'array',
            'connections': 'object'
        }
        for field, expected_type in required_fields.items():
            if field not in workflow:
                logger.error(f"Missing required field: {field}", extra={'operation_id': context.get('operation_id', 'unknown'), 'field': field, 'error_type': 'MissingField'})
                errors.append(ValidationError(
                    field=field,
                    issue=f"Missing required field '{field}'",
                    current_value="missing",
                    expected_format=f"{expected_type}",
                    fix_instruction=f"Add the '{field}' field to your workflow JSON",
                    example=self._get_field_example(field)
                ))
            else:
                # Check type
                actual_type = self._get_json_type(workflow[field])
                if actual_type != expected_type:
                    logger.error(f"Wrong type for field: {field}", extra={'operation_id': context.get('operation_id', 'unknown'), 'field': field, 'error_type': 'TypeError'})
                    errors.append(ValidationError(
                        field=field,
                        issue=f"Wrong type for field '{field}'",
                        current_value=actual_type,
                        expected_format=expected_type,
                        fix_instruction=f"Change '{field}' to be a {expected_type}",
                        example=self._get_field_example(field)
                    ))
        # Validate nodes structure
        if 'nodes' in workflow and isinstance(workflow['nodes'], list):
            errors.extend(self._validate_nodes_structure(workflow['nodes']))
        # Validate connections structure
        if 'connections' in workflow and isinstance(workflow['connections'], dict):
            errors.extend(self._validate_connections_structure(workflow['connections'], workflow.get('nodes', [])))
        if errors:
            logger.error(f"Workflow input validation failed with {len(errors)} errors", extra={'operation_id': context.get('operation_id', 'unknown'), 'error_type': 'ValidationError'})
        return errors
    
    def validate_modification_description(self, description: str) -> List[ValidationError]:
        """Validate modification description with helpful guidance."""
        errors = []
        
        if not description or not description.strip():
            errors.append(ValidationError(
                field="modification_description",
                issue="Empty modification description",
                current_value="empty",
                expected_format="Clear description of changes needed",
                fix_instruction="Provide a clear description of what you want to change",
                example="Add error handling to the email sending node"
            ))
            return errors
        
        description = description.strip()
        
        # Check for minimal length
        if len(description) < 10:
            errors.append(ValidationError(
                field="modification_description",
                issue="Description too short",
                current_value=f"{len(description)} characters",
                expected_format="At least 10 characters",
                fix_instruction="Provide more detail about what changes you want",
                example="Add retry logic with exponential backoff to handle network failures"
            ))
        
        # Check for actionable content
        actionable_keywords = [
            'add', 'remove', 'change', 'modify', 'update', 'replace', 'insert', 
            'delete', 'improve', 'fix', 'enhance', 'configure', 'set', 'enable',
            'disable', 'connect', 'disconnect'
        ]
        
        if not any(keyword in description.lower() for keyword in actionable_keywords):
            errors.append(ValidationError(
                field="modification_description",
                issue="Description lacks clear action",
                current_value=description[:50] + "..." if len(description) > 50 else description,
                expected_format="Description with clear action words",
                fix_instruction="Use action words like 'add', 'remove', 'change', etc.",
                example="Add a delay node before the email sending to prevent rate limiting"
            ))
        
        return errors
    
    def create_llm_error_guidance(self, error: Exception, context: Dict[str, Any]) -> ErrorDetail:
        """Create specific guidance for LLM-related errors."""
        error_str = str(error).lower()
        
        if "connection" in error_str or "timeout" in error_str:
            return ErrorDetail(
                category=ErrorCategory.LLM_COMMUNICATION,
                severity=ErrorSeverity.ERROR,
                title="LLM Connection Failed",
                message="Unable to connect to the AI service for workflow modification",
                user_guidance="The AI service is temporarily unavailable. The system will use a fallback method to process your request.",
                technical_details=str(error),
                fix_suggestions=[
                    "Check if your LLM server (LM Studio) is running",
                    "Verify the server URL in your configuration",
                    "Try again in a few moments - temporary network issues may resolve",
                    "The system will provide a basic modification using built-in patterns"
                ],
                documentation_links=[
                    "https://lmstudio.ai/docs/local-server",
                    "Configuration guide: Check your config.py file"
                ],
                context=context
            )
        elif "404" in error_str or "not found" in error_str:
            return ErrorDetail(
                category=ErrorCategory.LLM_COMMUNICATION,
                severity=ErrorSeverity.ERROR,
                title="LLM Service Not Found",
                message="The AI service endpoint is not responding",
                user_guidance="Please check your LLM server configuration and ensure the service is running.",
                technical_details=str(error),
                fix_suggestions=[
                    "Start your LM Studio server",
                    "Load a model in LM Studio",
                    "Check the server endpoint URL in config.py",
                    "Verify the model name matches your configuration"
                ],
                documentation_links=[
                    "LM Studio setup guide",
                    "Model configuration documentation"
                ],
                context=context
            )
        else:
            return ErrorDetail(
                category=ErrorCategory.LLM_COMMUNICATION,
                severity=ErrorSeverity.WARNING,
                title="AI Service Error",
                message="The AI service encountered an error while processing your request",
                user_guidance="The system will attempt to process your request using alternative methods.",
                technical_details=str(error),
                fix_suggestions=[
                    "Try rephrasing your modification description",
                    "Break complex requests into smaller parts",
                    "Check if your modification description is clear and specific"
                ],
                context=context
            )
    
    def create_json_error_guidance(self, error: json.JSONDecodeError, context: Dict[str, Any]) -> ErrorDetail:
        """Create specific guidance for JSON parsing errors."""
        return ErrorDetail(
            category=ErrorCategory.JSON_PARSING,
            severity=ErrorSeverity.ERROR,
            title="Workflow JSON Format Error",
            message=f"The workflow JSON is not properly formatted (Line {error.lineno}, Column {error.colno})",
            user_guidance="Please check your workflow JSON for syntax errors and ensure it follows the correct format.",
            technical_details=f"JSON Error: {str(error)}",
            fix_suggestions=[
                f"Check line {error.lineno}, column {error.colno} for syntax errors",
                "Ensure all quotes are properly closed",
                "Check for missing commas between object properties",
                "Verify all brackets and braces are properly matched",
                "Use a JSON validator to check the format"
            ],
            documentation_links=[
                "JSON syntax guide: https://www.json.org/json-en.html",
                "Online JSON validator: https://jsonlint.com/"
            ],
            context=context
        )
    
    def create_validation_error_summary(self, validation_errors: List[ValidationError]) -> ErrorDetail:
        """Create a summary of validation errors with fix guidance."""
        if not validation_errors:
            return ErrorDetail(
                category=ErrorCategory.INPUT_VALIDATION,
                severity=ErrorSeverity.INFO,
                title="Validation Successful",
                message="All validation checks passed successfully",
                user_guidance="Your input is valid and ready for processing.",
                fix_suggestions=[],
                context={"validation_errors": []}
            )
        
        # Group errors by type
        error_groups = {}
        for error in validation_errors:
            if error.field not in error_groups:
                error_groups[error.field] = []
            error_groups[error.field].append(error)
        
        # Create summary message
        error_count = len(validation_errors)
        field_count = len(error_groups)
        
        summary_message = f"Found {error_count} validation issue{'s' if error_count != 1 else ''} in {field_count} field{'s' if field_count != 1 else ''}"
        
        # Create detailed guidance
        guidance_parts = []
        fix_suggestions = []
        
        for field, field_errors in error_groups.items():
            field_issues = [err.issue for err in field_errors]
            guidance_parts.append(f"• {field}: {', '.join(field_issues)}")
            fix_suggestions.extend([err.fix_instruction for err in field_errors])
        
        user_guidance = "Please fix the following issues:\n" + "\n".join(guidance_parts)
        
        return ErrorDetail(
            category=ErrorCategory.INPUT_VALIDATION,
            severity=ErrorSeverity.ERROR,
            title="Workflow Validation Failed",
            message=summary_message,
            user_guidance=user_guidance,
            fix_suggestions=fix_suggestions[:5],  # Limit to 5 suggestions
            context={"validation_errors": [err.__dict__ for err in validation_errors]}
        )
    
    def _initialize_error_patterns(self) -> Dict[str, Callable]:
        """Initialize error pattern matching."""
        return {
            'json': self._handle_json_error,
            'connection': self._handle_connection_error,
            'timeout': self._handle_timeout_error,
            'validationerror': self._handle_validation_error,
            'keyerror': self._handle_key_error,
            'typeerror': self._handle_type_error,
            'valueerror': self._handle_value_error
        }
    
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize validation rules."""
        return {
            'node_required_fields': ['id', 'name', 'type'],
            'connection_required_fields': ['node', 'type', 'index'],
            'workflow_required_fields': ['name', 'nodes', 'connections']
        }
    
    def _handle_json_error(self, error: Exception, context: Dict[str, Any]) -> ErrorDetail:
        """Handle JSON-related errors."""
        if isinstance(error, json.JSONDecodeError):
            return self.create_json_error_guidance(error, context)
        else:
            return ErrorDetail(
                category=ErrorCategory.JSON_PARSING,
                severity=ErrorSeverity.ERROR,
                title="JSON Processing Error",
                message="There was an error processing the JSON data",
                user_guidance="Please check that your workflow JSON is properly formatted.",
                technical_details=str(error),
                fix_suggestions=[
                    "Validate your JSON format",
                    "Check for proper quote usage",
                    "Ensure all brackets are matched"
                ],
                context=context
            )
    
    def _handle_connection_error(self, error: Exception, context: Dict[str, Any]) -> ErrorDetail:
        """Handle connection-related errors."""
        return self.create_llm_error_guidance(error, context)
    
    def _handle_timeout_error(self, error: Exception, context: Dict[str, Any]) -> ErrorDetail:
        """Handle timeout-related errors."""
        return ErrorDetail(
            category=ErrorCategory.PERFORMANCE,
            severity=ErrorSeverity.WARNING,
            title="Operation Timed Out",
            message="The operation took longer than expected to complete",
            user_guidance="The request may be too complex or the service may be busy. Try simplifying your request.",
            technical_details=str(error),
            fix_suggestions=[
                "Try breaking complex modifications into smaller parts",
                "Simplify your modification description",
                "Try again in a few moments",
                "Check if your workflow is very large and may need more time"
            ],
            context=context
        )
    
    def _handle_validation_error(self, error: Exception, context: Dict[str, Any]) -> ErrorDetail:
        """Handle validation-related errors."""
        return ErrorDetail(
            category=ErrorCategory.INPUT_VALIDATION,
            severity=ErrorSeverity.ERROR,
            title="Input Validation Failed",
            message="The provided input does not meet the required format",
            user_guidance="Please check your input data and ensure it matches the expected format.",
            technical_details=str(error),
            fix_suggestions=[
                "Check the format of your workflow JSON",
                "Ensure all required fields are present",
                "Verify data types match expectations"
            ],
            context=context
        )
    
    def _handle_key_error(self, error: Exception, context: Dict[str, Any]) -> ErrorDetail:
        """Handle missing key errors."""
        missing_key = str(error).strip("'\"")
        return ErrorDetail(
            category=ErrorCategory.WORKFLOW_STRUCTURE,
            severity=ErrorSeverity.ERROR,
            title="Missing Required Field",
            message=f"Required field '{missing_key}' is missing from the workflow",
            user_guidance=f"Please add the '{missing_key}' field to your workflow JSON.",
            technical_details=str(error),
            fix_suggestions=[
                f"Add the '{missing_key}' field to your workflow",
                "Check the workflow structure documentation",
                "Verify all required fields are present"
            ],
            context=context
        )
    
    def _handle_type_error(self, error: Exception, context: Dict[str, Any]) -> ErrorDetail:
        """Handle type-related errors."""
        return ErrorDetail(
            category=ErrorCategory.WORKFLOW_STRUCTURE,
            severity=ErrorSeverity.ERROR,
            title="Data Type Mismatch",
            message="A field has the wrong data type",
            user_guidance="Please check that all fields have the correct data types (string, number, array, object).",
            technical_details=str(error),
            fix_suggestions=[
                "Check field data types in your workflow JSON",
                "Ensure strings are quoted",
                "Verify arrays use square brackets []",
                "Ensure objects use curly braces {}"
            ],
            context=context
        )
    
    def _handle_value_error(self, error: Exception, context: Dict[str, Any]) -> ErrorDetail:
        """Handle value-related errors."""
        return ErrorDetail(
            category=ErrorCategory.INPUT_VALIDATION,
            severity=ErrorSeverity.ERROR,
            title="Invalid Value",
            message="One or more values are invalid",
            user_guidance="Please check that all values in your workflow are valid and properly formatted.",
            technical_details=str(error),
            fix_suggestions=[
                "Check for invalid characters in field values",
                "Ensure numeric values are properly formatted",
                "Verify required fields are not empty"
            ],
            context=context
        )
    
    def _create_generic_error(self, error: Exception, context: Dict[str, Any]) -> ErrorDetail:
        """Create a generic error detail."""
        return ErrorDetail(
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.ERROR,
            title="Unexpected Error",
            message="An unexpected error occurred while processing your request",
            user_guidance="Please try again. If the problem persists, check your input data for any issues.",
            technical_details=str(error),
            fix_suggestions=[
                "Try your request again",
                "Check your input data for any obvious issues",
                "Simplify your request if it's complex",
                "Report this error if it continues to occur"
            ],
            context=context
        )
    
    def _validate_nodes_structure(self, nodes: List[Dict[str, Any]]) -> List[ValidationError]:
        """Validate nodes structure."""
        errors = []
        
        if not nodes:
            errors.append(ValidationError(
                field="nodes",
                issue="Workflow should have at least one node",
                current_value="empty array",
                expected_format="Array with at least one node",
                fix_instruction="Add at least one node to your workflow",
                example='[{"id": "1", "name": "Trigger", "type": "n8n-nodes-base.manualTrigger"}]'
            ))
            return errors
        
        required_node_fields = ['id', 'name', 'type']
        
        for i, node in enumerate(nodes):
            if not isinstance(node, dict):
                errors.append(ValidationError(
                    field=f"nodes[{i}]",
                    issue="Node must be an object",
                    current_value=type(node).__name__,
                    expected_format="object",
                    fix_instruction=f"Make sure node at index {i} is a JSON object",
                    example='{"id": "1", "name": "My Node", "type": "n8n-nodes-base.manualTrigger"}'
                ))
                continue
            
            for field in required_node_fields:
                if field not in node:
                    errors.append(ValidationError(
                        field=f"nodes[{i}].{field}",
                        issue=f"Missing required field '{field}'",
                        current_value="missing",
                        expected_format="string",
                        fix_instruction=f"Add '{field}' field to node {i}",
                        example=f'"{field}": "example_value"'
                    ))
        
        return errors
    
    def _validate_connections_structure(self, connections: Dict[str, Any], nodes: List[Dict[str, Any]]) -> List[ValidationError]:
        """Validate connections structure."""
        errors = []
        
        # Get valid node names
        valid_node_names = {node.get('name') for node in nodes if isinstance(node, dict) and 'name' in node}
        
        for source_node, connection_data in connections.items():
            if source_node not in valid_node_names:
                errors.append(ValidationError(
                    field=f"connections.{source_node}",
                    issue=f"Connection references non-existent node '{source_node}'",
                    current_value=source_node,
                    expected_format="Valid node name",
                    fix_instruction=f"Ensure node '{source_node}' exists in the nodes array or remove this connection",
                    example="Use exact node name from nodes array"
                ))
        
        return errors
    
    def _get_json_type(self, value: Any) -> str:
        """Get JSON type name for a value."""
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "number"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        elif value is None:
            return "null"
        else:
            return "unknown"
    
    def _get_field_example(self, field: str) -> str:
        """Get example value for a field."""
        examples = {
            'name': '"My Workflow"',
            'nodes': '[{"id": "1", "name": "Trigger", "type": "n8n-nodes-base.manualTrigger"}]',
            'connections': '{"Trigger": {"main": [["Next Node", 0]]}}',
            'id': '"1"',
            'type': '"n8n-nodes-base.manualTrigger"'
        }
        return examples.get(field, f'"{field}_value"') 