#!/usr/bin/env python3
"""
Test Suite for Project API Endpoints
Tests the FastAPI endpoints for project management functionality.

Task 2.0.3: Project API endpoints - Testing
"""

import unittest
import tempfile
import shutil
import json
import asyncio
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

class TestProjectAPI(unittest.TestCase):
    """Test the project API endpoints."""
    
    def setUp(self):
        """Set up test fixtures with temporary directory and test client."""
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
        
        # Sample workflow data for testing
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
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Restore original instances
        app_module.project_manager = self.original_project_manager
        app_module.filesystem_utils = self.original_filesystem_utils
        
        # Remove temporary directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_list_projects_empty(self):
        """Test listing projects when none exist."""
        response = self.client.get("/projects")
        
        self.assertEqual(response.status_code, 200)
        projects = response.json()
        self.assertEqual(len(projects), 0)
        self.assertIsInstance(projects, list)
    
    def test_create_project_basic(self):
        """Test creating a basic project."""
        project_data = {
            "name": "test-project",
            "description": "A test project"
        }
        
        response = self.client.post("/projects/test-project", json=project_data)
        
        self.assertEqual(response.status_code, 200)
        project = response.json()
        
        self.assertEqual(project["name"], "test-project")
        self.assertEqual(project["description"], "A test project")
        self.assertEqual(project["workflow_count"], 0)
        self.assertIsInstance(project["workflows"], list)
        self.assertIn("created_date", project)
        self.assertIn("last_modified", project)
    
    def test_create_project_with_initial_workflows(self):
        """Test creating a project with initial workflows."""
        project_data = {
            "name": "workflow-project",
            "description": "Project with workflows",
            "initial_workflows": ["email-automation", "data-processing"]
        }
        
        response = self.client.post("/projects/workflow-project", json=project_data)
        
        self.assertEqual(response.status_code, 200)
        project = response.json()
        
        self.assertEqual(project["name"], "workflow-project")
        self.assertEqual(project["workflow_count"], 2)
        self.assertEqual(len(project["workflows"]), 2)
        self.assertIn("email-automation.json", project["workflows"])
        self.assertIn("data-processing.json", project["workflows"])
    
    def test_create_project_duplicate_name(self):
        """Test creating a project with duplicate name fails."""
        project_data = {"name": "duplicate-project", "description": "First project"}
        
        # Create first project
        response1 = self.client.post("/projects/duplicate-project", json=project_data)
        self.assertEqual(response1.status_code, 200)
        
        # Try to create duplicate
        response2 = self.client.post("/projects/duplicate-project", json=project_data)
        self.assertEqual(response2.status_code, 400)
        self.assertIn("already exists", response2.json()["detail"])
    
    def test_create_project_invalid_name(self):
        """Test creating a project with invalid name fails."""
        # Test with empty name in request body (should take precedence)
        project_data = {"name": "", "description": "Invalid name"}
        
        response = self.client.post("/projects/placeholder", json=project_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("cannot be empty", response.json()["detail"])
        
        # Test with whitespace-only name
        project_data_whitespace = {"name": "   ", "description": "Whitespace name"}
        
        response_whitespace = self.client.post("/projects/placeholder2", json=project_data_whitespace)
        self.assertEqual(response_whitespace.status_code, 400)
        self.assertIn("cannot be empty", response_whitespace.json()["detail"])
    
    def test_get_project_details(self):
        """Test getting project details."""
        # Create project first
        project_data = {"name": "detail-project", "description": "Project for details test"}
        create_response = self.client.post("/projects/detail-project", json=project_data)
        self.assertEqual(create_response.status_code, 200)
        
        # Get project details
        response = self.client.get("/projects/detail-project")
        
        self.assertEqual(response.status_code, 200)
        project = response.json()
        
        self.assertEqual(project["name"], "detail-project")
        self.assertEqual(project["description"], "Project for details test")
        self.assertIn("path", project)
        self.assertIn("created_date", project)
    
    def test_get_nonexistent_project(self):
        """Test getting a project that doesn't exist."""
        response = self.client.get("/projects/nonexistent-project")
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])
    
    def test_list_projects_with_data(self):
        """Test listing projects when some exist."""
        # Create multiple projects
        projects_to_create = [
            {"name": "project-1", "description": "First project"},
            {"name": "project-2", "description": "Second project"},
            {"name": "project-3", "description": "Third project"}
        ]
        
        for project_data in projects_to_create:
            response = self.client.post(f"/projects/{project_data['name']}", json=project_data)
            self.assertEqual(response.status_code, 200)
        
        # List all projects
        response = self.client.get("/projects")
        
        self.assertEqual(response.status_code, 200)
        projects = response.json()
        
        self.assertEqual(len(projects), 3)
        project_names = [p["name"] for p in projects]
        self.assertIn("project-1", project_names)
        self.assertIn("project-2", project_names)
        self.assertIn("project-3", project_names)
    
    def test_list_project_workflows_empty(self):
        """Test listing workflows in an empty project."""
        # Create empty project
        project_data = {"name": "empty-project", "description": "Empty project"}
        create_response = self.client.post("/projects/empty-project", json=project_data)
        self.assertEqual(create_response.status_code, 200)
        
        # List workflows
        response = self.client.get("/projects/empty-project/workflows")
        
        self.assertEqual(response.status_code, 200)
        workflows = response.json()
        self.assertEqual(len(workflows), 0)
        self.assertIsInstance(workflows, list)
    
    def test_list_project_workflows_with_data(self):
        """Test listing workflows in a project with workflows."""
        # Create project with initial workflows
        project_data = {
            "name": "workflow-project",
            "description": "Project with workflows",
            "initial_workflows": ["workflow1", "workflow2"]
        }
        create_response = self.client.post("/projects/workflow-project", json=project_data)
        self.assertEqual(create_response.status_code, 200)
        
        # List workflows
        response = self.client.get("/projects/workflow-project/workflows")
        
        self.assertEqual(response.status_code, 200)
        workflows = response.json()
        
        self.assertEqual(len(workflows), 2)
        self.assertIn("workflow1.json", workflows)
        self.assertIn("workflow2.json", workflows)
    
    def test_list_workflows_nonexistent_project(self):
        """Test listing workflows for a project that doesn't exist."""
        response = self.client.get("/projects/nonexistent/workflows")
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])
    
    def test_save_and_get_workflow_file(self):
        """Test saving and retrieving a workflow file."""
        # Create project
        project_data = {"name": "file-project", "description": "Project for file operations"}
        create_response = self.client.post("/projects/file-project", json=project_data)
        self.assertEqual(create_response.status_code, 200)
        
        # Save workflow file
        workflow_request = {
            "workflow_data": self.sample_workflow_data,
            "create_backup": False
        }
        
        save_response = self.client.put(
            "/projects/file-project/workflows/test-workflow.json",
            json=workflow_request
        )
        
        self.assertEqual(save_response.status_code, 200)
        save_result = save_response.json()
        
        self.assertEqual(save_result["filename"], "test-workflow.json")
        self.assertEqual(save_result["project_name"], "file-project")
        self.assertIn("message", save_result)
        self.assertIn("file_size", save_result)
        
        # Get workflow file
        get_response = self.client.get("/projects/file-project/workflows/test-workflow.json")
        
        self.assertEqual(get_response.status_code, 200)
        workflow_file = get_response.json()
        
        self.assertEqual(workflow_file["filename"], "test-workflow.json")
        self.assertEqual(workflow_file["project_name"], "file-project")
        self.assertEqual(workflow_file["workflow_data"]["name"], "Test Workflow")
        self.assertEqual(len(workflow_file["workflow_data"]["nodes"]), 2)
        self.assertGreater(workflow_file["file_size"], 0)
    
    def test_save_workflow_invalid_json(self):
        """Test saving a workflow with invalid JSON structure."""
        # Create project
        project_data = {"name": "invalid-project", "description": "Project for invalid JSON test"}
        create_response = self.client.post("/projects/invalid-project", json=project_data)
        self.assertEqual(create_response.status_code, 200)
        
        # Try to save invalid workflow
        invalid_workflow = {
            "workflow_data": {"invalid": "structure"},  # Missing required fields
            "create_backup": False
        }
        
        response = self.client.put(
            "/projects/invalid-project/workflows/invalid.json",
            json=invalid_workflow
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid workflow JSON", response.json()["detail"])
    
    def test_get_nonexistent_workflow_file(self):
        """Test getting a workflow file that doesn't exist."""
        # Create project
        project_data = {"name": "test-project", "description": "Test project"}
        create_response = self.client.post("/projects/test-project", json=project_data)
        self.assertEqual(create_response.status_code, 200)
        
        # Try to get nonexistent workflow
        response = self.client.get("/projects/test-project/workflows/nonexistent.json")
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])
    
    def test_save_workflow_to_nonexistent_project(self):
        """Test saving a workflow to a project that doesn't exist."""
        workflow_request = {
            "workflow_data": self.sample_workflow_data,
            "create_backup": False
        }
        
        response = self.client.put(
            "/projects/nonexistent/workflows/test.json",
            json=workflow_request
        )
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("does not exist", response.json()["detail"])
    
    def test_delete_project(self):
        """Test deleting a project."""
        # Create project
        project_data = {"name": "delete-project", "description": "Project to be deleted"}
        create_response = self.client.post("/projects/delete-project", json=project_data)
        self.assertEqual(create_response.status_code, 200)
        
        # Verify project exists
        get_response = self.client.get("/projects/delete-project")
        self.assertEqual(get_response.status_code, 200)
        
        # Delete project with confirmation
        delete_response = self.client.delete("/projects/delete-project?confirm=true")
        
        self.assertEqual(delete_response.status_code, 200)
        delete_result = delete_response.json()
        self.assertIn("deleted successfully", delete_result["message"])
        
        # Verify project no longer exists
        get_response_after = self.client.get("/projects/delete-project")
        self.assertEqual(get_response_after.status_code, 404)
    
    def test_delete_project_without_confirmation(self):
        """Test deleting a project without confirmation fails."""
        # Create project
        project_data = {"name": "no-confirm-project", "description": "Project without confirmation"}
        create_response = self.client.post("/projects/no-confirm-project", json=project_data)
        self.assertEqual(create_response.status_code, 200)
        
        # Try to delete without confirmation
        delete_response = self.client.delete("/projects/no-confirm-project")
        
        self.assertEqual(delete_response.status_code, 400)
        self.assertIn("requires explicit confirmation", delete_response.json()["detail"])
    
    def test_delete_nonexistent_project(self):
        """Test deleting a project that doesn't exist."""
        response = self.client.delete("/projects/nonexistent?confirm=true")
        
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])
    
    def test_get_project_stats(self):
        """Test getting project statistics."""
        # Create multiple projects with workflows
        projects_data = [
            {
                "name": "stats-project-1",
                "description": "First stats project",
                "initial_workflows": ["workflow1", "workflow2"]
            },
            {
                "name": "stats-project-2", 
                "description": "Second stats project",
                "initial_workflows": ["workflow3"]
            },
            {
                "name": "stats-project-3",
                "description": "Third stats project"
            }
        ]
        
        for project_data in projects_data:
            response = self.client.post(f"/projects/{project_data['name']}", json=project_data)
            self.assertEqual(response.status_code, 200)
        
        # Get stats
        response = self.client.get("/projects/stats")
        
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        
        self.assertEqual(stats["total_projects"], 3)
        self.assertEqual(stats["total_workflows"], 3)  # 2 + 1 + 0
        self.assertGreater(stats["average_workflows_per_project"], 0)
        self.assertEqual(len(stats["project_names"]), 3)
        self.assertIn("stats-project-1", stats["project_names"])
        self.assertIn("projects_root", stats)

