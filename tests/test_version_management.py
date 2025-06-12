#!/usr/bin/env python3
"""
Test Suite for Version Management System
Tests the enhanced versioning functionality and API endpoints.

Task 2.0.4: Smart file versioning system - Testing
"""

import unittest
import tempfile
import shutil
import json
import time
from pathlib import Path
import sys
from datetime import datetime
from fastapi.testclient import TestClient

# Add the n8n_builder module to path
sys.path.append(str(Path(__file__).parent.parent))

# Import after path setup
from n8n_builder.app import app
from n8n_builder.project_manager import ProjectManager, FileSystemUtilities
import sys

# Get the actual module, not just the app object
app_module = sys.modules['n8n_builder.app']

class TestVersionManagement(unittest.TestCase):
    """Test the enhanced version management functionality."""
    
    def setUp(self):
        """Set up test fixtures with temporary directory and test instances."""
        # Create temporary directory for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Store original instances
        self.original_project_manager = app_module.project_manager
        self.original_filesystem_utils = app_module.filesystem_utils
        
        # Create test instances
        self.test_project_manager = ProjectManager(projects_root=self.temp_dir)
        self.test_filesystem_utils = FileSystemUtilities(self.test_project_manager)
        
        # Replace global instances in the app module
        app_module.project_manager = self.test_project_manager
        app_module.filesystem_utils = self.test_filesystem_utils
        
        # Create test client
        self.client = TestClient(app)
        
        # Create test project and workflow
        self.test_project = "version-test-project"
        self.test_workflow = "test-workflow.json"
        
        # Sample workflow data for testing
        self.sample_workflow_v1 = {
            "name": "Test Workflow V1",
            "nodes": [
                {
                    "id": "1",
                    "name": "Start",
                    "type": "n8n-nodes-base.manualTrigger",
                    "parameters": {},
                    "position": [100, 100]
                }
            ],
            "connections": {},
            "settings": {},
            "active": False,
            "tags": ["test", "v1"]
        }
        
        self.sample_workflow_v2 = {
            "name": "Test Workflow V2",
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
            "settings": {"timezone": "UTC"},
            "active": True,
            "tags": ["test", "v2", "enhanced"]
        }
        
        # Create test project and initial workflow
        self.test_project_manager.create_project(self.test_project, "Test project for versioning")
        self.test_filesystem_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow, 
            self.sample_workflow_v1,
            create_backup=False
        )
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Restore original instances
        app_module.project_manager = self.original_project_manager
        app_module.filesystem_utils = self.original_filesystem_utils
        
        # Remove temporary directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_create_workflow_versions(self):
        """Test creating multiple versions of a workflow."""
        # Update workflow to create version 1
        self.test_filesystem_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow, 
            self.sample_workflow_v2,
            create_backup=True
        )
        
        # Small delay to ensure different timestamps
        time.sleep(0.2)
        
        # Update workflow again to create version 2
        modified_v2 = self.sample_workflow_v2.copy()
        modified_v2["name"] = "Test Workflow V2 Modified"
        modified_v2["tags"].append("modified")
        
        self.test_filesystem_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow, 
            modified_v2,
            create_backup=True
        )
        
        # List versions
        versions = self.test_filesystem_utils.list_workflow_versions(self.test_project, self.test_workflow)
        
        # Should have 2 versions (newest first)
        self.assertEqual(len(versions), 2)
        self.assertTrue(all(version.endswith('.json') for version in versions))
        self.assertTrue(all('test-workflow_' in version for version in versions))
    
    def test_get_version_info(self):
        """Test getting detailed information about a workflow version."""
        # Create a version
        self.test_filesystem_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow, 
            self.sample_workflow_v2,
            create_backup=True
        )
        
        # Get versions
        versions = self.test_filesystem_utils.list_workflow_versions(self.test_project, self.test_workflow)
        self.assertGreater(len(versions), 0)
        
        # Get version info
        version_info = self.test_filesystem_utils.get_version_info(
            self.test_project, 
            self.test_workflow, 
            versions[0]
        )
        
        # Verify version info structure
        self.assertIn('filename', version_info)
        self.assertIn('timestamp', version_info)
        self.assertIn('created_date', version_info)
        self.assertIn('file_size', version_info)
        self.assertIn('workflow_name', version_info)
        self.assertIn('node_count', version_info)
        self.assertIn('tags', version_info)
        self.assertTrue(version_info['is_backup'])
        
        # Verify content
        self.assertEqual(version_info['workflow_name'], "Test Workflow V1")
        self.assertEqual(version_info['node_count'], 1)
        self.assertEqual(version_info['tags'], ["test", "v1"])
    
    def test_restore_workflow_version(self):
        """Test restoring a workflow from a specific version."""
        # Create a version by updating the workflow
        self.test_filesystem_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow, 
            self.sample_workflow_v2,
            create_backup=True
        )
        
        # Get the version filename
        versions = self.test_filesystem_utils.list_workflow_versions(self.test_project, self.test_workflow)
        self.assertGreater(len(versions), 0)
        version_to_restore = versions[0]
        
        # Verify current workflow is V2
        current_workflow = self.test_filesystem_utils.read_workflow_file(self.test_project, self.test_workflow)
        self.assertEqual(current_workflow["name"], "Test Workflow V2")
        self.assertEqual(len(current_workflow["nodes"]), 2)
        
        # Restore from version (should be V1)
        success = self.test_filesystem_utils.restore_workflow_version(
            self.test_project, 
            self.test_workflow, 
            version_to_restore,
            create_backup=True
        )
        
        self.assertTrue(success)
        
        # Verify workflow is now V1
        restored_workflow = self.test_filesystem_utils.read_workflow_file(self.test_project, self.test_workflow)
        self.assertEqual(restored_workflow["name"], "Test Workflow V1")
        self.assertEqual(len(restored_workflow["nodes"]), 1)
        self.assertEqual(restored_workflow["tags"], ["test", "v1"])
    
    def test_compare_workflow_versions(self):
        """Test comparing two workflow versions."""
        # Create a version by updating the workflow
        self.test_filesystem_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow, 
            self.sample_workflow_v2,
            create_backup=True
        )
        
        # Get the version filename
        versions = self.test_filesystem_utils.list_workflow_versions(self.test_project, self.test_workflow)
        self.assertGreater(len(versions), 0)
        
        # Compare current version with backup version
        comparison = self.test_filesystem_utils.compare_workflow_versions(
            self.test_project, 
            self.test_workflow, 
            'current', 
            versions[0]
        )
        
        # Verify comparison structure
        self.assertIn('version1', comparison)
        self.assertIn('version2', comparison)
        self.assertIn('differences', comparison)
        self.assertIn('summary', comparison)
        
        # Verify differences detected
        self.assertTrue(comparison['differences']['name_changed'])
        self.assertTrue(comparison['differences']['node_count_changed'])
        self.assertTrue(comparison['differences']['tags_changed'])
        self.assertTrue(comparison['differences']['active_changed'])
        self.assertTrue(comparison['summary']['has_changes'])
        self.assertGreater(comparison['summary']['change_count'], 0)
        
        # Verify version details
        self.assertEqual(comparison['version1']['name'], "Test Workflow V2")
        self.assertEqual(comparison['version1']['node_count'], 2)
        self.assertEqual(comparison['version2']['name'], "Test Workflow V1")
        self.assertEqual(comparison['version2']['node_count'], 1)
    
    def test_delete_workflow_version(self):
        """Test deleting a specific workflow version."""
        # Create multiple versions
        self.test_filesystem_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow, 
            self.sample_workflow_v2,
            create_backup=True
        )
        
        time.sleep(0.2)
        
        modified_v2 = self.sample_workflow_v2.copy()
        modified_v2["name"] = "Test Workflow V3"
        self.test_filesystem_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow, 
            modified_v2,
            create_backup=True
        )
        
        # Get versions
        versions_before = self.test_filesystem_utils.list_workflow_versions(self.test_project, self.test_workflow)
        self.assertEqual(len(versions_before), 2)
        
        # Delete one version
        success = self.test_filesystem_utils.delete_workflow_version(
            self.test_project, 
            self.test_workflow, 
            versions_before[0],
            confirm=True
        )
        
        self.assertTrue(success)
        
        # Verify version was deleted
        versions_after = self.test_filesystem_utils.list_workflow_versions(self.test_project, self.test_workflow)
        self.assertEqual(len(versions_after), 1)
        self.assertNotIn(versions_before[0], versions_after)
    
    def test_cleanup_old_versions(self):
        """Test cleaning up old versions with retention policy."""
        # Create multiple versions
        for i in range(5):
            modified_workflow = self.sample_workflow_v1.copy()
            modified_workflow["name"] = f"Test Workflow V{i+1}"
            modified_workflow["tags"] = ["test", f"v{i+1}"]
            
            self.test_filesystem_utils.write_workflow_file(
                self.test_project, 
                self.test_workflow, 
                modified_workflow,
                create_backup=True
            )
            time.sleep(0.1)  # Small delay for unique timestamps
        
        # Verify we have 5 versions (5 updates, each creating a backup of the previous)
        versions_before = self.test_filesystem_utils.list_workflow_versions(self.test_project, self.test_workflow)
        self.assertEqual(len(versions_before), 5)
        
        # Cleanup keeping only 2 versions
        deleted_count = self.test_filesystem_utils.cleanup_old_versions(
            self.test_project, 
            self.test_workflow, 
            keep_versions=2
        )
        
        self.assertEqual(deleted_count, 3)
        
        # Verify only 2 versions remain
        versions_after = self.test_filesystem_utils.list_workflow_versions(self.test_project, self.test_workflow)
        self.assertEqual(len(versions_after), 2)
    
    def test_version_management_error_handling(self):
        """Test error handling in version management operations."""
        # Test with nonexistent project
        with self.assertRaises(ValueError):
            self.test_filesystem_utils.get_version_info("nonexistent", "test.json", "version.json")
        
        # Test with nonexistent version file
        with self.assertRaises(ValueError):
            self.test_filesystem_utils.get_version_info(self.test_project, self.test_workflow, "nonexistent.json")
        
        # Test restore with nonexistent version
        with self.assertRaises(ValueError):
            self.test_filesystem_utils.restore_workflow_version(
                self.test_project, 
                self.test_workflow, 
                "nonexistent.json"
            )
        
        # Test delete without confirmation
        with self.assertRaises(ValueError):
            self.test_filesystem_utils.delete_workflow_version(
                self.test_project, 
                self.test_workflow, 
                "some-version.json",
                confirm=False
            )

