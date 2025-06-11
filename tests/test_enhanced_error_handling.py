#!/usr/bin/env python3
"""
Test Suite for Enhanced Error Handling System
Verifies that detailed error messages and user guidance work correctly.

Task 1.1.3: Improve Error Messages and User Feedback - Testing
"""

import unittest
import json
import asyncio
from unittest.mock import patch, Mock
import logging
from pathlib import Path
import sys

# Add the n8n_builder module to path
sys.path.append(str(Path(__file__).parent.parent))

from n8n_builder.error_handler import (
    EnhancedErrorHandler, 
    ErrorDetail, 
    ValidationError, 
    ErrorCategory, 
    ErrorSeverity
)
from n8n_builder.validators import EdgeCaseValidator, EdgeCaseValidationResult
from n8n_builder.n8n_builder import N8NBuilder

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestEnhancedErrorHandler(unittest.TestCase):
    """Test the enhanced error handling system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.error_handler = EnhancedErrorHandler()
        self.builder = N8NBuilder()
    
    def test_workflow_json_validation_empty_input(self):
        """Test validation of empty workflow JSON."""
        errors = self.error_handler.validate_workflow_input("")
        
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].field, "workflow_json")
        self.assertEqual(errors[0].issue, "Invalid JSON format")
        self.assertIn("JSON validator", errors[0].fix_instruction)
    
    def test_workflow_json_validation_invalid_json(self):
        """Test validation of malformed JSON."""
        invalid_json = '{"name": "Test", "nodes": [}'  # Missing closing bracket
        errors = self.error_handler.validate_workflow_input(invalid_json)
        
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].field, "workflow_json")
        self.assertEqual(errors[0].issue, "Invalid JSON format")
        self.assertIn("brackets", errors[0].fix_instruction)
    
    def test_workflow_json_validation_missing_required_fields(self):
        """Test validation when required fields are missing."""
        incomplete_workflow = '{"name": "Test"}'  # Missing nodes and connections
        errors = self.error_handler.validate_workflow_input(incomplete_workflow)
        
        self.assertGreaterEqual(len(errors), 2)  # Should have errors for missing nodes and connections
        
        # Check for missing nodes field
        nodes_error = next((e for e in errors if e.field == "nodes"), None)
        self.assertIsNotNone(nodes_error)
        self.assertEqual(nodes_error.issue, "Missing required field 'nodes'")
        
        # Check for missing connections field
        connections_error = next((e for e in errors if e.field == "connections"), None)
        self.assertIsNotNone(connections_error)
        self.assertEqual(connections_error.issue, "Missing required field 'connections'")
    
    def test_workflow_json_validation_wrong_field_types(self):
        """Test validation when fields have wrong types."""
        wrong_types_workflow = '{"name": "Test", "nodes": "should_be_array", "connections": []}'
        errors = self.error_handler.validate_workflow_input(wrong_types_workflow)
        
        self.assertGreater(len(errors), 0)
        
        # Check for wrong type on nodes
        nodes_error = next((e for e in errors if e.field == "nodes"), None)
        self.assertIsNotNone(nodes_error)
        self.assertEqual(nodes_error.issue, "Wrong type for field 'nodes'")
        self.assertEqual(nodes_error.current_value, "string")
        self.assertEqual(nodes_error.expected_format, "array")
    
    def test_workflow_json_validation_empty_nodes_array(self):
        """Test validation when nodes array is empty."""
        empty_nodes_workflow = '{"name": "Test", "nodes": [], "connections": {}}'
        errors = self.error_handler.validate_workflow_input(empty_nodes_workflow)
        
        self.assertGreater(len(errors), 0)
        
        # Check for empty nodes array
        nodes_error = next((e for e in errors if e.field == "nodes"), None)
        self.assertIsNotNone(nodes_error)
        self.assertEqual(nodes_error.issue, "Workflow should have at least one node")
        self.assertIn("Add at least one node", nodes_error.fix_instruction)
    
    def test_modification_description_validation_empty(self):
        """Test validation of empty modification description."""
        errors = self.error_handler.validate_modification_description("")
        
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].field, "modification_description")
        self.assertEqual(errors[0].issue, "Empty modification description")
        self.assertIn("clear description", errors[0].fix_instruction)
    
    def test_modification_description_validation_too_short(self):
        """Test validation of too short modification description."""
        errors = self.error_handler.validate_modification_description("short")
        
        # Should have at least 1 error (may have more due to multiple validation rules)
        self.assertGreaterEqual(len(errors), 1)
        # Check that at least one error is about being too short
        short_errors = [e for e in errors if "short" in e.issue.lower()]
        self.assertGreater(len(short_errors), 0)
        self.assertEqual(short_errors[0].field, "modification_description")
        self.assertIn("more detail", short_errors[0].fix_instruction)
    
    def test_modification_description_validation_no_action_words(self):
        """Test validation when description lacks actionable content."""
        errors = self.error_handler.validate_modification_description("This workflow looks interesting and might be useful")
        
        self.assertGreater(len(errors), 0)
        
        # Should have error about lacking clear action
        action_error = next((e for e in errors if "action" in e.issue.lower()), None)
        self.assertIsNotNone(action_error)
        self.assertIn("action words", action_error.fix_instruction)
    
    def test_modification_description_validation_valid(self):
        """Test validation of valid modification description."""
        errors = self.error_handler.validate_modification_description("Add error handling to the email sending node")
        
        self.assertEqual(len(errors), 0)  # Should be valid
    
    def test_llm_error_guidance_connection_error(self):
        """Test LLM error guidance for connection errors."""
        connection_error = Exception("Connection failed: Unable to connect to server")
        error_detail = self.error_handler.create_llm_error_guidance(connection_error, {})
        
        self.assertEqual(error_detail.category, ErrorCategory.LLM_COMMUNICATION)
        self.assertEqual(error_detail.severity, ErrorSeverity.ERROR)
        self.assertEqual(error_detail.title, "LLM Connection Failed")
        self.assertIn("AI service is temporarily unavailable", error_detail.user_guidance)
        self.assertIn("LM Studio", error_detail.fix_suggestions[0])
    
    def test_llm_error_guidance_404_error(self):
        """Test LLM error guidance for 404 errors."""
        not_found_error = Exception("404 Not Found: Model not loaded")
        error_detail = self.error_handler.create_llm_error_guidance(not_found_error, {})
        
        self.assertEqual(error_detail.category, ErrorCategory.LLM_COMMUNICATION)
        self.assertEqual(error_detail.severity, ErrorSeverity.ERROR)
        self.assertEqual(error_detail.title, "LLM Service Not Found")
        # Check that the guidance mentions server configuration
        self.assertIn("server", error_detail.user_guidance.lower())
        self.assertIn("Start your LM Studio", error_detail.fix_suggestions[0])
    
    def test_json_error_guidance(self):
        """Test JSON error guidance creation."""
        json_error = json.JSONDecodeError("Expecting ',' delimiter", "test", 10)
        error_detail = self.error_handler.create_json_error_guidance(json_error, {})
        
        self.assertEqual(error_detail.category, ErrorCategory.JSON_PARSING)
        self.assertEqual(error_detail.severity, ErrorSeverity.ERROR)
        self.assertEqual(error_detail.title, "Workflow JSON Format Error")
        # Check that line information is included (may be different due to JSON parsing specifics)
        self.assertIn("line", error_detail.message.lower())
        self.assertIn("JSON validator", error_detail.fix_suggestions[-1])
    
    def test_validation_error_summary_single_error(self):
        """Test validation error summary with single error."""
        validation_errors = [
            ValidationError(
                field="nodes",
                issue="Missing required field",
                current_value="missing",
                expected_format="array",
                fix_instruction="Add nodes field"
            )
        ]
        
        error_detail = self.error_handler.create_validation_error_summary(validation_errors)
        
        self.assertEqual(error_detail.category, ErrorCategory.INPUT_VALIDATION)
        self.assertEqual(error_detail.severity, ErrorSeverity.ERROR)
        self.assertEqual(error_detail.title, "Workflow Validation Failed")
        self.assertIn("1 validation issue", error_detail.message)
        self.assertIn("nodes: Missing required field", error_detail.user_guidance)
    
    def test_validation_error_summary_multiple_errors(self):
        """Test validation error summary with multiple errors."""
        validation_errors = [
            ValidationError(
                field="nodes",
                issue="Missing required field",
                current_value="missing",
                expected_format="array",
                fix_instruction="Add nodes field"
            ),
            ValidationError(
                field="connections",
                issue="Wrong type",
                current_value="string",
                expected_format="object",
                fix_instruction="Change to object"
            )
        ]
        
        error_detail = self.error_handler.create_validation_error_summary(validation_errors)
        
        self.assertIn("2 validation issues", error_detail.message)
        self.assertIn("2 fields", error_detail.message)
        self.assertIn("nodes: Missing required field", error_detail.user_guidance)
        self.assertIn("connections: Wrong type", error_detail.user_guidance)
    
    def test_error_categorization_json_decode_error(self):
        """Test error categorization for JSON decode errors."""
        json_error = json.JSONDecodeError("Invalid syntax", "test", 5)
        error_detail = self.error_handler.categorize_error(json_error)
        
        self.assertEqual(error_detail.category, ErrorCategory.JSON_PARSING)
        # Check that line information is included (may be different due to JSON parsing specifics)
        self.assertIn("line", error_detail.message.lower())
    
    def test_error_categorization_key_error(self):
        """Test error categorization for KeyError."""
        key_error = KeyError("'missing_field'")
        error_detail = self.error_handler.categorize_error(key_error)
        
        self.assertEqual(error_detail.category, ErrorCategory.WORKFLOW_STRUCTURE)
        self.assertEqual(error_detail.title, "Missing Required Field")
        self.assertIn("missing_field", error_detail.message)
    
    def test_error_categorization_type_error(self):
        """Test error categorization for TypeError."""
        type_error = TypeError("'str' object is not subscriptable")
        error_detail = self.error_handler.categorize_error(type_error)
        
        self.assertEqual(error_detail.category, ErrorCategory.WORKFLOW_STRUCTURE)
        self.assertEqual(error_detail.title, "Data Type Mismatch")
        self.assertIn("data types", error_detail.user_guidance)
    
    def test_error_categorization_generic_error(self):
        """Test error categorization for unknown errors."""
        generic_error = RuntimeError("Something unexpected happened")
        error_detail = self.error_handler.categorize_error(generic_error)
        
        self.assertEqual(error_detail.category, ErrorCategory.SYSTEM)
        self.assertEqual(error_detail.title, "Unexpected Error")
        self.assertIn("try again", error_detail.user_guidance.lower())

class TestN8NBuilderEnhancedErrorHandling(unittest.TestCase):
    """Test N8N Builder integration with enhanced error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.builder = N8NBuilder()
    
    def test_modify_workflow_invalid_json_input(self):
        """Test modify_workflow with invalid JSON input."""
        invalid_json = '{"name": "Test"'  # Missing closing brace
        description = "Add error handling"
        
        result = self.builder.modify_workflow(invalid_json, description, "test-workflow")
        
        # Should return original workflow (which is the invalid JSON in this case)
        self.assertEqual(result, invalid_json)
    
    def test_modify_workflow_empty_description(self):
        """Test modify_workflow with empty description."""
        valid_workflow = '{"name": "Test", "nodes": [{"id": "1", "name": "Test", "type": "test"}], "connections": {}}'
        empty_description = ""
        
        result = self.builder.modify_workflow(valid_workflow, empty_description, "test-workflow")
        
        # Should return original workflow due to validation failure
        self.assertEqual(result, valid_workflow)
    
    def test_modify_workflow_short_description(self):
        """Test modify_workflow with too short description."""
        valid_workflow = '{"name": "Test", "nodes": [{"id": "1", "name": "Test", "type": "test"}], "connections": {}}'
        short_description = "fix"  # Too short
        
        result = self.builder.modify_workflow(valid_workflow, short_description, "test-workflow")
        
        # Should return original workflow due to validation failure
        self.assertEqual(result, valid_workflow)
    
    def test_iterate_workflow_missing_workflow_id(self):
        """Test iterate_workflow with missing workflow ID."""
        valid_workflow = '{"name": "Test", "nodes": [{"id": "1", "name": "Test", "type": "test"}], "connections": {}}'
        feedback = "The workflow works but needs error handling"
        
        result = self.builder.iterate_workflow("", valid_workflow, feedback, "")
        
        # Should return original workflow due to validation failure
        self.assertEqual(result, valid_workflow)
    
    def test_iterate_workflow_empty_feedback(self):
        """Test iterate_workflow with empty feedback."""
        valid_workflow = '{"name": "Test", "nodes": [{"id": "1", "name": "Test", "type": "test"}], "connections": {}}'
        empty_feedback = ""
        
        result = self.builder.iterate_workflow("test-workflow", valid_workflow, empty_feedback, "")
        
        # Should return original workflow due to validation failure
        self.assertEqual(result, valid_workflow)
    
    def test_iterate_workflow_invalid_json(self):
        """Test iterate_workflow with invalid JSON."""
        invalid_json = '{"name": "Test"'  # Missing closing brace
        feedback = "The workflow needs improvement"
        
        result = self.builder.iterate_workflow("test-workflow", invalid_json, feedback, "")
        
        # Should return original workflow (which is the invalid JSON in this case)
        self.assertEqual(result, invalid_json)
    
    @patch('n8n_builder.n8n_builder.asyncio.run')
    def test_modify_workflow_llm_connection_error(self, mock_asyncio_run):
        """Test modify_workflow with LLM connection error."""
        # Mock LLM connection failure
        mock_asyncio_run.side_effect = Exception("Connection failed: Unable to connect to localhost:1234")
        
        valid_workflow = '{"name": "Test", "nodes": [{"id": "1", "name": "Manual Trigger", "type": "n8n-nodes-base.manualTrigger"}], "connections": {}}'
        description = "Add error handling to this workflow"
        
        result = self.builder.modify_workflow(valid_workflow, description, "test-workflow")
        
        # Should still return a result (fallback to mock response)
        self.assertIsNotNone(result)
        self.assertNotEqual(result, "")
    
    def test_error_handler_field_examples(self):
        """Test that error handler provides useful field examples."""
        handler = self.builder.error_handler
        
        # Test field examples
        name_example = handler._get_field_example('name')
        self.assertIn('"My Workflow"', name_example)
        
        nodes_example = handler._get_field_example('nodes')
        self.assertIn('manualTrigger', nodes_example)
        
        connections_example = handler._get_field_example('connections')
        self.assertIn('main', connections_example)
    
    def test_json_type_detection(self):
        """Test JSON type detection utility."""
        handler = self.builder.error_handler
        
        self.assertEqual(handler._get_json_type("test"), "string")
        self.assertEqual(handler._get_json_type(42), "number")
        self.assertEqual(handler._get_json_type(3.14), "number")
        self.assertEqual(handler._get_json_type(True), "boolean")
        self.assertEqual(handler._get_json_type([]), "array")
        self.assertEqual(handler._get_json_type({}), "object")
        self.assertEqual(handler._get_json_type(None), "null")

