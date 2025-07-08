"""
Workflow logic validation for workflows.
"""
from typing import Any, Dict, List, Optional, Set
from ..validation_service import Validator, ValidationResult, ValidationError, ValidationWarning, ValidationMode
from ..error_codes import ValidationErrorCode, ValidationWarningCode, format_error_message, format_warning_message

class WorkflowLogicValidator(Validator):
    """Validates the logical structure and flow of workflows."""
    
    def validate(self, data: Dict[str, Any], nodes: Optional[List[Dict[str, Any]]] = None, connections: Optional[List[Dict[str, Any]]] = None) -> ValidationResult:
        """Validate the logical structure of the workflow."""
        result = ValidationResult(is_valid=True)
        
        if not isinstance(data, dict):
            result.add_error(ValidationError(
                code=ValidationErrorCode.INVALID_WORKFLOW_LOGIC,
                message=format_error_message(
                    ValidationErrorCode.INVALID_WORKFLOW_LOGIC.value,
                    details="Workflow must be a dictionary"
                )
            ))
            return result

        # Extract nodes and connections from workflow data if not provided separately
        if nodes is None:
            nodes = data.get('nodes', [])
        if connections is None:
            connections = data.get('connections', [])

        # Build node and connection maps
        node_map = {node['id']: node for node in nodes if isinstance(node, dict) and 'id' in node}
        connection_map = self._build_connection_map(connections)
        
        # Check for cycles first
        cycle_result = self._check_for_cycles(connection_map)
        result.errors.extend(cycle_result.errors)
        result.warnings.extend(cycle_result.warnings)
        is_acyclic = not cycle_result.has_errors()
        
        if cycle_result.has_errors():
            result.is_valid = False
            if self.mode == ValidationMode.STRICT:
                # Add metadata before returning
                result.metadata.update({
                    'has_start_node': self._has_start_node(node_map),
                    'has_end_node': self._has_end_node(node_map),
                    'is_acyclic': is_acyclic
                })
                return result
        
        # Validate workflow structure
        structure_result = self._validate_workflow_structure(node_map, connection_map)
        result.errors.extend(structure_result.errors)
        result.warnings.extend(structure_result.warnings)
        
        if structure_result.has_errors():
            result.is_valid = False
            if self.mode == ValidationMode.STRICT:
                # Add metadata before returning
                result.metadata.update({
                    'has_start_node': self._has_start_node(node_map),
                    'has_end_node': self._has_end_node(node_map),
                    'is_acyclic': is_acyclic
                })
                return result

        # Validate node types and connections
        type_result = self._validate_node_types(node_map, connection_map)
        result.errors.extend(type_result.errors)
        result.warnings.extend(type_result.warnings)
        
        if type_result.has_errors():
            result.is_valid = False
            if self.mode == ValidationMode.STRICT:
                # Add metadata before returning
                result.metadata.update({
                    'has_start_node': self._has_start_node(node_map),
                    'has_end_node': self._has_end_node(node_map),
                    'is_acyclic': is_acyclic
                })
                return result

        # Validate workflow completeness
        completeness_result = self._validate_workflow_completeness(node_map, connection_map)
        result.errors.extend(completeness_result.errors)
        result.warnings.extend(completeness_result.warnings)
        
        if completeness_result.has_errors():
            result.is_valid = False

        # Add metadata
        result.metadata.update({
            'has_start_node': self._has_start_node(node_map),
            'has_end_node': self._has_end_node(node_map),
            'is_acyclic': is_acyclic
        })

        return result

    def _build_connection_map(self, connections: List[Dict[str, Any]]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """Build a map of node connections."""
        connection_map = {}
        
        for conn in connections:
            if not isinstance(conn, dict) or 'source' not in conn or 'target' not in conn:
                continue
                
            source = conn['source']
            target = conn['target']
            
            if source not in connection_map:
                connection_map[source] = {'outgoing': [], 'incoming': []}
            if target not in connection_map:
                connection_map[target] = {'outgoing': [], 'incoming': []}
                
            connection_map[source]['outgoing'].append(conn)
            connection_map[target]['incoming'].append(conn)
            
        return connection_map

    def _validate_workflow_structure(self, node_map: Dict[str, Dict[str, Any]], 
                                   connection_map: Dict[str, Dict[str, List[Dict[str, Any]]]]) -> ValidationResult:
        """Validate the basic structure of the workflow."""
        result = ValidationResult(is_valid=True)
        
        # Check for isolated nodes
        for node_id in node_map:
            if node_id not in connection_map:
                result.add_warning(ValidationWarning(
                    code=ValidationWarningCode.ISOLATED_NODE,
                    message=format_warning_message(
                        ValidationWarningCode.ISOLATED_NODE.value,
                        node_id=node_id
                    )
                ))
            elif not connection_map[node_id]['incoming'] and not connection_map[node_id]['outgoing']:
                result.add_warning(ValidationWarning(
                    code=ValidationWarningCode.ISOLATED_NODE,
                    message=format_warning_message(
                        ValidationWarningCode.ISOLATED_NODE.value,
                        node_id=node_id
                    )
                ))

        # Check for nodes with no incoming connections
        for node_id, connections in connection_map.items():
            if not connections['incoming'] and node_id in node_map:
                node_type = node_map[node_id].get('type', '')
                if not self._is_start_node_type(node_type):
                    result.add_warning(ValidationWarning(
                        code=ValidationWarningCode.NO_INCOMING_CONNECTIONS,
                        message=format_warning_message(
                            ValidationWarningCode.NO_INCOMING_CONNECTIONS.value,
                            node_id=node_id
                        )
                    ))

        # Check for nodes with no outgoing connections
        for node_id, connections in connection_map.items():
            if not connections['outgoing'] and node_id in node_map:
                node_type = node_map[node_id].get('type', '')
                if not self._is_end_node_type(node_type):
                    result.add_warning(ValidationWarning(
                        code=ValidationWarningCode.NO_OUTGOING_CONNECTIONS,
                        message=format_warning_message(
                            ValidationWarningCode.NO_OUTGOING_CONNECTIONS.value,
                            node_id=node_id
                        )
                    ))

        return result

    def _validate_node_types(self, node_map: Dict[str, Dict[str, Any]], 
                           connection_map: Dict[str, Dict[str, List[Dict[str, Any]]]]) -> ValidationResult:
        """Validate node types and their connections."""
        result = ValidationResult(is_valid=True)
        
        # Check for multiple start nodes
        start_nodes = [node_id for node_id, node in node_map.items() 
                      if self._is_start_node_type(node.get('type', ''))]
        if len(start_nodes) > 1:
            result.add_error(ValidationError(
                code=ValidationErrorCode.MULTIPLE_START_NODES,
                message=format_error_message(
                    ValidationErrorCode.MULTIPLE_START_NODES.value,
                    nodes=", ".join(start_nodes)
                )
            ))
        
        # Check for multiple end nodes
        end_nodes = [node_id for node_id, node in node_map.items() 
                    if self._is_end_node_type(node.get('type', ''))]
        if len(end_nodes) > 1:
            result.add_error(ValidationError(
                code=ValidationErrorCode.MULTIPLE_END_NODES,
                message=format_error_message(
                    ValidationErrorCode.MULTIPLE_END_NODES.value,
                    nodes=", ".join(end_nodes)
                )
            ))
        
        # Validate node type compatibility
        for node_id, node in node_map.items():
            node_type = node.get('type', '')
            
            if node_id in connection_map:
                for conn in connection_map[node_id]['outgoing']:
                    target_id = conn['target']
                    if target_id in node_map:
                        target_type = node_map[target_id].get('type', '')
                        if not self._are_types_compatible(node_type, target_type):
                            result.add_error(ValidationError(
                                code=ValidationErrorCode.INCOMPATIBLE_NODE_TYPES,
                                message=format_error_message(
                                    ValidationErrorCode.INCOMPATIBLE_NODE_TYPES.value,
                                    source=node_id,
                                    target=target_id
                                )
                            ))

        return result

    def _validate_workflow_completeness(self, node_map: Dict[str, Dict[str, Any]], 
                                      connection_map: Dict[str, Dict[str, List[Dict[str, Any]]]]) -> ValidationResult:
        """Validate the completeness of the workflow."""
        result = ValidationResult(is_valid=True)
        
        # Check for required node types
        has_start = False
        has_end = False
        
        for node in node_map.values():
            node_type = node.get('type', '')
            if self._is_start_node_type(node_type):
                has_start = True
            elif self._is_end_node_type(node_type):
                has_end = True
        
        if not has_start:
            result.add_error(ValidationError(
                code=ValidationErrorCode.MISSING_START_NODE,
                message=format_error_message(
                    ValidationErrorCode.MISSING_START_NODE.value
                )
            ))
            
        if not has_end:
            result.add_error(ValidationError(
                code=ValidationErrorCode.MISSING_END_NODE,
                message=format_error_message(
                    ValidationErrorCode.MISSING_END_NODE.value
                )
            ))

        # Check for disconnected paths
        for node_id, connections in connection_map.items():
            if node_id in node_map:
                node_type = node_map[node_id].get('type', '')
                if not self._is_start_node_type(node_type) and not connections['incoming']:
                    result.add_error(ValidationError(
                        code=ValidationErrorCode.DISCONNECTED_PATH,
                        message=format_error_message(
                            ValidationErrorCode.DISCONNECTED_PATH.value,
                            source="start",
                            target=node_id
                        )
                    ))

        return result

    def _is_start_node_type(self, node_type: str) -> bool:
        """Check if a node type is a start node type."""
        return node_type in {
            'n8n-nodes-base.webhook',
            'n8n-nodes-base.manualTrigger',
            'n8n-nodes-base.scheduleTrigger'
        }

    def _is_end_node_type(self, node_type: str) -> bool:
        """Check if a node type is an end node type."""
        return node_type in {
            'n8n-nodes-base.noOp',
            'n8n-nodes-base.set',
            'n8n-nodes-base.merge'
        }

    def _are_types_compatible(self, source_type: str, target_type: str) -> bool:
        """Check if two node types are compatible for connection."""
        # This is a simplified check - in reality, we would need a more comprehensive
        # compatibility matrix based on node types and their input/output specifications
        return True

    def _has_start_node(self, node_map: Dict[str, Dict[str, Any]]) -> bool:
        """Check if the workflow has a start node."""
        for node in node_map.values():
            if self._is_start_node_type(node.get('type', '')):
                return True
        return False

    def _has_end_node(self, node_map: Dict[str, Dict[str, Any]]) -> bool:
        """Check if the workflow has an end node."""
        for node in node_map.values():
            if self._is_end_node_type(node.get('type', '')):
                return True
        return False

    def _check_for_cycles(self, connection_map: Dict[str, Dict[str, List[Dict[str, Any]]]]) -> ValidationResult:
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
            
            # Get outgoing connections
            outgoing = connection_map.get(node, {}).get('outgoing', [])
            for conn in outgoing:
                target = conn.get('target')
                if target:
                    dfs(target)
            
            path.remove(node)

        # Start DFS from each node to find all cycles
        for node in connection_map:
            if node not in visited:
                dfs(node)

        return result 