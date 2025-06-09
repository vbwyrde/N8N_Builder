from typing import Dict, List, Tuple, Any
from pydantic import BaseModel
import json
import re

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]

class BaseWorkflowValidator:
    """Base class for workflow validation."""
    
    def validate_workflow(self, workflow_json: str) -> ValidationResult:
        """Validate a workflow JSON string."""
        try:
            # Basic JSON validation
            workflow = json.loads(workflow_json)
            
            errors = []
            warnings = []
            suggestions = []
            
            # Validate basic structure
            if not self._validate_basic_structure(workflow, errors):
                return ValidationResult(is_valid=False, errors=errors, warnings=warnings, suggestions=suggestions)
            
            # Validate nodes
            node_errors = self._validate_nodes(workflow.get('nodes', []))
            errors.extend(node_errors)
            
            # Validate connections
            connection_errors = self._validate_connections(workflow.get('connections', {}))
            errors.extend(connection_errors)
            
            # Check for best practices
            warnings.extend(self._check_best_practices(workflow))
            
            # Generate suggestions
            suggestions.extend(self._generate_suggestions(workflow))
            
            return ValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions
            )
            
        except json.JSONDecodeError as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Invalid JSON: {str(e)}"],
                warnings=[],
                suggestions=[]
            )
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                warnings=[],
                suggestions=[]
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