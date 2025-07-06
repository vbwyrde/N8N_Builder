from typing import Dict, List, Tuple, Any, Set
from pydantic import BaseModel
import json
import re
import sys
import logging
import time
from collections import defaultdict, deque

validation_logger = logging.getLogger('n8n_builder.validation')

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]

class EdgeCaseValidationResult(BaseModel):
    """Extended validation result for edge cases."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    edge_cases_detected: List[str]
    performance_metrics: Dict[str, Any]

class EdgeCaseValidator:
    """Validator specifically for common edge cases in N8N workflows."""
    
    def __init__(self):
        self.max_workflow_size = 10 * 1024 * 1024  # 10MB max workflow size
        self.max_nodes = 1000  # Maximum number of nodes
        self.max_description_length = 50000  # Maximum description length
        self.max_node_name_length = 200  # Maximum node name length
        self.known_node_types = self._initialize_known_node_types()
        validation_logger.info("EdgeCaseValidator initialized with size limits and node type validation")
    
    def validate_edge_cases(self, workflow_json: str, description: str = "") -> EdgeCaseValidationResult:
        """Comprehensive edge case validation."""
        validation_id = f"edge_case_validation_{int(time.time() * 1000)}"
        validation_logger.info(f"Starting edge case validation [ID: {validation_id}]", extra={
            'validation_id': validation_id,
            'workflow_size': len(workflow_json.encode('utf-8')),
            'description_length': len(description)
        })
        
        errors = []
        warnings = []
        suggestions = []
        edge_cases_detected = []
        performance_metrics = {}
        
        # Track validation performance
        start_time = time.time()
        
        try:
            # 1. Size and Performance Edge Cases
            size_errors, size_warnings, size_metrics = self._validate_size_limits(workflow_json, description)
            errors.extend(size_errors)
            warnings.extend(size_warnings)
            performance_metrics.update(size_metrics)
            
            if size_errors:
                validation_logger.warning(f"Size validation failed [ID: {validation_id}]", extra={
                    'validation_id': validation_id,
                    'errors': size_errors,
                    'warnings': size_warnings,
                    'metrics': size_metrics
                })
                edge_cases_detected.append("workflow_size_exceeded")
                return EdgeCaseValidationResult(
                    is_valid=False,
                    errors=errors,
                    warnings=warnings,
                    suggestions=suggestions,
                    edge_cases_detected=edge_cases_detected,
                    performance_metrics=performance_metrics
                )
            
            # 2. Parse workflow JSON
            try:
                workflow = json.loads(workflow_json)
            except json.JSONDecodeError as e:
                validation_logger.exception(f"JSON parsing failed [ID: {validation_id}]", extra={
                    'validation_id': validation_id,
                    'error': str(e)
                })
                errors.append(f"JSON parsing failed: {str(e)}")
                edge_cases_detected.append("json_parse_error")
                return EdgeCaseValidationResult(
                    is_valid=False,
                    errors=errors,
                    warnings=warnings,
                    suggestions=suggestions,
                    edge_cases_detected=edge_cases_detected,
                    performance_metrics=performance_metrics
                )
            
            # 3. Empty Workflow Edge Cases
            empty_errors, empty_warnings = self._validate_empty_workflow(workflow)
            errors.extend(empty_errors)
            warnings.extend(empty_warnings)
            if empty_errors:
                validation_logger.warning(f"Empty workflow detected [ID: {validation_id}]", extra={
                    'validation_id': validation_id,
                    'errors': empty_errors,
                    'warnings': empty_warnings
                })
                edge_cases_detected.append("empty_workflow")
            
            # 4. Node-related Edge Cases
            if 'nodes' in workflow and isinstance(workflow['nodes'], list):
                node_errors, node_warnings, node_edge_cases = self._validate_node_edge_cases(workflow['nodes'])
                errors.extend(node_errors)
                warnings.extend(node_warnings)
                edge_cases_detected.extend(node_edge_cases)
                if node_errors or node_warnings:
                    validation_logger.warning(f"Node validation issues [ID: {validation_id}]", extra={
                        'validation_id': validation_id,
                        'errors': node_errors,
                        'warnings': node_warnings,
                        'edge_cases': node_edge_cases
                    })
            
            # 5. Connection Edge Cases
            if 'connections' in workflow and 'nodes' in workflow:
                conn_errors, conn_warnings, conn_edge_cases = self._validate_connection_edge_cases(
                    workflow['connections'], workflow['nodes']
                )
                errors.extend(conn_errors)
                warnings.extend(conn_warnings)
                edge_cases_detected.extend(conn_edge_cases)
                if conn_errors or conn_warnings:
                    validation_logger.warning(f"Connection validation issues [ID: {validation_id}]", extra={
                        'validation_id': validation_id,
                        'errors': conn_errors,
                        'warnings': conn_warnings,
                        'edge_cases': conn_edge_cases
                    })
            
            # 6. Workflow Structure Edge Cases
            if 'nodes' in workflow and 'connections' in workflow:
                struct_errors, struct_warnings, struct_edge_cases = self._validate_workflow_structure_edge_cases(
                    workflow['nodes'], workflow['connections']
                )
                errors.extend(struct_errors)
                warnings.extend(struct_warnings)
                edge_cases_detected.extend(struct_edge_cases)
                if struct_errors or struct_warnings:
                    validation_logger.warning(f"Structure validation issues [ID: {validation_id}]", extra={
                        'validation_id': validation_id,
                        'errors': struct_errors,
                        'warnings': struct_warnings,
                        'edge_cases': struct_edge_cases
                    })
            
            # 7. Input Description Edge Cases
            desc_errors, desc_warnings = self._validate_description_edge_cases(description)
            errors.extend(desc_errors)
            warnings.extend(desc_warnings)
            if desc_errors or desc_warnings:
                validation_logger.warning(f"Description validation issues [ID: {validation_id}]", extra={
                    'validation_id': validation_id,
                    'errors': desc_errors,
                    'warnings': desc_warnings
                })
                edge_cases_detected.append("description_edge_case")
            
            # 8. Generate suggestions based on detected edge cases
            suggestions.extend(self._generate_edge_case_suggestions(edge_cases_detected, workflow))
            
            # Final performance metrics
            performance_metrics['total_validation_time'] = time.time() - start_time
            performance_metrics['edge_cases_count'] = len(edge_cases_detected)
            
            validation_logger.info(f"Edge case validation completed [ID: {validation_id}]", extra={
                'validation_id': validation_id,
                'is_valid': len(errors) == 0,
                'error_count': len(errors),
                'warning_count': len(warnings),
                'edge_cases_count': len(edge_cases_detected),
                'validation_time': performance_metrics['total_validation_time']
            })
            
            return EdgeCaseValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                edge_cases_detected=edge_cases_detected,
                performance_metrics=performance_metrics
            )
            
        except Exception as e:
            validation_logger.exception(f"Unexpected validation error [ID: {validation_id}]", extra={
                'validation_id': validation_id,
                'error': str(e)
            })
            errors.append(f"Unexpected validation error: {str(e)}")
            edge_cases_detected.append("validation_system_error")
            return EdgeCaseValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                edge_cases_detected=edge_cases_detected,
                performance_metrics=performance_metrics
            )
    
    def _validate_size_limits(self, workflow_json: str, description: str) -> Tuple[List[str], List[str], Dict[str, Any]]:
        """Validate size-related edge cases."""
        errors = []
        warnings = []
        metrics = {}
        
        # Check workflow JSON size
        workflow_size = len(workflow_json.encode('utf-8'))
        metrics['workflow_size_bytes'] = workflow_size
        
        if workflow_size > self.max_workflow_size:
            errors.append(f"Workflow size ({workflow_size:,} bytes) exceeds maximum allowed size ({self.max_workflow_size:,} bytes)")
        elif workflow_size > self.max_workflow_size * 0.8:
            warnings.append(f"Workflow size ({workflow_size:,} bytes) is approaching the maximum limit")
        
        # Check description length
        desc_length = len(description)
        metrics['description_length'] = desc_length
        
        if desc_length > self.max_description_length:
            errors.append(f"Description length ({desc_length:,} characters) exceeds maximum allowed length ({self.max_description_length:,} characters)")
        elif desc_length > self.max_description_length * 0.8:
            warnings.append(f"Description length ({desc_length:,} characters) is approaching the maximum limit")
        
        # Check for potential memory issues
        if workflow_size > 1024 * 1024:  # 1MB
            warnings.append("Large workflow detected - may impact processing performance")
        
        return errors, warnings, metrics
    
    def _validate_empty_workflow(self, workflow: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Validate empty workflow edge cases."""
        errors = []
        warnings = []
        
        # Check for completely empty workflow
        if not workflow:
            errors.append("Workflow is completely empty")
            return errors, warnings
        
        # Check for empty nodes
        nodes = workflow.get('nodes', [])
        if not nodes or len(nodes) == 0:
            errors.append("Workflow has no nodes - at least one node is required")
        
        # Check for empty workflow name
        name = workflow.get('name', '')
        if not name or not name.strip():
            warnings.append("Workflow has no name - consider adding a descriptive name")
        
        # Check for workflows with only trigger nodes
        if nodes:
            trigger_nodes = [n for n in nodes if 'trigger' in n.get('type', '').lower()]
            if len(trigger_nodes) == len(nodes):
                warnings.append("Workflow contains only trigger nodes - consider adding action nodes")
        
        return errors, warnings
    
    def _validate_node_edge_cases(self, nodes: List[Dict[str, Any]]) -> Tuple[List[str], List[str], List[str]]:
        """Validate node-related edge cases."""
        errors = []
        warnings = []
        edge_cases = []
        
        if len(nodes) > self.max_nodes:
            errors.append(f"Too many nodes ({len(nodes)}) - maximum allowed is {self.max_nodes}")
            edge_cases.append("too_many_nodes")
        
        # Check for duplicate node IDs
        node_ids = []
        node_names = []
        for i, node in enumerate(nodes):
            node_id = node.get('id')
            node_name = node.get('name')
            
            # Duplicate ID check
            if node_id:
                if node_id in node_ids:
                    errors.append(f"Duplicate node ID '{node_id}' found at node {i}")
                    edge_cases.append("duplicate_node_ids")
                else:
                    node_ids.append(node_id)
            
            # Duplicate name check (warning only)
            if node_name:
                if node_name in node_names:
                    warnings.append(f"Duplicate node name '{node_name}' found at node {i}")
                    edge_cases.append("duplicate_node_names")
                else:
                    node_names.append(node_name)
            
            # Check node name length
            if node_name and len(node_name) > self.max_node_name_length:
                errors.append(f"Node {i} name too long ({len(node_name)} characters) - maximum is {self.max_node_name_length}")
                edge_cases.append("node_name_too_long")
            
            # Check for invalid characters in node ID
            if node_id and not re.match(r'^[a-zA-Z0-9_-]+$', str(node_id)):
                warnings.append(f"Node {i} ID '{node_id}' contains special characters - may cause issues")
                edge_cases.append("invalid_node_id_characters")
            
            # Check for unknown node types
            node_type = node.get('type')
            if node_type and not self._is_known_node_type(node_type):
                warnings.append(f"Node {i} uses unknown type '{node_type}' - may not be supported")
                edge_cases.append("unknown_node_type")
        
        return errors, warnings, edge_cases
    
    def _validate_connection_edge_cases(self, connections: Dict[str, Any], nodes: List[Dict[str, Any]]) -> Tuple[List[str], List[str], List[str]]:
        """Validate connection-related edge cases."""
        errors = []
        warnings = []
        edge_cases = []
        
        # Build node ID to name mapping
        node_lookup = {node.get('id'): node.get('name', f"Node_{i}") for i, node in enumerate(nodes)}
        node_names = {node.get('name'): node.get('id') for node in nodes if node.get('name')}
        
        # Check for self-referencing connections
        for source, targets in connections.items():
            if not isinstance(targets, dict):
                continue
                
            for connection_type, target_lists in targets.items():
                if not isinstance(target_lists, list):
                    continue
                    
                for target_list in target_lists:
                    if not isinstance(target_list, list):
                        continue
                        
                    for target in target_list:
                        if not isinstance(target, dict):
                            continue
                            
                        target_node = target.get('node')
                        if target_node == source:
                            errors.append(f"Self-referencing connection detected: node '{source}' connects to itself")
                            edge_cases.append("self_referencing_connection")
        
        # Check for connections to non-existent nodes
        all_node_identifiers = set()
        for node in nodes:
            if node.get('id'):
                all_node_identifiers.add(node.get('id'))
            if node.get('name'):
                all_node_identifiers.add(node.get('name'))
        
        for source, targets in connections.items():
            # Check if source node exists
            if source not in all_node_identifiers:
                errors.append(f"Connection references non-existent source node: '{source}'")
                edge_cases.append("connection_to_nonexistent_node")
            
            if isinstance(targets, dict):
                for connection_type, target_lists in targets.items():
                    if isinstance(target_lists, list):
                        for target_list in target_lists:
                            if isinstance(target_list, list):
                                for target in target_list:
                                    if isinstance(target, dict):
                                        target_node = target.get('node')
                                        if target_node and target_node not in all_node_identifiers:
                                            errors.append(f"Connection references non-existent target node: '{target_node}'")
                                            edge_cases.append("connection_to_nonexistent_node")
        
        return errors, warnings, edge_cases
    
    def _validate_workflow_structure_edge_cases(self, nodes: List[Dict[str, Any]], connections: Dict[str, Any]) -> Tuple[List[str], List[str], List[str]]:
        """Validate workflow structure edge cases like circular dependencies and orphaned nodes."""
        errors = []
        warnings = []
        edge_cases = []
        
        # Build adjacency list for graph analysis
        graph = defaultdict(list)
        node_ids = set()
        
        for node in nodes:
            node_id = node.get('id') or node.get('name')
            if node_id:
                node_ids.add(node_id)
        
        # Build graph from connections
        for source, targets in connections.items():
            if isinstance(targets, dict):
                for connection_type, target_lists in targets.items():
                    if isinstance(target_lists, list):
                        for target_list in target_lists:
                            if isinstance(target_list, list):
                                for target in target_list:
                                    if isinstance(target, dict):
                                        target_node = target.get('node')
                                        if target_node:
                                            graph[source].append(target_node)
        
        # Check for circular dependencies
        circular_deps = self._detect_circular_dependencies(graph)
        if circular_deps:
            for cycle in circular_deps:
                errors.append(f"Circular dependency detected: {' -> '.join(cycle)} -> {cycle[0]}")
                edge_cases.append("circular_dependency")
        
        # Check for orphaned nodes
        connected_nodes = set()
        for source, targets in graph.items():
            connected_nodes.add(source)
            connected_nodes.update(targets)
        
        orphaned_nodes = node_ids - connected_nodes
        if orphaned_nodes and len(node_ids) > 1:  # Only warn if there are multiple nodes
            for orphan in orphaned_nodes:
                warnings.append(f"Orphaned node detected: '{orphan}' has no connections")
                edge_cases.append("orphaned_nodes")
        
        # Check for unreachable nodes (nodes with no path from trigger nodes)
        trigger_nodes = []
        for node in nodes:
            node_type = node.get('type', '').lower()
            node_id = node.get('id') or node.get('name')
            if 'trigger' in node_type or 'webhook' in node_type or 'schedule' in node_type:
                trigger_nodes.append(node_id)
        
        if trigger_nodes:
            reachable = self._find_reachable_nodes(graph, trigger_nodes)
            unreachable = node_ids - reachable
            if unreachable:
                for unreachable_node in unreachable:
                    warnings.append(f"Unreachable node detected: '{unreachable_node}' cannot be reached from trigger nodes")
                    edge_cases.append("unreachable_nodes")
        
        return errors, warnings, edge_cases
    
    def _validate_description_edge_cases(self, description: str) -> Tuple[List[str], List[str]]:
        """Validate description edge cases."""
        errors = []
        warnings = []
        
        if not description:
            return errors, warnings
        
        # Check for encoding issues
        try:
            description.encode('utf-8')
        except UnicodeEncodeError:
            errors.append("Description contains invalid Unicode characters")
        
        # Check for extremely long single lines
        lines = description.split('\n')
        for i, line in enumerate(lines):
            if len(line) > 1000:
                warnings.append(f"Line {i+1} in description is very long ({len(line)} characters) - consider breaking it up")
        
        # Check for potential script injection patterns (basic check)
        suspicious_patterns = ['<script', 'javascript:', 'eval(', 'exec(', '<?php', '<%']
        for pattern in suspicious_patterns:
            if pattern.lower() in description.lower():
                warnings.append(f"Description contains potentially suspicious content: '{pattern}'")
        
        # Check for excessive special characters
        special_char_count = sum(1 for c in description if not c.isalnum() and not c.isspace())
        if special_char_count > len(description) * 0.3:  # More than 30% special characters
            warnings.append("Description contains a high percentage of special characters - ensure it's intended")
        
        return errors, warnings
    
    def _detect_circular_dependencies(self, graph: Dict[str, List[str]]) -> List[List[str]]:
        """Detect circular dependencies using DFS."""
        white = set(graph.keys())
        gray = set()
        black = set()
        cycles = []
        
        def dfs(node, path):
            if node in black:
                return
            if node in gray:
                # Found a cycle
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:])
                return
                
            gray.add(node)
            white.discard(node)
            
            for neighbor in graph.get(node, []):
                dfs(neighbor, path + [neighbor])
                
            gray.remove(node)
            black.add(node)
        
        for node in list(white):
            if node in white:
                dfs(node, [node])
        
        return cycles
    
    def _find_reachable_nodes(self, graph: Dict[str, List[str]], start_nodes: List[str]) -> Set[str]:
        """Find all nodes reachable from start nodes using BFS."""
        reachable = set()
        queue = deque(start_nodes)
        
        while queue:
            node = queue.popleft()
            if node in reachable:
                continue
                
            reachable.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in reachable:
                    queue.append(neighbor)
        
        return reachable
    
    def _is_known_node_type(self, node_type: str) -> bool:
        """Check if node type is in our known types."""
        return node_type in self.known_node_types
    
    def _initialize_known_node_types(self) -> Set[str]:
        """Initialize set of known N8N node types."""
        return {
            'n8n-nodes-base.manualTrigger',
            'n8n-nodes-base.webhook',
            'n8n-nodes-base.scheduleTrigger',
            'n8n-nodes-base.emailSend',
            'n8n-nodes-base.httpRequest',
            'n8n-nodes-base.postgres',
            'n8n-nodes-base.mysql',
            'n8n-nodes-base.function',
            'n8n-nodes-base.if',
            'n8n-nodes-base.switch',
            'n8n-nodes-base.merge',
            'n8n-nodes-base.split',
            'n8n-nodes-base.set',
            'n8n-nodes-base.noOp',
            'n8n-nodes-base.errorTrigger',
            'n8n-nodes-base.wait',
            'n8n-nodes-base.code',
            'n8n-nodes-base.spreadsheetFile',
            'n8n-nodes-base.readBinaryFile',
            'n8n-nodes-base.writeBinaryFile',
            'n8n-nodes-base.ftp',
            'n8n-nodes-base.ssh',
            'n8n-nodes-base.slack',
            'n8n-nodes-base.discord',
            'n8n-nodes-base.googleSheets',
            'n8n-nodes-base.googleDrive',
            'n8n-nodes-base.googleCalendar',
            'n8n-nodes-base.notion',
            'n8n-nodes-base.airtable',
            'n8n-nodes-base.jira',
            'n8n-nodes-base.github',
            'n8n-nodes-base.gitlab'
        }
    
    def _generate_edge_case_suggestions(self, edge_cases: List[str], workflow: Dict[str, Any]) -> List[str]:
        """Generate suggestions based on detected edge cases."""
        suggestions = []
        
        if "duplicate_node_ids" in edge_cases:
            suggestions.append("Consider using unique, descriptive IDs for all nodes to avoid conflicts")
        
        if "circular_dependency" in edge_cases:
            suggestions.append("Review workflow logic to eliminate circular dependencies - consider using conditional logic or breaking the cycle")
        
        if "orphaned_nodes" in edge_cases:
            suggestions.append("Connect orphaned nodes to the workflow or remove them if they're not needed")
        
        if "unreachable_nodes" in edge_cases:
            suggestions.append("Ensure all nodes are reachable from trigger nodes by adding appropriate connections")
        
        if "too_many_nodes" in edge_cases:
            suggestions.append("Consider breaking this large workflow into smaller, manageable sub-workflows")
        
        if "unknown_node_type" in edge_cases:
            suggestions.append("Verify that all node types are supported in your N8N installation")
        
        if "workflow_size_exceeded" in edge_cases:
            suggestions.append("Consider optimizing the workflow size by removing unnecessary nodes or splitting into multiple workflows")
        
        return suggestions

