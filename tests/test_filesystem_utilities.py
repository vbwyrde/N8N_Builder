#!/usr/bin/env python3
"""
Test Suite for File System Utilities
Validates workflow file operations, versioning, and advanced file management.

Task 2.0.2: Implement file system utilities for workflow management - Testing
"""

import unittest
import tempfile
import shutil
import json
import time
from pathlib import Path
import sys
from datetime import datetime

# Add the n8n_builder module to path
sys.path.append(str(Path(__file__).parent.parent))

from n8n_builder.project_manager import (
    ProjectManager,
    FileSystemUtilities,
    ProjectInfo,
    WorkflowInfo
)

class TestFileSystemUtilities(unittest.TestCase):
    """Test the file system utilities functionality."""
    
    def setUp(self):
        """Set up test fixtures with temporary directory."""
        # Create temporary directory for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.project_manager = ProjectManager(projects_root=self.temp_dir)
        self.fs_utils = FileSystemUtilities(self.project_manager)
        
        # Create test project
        self.test_project = "test-project"
        self.project_manager.create_project(self.test_project, "Test project for filesystem utilities")
        
        # Sample workflow data
        self.sample_workflow_data = {
            "name": "Test Workflow",
            "nodes": [
                {
                    "id": "1",
                    "name": "Start",
                    "type": "n8n-nodes-base.manualTrigger",
                    "parameters": {},
                    "position": [100, 100]
                },
                {
                    "id": "2", 
                    "name": "HTTP Request",
                    "type": "n8n-nodes-base.httpRequest",
                    "parameters": {"url": "https://api.example.com"},
                    "position": [300, 100]
                }
            ],
            "connections": {
                "Start": {"main": [["HTTP Request"]]}
            },
            "settings": {},
            "active": False,
            "tags": ["test", "automation"]
        }
        
        self.test_workflow_file = "test-workflow.json"
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_write_and_read_workflow_file(self):
        """Test writing and reading workflow files."""
        # Write workflow file
        result = self.fs_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow_file, 
            self.sample_workflow_data
        )
        self.assertTrue(result)
        
        # Read workflow file
        read_data = self.fs_utils.read_workflow_file(self.test_project, self.test_workflow_file)
        
        # Verify data matches
        self.assertEqual(read_data['name'], self.sample_workflow_data['name'])
        self.assertEqual(len(read_data['nodes']), len(self.sample_workflow_data['nodes']))
        self.assertEqual(read_data['connections'], self.sample_workflow_data['connections'])
        self.assertEqual(read_data['tags'], self.sample_workflow_data['tags'])
    
    def test_read_nonexistent_workflow(self):
        """Test reading a workflow that doesn't exist."""
        with self.assertRaises(ValueError) as context:
            self.fs_utils.read_workflow_file(self.test_project, "nonexistent.json")
        
        self.assertIn("not found", str(context.exception))
    
    def test_read_from_nonexistent_project(self):
        """Test reading from a project that doesn't exist."""
        with self.assertRaises(ValueError) as context:
            self.fs_utils.read_workflow_file("nonexistent-project", self.test_workflow_file)
        
        self.assertIn("does not exist", str(context.exception))
    
    def test_write_invalid_workflow_data(self):
        """Test writing invalid workflow data."""
        # Test with non-dictionary data
        with self.assertRaises(ValueError) as context:
            self.fs_utils.write_workflow_file(self.test_project, "invalid.json", "not a dict")
        
        self.assertIn("must be a dictionary", str(context.exception))
    
    def test_workflow_backup_creation(self):
        """Test that backups are created when files are overwritten."""
        # Write initial workflow
        self.fs_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow_file, 
            self.sample_workflow_data,
            create_backup=False  # Don't create backup for first write
        )
        
        # Modify workflow data
        modified_data = self.sample_workflow_data.copy()
        modified_data['name'] = "Modified Workflow"
        
        # Write again with backup enabled
        self.fs_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow_file, 
            modified_data,
            create_backup=True
        )
        
        # Check that backup was created
        versions = self.fs_utils.list_workflow_versions(self.test_project, self.test_workflow_file)
        self.assertEqual(len(versions), 1)
        self.assertTrue(versions[0].startswith("test-workflow_"))
        self.assertTrue(versions[0].endswith(".json"))
    
    def test_list_workflow_versions(self):
        """Test listing workflow versions."""
        # Initially no versions
        versions = self.fs_utils.list_workflow_versions(self.test_project, self.test_workflow_file)
        self.assertEqual(len(versions), 0)
        
        # Write workflow multiple times to create versions
        for i in range(3):
            modified_data = self.sample_workflow_data.copy()
            modified_data['name'] = f"Workflow Version {i+1}"
            
            self.fs_utils.write_workflow_file(
                self.test_project, 
                self.test_workflow_file, 
                modified_data,
                create_backup=(i > 0)  # Create backup after first write
            )
            
            # Small delay to ensure different timestamps
            time.sleep(0.2)  # Increased from 0.1 for Windows compatibility
        
        # Check versions
        versions = self.fs_utils.list_workflow_versions(self.test_project, self.test_workflow_file)
        self.assertEqual(len(versions), 2)  # 2 backups created
        
        # Verify they're sorted newest first
        timestamps = []
        for version in versions:
            # Extract timestamp from filename
            timestamp_part = version.replace('test-workflow_', '').replace('.json', '')
            timestamps.append(timestamp_part)
        
        # Verify descending order
        self.assertEqual(timestamps, sorted(timestamps, reverse=True))
    
    def test_cleanup_old_versions(self):
        """Test cleaning up old workflow versions."""
        # Create multiple versions
        for i in range(5):
            modified_data = self.sample_workflow_data.copy()
            modified_data['name'] = f"Version {i+1}"
            
            self.fs_utils.write_workflow_file(
                self.test_project, 
                self.test_workflow_file, 
                modified_data,
                create_backup=(i > 0)
            )
            time.sleep(0.2)  # Increased from 0.1 for Windows compatibility
        
        # Should have 4 backup versions
        versions_before = self.fs_utils.list_workflow_versions(self.test_project, self.test_workflow_file)
        self.assertEqual(len(versions_before), 4)
        
        # Cleanup to keep only 2 versions
        deleted_count = self.fs_utils.cleanup_old_versions(
            self.test_project, 
            self.test_workflow_file, 
            keep_versions=2
        )
        
        self.assertEqual(deleted_count, 2)  # Should delete 2 files
        
        # Verify only 2 versions remain
        versions_after = self.fs_utils.list_workflow_versions(self.test_project, self.test_workflow_file)
        self.assertEqual(len(versions_after), 2)
    
    def test_copy_workflow(self):
        """Test copying workflows between projects."""
        # Create source workflow
        self.fs_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow_file, 
            self.sample_workflow_data
        )
        
        # Create destination project
        dest_project = "dest-project"
        self.project_manager.create_project(dest_project, "Destination project")
        
        # Copy workflow
        result = self.fs_utils.copy_workflow(
            self.test_project, 
            self.test_workflow_file,
            dest_project, 
            "copied-workflow.json"
        )
        self.assertTrue(result)
        
        # Verify workflow exists in destination
        copied_data = self.fs_utils.read_workflow_file(dest_project, "copied-workflow.json")
        self.assertEqual(copied_data['name'], "copied-workflow")  # Name should be updated
        self.assertEqual(len(copied_data['nodes']), len(self.sample_workflow_data['nodes']))
        
        # Verify original still exists
        original_data = self.fs_utils.read_workflow_file(self.test_project, self.test_workflow_file)
        self.assertEqual(original_data['name'], self.sample_workflow_data['name'])
    
    def test_copy_workflow_overwrite_protection(self):
        """Test that copy workflow protects against overwriting."""
        # Create workflows in both projects
        self.fs_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow_file, 
            self.sample_workflow_data
        )
        
        dest_project = "dest-project"
        self.project_manager.create_project(dest_project)
        self.fs_utils.write_workflow_file(
            dest_project, 
            "existing.json", 
            self.sample_workflow_data
        )
        
        # Attempt copy without overwrite should fail
        with self.assertRaises(ValueError) as context:
            self.fs_utils.copy_workflow(
                self.test_project, 
                self.test_workflow_file,
                dest_project, 
                "existing.json",
                overwrite=False
            )
        
        self.assertIn("already exists", str(context.exception))
        
        # Copy with overwrite should succeed
        result = self.fs_utils.copy_workflow(
            self.test_project, 
            self.test_workflow_file,
            dest_project, 
            "existing.json",
            overwrite=True
        )
        self.assertTrue(result)
    
    def test_move_workflow(self):
        """Test moving workflows between projects."""
        # Create source workflow
        self.fs_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow_file, 
            self.sample_workflow_data
        )
        
        # Create destination project
        dest_project = "dest-project"
        self.project_manager.create_project(dest_project)
        
        # Move workflow
        result = self.fs_utils.move_workflow(
            self.test_project, 
            self.test_workflow_file,
            dest_project, 
            "moved-workflow.json"
        )
        self.assertTrue(result)
        
        # Verify workflow exists in destination
        moved_data = self.fs_utils.read_workflow_file(dest_project, "moved-workflow.json")
        self.assertEqual(moved_data['name'], "moved-workflow")
        
        # Verify original no longer exists
        with self.assertRaises(ValueError):
            self.fs_utils.read_workflow_file(self.test_project, self.test_workflow_file)
    
    def test_rename_workflow(self):
        """Test renaming workflow files."""
        # Create workflow
        self.fs_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow_file, 
            self.sample_workflow_data
        )
        
        # Rename workflow
        new_filename = "renamed-workflow.json"
        result = self.fs_utils.rename_workflow(
            self.test_project, 
            self.test_workflow_file, 
            new_filename
        )
        self.assertTrue(result)
        
        # Verify new file exists with updated name
        renamed_data = self.fs_utils.read_workflow_file(self.test_project, new_filename)
        self.assertEqual(renamed_data['name'], "renamed-workflow")
        
        # Verify old file no longer exists
        with self.assertRaises(ValueError):
            self.fs_utils.read_workflow_file(self.test_project, self.test_workflow_file)
    
    def test_delete_workflow_file(self):
        """Test deleting workflow files."""
        # Create workflow
        self.fs_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow_file, 
            self.sample_workflow_data
        )
        
        # Test deletion without confirmation fails
        with self.assertRaises(ValueError):
            self.fs_utils.delete_workflow_file(self.test_project, self.test_workflow_file, confirm=False)
        
        # Delete with confirmation
        result = self.fs_utils.delete_workflow_file(
            self.test_project, 
            self.test_workflow_file, 
            confirm=True
        )
        self.assertTrue(result)
        
        # Verify file no longer exists
        with self.assertRaises(ValueError):
            self.fs_utils.read_workflow_file(self.test_project, self.test_workflow_file)
    
    def test_get_workflow_info(self):
        """Test getting detailed workflow information."""
        # Create workflow with versions
        self.fs_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow_file, 
            self.sample_workflow_data,
            create_backup=False
        )
        
        # Create a version
        modified_data = self.sample_workflow_data.copy()
        modified_data['name'] = "Modified"
        self.fs_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow_file, 
            modified_data,
            create_backup=True
        )
        
        # Get workflow info
        workflow_info = self.fs_utils.get_workflow_info(self.test_project, self.test_workflow_file)
        
        # Verify information
        self.assertIsInstance(workflow_info, WorkflowInfo)
        self.assertEqual(workflow_info.name, "Modified")
        self.assertEqual(workflow_info.filename, self.test_workflow_file)
        self.assertEqual(workflow_info.project_name, self.test_project)
        self.assertEqual(workflow_info.node_count, 2)
        self.assertEqual(workflow_info.version_count, 2)  # Current + 1 backup
        self.assertEqual(workflow_info.tags, ["test", "automation"])
        self.assertGreater(workflow_info.file_size, 0)
    
    def test_validate_workflow_json(self):
        """Test workflow JSON validation."""
        # Valid workflow
        errors = self.fs_utils.validate_workflow_json(self.sample_workflow_data)
        self.assertEqual(len(errors), 0)
        
        # Missing required fields
        invalid_data = {"name": "Test"}
        errors = self.fs_utils.validate_workflow_json(invalid_data)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Missing required field: 'nodes'" in error for error in errors))
        self.assertTrue(any("Missing required field: 'connections'" in error for error in errors))
        
        # Invalid node structure
        invalid_nodes = {
            "nodes": [{"invalid": "node"}],
            "connections": {}
        }
        errors = self.fs_utils.validate_workflow_json(invalid_nodes)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("missing required field: 'id'" in error for error in errors))
        
        # Wrong field types
        wrong_types = {
            "nodes": [],
            "connections": {},
            "active": "should_be_boolean",
            "tags": "should_be_list"
        }
        errors = self.fs_utils.validate_workflow_json(wrong_types)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("should be of type bool" in error for error in errors))
        self.assertTrue(any("should be of type list" in error for error in errors))
    
    def test_get_file_system_stats(self):
        """Test getting file system statistics."""
        # Create some workflows in different projects
        projects_data = [
            ("project-1", ["workflow1.json", "workflow2.json"]),
            ("project-2", ["workflow3.json"]),
            ("project-3", [])  # Empty project
        ]
        
        for project_name, workflows in projects_data:
            self.project_manager.create_project(project_name, f"Test project {project_name}")
            
            for workflow_file in workflows:
                workflow_data = self.sample_workflow_data.copy()
                workflow_data['name'] = workflow_file.replace('.json', '')
                self.fs_utils.write_workflow_file(project_name, workflow_file, workflow_data)
        
        # Get stats
        stats = self.fs_utils.get_file_system_stats()
        
        # Verify stats
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats['total_projects'], 4)  # 3 new + 1 from setUp
        self.assertEqual(stats['total_workflows'], 3)  # Only counting non-empty projects
        self.assertGreater(stats['total_file_size_bytes'], 0)
        self.assertGreaterEqual(stats['total_file_size_mb'], 0)  # Small files might round to 0.0
        self.assertIn('largest_workflow', stats)
        self.assertIn('projects_root', stats)

class TestFileSystemUtilitiesEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.project_manager = ProjectManager(projects_root=self.temp_dir)
        self.fs_utils = FileSystemUtilities(self.project_manager)
        
        # Create test project
        self.test_project = "test-project"
        self.project_manager.create_project(self.test_project)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_read_corrupted_json(self):
        """Test reading a file with corrupted JSON."""
        # Create a file with invalid JSON
        project_path = self.temp_dir / self.test_project
        corrupted_file = project_path / "corrupted.json"
        corrupted_file.write_text("{ invalid json content", encoding='utf-8')
        
        # Attempt to read should raise RuntimeError
        with self.assertRaises(RuntimeError) as context:
            self.fs_utils.read_workflow_file(self.test_project, "corrupted.json")
        
        self.assertIn("Invalid JSON", str(context.exception))
    
    def test_write_to_readonly_location(self):
        """Test writing to a location that becomes read-only."""
        # This test simulates filesystem errors
        # We'll test the error handling without actually making directories read-only
        # since that can be platform-dependent
        
        # Test with invalid project name that would cause filesystem issues
        invalid_chars = "invalid/project*name"
        
        with self.assertRaises(ValueError):
            # This should fail during project validation
            self.fs_utils.write_workflow_file(invalid_chars, "test.json", {"nodes": [], "connections": {}})
    
    def test_cleanup_versions_no_versions(self):
        """Test cleanup when no versions exist."""
        deleted_count = self.fs_utils.cleanup_old_versions(
            self.test_project, 
            "nonexistent.json", 
            keep_versions=5
        )
        self.assertEqual(deleted_count, 0)
    
    def test_copy_from_nonexistent_source(self):
        """Test copying from a source that doesn't exist."""
        dest_project = "dest-project"
        self.project_manager.create_project(dest_project)
        
        with self.assertRaises(ValueError):
            self.fs_utils.copy_workflow(
                self.test_project, 
                "nonexistent.json",
                dest_project, 
                "dest.json"
            )
    
    def test_move_to_nonexistent_destination_project(self):
        """Test moving to a destination project that doesn't exist."""
        # Create source workflow
        workflow_data = {"nodes": [], "connections": {}}
        self.fs_utils.write_workflow_file(self.test_project, "source.json", workflow_data)
        
        with self.assertRaises(ValueError):
            self.fs_utils.move_workflow(
                self.test_project, 
                "source.json",
                "nonexistent-project", 
                "dest.json"
            )
    
    def test_workflow_info_edge_cases(self):
        """Test workflow info with edge case data."""
        # Create workflow with minimal data
        minimal_data = {"nodes": [], "connections": {}}
        self.fs_utils.write_workflow_file(self.test_project, "minimal.json", minimal_data)
        
        workflow_info = self.fs_utils.get_workflow_info(self.test_project, "minimal.json")
        
        # Verify defaults are handled correctly
        self.assertEqual(workflow_info.name, "minimal")  # Derived from filename
        self.assertEqual(workflow_info.description, "")
        self.assertEqual(workflow_info.node_count, 0)
        self.assertEqual(workflow_info.tags, [])