class TestProjectAPIIntegration(unittest.TestCase):
    """Test integration scenarios for project API."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Override global instances
        app_module.project_manager = ProjectManager(projects_root=self.temp_dir)
        app_module.filesystem_utils = FileSystemUtilities(app_module.project_manager)
        
        self.client = TestClient(app)
        
        # Complex workflow for testing
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
                }
            ],
            "connections": {
                "Order Webhook": {"main": [["Validate Order"]]},
                "Validate Order": {"main": [["Process Payment"]]}
            },
            "settings": {"timezone": "UTC"},
            "active": True,
            "tags": ["ecommerce", "payment", "automation"]
        }
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_complete_project_workflow_lifecycle(self):
        """Test a complete project and workflow lifecycle through the API."""
        # 1. Create project
        project_data = {
            "name": "ecommerce-automation",
            "description": "E-commerce automation workflows"
        }
        
        create_response = self.client.post("/projects/ecommerce-automation", json=project_data)
        self.assertEqual(create_response.status_code, 200)
        
        # 2. Save workflow
        workflow_request = {
            "workflow_data": self.complex_workflow,
            "create_backup": False
        }
        
        save_response = self.client.put(
            "/projects/ecommerce-automation/workflows/order-processing.json",
            json=workflow_request
        )
        self.assertEqual(save_response.status_code, 200)
        
        # 3. List workflows
        list_response = self.client.get("/projects/ecommerce-automation/workflows")
        self.assertEqual(list_response.status_code, 200)
        workflows = list_response.json()
        self.assertIn("order-processing.json", workflows)
        
        # 4. Get workflow
        get_response = self.client.get("/projects/ecommerce-automation/workflows/order-processing.json")
        self.assertEqual(get_response.status_code, 200)
        workflow_file = get_response.json()
        self.assertEqual(workflow_file["workflow_data"]["name"], "E-commerce Order Processing")
        
        # 5. Update workflow (with backup)
        updated_workflow = self.complex_workflow.copy()
        updated_workflow["name"] = "Enhanced Order Processing"
        updated_workflow["tags"].append("enhanced")
        
        update_request = {
            "workflow_data": updated_workflow,
            "create_backup": True
        }
        
        update_response = self.client.put(
            "/projects/ecommerce-automation/workflows/order-processing.json",
            json=update_request
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertTrue(update_response.json()["backup_created"])
        
        # 6. Verify update
        get_updated_response = self.client.get("/projects/ecommerce-automation/workflows/order-processing.json")
        self.assertEqual(get_updated_response.status_code, 200)
        updated_file = get_updated_response.json()
        self.assertEqual(updated_file["workflow_data"]["name"], "Enhanced Order Processing")
        self.assertIn("enhanced", updated_file["workflow_data"]["tags"])
        
        # 7. Get project details
        project_response = self.client.get("/projects/ecommerce-automation")
        self.assertEqual(project_response.status_code, 200)
        project = project_response.json()
        self.assertEqual(project["workflow_count"], 1)
        self.assertIn("order-processing.json", project["workflows"])
    
    def test_multiple_projects_and_workflows(self):
        """Test managing multiple projects with multiple workflows."""
        # Create multiple projects
        projects = [
            {"name": "project-a", "description": "Project A"},
            {"name": "project-b", "description": "Project B"},
            {"name": "project-c", "description": "Project C"}
        ]
        
        for project_data in projects:
            response = self.client.post(f"/projects/{project_data['name']}", json=project_data)
            self.assertEqual(response.status_code, 200)
        
        # Add workflows to each project
        workflows_per_project = {
            "project-a": ["workflow-a1.json", "workflow-a2.json"],
            "project-b": ["workflow-b1.json"],
            "project-c": ["workflow-c1.json", "workflow-c2.json", "workflow-c3.json"]
        }
        
        for project_name, workflow_files in workflows_per_project.items():
            for workflow_file in workflow_files:
                workflow_data = self.complex_workflow.copy()
                workflow_data["name"] = workflow_file.replace(".json", "")
                
                workflow_request = {
                    "workflow_data": workflow_data,
                    "create_backup": False
                }
                
                response = self.client.put(
                    f"/projects/{project_name}/workflows/{workflow_file}",
                    json=workflow_request
                )
                self.assertEqual(response.status_code, 200)
        
        # Verify all projects and workflows
        list_response = self.client.get("/projects")
        self.assertEqual(list_response.status_code, 200)
        all_projects = list_response.json()
        self.assertEqual(len(all_projects), 3)
        
        # Check workflow counts
        project_workflow_counts = {p["name"]: p["workflow_count"] for p in all_projects}
        self.assertEqual(project_workflow_counts["project-a"], 2)
        self.assertEqual(project_workflow_counts["project-b"], 1)
        self.assertEqual(project_workflow_counts["project-c"], 3)
        
        # Get stats
        stats_response = self.client.get("/projects/stats")
        self.assertEqual(stats_response.status_code, 200)
        stats = stats_response.json()
        self.assertEqual(stats["total_projects"], 3)
        self.assertEqual(stats["total_workflows"], 6)

if __name__ == '__main__':
    # Run with increased verbosity
    unittest.main(verbosity=2) 