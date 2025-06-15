#!/usr/bin/env python3
"""
Test Suite for Workflow Diffing and Comparison System
Validates detailed workflow comparison, change detection, and diff reporting.

Task 1.1.7: Implement basic workflow diffing/comparison - Testing
"""

import unittest
import json
import time
from pathlib import Path
import sys
from datetime import datetime

# Add the n8n_builder module to path
sys.path.append(str(Path(__file__).parent.parent))

from n8n_builder.workflow_differ import (
    WorkflowDiffer, 
    WorkflowDiff, 
    NodeDiff, 
    ConnectionDiff,
    ChangeType, 
    DiffSeverity,
    workflow_differ
)
from n8n_builder.n8n_builder import N8NBuilder

class TestWorkflowDiffer(unittest.TestCase):
    """Test the core workflow diffing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.differ = WorkflowDiffer()
        
        # Sample workflows for testing
        self.simple_workflow = {
            "name": "Simple Test Workflow",
            "nodes": [
                {
                    "id": "1",
                    "name": "Start",
                    "type": "n8n-nodes-base.start",
                    "parameters": {},
                    "position": [100, 100]
                },
                {
                    "id": "2", 
                    "name": "Email",
                    "type": "n8n-nodes-base.emailSend",
                    "parameters": {
                        "to": "test@example.com",
                        "subject": "Test Email"
                    },
                    "position": [300, 100]
                }
            ],
            "connections": {
                "Start": {
                    "main": [
                        [
                            {
                                "node": "Email",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                }
            },
            "settings": {},
            "active": True
        }
    
    def test_workflow_hash_computation(self):
        """Test workflow hash computation for consistency."""
        workflow_json = json.dumps(self.simple_workflow)
        
        # Same workflow should produce same hash
        hash1 = self.differ.compute_workflow_hash(workflow_json)
        hash2 = self.differ.compute_workflow_hash(workflow_json)
        self.assertEqual(hash1, hash2)
        
        # Hash should be 16 characters (truncated SHA-256)
        self.assertEqual(len(hash1), 16)
    
    def test_identical_workflows_comparison(self):
        """Test comparing identical workflows."""
        workflow_json = json.dumps(self.simple_workflow)
        
        diff = self.differ.compare_workflows(workflow_json, workflow_json)
        
        self.assertFalse(diff.has_changes)
        self.assertEqual(diff.overall_severity, DiffSeverity.MINOR)
        self.assertEqual(diff.nodes_added, 0)
        self.assertEqual(diff.nodes_removed, 0)
        self.assertEqual(diff.nodes_modified, 0)
        self.assertEqual(diff.connections_added, 0)
        self.assertEqual(diff.connections_removed, 0)
        self.assertEqual(len(diff.node_diffs), 0)
        self.assertEqual(len(diff.connection_diffs), 0)
        self.assertEqual(diff.change_summary, "No changes detected")
    
    def test_node_addition_detection(self):
        """Test detection of added nodes."""
        original_json = json.dumps(self.simple_workflow)
        
        # Add a new node
        modified_workflow = json.loads(original_json)
        new_node = {
            "id": "3",
            "name": "Database Log",
            "type": "n8n-nodes-base.postgres",
            "parameters": {
                "operation": "insert",
                "table": "logs"
            },
            "position": [500, 100]
        }
        modified_workflow["nodes"].append(new_node)
        modified_json = json.dumps(modified_workflow)
        
        diff = self.differ.compare_workflows(original_json, modified_json)
        
        self.assertTrue(diff.has_changes)
        self.assertEqual(diff.nodes_added, 1)
        self.assertEqual(diff.nodes_removed, 0)
        self.assertEqual(diff.nodes_modified, 0)
        self.assertEqual(len(diff.node_diffs), 1)
        
        added_node_diff = diff.node_diffs[0]
        self.assertEqual(added_node_diff.change_type, ChangeType.NODE_ADDED)
        self.assertEqual(added_node_diff.node_id, "3")
        self.assertEqual(added_node_diff.node_name, "Database Log")
        self.assertEqual(added_node_diff.severity, DiffSeverity.MAJOR)
        self.assertIsNotNone(added_node_diff.new_data)
        self.assertIsNone(added_node_diff.old_data)
    
    def test_node_modification_detection(self):
        """Test detection of modified nodes."""
        original_json = json.dumps(self.simple_workflow)
        
        # Modify node parameters
        modified_workflow = json.loads(original_json)
        email_node = next(n for n in modified_workflow["nodes"] if n["id"] == "2")
        email_node["parameters"]["to"] = "modified@example.com"
        email_node["parameters"]["subject"] = "Modified Subject"
        email_node["parameters"]["new_field"] = "new_value"
        modified_json = json.dumps(modified_workflow)
        
        diff = self.differ.compare_workflows(original_json, modified_json)
        
        self.assertTrue(diff.has_changes)
        self.assertEqual(diff.nodes_added, 0)
        self.assertEqual(diff.nodes_removed, 0)
        self.assertEqual(diff.nodes_modified, 1)
        self.assertGreater(diff.parameters_changed, 0)
        
        modified_node_diff = diff.node_diffs[0]
        self.assertEqual(modified_node_diff.change_type, ChangeType.NODE_MODIFIED)
        self.assertEqual(modified_node_diff.node_id, "2")
        self.assertEqual(modified_node_diff.severity, DiffSeverity.MODERATE)
        
        # Check parameter changes
        param_changes = modified_node_diff.parameter_changes
        self.assertIn("to", param_changes)
        self.assertIn("subject", param_changes)
        self.assertIn("new_field", param_changes)
        
        self.assertEqual(param_changes["to"]["change_type"], "modified")
        self.assertEqual(param_changes["to"]["old_value"], "test@example.com")
        self.assertEqual(param_changes["to"]["new_value"], "modified@example.com")
        
        self.assertEqual(param_changes["new_field"]["change_type"], "added")
        self.assertEqual(param_changes["new_field"]["new_value"], "new_value")
    
    def test_human_readable_summary(self):
        """Test human-readable summary generation."""
        original_json = json.dumps(self.simple_workflow)
        
        # Make several changes
        modified_workflow = json.loads(original_json)
        # Add node
        modified_workflow["nodes"].append({
            "id": "3",
            "name": "New Node",
            "type": "n8n-nodes-base.noOp",
            "parameters": {},
            "position": [500, 100]
        })
        # Modify existing node
        modified_workflow["nodes"][1]["parameters"]["to"] = "new@example.com"
        modified_json = json.dumps(modified_workflow)
        
        diff = self.differ.compare_workflows(original_json, modified_json)
        summary = diff.get_human_readable_summary()
        
        self.assertIsInstance(summary, str)
        self.assertIn("node", summary.lower())
        self.assertIn("parameter", summary.lower())
        self.assertIn("severity", summary.lower())

class TestN8NBuilderDiffIntegration(unittest.TestCase):
    """Test N8N Builder integration with workflow diffing."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.builder = N8NBuilder()
        
        self.sample_workflow_1 = {
            "name": "Email Workflow",
            "nodes": [
                {
                    "id": "1",
                    "name": "Trigger",
                    "type": "n8n-nodes-base.manualTrigger",
                    "parameters": {},
                    "position": [100, 100]
                },
                {
                    "id": "2",
                    "name": "Send Email",
                    "type": "n8n-nodes-base.emailSend",
                    "parameters": {
                        "to": "user@example.com",
                        "subject": "Test"
                    },
                    "position": [300, 100]
                }
            ],
            "connections": {
                "Trigger": {
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
            "active": True
        }
        
        self.sample_workflow_2 = {
            "name": "Enhanced Email Workflow",
            "nodes": [
                {
                    "id": "1",
                    "name": "Trigger",
                    "type": "n8n-nodes-base.manualTrigger",
                    "parameters": {},
                    "position": [100, 100]
                },
                {
                    "id": "2",
                    "name": "Send Email",
                    "type": "n8n-nodes-base.emailSend",
                    "parameters": {
                        "to": "admin@example.com",
                        "subject": "Enhanced Test",
                        "attachments": True
                    },
                    "position": [300, 100]
                },
                {
                    "id": "3",
                    "name": "Log Action",
                    "type": "n8n-nodes-base.function",
                    "parameters": {
                        "code": "console.log('Email sent');"
                    },
                    "position": [500, 100]
                }
            ],
            "connections": {
                "Trigger": {
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
                                "node": "Log Action",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                }
            },
            "settings": {},
            "active": True
        }
    
    def test_enhanced_summarize_changes(self):
        """Test enhanced _summarize_changes method."""
        original_json = json.dumps(self.sample_workflow_1)
        modified_json = json.dumps(self.sample_workflow_2)
        
        # Clear any existing cache to ensure fresh analysis
        workflow_differ.clear_cache()
        
        summary = self.builder._summarize_changes(original_json, modified_json)
        
        # Check basic compatibility fields
        self.assertIn("nodes_added", summary)
        self.assertIn("connections_changed", summary)
        self.assertIn("parameters_modified", summary)
        
        # Check enhanced fields
        self.assertIn("detailed_analysis", summary)
        self.assertIn("has_changes", summary)
        self.assertIn("overall_severity", summary)
        self.assertIn("change_summary", summary)
        self.assertIn("human_readable_summary", summary)
        self.assertIn("analysis_duration_ms", summary)
        
        # Verify values
        self.assertTrue(summary["has_changes"])
        self.assertEqual(summary["nodes_added"], 1)
        self.assertTrue(summary["parameters_modified"])
        self.assertIsInstance(summary["analysis_duration_ms"], float)
        # Note: analysis_duration_ms might be 0.0 due to caching, which is acceptable
        self.assertGreaterEqual(summary["analysis_duration_ms"], 0)
    
    def test_compare_workflow_versions_method(self):
        """Test compare_workflow_versions method."""
        original_json = json.dumps(self.sample_workflow_1)
        modified_json = json.dumps(self.sample_workflow_2)
        
        diff = self.builder.compare_workflow_versions(original_json, modified_json)
        
        self.assertIsInstance(diff, WorkflowDiff)
        self.assertTrue(diff.has_changes)
        self.assertEqual(diff.nodes_added, 1)
        self.assertGreater(diff.parameters_changed, 0)
        self.assertEqual(diff.overall_severity, DiffSeverity.MAJOR)
    
    def test_generate_workflow_diff_report_html(self):
        """Test HTML diff report generation."""
        original_json = json.dumps(self.sample_workflow_1)
        modified_json = json.dumps(self.sample_workflow_2)
        
        html_report = self.builder.generate_workflow_diff_report(
            original_json, modified_json, format="html"
        )
        
        self.assertIsInstance(html_report, str)
        self.assertIn("<!DOCTYPE html>", html_report)
        self.assertIn("Workflow Diff Report", html_report)
        self.assertIn("MAJOR", html_report)  # Severity
        self.assertIn("Log Action", html_report)  # Added node
        self.assertIn("parameter", html_report.lower())
    
    def test_generate_workflow_diff_report_text(self):
        """Test text diff report generation."""
        original_json = json.dumps(self.sample_workflow_1)
        modified_json = json.dumps(self.sample_workflow_2)
        
        text_report = self.builder.generate_workflow_diff_report(
            original_json, modified_json, format="text"
        )
        
        self.assertIsInstance(text_report, str)
        self.assertIn("WORKFLOW DIFF REPORT", text_report)
        self.assertIn("STATISTICS:", text_report)
        self.assertIn("NODE CHANGES:", text_report)
        self.assertIn("+ Log Action", text_report)  # Added node
        self.assertIn("~ Send Email", text_report)  # Modified node
    
    def test_generate_workflow_diff_report_json(self):
        """Test JSON diff report generation."""
        original_json = json.dumps(self.sample_workflow_1)
        modified_json = json.dumps(self.sample_workflow_2)
        
        json_report = self.builder.generate_workflow_diff_report(
            original_json, modified_json, format="json"
        )
        
        self.assertIsInstance(json_report, str)
        
        # Parse the JSON to verify structure
        report_data = json.loads(json_report)
        self.assertIn("has_changes", report_data)
        self.assertIn("overall_severity", report_data)
        self.assertIn("node_diffs", report_data)
        self.assertIn("statistics", report_data)
        
        self.assertTrue(report_data["has_changes"])
        self.assertEqual(report_data["overall_severity"], "major")
    
    def test_get_workflow_diff_history(self):
        """Test workflow diff history retrieval."""
        original_json = json.dumps(self.sample_workflow_1)
        modified_json = json.dumps(self.sample_workflow_2)
        
        # Perform some comparisons
        self.builder.compare_workflow_versions(original_json, modified_json)
        self.builder.compare_workflow_versions(modified_json, original_json)
        
        history = self.builder.get_workflow_diff_history()
        
        self.assertIsInstance(history, list)
        self.assertGreaterEqual(len(history), 2)
        
        # Check history entry structure
        for entry in history:
            self.assertIn("has_changes", entry)
            self.assertIn("overall_severity", entry)
            self.assertIn("analysis_timestamp", entry)
            self.assertIn("statistics", entry)
    
    def test_diff_report_invalid_format(self):
        """Test error handling for invalid report format."""
        original_json = json.dumps(self.sample_workflow_1)
        modified_json = json.dumps(self.sample_workflow_2)
        
        with self.assertRaises(ValueError) as context:
            self.builder.generate_workflow_diff_report(
                original_json, modified_json, format="invalid"
            )
        
        self.assertIn("Unsupported format", str(context.exception))
    
    def test_fallback_on_diff_error(self):
        """Test fallback behavior when diffing fails."""
        # Invalid JSON should trigger fallback
        invalid_json = "{'invalid': json}"
        valid_json = json.dumps(self.sample_workflow_1)
        
        summary = self.builder._summarize_changes(invalid_json, valid_json)
        
        # The comprehensive diffing system handles errors gracefully
        # Check for error indication in change_summary or overall_severity
        self.assertTrue(
            "error" in summary.get("change_summary", "").lower() or 
            summary.get("overall_severity") == "critical" or
            "comparison failed" in summary.get("change_summary", "").lower()
        )
        
        # Should still have basic structure
        self.assertIn("has_changes", summary)
        self.assertIn("overall_severity", summary)

if __name__ == '__main__':
    # Run with increased verbosity to see detailed test output
    unittest.main(verbosity=2) 