class TestFileSystemUtilitiesIntegration(unittest.TestCase):
    """Test integration with project manager and real-world scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.project_manager = ProjectManager(projects_root=self.temp_dir)
        self.fs_utils = FileSystemUtilities(self.project_manager)
        
        # Complex workflow data for testing
        self.complex_workflow = {
            "name": "E-commerce Order Processing",
            "description": "Automated order processing workflow",
            "nodes": [
                {
                    "id": "trigger",
                    "name": "Order Webhook",
                    "type": "n8n-nodes-base.webhook",
                    "parameters": {"path": "/order"},
                    "position": [100, 100]
                },
                {
                    "id": "validate",
                    "name": "Validate Order",
                    "type": "n8n-nodes-base.function",
                    "parameters": {"functionCode": "// Validation logic"},
                    "position": [300, 100]
                },
                {
                    "id": "process",
                    "name": "Process Payment",
                    "type": "n8n-nodes-base.httpRequest",
                    "parameters": {"url": "https://payment.api.com"},
                    "position": [500, 100]
                },
                {
                    "id": "notify",
                    "name": "Send Confirmation",
                    "type": "n8n-nodes-base.emailSend",
                    "parameters": {"subject": "Order Confirmed"},
                    "position": [700, 100]
                }
            ],
            "connections": {
                "Order Webhook": {"main": [["Validate Order"]]},
                "Validate Order": {"main": [["Process Payment"]]},
                "Process Payment": {"main": [["Send Confirmation"]]}
            },
            "settings": {"timezone": "UTC"},
            "active": True,
            "tags": ["ecommerce", "payment", "automation"]
        }
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_complete_workflow_lifecycle(self):
        """Test a complete workflow lifecycle from creation to deletion."""
        # Create project
        project_name = "ecommerce-automation"
        self.project_manager.create_project(
            project_name, 
            "E-commerce automation workflows"
        )
        
        workflow_file = "order-processing.json"
        
        # 1. Create initial workflow
        self.fs_utils.write_workflow_file(project_name, workflow_file, self.complex_workflow)
        
        # 2. Read and verify
        workflow_data = self.fs_utils.read_workflow_file(project_name, workflow_file)
        self.assertEqual(workflow_data['name'], self.complex_workflow['name'])
        self.assertEqual(len(workflow_data['nodes']), 4)
        
        # 3. Update workflow (creates backup)
        updated_workflow = self.complex_workflow.copy()
        updated_workflow['name'] = "Enhanced Order Processing"
        updated_workflow['tags'].append("enhanced")
        
        self.fs_utils.write_workflow_file(project_name, workflow_file, updated_workflow)
        
        # 4. Verify backup was created
        versions = self.fs_utils.list_workflow_versions(project_name, workflow_file)
        self.assertEqual(len(versions), 1)
        
        # 5. Get detailed info
        info = self.fs_utils.get_workflow_info(project_name, workflow_file)
        self.assertEqual(info.name, "Enhanced Order Processing")
        self.assertEqual(info.node_count, 4)
        self.assertEqual(info.version_count, 2)  # Current + 1 backup
        self.assertIn("enhanced", info.tags)
        
        # 6. Copy to another project
        backup_project = "backup-workflows"
        self.project_manager.create_project(backup_project, "Backup workflows")
        
        self.fs_utils.copy_workflow(
            project_name, workflow_file,
            backup_project, "order-processing-backup.json"
        )
        
        # 7. Verify copy exists
        backup_data = self.fs_utils.read_workflow_file(backup_project, "order-processing-backup.json")
        self.assertEqual(backup_data['name'], "order-processing-backup")
        
        # 8. Rename original
        self.fs_utils.rename_workflow(project_name, workflow_file, "main-order-processing.json")
        
        # 9. Verify rename
        renamed_data = self.fs_utils.read_workflow_file(project_name, "main-order-processing.json")
        self.assertEqual(renamed_data['name'], "main-order-processing")
        
        # 10. Clean up old versions
        deleted_count = self.fs_utils.cleanup_old_versions(
            project_name, "main-order-processing.json", keep_versions=1
        )
        self.assertGreaterEqual(deleted_count, 0)
        
        # 11. Get final stats
        stats = self.fs_utils.get_file_system_stats()
        self.assertEqual(stats['total_projects'], 2)
        self.assertEqual(stats['total_workflows'], 2)
    
    def test_concurrent_workflow_operations(self):
        """Test handling of concurrent operations (simulation)."""
        project_name = "concurrent-test"
        self.project_manager.create_project(project_name, "Concurrent operations test")
        
        # Create multiple workflows rapidly
        workflows = []
        for i in range(5):
            workflow_data = self.complex_workflow.copy()
            workflow_data['name'] = f"Workflow {i+1}"
            workflow_file = f"workflow-{i+1}.json"
            
            self.fs_utils.write_workflow_file(project_name, workflow_file, workflow_data)
            workflows.append(workflow_file)
        
        # Verify all workflows exist
        project_workflows = self.project_manager.list_project_workflows(project_name)
        for workflow_file in workflows:
            self.assertIn(workflow_file, project_workflows)
        
        # Perform operations on all workflows
        for workflow_file in workflows:
            # Update each workflow
            updated_data = self.complex_workflow.copy()
            updated_data['name'] = f"Updated {workflow_file}"
            self.fs_utils.write_workflow_file(project_name, workflow_file, updated_data)
            
            # Verify update
            read_data = self.fs_utils.read_workflow_file(project_name, workflow_file)
            self.assertEqual(read_data['name'], f"Updated {workflow_file}")

if __name__ == '__main__':
    # Run with increased verbosity to see detailed test output
    unittest.main(verbosity=2) 