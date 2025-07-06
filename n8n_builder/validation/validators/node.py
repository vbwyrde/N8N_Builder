"""
Node validation for workflows.
"""
from typing import Any, Dict, List, Optional, Set
from ..validation_service import Validator, ValidationResult, ValidationError, ValidationWarning, ValidationMode
from ..error_codes import ValidationErrorCode, ValidationWarningCode, format_error_message, format_warning_message

class NodeValidator(Validator):
    """Validates individual nodes in a workflow."""
    
    REQUIRED_NODE_FIELDS = {
        'id': str,
        'type': str
    }
    
    OPTIONAL_NODE_FIELDS = {
        'name': str,
        'parameters': dict,
        'position': list,
        'typeVersion': (int, float),
        'disabled': bool,
        'notes': str,
        'continueOnFail': bool
    }

    def validate(self, data: Dict[str, Any], existing_nodes: Optional[List[Dict[str, Any]]] = None) -> ValidationResult:
        """Validate a single node or list of nodes."""
        result = ValidationResult(is_valid=True)
        
        # Handle case where a list of nodes is passed (for duplicate checking)
        if isinstance(data, list):
            return self._validate_node_list(data)
        
        if not isinstance(data, dict):
            result.add_error(ValidationError(
                code=ValidationErrorCode.INVALID_NODE_STRUCTURE,
                message=format_error_message(
                    ValidationErrorCode.INVALID_NODE_STRUCTURE.value,
                    details="Node must be a dictionary"
                )
            ))
            return result

        # Get existing node IDs for duplicate checking
        node_ids = {node['id'] for node in (existing_nodes or []) if isinstance(node, dict) and 'id' in node}
        
        # Validate the node
        node_result = self._validate_node(data, node_ids)
        result.errors.extend(node_result.errors)
        result.warnings.extend(node_result.warnings)
        result.metadata.update(node_result.metadata)
        
        if node_result.has_errors():
            result.is_valid = False
            if self.mode == ValidationMode.STRICT:
                return result

        return result

    def _validate_node_list(self, nodes: List[Dict[str, Any]]) -> ValidationResult:
        """Validate a list of nodes for duplicate IDs."""
        result = ValidationResult(is_valid=True)
        node_ids = set()
        
        for node in nodes:
            if isinstance(node, dict) and 'id' in node:
                if node['id'] in node_ids:
                    result.add_error(ValidationError(
                        code=ValidationErrorCode.DUPLICATE_NODE_ID,
                        message=format_error_message(
                            ValidationErrorCode.DUPLICATE_NODE_ID.value,
                            node_id=node['id']
                        )
                    ))
                    result.is_valid = False
                else:
                    node_ids.add(node['id'])
        
        return result

    def _validate_node(self, node: Dict[str, Any], node_ids: Set[str]) -> ValidationResult:
        """Validate a single node."""
        result = ValidationResult(is_valid=True)
        
        # Check if node is a dictionary
        if not isinstance(node, dict):
            result.add_error(ValidationError(
                code=ValidationErrorCode.INVALID_NODE_STRUCTURE,
                message=format_error_message(
                    ValidationErrorCode.INVALID_NODE_STRUCTURE.value,
                    details="Node must be a dictionary"
                )
            ))
            return result

        # Validate required fields
        for field, expected_type in self.REQUIRED_NODE_FIELDS.items():
            if field not in node:
                result.add_error(ValidationError(
                    code=ValidationErrorCode.MISSING_REQUIRED_FIELD,
                    message=format_error_message(
                        ValidationErrorCode.MISSING_REQUIRED_FIELD.value,
                        field=field,
                        location="node"
                    )
                ))
            elif not isinstance(node[field], expected_type):
                result.add_error(ValidationError(
                    code=ValidationErrorCode.INVALID_FIELD_TYPE,
                    message=format_error_message(
                        ValidationErrorCode.INVALID_FIELD_TYPE.value,
                        field=field,
                        location="node",
                        expected_type=expected_type.__name__,
                        actual_type=type(node[field]).__name__
                    )
                ))

        # Validate optional fields if present
        for field, expected_type in self.OPTIONAL_NODE_FIELDS.items():
            if field in node:
                if not isinstance(node[field], expected_type):
                    result.add_error(ValidationError(
                        code=ValidationErrorCode.INVALID_FIELD_TYPE,
                        message=format_error_message(
                            ValidationErrorCode.INVALID_FIELD_TYPE.value,
                            field=field,
                            location="node",
                            expected_type=expected_type.__name__ if isinstance(expected_type, type) else " or ".join(t.__name__ for t in expected_type),
                            actual_type=type(node[field]).__name__
                        )
                    ))

        # Check for duplicate node IDs
        if 'id' in node:
            if node['id'] in node_ids:
                result.add_error(ValidationError(
                    code=ValidationErrorCode.DUPLICATE_NODE_ID,
                    message=format_error_message(
                        ValidationErrorCode.DUPLICATE_NODE_ID.value,
                        node_id=node['id']
                    )
                ))
            else:
                node_ids.add(node['id'])

        # Validate node type
        if 'type' in node:
            if not self._is_valid_node_type(node['type']):
                result.add_error(ValidationError(
                    code=ValidationErrorCode.INVALID_NODE_TYPE,
                    message=format_error_message(
                        ValidationErrorCode.INVALID_NODE_TYPE.value,
                        node_type=node['type'],
                        node_id=node.get('id', 'unknown')
                    )
                ))

        # Validate parameters
        if 'parameters' in node:
            param_result = self._validate_parameters(node['parameters'], node.get('id', 'unknown'))
            result.errors.extend(param_result.errors)
            result.warnings.extend(param_result.warnings)
        else:
            result.add_warning(ValidationWarning(
                code=ValidationWarningCode.MISSING_PARAMETERS,
                message=format_warning_message(
                    ValidationWarningCode.MISSING_PARAMETERS.value,
                    node_id=node.get('id', 'unknown')
                )
            ))

        # Check for unknown fields
        known_fields = set(self.REQUIRED_NODE_FIELDS.keys()) | set(self.OPTIONAL_NODE_FIELDS.keys())
        for field in node:
            if field not in known_fields:
                result.add_warning(ValidationWarning(
                    code=ValidationWarningCode.UNKNOWN_FIELD,
                    message=format_warning_message(
                        ValidationWarningCode.UNKNOWN_FIELD.value,
                        field=field,
                        location="node"
                    )
                ))

        # Add metadata
        result.metadata.update({
            'node_type': node.get('type'),
            'node_id': node.get('id'),
            'has_parameters': 'parameters' in node,
            'has_position': 'position' in node,
            'is_disabled': node.get('disabled', False),
            'has_notes': 'notes' in node
        })

        return result

    def _validate_parameters(self, parameters: Dict[str, Any], node_id: str) -> ValidationResult:
        """Validate node parameters."""
        result = ValidationResult(is_valid=True)
        
        if not isinstance(parameters, dict):
            result.add_error(ValidationError(
                code=ValidationErrorCode.INVALID_NODE_PARAMETER,
                message=format_error_message(
                    ValidationErrorCode.INVALID_NODE_PARAMETER.value,
                    parameter="parameters",
                    node_id=node_id,
                    details="Parameters must be a dictionary"
                )
            ))
            return result

        # Add parameter validation logic here
        # This will be expanded based on specific node type requirements

        return result

    def _is_valid_node_type(self, node_type: str) -> bool:
        """Check if a node type is valid."""
        # This should be expanded with actual node type validation
        # For now, we'll just check if it's not empty
        return bool(node_type and isinstance(node_type, str)) 