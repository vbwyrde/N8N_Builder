"""
Comprehensive Workflow Diffing and Comparison System
Provides detailed analysis of changes between N8N workflow versions.

Task 1.1.7: Implement basic workflow diffing/comparison
"""

import json
from .logging_config import get_logger
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import difflib

logger = get_logger(__name__)
diff_logger = get_logger('n8n_builder.diff')

class ChangeType(Enum):
    """Types of changes that can occur in workflows."""
    NODE_ADDED = "node_added"
    NODE_REMOVED = "node_removed"
    NODE_MODIFIED = "node_modified"
    NODE_RENAMED = "node_renamed"
    NODE_MOVED = "node_moved"
    CONNECTION_ADDED = "connection_added"
    CONNECTION_REMOVED = "connection_removed"
    CONNECTION_MODIFIED = "connection_modified"
    PARAMETER_ADDED = "parameter_added"
    PARAMETER_REMOVED = "parameter_removed"
    PARAMETER_MODIFIED = "parameter_modified"
    WORKFLOW_RENAMED = "workflow_renamed"
    WORKFLOW_SETTINGS_CHANGED = "workflow_settings_changed"

class DiffSeverity(Enum):
    """Severity levels for workflow changes."""
    MINOR = "minor"           # Parameter tweaks, cosmetic changes
    MODERATE = "moderate"     # Node parameter changes, connections
    MAJOR = "major"          # Node additions/removals, flow changes
    CRITICAL = "critical"    # Breaking changes, structure changes

@dataclass
class NodeDiff:
    """Detailed difference information for a single node."""
    node_id: str
    node_name: str
    change_type: ChangeType
    severity: DiffSeverity
    old_data: Optional[Dict[str, Any]] = None
    new_data: Optional[Dict[str, Any]] = None
    parameter_changes: Dict[str, Any] = field(default_factory=dict)
    position_changed: bool = False
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert node diff to dictionary."""
        return {
            'node_id': self.node_id,
            'node_name': self.node_name,
            'change_type': self.change_type.value,
            'severity': self.severity.value,
            'old_data': self.old_data,
            'new_data': self.new_data,
            'parameter_changes': self.parameter_changes,
            'position_changed': self.position_changed,
            'description': self.description
        }

@dataclass
class ConnectionDiff:
    """Detailed difference information for workflow connections."""
    source_node: str
    target_node: str
    connection_type: str
    change_type: ChangeType
    severity: DiffSeverity
    old_connection: Optional[Dict[str, Any]] = None
    new_connection: Optional[Dict[str, Any]] = None
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert connection diff to dictionary."""
        return {
            'source_node': self.source_node,
            'target_node': self.target_node,
            'connection_type': self.connection_type,
            'change_type': self.change_type.value,
            'severity': self.severity.value,
            'old_connection': self.old_connection,
            'new_connection': self.new_connection,
            'description': self.description
        }

