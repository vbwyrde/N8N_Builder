"""
Error codes and message templates for validation errors.
"""
from enum import Enum
from typing import Dict, Any

class ValidationErrorCode(Enum):
    """Error codes for validation errors."""
    # Structure errors
    INVALID_WORKFLOW_STRUCTURE = "E001"
    MISSING_REQUIRED_FIELD = "E002"
    INVALID_FIELD_TYPE = "E003"
    INVALID_FIELD_VALUE = "E004"
    
    # Node errors
    INVALID_NODE_STRUCTURE = "E101"
    DUPLICATE_NODE_ID = "E102"
    INVALID_NODE_TYPE = "E103"
    MISSING_NODE_PARAMETER = "E104"
    INVALID_NODE_PARAMETER = "E105"
    
    # Connection errors
    INVALID_CONNECTION_STRUCTURE = "E201"
    NONEXISTENT_NODE = "E202"
    INVALID_CONNECTION_TYPE = "E203"
    CYCLE_DETECTED = "E204"
    SELF_CONNECTION = "E205"
    DUPLICATE_CONNECTION = "E206"
    
    # Logic errors
    INVALID_WORKFLOW_LOGIC = "E301"
    MISSING_START_NODE = "E302"
    MISSING_END_NODE = "E303"
    INCOMPATIBLE_NODE_TYPES = "E304"
    MULTIPLE_START_NODES = "E305"
    MULTIPLE_END_NODES = "E306"
    DISCONNECTED_PATH = "E307"
    INVALID_NODE_CONFIGURATION = "E308"
    
    # System errors
    VALIDATOR_ERROR = "E901"
    INTERNAL_ERROR = "E902"

class ValidationWarningCode(Enum):
    """Warning codes for validation warnings."""
    # Structure warnings
    DEPRECATED_FIELD = "W001"
    UNUSED_FIELD = "W002"
    UNKNOWN_FIELD = "W003"
    EMPTY_WORKFLOW = "W004"
    
    # Node warnings
    DEPRECATED_NODE_TYPE = "W101"
    UNUSED_NODE_PARAMETER = "W102"
    INEFFICIENT_NODE_CONFIG = "W103"
    MISSING_PARAMETERS = "W104"
    
    # Connection warnings
    REDUNDANT_CONNECTION = "W201"
    INEFFICIENT_CONNECTION = "W202"
    NO_INCOMING_CONNECTIONS = "W203"
    NO_OUTGOING_CONNECTIONS = "W204"
    
    # Logic warnings
    INEFFICIENT_WORKFLOW = "W301"
    POTENTIAL_PERFORMANCE_ISSUE = "W302"
    ISOLATED_NODE = "W303"