class BaseWorkflowValidator:
    """Base class for workflow validation."""
    
    def validate_workflow(self, workflow_json: str) -> ValidationResult:
        """Validate a workflow JSON string."""
        validation_id = f"workflow_validation_{int(time.time() * 1000)}"
        validation_logger.info(f"Starting workflow validation [ID: {validation_id}]", extra={
            'validation_id': validation_id,
            'workflow_size': len(workflow_json.encode('utf-8'))
        })
        
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Parse workflow JSON
            try:
                workflow = json.loads(workflow_json)
            except json.JSONDecodeError as e:
                validation_logger.exception(f"JSON parsing failed [ID: {validation_id}]", extra={
                    'validation_id': validation_id,
                    'error': str(e)
                })
                errors.append(f"Invalid JSON: {str(e)}")
                return ValidationResult(
                    is_valid=False,
                    errors=errors,
                    warnings=warnings,
                    suggestions=suggestions
                )
            
            # Validate basic structure
            if not self._validate_basic_structure(workflow, errors):
                validation_logger.warning(f"Basic structure validation failed [ID: {validation_id}]", extra={
                    'validation_id': validation_id,
                    'errors': errors
                })
                return ValidationResult(
                    is_valid=False,
                    errors=errors,
                    warnings=warnings,
                    suggestions=suggestions
                )
            
            # Validate nodes
            if 'nodes' in workflow:
                node_errors = self._validate_nodes(workflow['nodes'])
                if node_errors:
                    validation_logger.warning(f"Node validation failed [ID: {validation_id}]", extra={
                        'validation_id': validation_id,
                        'errors': node_errors
                    })
                    errors.extend(node_errors)
            
            # Validate connections
            if 'connections' in workflow:
                conn_errors = self._validate_connections(workflow['connections'])
                if conn_errors:
                    validation_logger.warning(f"Connection validation failed [ID: {validation_id}]", extra={
                        'validation_id': validation_id,
                        'errors': conn_errors
                    })
                    errors.extend(conn_errors)
            
            # Check best practices
            best_practice_warnings = self._check_best_practices(workflow)
            if best_practice_warnings:
                validation_logger.info(f"Best practice warnings [ID: {validation_id}]", extra={
                    'validation_id': validation_id,
                    'warnings': best_practice_warnings
                })
                warnings.extend(best_practice_warnings)
            
            # Generate suggestions
            suggestions.extend(self._generate_suggestions(workflow))
            
            validation_logger.info(f"Workflow validation completed [ID: {validation_id}]", extra={
                'validation_id': validation_id,
                'is_valid': len(errors) == 0,
                'error_count': len(errors),
                'warning_count': len(warnings),
                'suggestion_count': len(suggestions)
            })
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions
            )
            
        except Exception as e:
            validation_logger.exception(f"Unexpected validation error [ID: {validation_id}]", extra={
                'validation_id': validation_id,
                'error': str(e)
            })
            errors.append(f"Unexpected validation error: {str(e)}")
            return ValidationResult(
                is_valid=False,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions
            )
    
    def _validate_basic_structure(self, workflow: Dict[str, Any], errors: List[str]) -> bool:
        """Validate the basic structure of the workflow."""
        required_fields = ['name', 'nodes', 'connections']
        for field in required_fields:
            if field not in workflow:
                errors.append(f"Missing required field: {field}")
        return len(errors) == 0
    
    def _validate_nodes(self, nodes: List[Dict[str, Any]]) -> List[str]:
        """Validate the nodes in the workflow."""
        errors = []
        for i, node in enumerate(nodes):
            # Check required node fields
            if 'id' not in node:
                errors.append(f"Node {i}: Missing required field 'id'")
            if 'type' not in node:
                errors.append(f"Node {i}: Missing required field 'type'")
            if 'position' not in node:
                errors.append(f"Node {i}: Missing required field 'position'")
            
            # Validate node type
            if 'type' in node and not self._is_valid_node_type(node['type']):
                errors.append(f"Node {i}: Invalid node type '{node['type']}'")
        
        return errors
    
    def _validate_connections(self, connections: Dict[str, Any]) -> List[str]:
        """Validate the connections between nodes."""
        errors = []
        for source_id, connection in connections.items():
            if 'main' not in connection:
                errors.append(f"Connection for node {source_id}: Missing 'main' field")
                continue
                
            for main_connection in connection['main']:
                for target in main_connection:
                    if 'node' not in target:
                        errors.append(f"Connection for node {source_id}: Missing 'node' field in target")
                    if 'type' not in target:
                        errors.append(f"Connection for node {source_id}: Missing 'type' field in target")
                    if 'index' not in target:
                        errors.append(f"Connection for node {source_id}: Missing 'index' field in target")
        
        return errors
    
    def _check_best_practices(self, workflow: Dict[str, Any]) -> List[str]:
        """Check for workflow best practices."""
        warnings = []
        
        # Check for descriptive names
        if 'name' in workflow and len(workflow['name']) < 5:
            warnings.append("Workflow name is too short. Consider using a more descriptive name.")
        
        # Check for proper node spacing
        nodes = workflow.get('nodes', [])
        for i in range(len(nodes) - 1):
            pos1 = nodes[i].get('position', [0, 0])
            pos2 = nodes[i + 1].get('position', [0, 0])
            if abs(pos1[0] - pos2[0]) < 100 or abs(pos1[1] - pos2[1]) < 50:
                warnings.append(f"Nodes {i} and {i+1} are too close together. Consider increasing spacing.")
        
        return warnings
    
    def _generate_suggestions(self, workflow: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions for the workflow."""
        suggestions = []
        
        # Check for error handling
        has_error_handling = False
        for node in workflow.get('nodes', []):
            if node.get('type') == 'n8n-nodes-base.errorTrigger':
                has_error_handling = True
                break
        
        if not has_error_handling:
            suggestions.append("Consider adding error handling nodes to make the workflow more robust.")
        
        # Check for documentation
        if 'description' not in workflow:
            suggestions.append("Add a description to document the workflow's purpose.")
        
        return suggestions
    
    def _is_valid_node_type(self, node_type: str) -> bool:
        """Check if a node type is valid."""
        # TODO: Implement node type validation
        return True 