@dataclass
class WorkflowDiff:
    """Comprehensive workflow difference analysis."""
    original_workflow_hash: str
    modified_workflow_hash: str
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    
    # High-level summary
    has_changes: bool = False
    overall_severity: DiffSeverity = DiffSeverity.MINOR
    change_summary: str = ""
    
    # Detailed changes
    node_diffs: List[NodeDiff] = field(default_factory=list)
    connection_diffs: List[ConnectionDiff] = field(default_factory=list)
    workflow_changes: Dict[str, Any] = field(default_factory=dict)
    
    # Statistics
    nodes_added: int = 0
    nodes_removed: int = 0
    nodes_modified: int = 0
    connections_added: int = 0
    connections_removed: int = 0
    connections_modified: int = 0
    parameters_changed: int = 0
    
    # Performance metrics
    analysis_duration_ms: float = 0.0
    comparison_complexity: str = "simple"  # simple, moderate, complex
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow diff to dictionary for serialization."""
        return {
            'original_workflow_hash': self.original_workflow_hash,
            'modified_workflow_hash': self.modified_workflow_hash,
            'analysis_timestamp': self.analysis_timestamp.isoformat(),
            'has_changes': self.has_changes,
            'overall_severity': self.overall_severity.value,
            'change_summary': self.change_summary,
            'node_diffs': [diff.to_dict() for diff in self.node_diffs],
            'connection_diffs': [diff.to_dict() for diff in self.connection_diffs],
            'workflow_changes': self.workflow_changes,
            'statistics': {
                'nodes_added': self.nodes_added,
                'nodes_removed': self.nodes_removed,
                'nodes_modified': self.nodes_modified,
                'connections_added': self.connections_added,
                'connections_removed': self.connections_removed,
                'connections_modified': self.connections_modified,
                'parameters_changed': self.parameters_changed
            },
            'performance_metrics': {
                'analysis_duration_ms': self.analysis_duration_ms,
                'comparison_complexity': self.comparison_complexity
            }
        }
    
    def get_human_readable_summary(self) -> str:
        """Generate human-readable summary of changes."""
        if not self.has_changes:
            return "No changes detected between workflow versions."
        
        summary_parts = []
        
        # Node changes
        if self.nodes_added > 0:
            summary_parts.append(f"{self.nodes_added} node(s) added")
        if self.nodes_removed > 0:
            summary_parts.append(f"{self.nodes_removed} node(s) removed")
        if self.nodes_modified > 0:
            summary_parts.append(f"{self.nodes_modified} node(s) modified")
        
        # Connection changes
        if self.connections_added > 0:
            summary_parts.append(f"{self.connections_added} connection(s) added")
        if self.connections_removed > 0:
            summary_parts.append(f"{self.connections_removed} connection(s) removed")
        if self.connections_modified > 0:
            summary_parts.append(f"{self.connections_modified} connection(s) modified")
        
        # Parameter changes
        if self.parameters_changed > 0:
            summary_parts.append(f"{self.parameters_changed} parameter(s) changed")
        
        base_summary = ", ".join(summary_parts)
        return f"{base_summary}. Overall severity: {self.overall_severity.value}."

class WorkflowDiffer:
    """Advanced workflow diffing and comparison engine."""
    
    def __init__(self):
        """Initialize the workflow differ."""
        self.diff_cache: Dict[str, WorkflowDiff] = {}
        self.comparison_history: List[WorkflowDiff] = []
        
        diff_logger.info("Workflow differ initialized")
    
    def compute_workflow_hash(self, workflow_json: str) -> str:
        """Compute a hash for a workflow for comparison purposes."""
        try:
            # Parse and normalize the workflow for consistent hashing
            workflow = json.loads(workflow_json)
            
            # Create a normalized version for hashing (order-independent)
            normalized = {
                'name': workflow.get('name', ''),
                'nodes': sorted(workflow.get('nodes', []), key=lambda x: x.get('id', '')),
                'connections': workflow.get('connections', {}),
                'settings': workflow.get('settings', {}),
                'active': workflow.get('active', True)
            }
            
            # Convert to JSON string with consistent ordering
            normalized_json = json.dumps(normalized, sort_keys=True, separators=(',', ':'))
            
            # Generate SHA-256 hash
            return hashlib.sha256(normalized_json.encode('utf-8')).hexdigest()[:16]
            
        except Exception as e:
            diff_logger.exception(f"Error computing workflow hash: {str(e)}", extra={'operation': 'compute_workflow_hash'})
            return hashlib.sha256(workflow_json.encode('utf-8')).hexdigest()[:16]
    
    def compare_workflows(self, 
                         original_json: str, 
                         modified_json: str,
                         cache_result: bool = True) -> WorkflowDiff:
        """
        Perform comprehensive comparison between two workflow versions.
        
        Args:
            original_json: Original workflow JSON string
            modified_json: Modified workflow JSON string  
            cache_result: Whether to cache the result for future use
            
        Returns:
            WorkflowDiff object containing detailed comparison results
        """
        start_time = datetime.now()
        
        # Compute hashes for caching
        original_hash = self.compute_workflow_hash(original_json)
        modified_hash = self.compute_workflow_hash(modified_json)
        
        # Check cache first
        cache_key = f"{original_hash}:{modified_hash}"
        if cache_key in self.diff_cache:
            diff_logger.info(f"Returning cached diff result for workflows")
            return self.diff_cache[cache_key]
        
        diff_logger.info(f"Starting workflow comparison", extra={
            'original_hash': original_hash,
            'modified_hash': modified_hash
        })
        
        # Initialize diff result
        workflow_diff = WorkflowDiff(
            original_workflow_hash=original_hash,
            modified_workflow_hash=modified_hash
        )
        
        try:
            # Parse workflows
            original_workflow = json.loads(original_json)
            modified_workflow = json.loads(modified_json)
            
            # Determine comparison complexity
            original_node_count = len(original_workflow.get('nodes', []))
            modified_node_count = len(modified_workflow.get('nodes', []))
            total_nodes = original_node_count + modified_node_count
            
            if total_nodes > 100:
                workflow_diff.comparison_complexity = "complex"
            elif total_nodes > 20:
                workflow_diff.comparison_complexity = "moderate"
            else:
                workflow_diff.comparison_complexity = "simple"
            
            # Perform detailed comparison
            self._compare_workflow_metadata(original_workflow, modified_workflow, workflow_diff)
            self._compare_nodes(original_workflow, modified_workflow, workflow_diff)
            self._compare_connections(original_workflow, modified_workflow, workflow_diff)
            
            # Calculate overall statistics and severity
            self._calculate_diff_statistics(workflow_diff)
            self._determine_overall_severity(workflow_diff)
            self._generate_change_summary(workflow_diff)
            
            # Record performance metrics
            end_time = datetime.now()
            workflow_diff.analysis_duration_ms = (end_time - start_time).total_seconds() * 1000
            
            # Cache result if requested
            if cache_result:
                self.diff_cache[cache_key] = workflow_diff
            
            # Add to comparison history
            self.comparison_history.append(workflow_diff)
            
            diff_logger.info(f"Workflow comparison completed", extra={
                'has_changes': workflow_diff.has_changes,
                'overall_severity': workflow_diff.overall_severity.value,
                'nodes_changed': workflow_diff.nodes_added + workflow_diff.nodes_removed + workflow_diff.nodes_modified,
                'analysis_duration_ms': workflow_diff.analysis_duration_ms
            })
            
            return workflow_diff
            
        except Exception as e:
            error_msg = f"Error comparing workflows: {str(e)}"
            diff_logger.exception(error_msg, extra={'operation': 'compare_workflows', 'original_hash': original_hash, 'modified_hash': modified_hash})
            
            # Return error diff
            workflow_diff.has_changes = False
            workflow_diff.change_summary = f"Comparison failed: {error_msg}"
            workflow_diff.overall_severity = DiffSeverity.CRITICAL
            return workflow_diff
    
    def _compare_workflow_metadata(self, 
                                  original: Dict[str, Any], 
                                  modified: Dict[str, Any], 
                                  diff: WorkflowDiff) -> None:
        """Compare workflow-level metadata (name, settings, etc.)."""
        
        # Compare workflow name
        if original.get('name') != modified.get('name'):
            diff.workflow_changes['name_changed'] = {
                'old_name': original.get('name'),
                'new_name': modified.get('name')
            }
        
        # Compare workflow settings
        original_settings = original.get('settings', {})
        modified_settings = modified.get('settings', {})
        
        if original_settings != modified_settings:
            diff.workflow_changes['settings_changed'] = {
                'old_settings': original_settings,
                'new_settings': modified_settings
            }
        
        # Compare active status
        if original.get('active') != modified.get('active'):
            diff.workflow_changes['active_status_changed'] = {
                'old_active': original.get('active'),
                'new_active': modified.get('active')
            }
    
    def _compare_nodes(self, 
                      original: Dict[str, Any], 
                      modified: Dict[str, Any], 
                      diff: WorkflowDiff) -> None:
        """Compare nodes between workflow versions."""
        
        original_nodes = {node['id']: node for node in original.get('nodes', [])}
        modified_nodes = {node['id']: node for node in modified.get('nodes', [])}
        
        original_node_ids = set(original_nodes.keys())
        modified_node_ids = set(modified_nodes.keys())
        
        # Find added nodes
        added_node_ids = modified_node_ids - original_node_ids
        for node_id in added_node_ids:
            node = modified_nodes[node_id]
            node_diff = NodeDiff(
                node_id=node_id,
                node_name=node.get('name', f'Node {node_id}'),
                change_type=ChangeType.NODE_ADDED,
                severity=DiffSeverity.MAJOR,
                new_data=node,
                description=f"Added new node '{node.get('name')}' of type '{node.get('type')}'"
            )
            diff.node_diffs.append(node_diff)
        
        # Find removed nodes
        removed_node_ids = original_node_ids - modified_node_ids
        for node_id in removed_node_ids:
            node = original_nodes[node_id]
            node_diff = NodeDiff(
                node_id=node_id,
                node_name=node.get('name', f'Node {node_id}'),
                change_type=ChangeType.NODE_REMOVED,
                severity=DiffSeverity.MAJOR,
                old_data=node,
                description=f"Removed node '{node.get('name')}' of type '{node.get('type')}'"
            )
            diff.node_diffs.append(node_diff)
        
        # Find modified nodes
        common_node_ids = original_node_ids & modified_node_ids
        for node_id in common_node_ids:
            original_node = original_nodes[node_id]
            modified_node = modified_nodes[node_id]
            
            node_diff = self._compare_individual_nodes(original_node, modified_node)
            if node_diff:
                diff.node_diffs.append(node_diff)
    
    def _compare_individual_nodes(self, 
                                 original_node: Dict[str, Any], 
                                 modified_node: Dict[str, Any]) -> Optional[NodeDiff]:
        """Compare two individual nodes for differences."""
        
        node_id = original_node.get('id')
        node_name = original_node.get('name', f'Node {node_id}')
        changes_detected = False
        parameter_changes = {}
        position_changed = False
        change_descriptions = []
        
        # Compare node name
        if original_node.get('name') != modified_node.get('name'):
            changes_detected = True
            change_descriptions.append(f"Name changed from '{original_node.get('name')}' to '{modified_node.get('name')}'")
        
        # Compare node type (this is unusual but possible)
        if original_node.get('type') != modified_node.get('type'):
            changes_detected = True
            change_descriptions.append(f"Type changed from '{original_node.get('type')}' to '{modified_node.get('type')}'")
        
        # Compare parameters
        original_params = original_node.get('parameters', {})
        modified_params = modified_node.get('parameters', {})
        
        param_diff = self._compare_parameters(original_params, modified_params)
        if param_diff:
            changes_detected = True
            parameter_changes = param_diff
            change_descriptions.append(f"{len(param_diff)} parameter(s) changed")
        
        # Compare position
        original_pos = original_node.get('position', [0, 0])
        modified_pos = modified_node.get('position', [0, 0])
        if original_pos != modified_pos:
            position_changed = True
            # Position changes are minor unless it's a significant move
            pos_distance = ((modified_pos[0] - original_pos[0])**2 + (modified_pos[1] - original_pos[1])**2)**0.5
            if pos_distance > 100:  # Significant position change
                changes_detected = True
                change_descriptions.append(f"Position moved significantly")
        
        if changes_detected or position_changed:
            # Determine severity
            severity = DiffSeverity.MINOR
            if parameter_changes or original_node.get('type') != modified_node.get('type'):
                severity = DiffSeverity.MODERATE
            if original_node.get('name') != modified_node.get('name'):
                severity = DiffSeverity.MODERATE
            
            return NodeDiff(
                node_id=node_id,
                node_name=node_name,
                change_type=ChangeType.NODE_MODIFIED,
                severity=severity,
                old_data=original_node,
                new_data=modified_node,
                parameter_changes=parameter_changes,
                position_changed=position_changed,
                description="; ".join(change_descriptions)
            )
        
        return None
    
    def _compare_parameters(self, 
                           original_params: Dict[str, Any], 
                           modified_params: Dict[str, Any]) -> Dict[str, Any]:
        """Compare parameter dictionaries and return changes."""
        
        changes = {}
        
        # Find all parameter keys
        all_keys = set(original_params.keys()) | set(modified_params.keys())
        
        for key in all_keys:
            original_value = original_params.get(key)
            modified_value = modified_params.get(key)
            
            if key not in original_params:
                changes[key] = {
                    'change_type': 'added',
                    'old_value': None,
                    'new_value': modified_value
                }
            elif key not in modified_params:
                changes[key] = {
                    'change_type': 'removed',
                    'old_value': original_value,
                    'new_value': None
                }
            elif original_value != modified_value:
                changes[key] = {
                    'change_type': 'modified',
                    'old_value': original_value,
                    'new_value': modified_value
                }
        
        return changes
    
    def _compare_connections(self, 
                           original: Dict[str, Any], 
                           modified: Dict[str, Any], 
                           diff: WorkflowDiff) -> None:
        """Compare connections between workflow versions."""
        
        original_connections = original.get('connections', {})
        modified_connections = modified.get('connections', {})
        
        # Convert connections to a comparable format
        original_conn_set = self._normalize_connections(original_connections)
        modified_conn_set = self._normalize_connections(modified_connections)
        
        # Find added connections
        added_connections = modified_conn_set - original_conn_set
        for conn in added_connections:
            source, target, conn_type = conn
            conn_diff = ConnectionDiff(
                source_node=source,
                target_node=target,
                connection_type=conn_type,
                change_type=ChangeType.CONNECTION_ADDED,
                severity=DiffSeverity.MODERATE,
                new_connection={'source': source, 'target': target, 'type': conn_type},
                description=f"Added connection from '{source}' to '{target}' via '{conn_type}'"
            )
            diff.connection_diffs.append(conn_diff)
        
        # Find removed connections
        removed_connections = original_conn_set - modified_conn_set
        for conn in removed_connections:
            source, target, conn_type = conn
            conn_diff = ConnectionDiff(
                source_node=source,
                target_node=target,
                connection_type=conn_type,
                change_type=ChangeType.CONNECTION_REMOVED,
                severity=DiffSeverity.MODERATE,
                old_connection={'source': source, 'target': target, 'type': conn_type},
                description=f"Removed connection from '{source}' to '{target}' via '{conn_type}'"
            )
            diff.connection_diffs.append(conn_diff)
    
    def _normalize_connections(self, connections: Dict[str, Any]) -> Set[Tuple[str, str, str]]:
        """Normalize connections to a set of tuples for comparison."""
        
        connection_set = set()
        
        for source_node, conn_data in connections.items():
            if isinstance(conn_data, dict):
                for conn_type, target_lists in conn_data.items():
                    if isinstance(target_lists, list):
                        for target_list in target_lists:
                            if isinstance(target_list, list):
                                for target in target_list:
                                    if isinstance(target, dict) and 'node' in target:
                                        connection_set.add((source_node, target['node'], conn_type))
        
        return connection_set
    
    def _calculate_diff_statistics(self, diff: WorkflowDiff) -> None:
        """Calculate summary statistics for the diff."""
        
        # Count changes by type
        for node_diff in diff.node_diffs:
            if node_diff.change_type == ChangeType.NODE_ADDED:
                diff.nodes_added += 1
            elif node_diff.change_type == ChangeType.NODE_REMOVED:
                diff.nodes_removed += 1
            elif node_diff.change_type == ChangeType.NODE_MODIFIED:
                diff.nodes_modified += 1
            
            # Count parameter changes
            diff.parameters_changed += len(node_diff.parameter_changes)
        
        for conn_diff in diff.connection_diffs:
            if conn_diff.change_type == ChangeType.CONNECTION_ADDED:
                diff.connections_added += 1
            elif conn_diff.change_type == ChangeType.CONNECTION_REMOVED:
                diff.connections_removed += 1
            elif conn_diff.change_type == ChangeType.CONNECTION_MODIFIED:
                diff.connections_modified += 1
        
        # Determine if there are changes
        diff.has_changes = (
            diff.nodes_added > 0 or diff.nodes_removed > 0 or diff.nodes_modified > 0 or
            diff.connections_added > 0 or diff.connections_removed > 0 or diff.connections_modified > 0 or
            len(diff.workflow_changes) > 0
        )
    
    def _determine_overall_severity(self, diff: WorkflowDiff) -> None:
        """Determine the overall severity of changes."""
        
        if not diff.has_changes:
            diff.overall_severity = DiffSeverity.MINOR
            return
        
        # Count severity levels
        critical_changes = 0
        major_changes = 0
        moderate_changes = 0
        minor_changes = 0
        
        for node_diff in diff.node_diffs:
            if node_diff.severity == DiffSeverity.CRITICAL:
                critical_changes += 1
            elif node_diff.severity == DiffSeverity.MAJOR:
                major_changes += 1
            elif node_diff.severity == DiffSeverity.MODERATE:
                moderate_changes += 1
            else:
                minor_changes += 1
        
        for conn_diff in diff.connection_diffs:
            if conn_diff.severity == DiffSeverity.CRITICAL:
                critical_changes += 1
            elif conn_diff.severity == DiffSeverity.MAJOR:
                major_changes += 1
            elif conn_diff.severity == DiffSeverity.MODERATE:
                moderate_changes += 1
            else:
                minor_changes += 1
        
        # Determine overall severity
        if critical_changes > 0:
            diff.overall_severity = DiffSeverity.CRITICAL
        elif major_changes > 0:
            diff.overall_severity = DiffSeverity.MAJOR
        elif moderate_changes > 0:
            diff.overall_severity = DiffSeverity.MODERATE
        else:
            diff.overall_severity = DiffSeverity.MINOR
    
    def _generate_change_summary(self, diff: WorkflowDiff) -> None:
        """Generate a human-readable change summary."""
        
        if not diff.has_changes:
            diff.change_summary = "No changes detected"
            return
        
        summary_parts = []
        
        # Node changes
        if diff.nodes_added > 0:
            summary_parts.append(f"Added {diff.nodes_added} node(s)")
        if diff.nodes_removed > 0:
            summary_parts.append(f"Removed {diff.nodes_removed} node(s)")
        if diff.nodes_modified > 0:
            summary_parts.append(f"Modified {diff.nodes_modified} node(s)")
        
        # Connection changes
        if diff.connections_added > 0:
            summary_parts.append(f"Added {diff.connections_added} connection(s)")
        if diff.connections_removed > 0:
            summary_parts.append(f"Removed {diff.connections_removed} connection(s)")
        
        # Parameter changes
        if diff.parameters_changed > 0:
            summary_parts.append(f"Changed {diff.parameters_changed} parameter(s)")
        
        # Workflow changes
        if diff.workflow_changes:
            workflow_change_count = len(diff.workflow_changes)
            summary_parts.append(f"Modified {workflow_change_count} workflow setting(s)")
        
        diff.change_summary = "; ".join(summary_parts)
    
    def generate_html_diff_report(self, diff: WorkflowDiff) -> str:
        """Generate an HTML report of the workflow differences."""
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Workflow Diff Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .summary {{ background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .severity-minor {{ color: #28a745; }}
                .severity-moderate {{ color: #ffc107; }}
                .severity-major {{ color: #fd7e14; }}
                .severity-critical {{ color: #dc3545; }}
                .change-section {{ margin-bottom: 20px; }}
                .change-item {{ margin-bottom: 10px; padding: 10px; border-left: 3px solid #007bff; background-color: #f8f9fa; }}
                .added {{ border-left-color: #28a745; }}
                .removed {{ border-left-color: #dc3545; }}
                .modified {{ border-left-color: #ffc107; }}
                .parameter-change {{ margin-left: 20px; font-size: 0.9em; color: #6c757d; }}
                pre {{ background-color: #f8f9fa; padding: 10px; border-radius: 3px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <h1>Workflow Diff Report</h1>
            
            <div class="summary">
                <h2>Summary</h2>
                <p><strong>Overall Severity:</strong> <span class="severity-{diff.overall_severity.value}">{diff.overall_severity.value.upper()}</span></p>
                <p><strong>Changes Detected:</strong> {'Yes' if diff.has_changes else 'No'}</p>
                <p><strong>Description:</strong> {diff.change_summary}</p>
                <p><strong>Analysis Duration:</strong> {diff.analysis_duration_ms:.2f}ms</p>
                <p><strong>Timestamp:</strong> {diff.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        """
        
        # Node changes section
        if diff.node_diffs:
            html += """
            <div class="change-section">
                <h2>Node Changes</h2>
            """
            
            for node_diff in diff.node_diffs:
                change_class = node_diff.change_type.value.replace('_', '-')
                html += f"""
                <div class="change-item {change_class}">
                    <h3>{node_diff.node_name} ({node_diff.node_id})</h3>
                    <p><strong>Change Type:</strong> {node_diff.change_type.value.replace('_', ' ').title()}</p>
                    <p><strong>Severity:</strong> <span class="severity-{node_diff.severity.value}">{node_diff.severity.value.upper()}</span></p>
                    <p><strong>Description:</strong> {node_diff.description}</p>
                """
                
                if node_diff.parameter_changes:
                    html += "<h4>Parameter Changes:</h4>"
                    for param_name, param_change in node_diff.parameter_changes.items():
                        html += f"""
                        <div class="parameter-change">
                            <strong>{param_name}:</strong> {param_change['change_type']}
                            {f" | Old: {param_change['old_value']}" if param_change['old_value'] is not None else ""}
                            {f" | New: {param_change['new_value']}" if param_change['new_value'] is not None else ""}
                        </div>
                        """
                
                html += "</div>"
            
            html += "</div>"
        
        # Connection changes section
        if diff.connection_diffs:
            html += """
            <div class="change-section">
                <h2>Connection Changes</h2>
            """
            
            for conn_diff in diff.connection_diffs:
                change_class = conn_diff.change_type.value.replace('_', '-')
                html += f"""
                <div class="change-item {change_class}">
                    <h3>Connection: {conn_diff.source_node} → {conn_diff.target_node}</h3>
                    <p><strong>Change Type:</strong> {conn_diff.change_type.value.replace('_', ' ').title()}</p>
                    <p><strong>Connection Type:</strong> {conn_diff.connection_type}</p>
                    <p><strong>Severity:</strong> <span class="severity-{conn_diff.severity.value}">{conn_diff.severity.value.upper()}</span></p>
                    <p><strong>Description:</strong> {conn_diff.description}</p>
                </div>
                """
            
            html += "</div>"
        
        # Statistics section
        html += f"""
            <div class="change-section">
                <h2>Statistics</h2>
                <ul>
                    <li>Nodes Added: {diff.nodes_added}</li>
                    <li>Nodes Removed: {diff.nodes_removed}</li>
                    <li>Nodes Modified: {diff.nodes_modified}</li>
                    <li>Connections Added: {diff.connections_added}</li>
                    <li>Connections Removed: {diff.connections_removed}</li>
                    <li>Parameters Changed: {diff.parameters_changed}</li>
                </ul>
            </div>
            
            </body>
            </html>
        """
        
        return html
    
    def get_comparison_history(self) -> List[WorkflowDiff]:
        """Get the history of workflow comparisons."""
        return self.comparison_history.copy()
    
    def clear_cache(self) -> None:
        """Clear the diff cache."""
        self.diff_cache.clear()
        diff_logger.info("Diff cache cleared")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            'cache_size': len(self.diff_cache),
            'comparison_history_size': len(self.comparison_history),
            'cache_keys': list(self.diff_cache.keys())
        }

# Global workflow differ instance
workflow_differ = WorkflowDiffer() 