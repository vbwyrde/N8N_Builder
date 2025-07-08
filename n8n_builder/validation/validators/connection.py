"""
Connection validation for workflows.
"""
from typing import Any, Dict, List, Optional, Set
from ..validation_service import Validator, ValidationResult, ValidationError, ValidationWarning, ValidationMode
from ..error_codes import ValidationErrorCode, ValidationWarningCode, format_error_message, format_warning_message

class ConnectionValidator(Validator):
    """Validates connections between nodes in a workflow."""
    
    REQUIRED_CONNECTION_FIELDS = {
        'source': str,
        'target': str
    }
    
    OPTIONAL_CONNECTION_FIELDS = {
        'sourceHandle': str,
        'targetHandle': str,
        'type': str,
        'data': dict
    }

    def validate(self, data: Dict[str, Any], nodes: Optional[List[Dict[str, Any]]] = None, existing_connections: Optional[List[Dict[str, Any]]] = None) -> ValidationResult:
        """Validate all connections in the workflow."""
        result = ValidationResult(is_valid=True)
        
        if not isinstance(data, dict):
            result.add_error(ValidationError(
                code=ValidationErrorCode.INVALID_CONNECTION_STRUCTURE,
                message=format_error_message(
                    ValidationErrorCode.INVALID_CONNECTION_STRUCTURE.value,
                    details="Connection must be a dictionary"
                )
            ))
            return result

        # Get all node IDs for reference
        node_ids = {node['id'] for node in (nodes or []) if isinstance(node, dict) and 'id' in node}
        
        # Track connections for cycle detection
        connection_map: Dict[str, Set[str]] = {}
        
        # Validate the connection
        conn_result = self._validate_connection(data, node_ids, connection_map, existing_connections or [])
        result.errors.extend(conn_result.errors)
        result.warnings.extend(conn_result.warnings)
        result.metadata.update(conn_result.metadata)
        
        if conn_result.has_errors():
            result.is_valid = False
            if self.mode == ValidationMode.STRICT:
                return result

        # Check for cycles in the workflow
        if result.is_valid:
            cycle_result = self._check_for_cycles(connection_map)
            result.errors.extend(cycle_result.errors)
            result.warnings.extend(cycle_result.warnings)
            if cycle_result.has_errors():
                result.is_valid = False

        return result

    def _validate_connection(self, connection: Dict[str, Any], node_ids: Set[str], 
                           connection_map: Dict[str, Set[str]], existing_connections: List[Dict[str, Any]]) -> ValidationResult:
        """Validate a single connection."""
        result = ValidationResult(is_valid=True)
        
        # Check if connection is a dictionary
        if not isinstance(connection, dict):
            result.add_error(ValidationError(
                code=ValidationErrorCode.INVALID_CONNECTION_STRUCTURE,
                message=format_error_message(
                    ValidationErrorCode.INVALID_CONNECTION_STRUCTURE.value,
                    details="Connection must be a dictionary"
                )
            ))
            return result

        # Validate required fields
        for field, expected_type in self.REQUIRED_CONNECTION_FIELDS.items():
            if field not in connection:
                result.add_error(ValidationError(
                    code=ValidationErrorCode.MISSING_REQUIRED_FIELD,
                    message=format_error_message(
                        ValidationErrorCode.MISSING_REQUIRED_FIELD.value,
                        field=field,
                        location="connection"
                    )
                ))
            elif not isinstance(connection[field], expected_type):
                result.add_error(ValidationError(
                    code=ValidationErrorCode.INVALID_FIELD_TYPE,
                    message=format_error_message(
                        ValidationErrorCode.INVALID_FIELD_TYPE.value,
                        field=field,
                        location="connection",
                        expected_type=expected_type.__name__,
                        actual_type=type(connection[field]).__name__
                    )
                ))

        # Validate optional fields if present
        for field, expected_type in self.OPTIONAL_CONNECTION_FIELDS.items():
            if field in connection:
                if not isinstance(connection[field], expected_type):
                    result.add_error(ValidationError(
                        code=ValidationErrorCode.INVALID_FIELD_TYPE,
                        message=format_error_message(
                            ValidationErrorCode.INVALID_FIELD_TYPE.value,
                            field=field,
                            location="connection",
                            expected_type=expected_type.__name__,
                            actual_type=type(connection[field]).__name__
                        )
                    ))

        # Validate node references
        if 'source' in connection and 'target' in connection:
            source_id = connection['source']
            target_id = connection['target']
            
            # Check if source node exists
            if source_id not in node_ids:
                result.add_error(ValidationError(
                    code=ValidationErrorCode.NONEXISTENT_NODE,
                    message=format_error_message(
                        ValidationErrorCode.NONEXISTENT_NODE.value,
                        node_id=source_id
                    )
                ))
            
            # Check if target node exists
            if target_id not in node_ids:
                result.add_error(ValidationError(
                    code=ValidationErrorCode.NONEXISTENT_NODE,
                    message=format_error_message(
                        ValidationErrorCode.NONEXISTENT_NODE.value,
                        node_id=target_id
                    )
                ))
            
            # Check for self-connection
            if source_id == target_id:
                result.add_error(ValidationError(
                    code=ValidationErrorCode.SELF_CONNECTION,
                    message=format_error_message(
                        ValidationErrorCode.SELF_CONNECTION.value,
                        node_id=source_id
                    )
                ))
            
            # Check for duplicate connection
            for existing in existing_connections:
                if (existing.get('source') == source_id and 
                    existing.get('target') == target_id and
                    existing.get('sourceHandle') == connection.get('sourceHandle') and
                    existing.get('targetHandle') == connection.get('targetHandle')):
                    result.add_error(ValidationError(
                        code=ValidationErrorCode.DUPLICATE_CONNECTION,
                        message=format_error_message(
                            ValidationErrorCode.DUPLICATE_CONNECTION.value,
                            source=source_id,
                            target=target_id
                        )
                    ))
                    break
            
            # Add to connection map for cycle detection
            if source_id in node_ids and target_id in node_ids:
                if source_id not in connection_map:
                    connection_map[source_id] = set()
                connection_map[source_id].add(target_id)

        # Check for unknown fields
        known_fields = set(self.REQUIRED_CONNECTION_FIELDS.keys()) | set(self.OPTIONAL_CONNECTION_FIELDS.keys())
        for field in connection:
            if field not in known_fields:
                result.add_warning(ValidationWarning(
                    code=ValidationWarningCode.UNKNOWN_FIELD,
                    message=format_warning_message(
                        ValidationWarningCode.UNKNOWN_FIELD.value,
                        field=field,
                        location="connection"
                    )
                ))

        # Add metadata
        result.metadata.update({
            'source_node': connection.get('source'),
            'target_node': connection.get('target'),
            'has_source_handle': 'sourceHandle' in connection,
            'has_target_handle': 'targetHandle' in connection,
            'has_type': 'type' in connection,
            'has_data': 'data' in connection
        })

        return result

    def _check_for_cycles(self, connection_map: Dict[str, Set[str]]) -> ValidationResult:
        """Check for cycles in the workflow graph."""
        result = ValidationResult(is_valid=True)
        visited = set()
        path = set()

        def dfs(node: str) -> None:
            if node in path:
                # Found a cycle
                cycle = list(path) + [node]
                result.add_error(ValidationError(
                    code=ValidationErrorCode.CYCLE_DETECTED,
                    message=format_error_message(
                        ValidationErrorCode.CYCLE_DETECTED.value,
                        path=" -> ".join(cycle)
                    )
                ))
                return
            
            if node in visited:
                return
            
            visited.add(node)
            path.add(node)
            
            for neighbor in connection_map.get(node, set()):
                dfs(neighbor)
            
            path.remove(node)

        # Start DFS from each node to find all cycles
        for node in connection_map:
            if node not in visited:
                dfs(node)

        return result 