class TestVersionManagementAPI(unittest.TestCase):
    """Test the version management API endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Store original instances
        self.original_project_manager = app_module.project_manager
        self.original_filesystem_utils = app_module.filesystem_utils
        
        # Override global instances
        app_module.project_manager = ProjectManager(projects_root=self.temp_dir)
        app_module.filesystem_utils = FileSystemUtilities(app_module.project_manager)
        
        self.client = TestClient(app)
        
        # Create test project and workflow with versions
        self.test_project = "api-test-project"
        self.test_workflow = "api-test-workflow.json"
        
        self.sample_workflow = {
            "name": "API Test Workflow",
            "nodes": [
                {
                    "id": "1",
                    "name": "Start",
                    "type": "n8n-nodes-base.manualTrigger",
                    "parameters": {},
                    "position": [100, 100]
                }
            ],
            "connections": {},
            "settings": {},
            "active": False,
            "tags": ["api", "test"]
        }
        
        # Create project and workflow
        app_module.project_manager.create_project(self.test_project, "API test project")
        app_module.filesystem_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow, 
            self.sample_workflow,
            create_backup=False
        )
        
        # Create a version by updating the workflow
        updated_workflow = self.sample_workflow.copy()
        updated_workflow["name"] = "API Test Workflow Updated"
        updated_workflow["tags"].append("updated")
        app_module.filesystem_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow, 
            updated_workflow,
            create_backup=True
        )
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Restore original instances
        app_module.project_manager = self.original_project_manager
        app_module.filesystem_utils = self.original_filesystem_utils
        
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_list_workflow_versions_api(self):
        """Test the list workflow versions API endpoint."""
        response = self.client.get(f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions")
        
        self.assertEqual(response.status_code, 200)
        versions = response.json()
        
        self.assertIsInstance(versions, list)
        self.assertGreater(len(versions), 0)
        self.assertTrue(all(version.endswith('.json') for version in versions))
    
    def test_get_version_info_api(self):
        """Test the get version info API endpoint."""
        # Get versions first
        versions_response = self.client.get(f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions")
        versions = versions_response.json()
        self.assertGreater(len(versions), 0)
        
        # Get version info
        response = self.client.get(
            f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions/{versions[0]}"
        )
        
        self.assertEqual(response.status_code, 200)
        version_info = response.json()
        
        # Verify response structure
        self.assertIn('filename', version_info)
        self.assertIn('timestamp', version_info)
        self.assertIn('workflow_name', version_info)
        self.assertIn('node_count', version_info)
        self.assertIn('file_size', version_info)
        self.assertTrue(version_info['is_backup'])
    
    def test_get_version_content_api(self):
        """Test the get version content API endpoint."""
        # Get versions first
        versions_response = self.client.get(f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions")
        versions = versions_response.json()
        self.assertGreater(len(versions), 0)
        
        # Get version content
        response = self.client.get(
            f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions/{versions[0]}/content"
        )
        
        self.assertEqual(response.status_code, 200)
        content = response.json()
        
        # Verify response structure
        self.assertIn('filename', content)
        self.assertIn('project_name', content)
        self.assertIn('workflow_data', content)
        self.assertTrue(content['is_version'])
        
        # Verify workflow data
        workflow_data = content['workflow_data']
        self.assertEqual(workflow_data['name'], "API Test Workflow")
        self.assertEqual(len(workflow_data['nodes']), 1)
    
    def test_restore_version_api(self):
        """Test the restore workflow version API endpoint."""
        # Get versions first
        versions_response = self.client.get(f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions")
        versions = versions_response.json()
        self.assertGreater(len(versions), 0)
        
        # Restore version
        restore_request = {"create_backup": True}
        response = self.client.post(
            f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions/{versions[0]}/restore",
            json=restore_request
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        # Verify response
        self.assertIn('message', result)
        self.assertEqual(result['project_name'], self.test_project)
        self.assertEqual(result['workflow_filename'], self.test_workflow)
        self.assertTrue(result['backup_created'])
        
        # Verify workflow was restored
        workflow_response = self.client.get(f"/projects/{self.test_project}/workflows/{self.test_workflow}")
        workflow = workflow_response.json()
        self.assertEqual(workflow['workflow_data']['name'], "API Test Workflow")
    
    def test_compare_versions_api(self):
        """Test the compare workflow versions API endpoint."""
        # Get versions first
        versions_response = self.client.get(f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions")
        versions = versions_response.json()
        self.assertGreater(len(versions), 0)
        
        # Compare current with version
        response = self.client.get(
            f"/projects/{self.test_project}/workflows/{self.test_workflow}/compare/current/{versions[0]}"
        )
        
        self.assertEqual(response.status_code, 200)
        comparison = response.json()
        
        # Verify comparison structure
        self.assertIn('version1', comparison)
        self.assertIn('version2', comparison)
        self.assertIn('differences', comparison)
        self.assertIn('summary', comparison)
        
        # Verify differences detected
        self.assertTrue(comparison['summary']['has_changes'])
        self.assertGreater(comparison['summary']['change_count'], 0)
    
    def test_delete_version_api(self):
        """Test the delete workflow version API endpoint."""
        # Create additional version
        modified_workflow = self.sample_workflow.copy()
        modified_workflow["name"] = "API Test Workflow V3"
        app_module.filesystem_utils.write_workflow_file(
            self.test_project, 
            self.test_workflow, 
            modified_workflow,
            create_backup=True
        )
        
        # Get versions
        versions_response = self.client.get(f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions")
        versions_before = versions_response.json()
        self.assertGreater(len(versions_before), 1)
        
        # Delete version with confirmation
        response = self.client.delete(
            f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions/{versions_before[0]}?confirm=true"
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        # Verify response
        self.assertIn('message', result)
        self.assertEqual(result['deleted_version'], versions_before[0])
        
        # Verify version was deleted
        versions_after_response = self.client.get(f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions")
        versions_after = versions_after_response.json()
        self.assertEqual(len(versions_after), len(versions_before) - 1)
        self.assertNotIn(versions_before[0], versions_after)
    
    def test_cleanup_versions_api(self):
        """Test the cleanup workflow versions API endpoint."""
        # Create multiple versions
        for i in range(3):
            modified_workflow = self.sample_workflow.copy()
            modified_workflow["name"] = f"API Test Workflow V{i+3}"
            app_module.filesystem_utils.write_workflow_file(
                self.test_project, 
                self.test_workflow, 
                modified_workflow,
                create_backup=True
            )
            time.sleep(0.1)
        
        # Verify we have multiple versions
        versions_response = self.client.get(f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions")
        versions_before = versions_response.json()
        self.assertGreater(len(versions_before), 2)
        
        # Cleanup keeping only 2 versions
        cleanup_request = {"keep_versions": 2}
        response = self.client.post(
            f"/projects/{self.test_project}/workflows/{self.test_workflow}/cleanup-versions",
            json=cleanup_request
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        
        # Verify response
        self.assertIn('message', result)
        self.assertEqual(result['versions_kept'], 2)
        self.assertGreater(result['versions_deleted'], 0)
        
        # Verify versions were cleaned up
        versions_after_response = self.client.get(f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions")
        versions_after = versions_after_response.json()
        self.assertEqual(len(versions_after), 2)
    
    def test_version_api_error_handling(self):
        """Test error handling in version management API endpoints."""
        # Test with nonexistent project
        response = self.client.get("/projects/nonexistent/workflows/test.json/versions")
        self.assertEqual(response.status_code, 404)
        
        # Test with nonexistent version
        response = self.client.get(
            f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions/nonexistent.json"
        )
        self.assertEqual(response.status_code, 404)
        
        # Test delete without confirmation
        versions_response = self.client.get(f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions")
        versions = versions_response.json()
        if versions:
            response = self.client.delete(
                f"/projects/{self.test_project}/workflows/{self.test_workflow}/versions/{versions[0]}"
            )
            self.assertEqual(response.status_code, 400)
            self.assertIn("confirmation", response.json()["detail"])

if __name__ == '__main__':
    # Run with increased verbosity
    unittest.main(verbosity=2) 