class TestEnhancedErrorHandlingIntegration(unittest.TestCase):
    """Integration tests for enhanced error handling across the system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.builder = N8NBuilder()
    
    def test_complete_error_flow_invalid_workflow(self):
        """Test complete error flow with invalid workflow."""
        # Create workflow with multiple issues
        problematic_workflow = {
            "name": "Test",
            "nodes": [
                {
                    "id": "1",
                    # Missing "name" field
                    "type": "n8n-nodes-base.manualTrigger"
                }
            ],
            "connections": {
                "NonExistentNode": {  # References non-existent node
                    "main": [["SomeOtherNode", 0]]
                }
            }
        }
        
        workflow_json = json.dumps(problematic_workflow)
        
        # Test workflow validation
        validation_errors = self.builder.error_handler.validate_workflow_input(workflow_json)
        self.assertGreater(len(validation_errors), 0)
        
        # Test error summary creation
        error_summary = self.builder.error_handler.create_validation_error_summary(validation_errors)
        self.assertIsNotNone(error_summary)
        self.assertEqual(error_summary.category, ErrorCategory.INPUT_VALIDATION)
        self.assertIn("validation issue", error_summary.message.lower())
    
    def test_complete_error_flow_llm_failure_recovery(self):
        """Test complete error flow with LLM failure and recovery."""
        valid_workflow = {
            "name": "Test Workflow",
            "nodes": [
                {
                    "id": "1",
                    "name": "Manual Trigger",
                    "type": "n8n-nodes-base.manualTrigger"
                }
            ],
            "connections": {}
        }
        
        workflow_json = json.dumps(valid_workflow)
        description = "Add comprehensive error handling and logging"
        
        # This should work even if LLM fails (uses mock response)
        result = self.builder.modify_workflow(workflow_json, description, "test-workflow")
        
        self.assertIsNotNone(result)
        self.assertNotEqual(result, "")
        
        # Result should be valid JSON
        try:
            result_parsed = json.loads(result)
            self.assertIsInstance(result_parsed, dict)
        except json.JSONDecodeError:
            self.fail("Result should be valid JSON")

class TestEdgeCaseValidator(unittest.TestCase):
    """Test the EdgeCaseValidator system for common edge cases."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.edge_case_validator = EdgeCaseValidator()
    
    def test_empty_workflow_validation(self):
        """Test validation of completely empty workflows."""
        empty_workflow = '{}'
        result = self.edge_case_validator.validate_edge_cases(empty_workflow, "Add email node")
        
        self.assertFalse(result.is_valid)
        self.assertIn("empty_workflow", result.edge_cases_detected)
        # Should have at least one error about the empty workflow
        self.assertGreater(len(result.errors), 0)
        # The errors should mention nodes or workflow being empty
        self.assertTrue(any("node" in error.lower() or "empty" in error.lower() for error in result.errors))
    
    def test_duplicate_node_ids_validation(self):
        """Test validation for duplicate node IDs."""
        workflow_with_duplicates = {
            "name": "Test Workflow",
            "nodes": [
                {"id": "1", "name": "Node 1", "type": "n8n-nodes-base.manualTrigger"},
                {"id": "1", "name": "Node 2", "type": "n8n-nodes-base.emailSend"}  # Duplicate ID
            ],
            "connections": {}
        }
        
        result = self.edge_case_validator.validate_edge_cases(
            json.dumps(workflow_with_duplicates), 
            "Modify workflow"
        )
        
        self.assertFalse(result.is_valid)
        self.assertIn("duplicate_node_ids", result.edge_cases_detected)
        self.assertTrue(any("duplicate node id" in error.lower() for error in result.errors))
    
    def test_circular_dependency_validation(self):
        """Test validation for circular dependencies."""
        workflow_with_cycle = {
            "name": "Circular Workflow",
            "nodes": [
                {"id": "A", "name": "Node A", "type": "n8n-nodes-base.manualTrigger"},
                {"id": "B", "name": "Node B", "type": "n8n-nodes-base.function"},
                {"id": "C", "name": "Node C", "type": "n8n-nodes-base.function"}
            ],
            "connections": {
                "A": {"main": [[{"node": "B", "type": "main", "index": 0}]]},
                "B": {"main": [[{"node": "C", "type": "main", "index": 0}]]},
                "C": {"main": [[{"node": "A", "type": "main", "index": 0}]]}  # Creates cycle
            }
        }
        
        result = self.edge_case_validator.validate_edge_cases(
            json.dumps(workflow_with_cycle), 
            "Fix workflow"
        )
        
        self.assertFalse(result.is_valid)
        self.assertIn("circular_dependency", result.edge_cases_detected)
        self.assertTrue(any("circular dependency" in error.lower() for error in result.errors))
    
    def test_self_referencing_connection_validation(self):
        """Test validation for self-referencing connections."""
        workflow_with_self_ref = {
            "name": "Self Reference Workflow",
            "nodes": [
                {"id": "A", "name": "Node A", "type": "n8n-nodes-base.function"}
            ],
            "connections": {
                "A": {"main": [[{"node": "A", "type": "main", "index": 0}]]}  # Self-reference
            }
        }
        
        result = self.edge_case_validator.validate_edge_cases(
            json.dumps(workflow_with_self_ref), 
            "Fix workflow"
        )
        
        self.assertFalse(result.is_valid)
        self.assertIn("self_referencing_connection", result.edge_cases_detected)
        self.assertTrue(any("self-referencing" in error.lower() for error in result.errors))
    
    def test_orphaned_nodes_validation(self):
        """Test validation for orphaned nodes."""
        workflow_with_orphans = {
            "name": "Orphaned Nodes Workflow",
            "nodes": [
                {"id": "connected", "name": "Connected Node", "type": "n8n-nodes-base.manualTrigger"},
                {"id": "orphan1", "name": "Orphan 1", "type": "n8n-nodes-base.function"},
                {"id": "orphan2", "name": "Orphan 2", "type": "n8n-nodes-base.emailSend"}
            ],
            "connections": {}  # No connections, so orphan1 and orphan2 are orphaned
        }
        
        result = self.edge_case_validator.validate_edge_cases(
            json.dumps(workflow_with_orphans), 
            "Fix workflow"
        )
        
        # Should be valid (warnings only for orphaned nodes)
        self.assertTrue(result.is_valid)
        self.assertIn("orphaned_nodes", result.edge_cases_detected)
        self.assertTrue(any("orphaned node" in warning.lower() for warning in result.warnings))
    
    def test_unknown_node_type_validation(self):
        """Test validation for unknown node types."""
        workflow_with_unknown_type = {
            "name": "Unknown Type Workflow",
            "nodes": [
                {"id": "1", "name": "Known Node", "type": "n8n-nodes-base.manualTrigger"},
                {"id": "2", "name": "Unknown Node", "type": "custom-unknown-node-type"}
            ],
            "connections": {}
        }
        
        result = self.edge_case_validator.validate_edge_cases(
            json.dumps(workflow_with_unknown_type), 
            "Fix workflow"
        )
        
        # Should be valid (warnings only for unknown types)
        self.assertTrue(result.is_valid)
        self.assertIn("unknown_node_type", result.edge_cases_detected)
        self.assertTrue(any("unknown type" in warning.lower() for warning in result.warnings))
    
    def test_workflow_size_limit_validation(self):
        """Test validation for workflow size limits."""
        # Create a very large workflow JSON
        large_workflow = {
            "name": "Large Workflow",
            "nodes": [],
            "connections": {}
        }
        
        # Add many nodes to exceed size limit
        for i in range(2000):  # This should create a large JSON
            large_workflow["nodes"].append({
                "id": f"node_{i}",
                "name": f"Node {i}",
                "type": "n8n-nodes-base.function",
                "parameters": {"code": "a" * 1000}  # Add some bulk
            })
        
        large_workflow_json = json.dumps(large_workflow)
        
        result = self.edge_case_validator.validate_edge_cases(large_workflow_json, "Fix workflow")
        
        # Check if size limits are detected
        self.assertIn("workflow_size_bytes", result.performance_metrics)
        self.assertGreater(result.performance_metrics["workflow_size_bytes"], 100000)  # Should be large
    
    def test_too_many_nodes_validation(self):
        """Test validation for too many nodes."""
        # Create workflow with too many nodes
        workflow_with_many_nodes = {
            "name": "Many Nodes Workflow",
            "nodes": [],
            "connections": {}
        }
        
        # Add more nodes than the limit
        for i in range(1100):  # Exceeds default limit of 1000
            workflow_with_many_nodes["nodes"].append({
                "id": f"node_{i}",
                "name": f"Node {i}",
                "type": "n8n-nodes-base.function"
            })
        
        result = self.edge_case_validator.validate_edge_cases(
            json.dumps(workflow_with_many_nodes), 
            "Fix workflow"
        )
        
        self.assertFalse(result.is_valid)
        self.assertIn("too_many_nodes", result.edge_cases_detected)
        self.assertTrue(any("too many nodes" in error.lower() for error in result.errors))
    
    def test_invalid_node_id_characters_validation(self):
        """Test validation for invalid characters in node IDs."""
        workflow_with_invalid_ids = {
            "name": "Invalid ID Workflow",
            "nodes": [
                {"id": "valid_id_123", "name": "Valid Node", "type": "n8n-nodes-base.manualTrigger"},
                {"id": "invalid@id!", "name": "Invalid Node", "type": "n8n-nodes-base.function"}
            ],
            "connections": {}
        }
        
        result = self.edge_case_validator.validate_edge_cases(
            json.dumps(workflow_with_invalid_ids), 
            "Fix workflow"
        )
        
        # Should be valid (warnings only for invalid characters)
        self.assertTrue(result.is_valid)
        self.assertIn("invalid_node_id_characters", result.edge_cases_detected)
        self.assertTrue(any("special characters" in warning.lower() for warning in result.warnings))
    
    def test_description_edge_cases_validation(self):
        """Test validation for description edge cases."""
        valid_workflow = {
            "name": "Test Workflow",
            "nodes": [{"id": "1", "name": "Test", "type": "n8n-nodes-base.manualTrigger"}],
            "connections": {}
        }
        
        # Test with suspicious content
        suspicious_description = "Add <script>alert('xss')</script> to the workflow"
        
        result = self.edge_case_validator.validate_edge_cases(
            json.dumps(valid_workflow), 
            suspicious_description
        )
        
        # Should be valid but with warnings
        self.assertTrue(result.is_valid)
        self.assertIn("description_edge_case", result.edge_cases_detected)
        self.assertTrue(any("suspicious" in warning.lower() for warning in result.warnings))
    
    def test_unreachable_nodes_validation(self):
        """Test validation for unreachable nodes."""
        workflow_with_unreachable = {
            "name": "Unreachable Workflow",
            "nodes": [
                {"id": "trigger", "name": "Trigger", "type": "n8n-nodes-base.manualTrigger"},
                {"id": "connected", "name": "Connected", "type": "n8n-nodes-base.function"},
                {"id": "unreachable", "name": "Unreachable", "type": "n8n-nodes-base.emailSend"}
            ],
            "connections": {
                "trigger": {"main": [[{"node": "connected", "type": "main", "index": 0}]]}
                # 'unreachable' node is not connected to trigger
            }
        }
        
        result = self.edge_case_validator.validate_edge_cases(
            json.dumps(workflow_with_unreachable), 
            "Fix workflow"
        )
        
        # Should be valid (warnings only for unreachable nodes)
        self.assertTrue(result.is_valid)
        self.assertIn("unreachable_nodes", result.edge_cases_detected)
        self.assertTrue(any("unreachable" in warning.lower() for warning in result.warnings))
    
    def test_connection_to_nonexistent_node_validation(self):
        """Test validation for connections to non-existent nodes."""
        workflow_with_bad_connections = {
            "name": "Bad Connections Workflow",
            "nodes": [
                {"id": "A", "name": "Node A", "type": "n8n-nodes-base.manualTrigger"}
            ],
            "connections": {
                "A": {"main": [[{"node": "NonExistent", "type": "main", "index": 0}]]}
            }
        }
        
        result = self.edge_case_validator.validate_edge_cases(
            json.dumps(workflow_with_bad_connections), 
            "Fix workflow"
        )
        
        self.assertFalse(result.is_valid)
        self.assertIn("connection_to_nonexistent_node", result.edge_cases_detected)
        self.assertTrue(any("non-existent" in error.lower() for error in result.errors))
    
    def test_performance_metrics_tracking(self):
        """Test that performance metrics are properly tracked."""
        valid_workflow = {
            "name": "Test Workflow",
            "nodes": [{"id": "1", "name": "Test", "type": "n8n-nodes-base.manualTrigger"}],
            "connections": {}
        }
        
        result = self.edge_case_validator.validate_edge_cases(
            json.dumps(valid_workflow), 
            "Test description"
        )
        
        # Check that performance metrics are included
        self.assertIn("total_validation_time", result.performance_metrics)
        self.assertIn("edge_cases_count", result.performance_metrics)
        self.assertIn("workflow_size_bytes", result.performance_metrics)
        self.assertIn("description_length", result.performance_metrics)
        
        # Validation time should be reasonable
        self.assertGreaterEqual(result.performance_metrics["total_validation_time"], 0)
        self.assertLess(result.performance_metrics["total_validation_time"], 2.0)
    
    def test_valid_workflow_no_edge_cases(self):
        """Test that a perfectly valid workflow passes all edge case validation."""
        perfect_workflow = {
            "name": "Perfect Workflow",
            "nodes": [
                {"id": "trigger1", "name": "Manual Trigger", "type": "n8n-nodes-base.manualTrigger"},
                {"id": "email1", "name": "Send Email", "type": "n8n-nodes-base.emailSend"}
            ],
            "connections": {
                "trigger1": {"main": [[{"node": "email1", "type": "main", "index": 0}]]}
            }
        }
        
        result = self.edge_case_validator.validate_edge_cases(
            json.dumps(perfect_workflow), 
            "Add error handling to this workflow"
        )
        
        # Should be completely valid
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.edge_cases_detected), 0)
        
        # Should have performance metrics
        self.assertIn("total_validation_time", result.performance_metrics)

if __name__ == '__main__':
    # Run with increased verbosity to see detailed test output
    unittest.main(verbosity=2) 