# Message templates for validation errors
ERROR_MESSAGES: Dict[str, str] = {
    # Structure errors
    ValidationErrorCode.INVALID_WORKFLOW_STRUCTURE.value: "Invalid workflow structure: {details}",
    ValidationErrorCode.MISSING_REQUIRED_FIELD.value: "Missing required field '{field}' in {location}",
    ValidationErrorCode.INVALID_FIELD_TYPE.value: "Invalid type for field '{field}' in {location}: expected {expected_type}, got {actual_type}",
    ValidationErrorCode.INVALID_FIELD_VALUE.value: "Invalid value for field '{field}' in {location}: {details}",
    
    # Node errors
    ValidationErrorCode.INVALID_NODE_STRUCTURE.value: "Invalid node structure: {details}",
    ValidationErrorCode.DUPLICATE_NODE_ID.value: "Duplicate node ID '{node_id}' found",
    ValidationErrorCode.INVALID_NODE_TYPE.value: "Invalid node type '{node_type}' for node '{node_id}'",
    ValidationErrorCode.MISSING_NODE_PARAMETER.value: "Missing required parameter '{parameter}' for node '{node_id}'",
    ValidationErrorCode.INVALID_NODE_PARAMETER.value: "Invalid parameter '{parameter}' for node '{node_id}': {details}",
    
    # Connection errors
    ValidationErrorCode.INVALID_CONNECTION_STRUCTURE.value: "Invalid connection structure: {details}",
    ValidationErrorCode.NONEXISTENT_NODE.value: "Connection references non-existent node '{node_id}'",
    ValidationErrorCode.INVALID_CONNECTION_TYPE.value: "Invalid connection type '{connection_type}' between nodes '{source}' and '{target}'",
    ValidationErrorCode.CYCLE_DETECTED.value: "Cycle detected in workflow: {path}",
    ValidationErrorCode.SELF_CONNECTION.value: "Self-connection detected for node '{node_id}'",
    ValidationErrorCode.DUPLICATE_CONNECTION.value: "Duplicate connection between nodes '{source}' and '{target}'",
    
    # Logic errors
    ValidationErrorCode.INVALID_WORKFLOW_LOGIC.value: "Invalid workflow logic: {details}",
    ValidationErrorCode.MISSING_START_NODE.value: "No start node found in workflow",
    ValidationErrorCode.MISSING_END_NODE.value: "No end node found in workflow",
    ValidationErrorCode.INCOMPATIBLE_NODE_TYPES.value: "Incompatible node types between '{source}' and '{target}'",
    ValidationErrorCode.MULTIPLE_START_NODES.value: "Multiple start nodes found: {nodes}",
    ValidationErrorCode.MULTIPLE_END_NODES.value: "Multiple end nodes found: {nodes}",
    ValidationErrorCode.DISCONNECTED_PATH.value: "Disconnected path detected between nodes '{source}' and '{target}'",
    ValidationErrorCode.INVALID_NODE_CONFIGURATION.value: "Invalid configuration for node '{node_id}': {details}",
    
    # System errors
    ValidationErrorCode.VALIDATOR_ERROR.value: "Validator error: {details}",
    ValidationErrorCode.INTERNAL_ERROR.value: "Internal validation error: {details}"
}

# Message templates for validation warnings
WARNING_MESSAGES: Dict[str, str] = {
    # Structure warnings
    ValidationWarningCode.DEPRECATED_FIELD.value: "Deprecated field '{field}' in {location}",
    ValidationWarningCode.UNUSED_FIELD.value: "Unused field '{field}' in {location}",
    ValidationWarningCode.UNKNOWN_FIELD.value: "Unknown field '{field}' in {location}",
    ValidationWarningCode.EMPTY_WORKFLOW.value: "Empty workflow: {details}",
    
    # Node warnings
    ValidationWarningCode.DEPRECATED_NODE_TYPE.value: "Deprecated node type '{node_type}' used in node '{node_id}'",
    ValidationWarningCode.UNUSED_NODE_PARAMETER.value: "Unused parameter '{parameter}' in node '{node_id}'",
    ValidationWarningCode.INEFFICIENT_NODE_CONFIG.value: "Inefficient configuration for node '{node_id}': {details}",
    ValidationWarningCode.MISSING_PARAMETERS.value: "Node '{node_id}' has no parameters",
    
    # Connection warnings
    ValidationWarningCode.REDUNDANT_CONNECTION.value: "Redundant connection between nodes '{source}' and '{target}'",
    ValidationWarningCode.INEFFICIENT_CONNECTION.value: "Inefficient connection between nodes '{source}' and '{target}': {details}",
    ValidationWarningCode.NO_INCOMING_CONNECTIONS.value: "Node '{node_id}' has no incoming connections",
    ValidationWarningCode.NO_OUTGOING_CONNECTIONS.value: "Node '{node_id}' has no outgoing connections",
    
    # Logic warnings
    ValidationWarningCode.INEFFICIENT_WORKFLOW.value: "Inefficient workflow structure: {details}",
    ValidationWarningCode.POTENTIAL_PERFORMANCE_ISSUE.value: "Potential performance issue: {details}",
    ValidationWarningCode.ISOLATED_NODE.value: "Isolated node '{node_id}' found"
}

def format_error_message(code: str, **kwargs: Any) -> str:
    """Format an error message using the template and provided arguments."""
    template = ERROR_MESSAGES.get(code, "Unknown error: {details}")
    return template.format(**kwargs)

def format_warning_message(code: str, **kwargs: Any) -> str:
    """Format a warning message using the template and provided arguments."""
    template = WARNING_MESSAGES.get(code, "Unknown warning: {details}")
    return template.format(**kwargs) 