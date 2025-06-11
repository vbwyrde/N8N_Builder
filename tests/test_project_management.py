#!/usr/bin/env python3
"""
Test Suite for Project Management System
Validates project folder creation, README generation, and file system operations.

Task 2.0.1: Create project folder structure and management - Testing
"""

import unittest
import tempfile
import shutil
import json
from pathlib import Path
import sys
from datetime import datetime

# Add the n8n_builder module to path
sys.path.append(str(Path(__file__).parent.parent))

from n8n_builder.project_manager import (
    ProjectManager,
    ProjectInfo,
    WorkflowInfo,
    project_manager
)

class TestProjectManager(unittest.TestCase):
    """Test the core project management functionality."""
    
    def setUp(self):
        """Set up test fixtures with temporary directory."""
        # Create temporary directory for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.project_manager = ProjectManager(projects_root=self.temp_dir)
        
        # Sample project data
        self.sample_project_name = "Test Project"
        self.sample_description = "A test project for N8N workflows"
        self.sample_workflows = ["email-notification", "data-processor"]
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_project_manager_initialization(self):
        """Test project manager initialization."""
        # Test with default path
        default_pm = ProjectManager()
        self.assertTrue(default_pm.projects_root.exists())
        
        # Test with custom path
        custom_pm = ProjectManager(self.temp_dir)
        self.assertEqual(custom_pm.projects_root, self.temp_dir)
        self.assertTrue(custom_pm.projects_root.exists())
    
    def test_project_name_sanitization(self):
        """Test project name sanitization."""
        test_cases = [
            ("My Project", "my-project"),
            ("Email & Database Workflow", "email-database-workflow"),
            ("Special!@#$%Characters", "specialcharacters"),
            ("   Spaces   Around   ", "spaces-around"),
            ("Multiple---Dashes", "multiple-dashes"),
            ("", "project-"),  # Empty name gets timestamp
            ("123Numbers456", "123numbers456")
        ]
        
        for input_name, expected_pattern in test_cases:
            sanitized = self.project_manager._sanitize_project_name(input_name)
            if expected_pattern.endswith("-"):
                # For empty names, check it starts with expected pattern
                self.assertTrue(sanitized.startswith(expected_pattern))
            else:
                self.assertEqual(sanitized, expected_pattern)
    
    def test_project_name_validation(self):
        """Test project name validation."""
        # Valid names should not raise exceptions
        valid_names = ["Test Project", "My Workflow", "automation-suite"]
        for name in valid_names:
            try:
                self.project_manager._validate_project_name(name)
            except ValueError:
                self.fail(f"Valid name '{name}' raised ValueError")
        
        # Invalid names should raise ValueError
        invalid_names = ["", "   ", "x" * 101]  # Empty, whitespace, too long
        for name in invalid_names:
            with self.assertRaises(ValueError):
                self.project_manager._validate_project_name(name)
    
    def test_create_project_basic(self):
        """Test basic project creation."""
        project_info = self.project_manager.create_project(
            name=self.sample_project_name,
            description=self.sample_description
        )
        
        # Verify project info
        self.assertEqual(project_info.name, "test-project")
        self.assertEqual(project_info.description, self.sample_description)
        self.assertTrue(project_info.path.exists())
        self.assertTrue(project_info.path.is_dir())
        
        # Verify README exists
        readme_path = project_info.path / "README.md"
        self.assertTrue(readme_path.exists())
        
        # Verify README content
        readme_content = readme_path.read_text(encoding='utf-8')
        self.assertIn("Test Project", readme_content)
        self.assertIn(self.sample_description, readme_content)
        self.assertIn("Project Information", readme_content)
        self.assertIn("Getting Started", readme_content)
    
    def test_create_project_with_workflows(self):
        """Test project creation with initial workflows."""
        project_info = self.project_manager.create_project(
            name=self.sample_project_name,
            description=self.sample_description,
            initial_workflows=self.sample_workflows
        )
        
        # Verify workflows were created
        self.assertEqual(project_info.workflow_count, len(self.sample_workflows))
        self.assertEqual(len(project_info.workflows), len(self.sample_workflows))
        
        # Verify workflow files exist
        for workflow_name in self.sample_workflows:
            expected_filename = f"{workflow_name}.json"
            workflow_path = project_info.path / expected_filename
            self.assertTrue(workflow_path.exists())
            
            # Verify workflow content
            workflow_content = json.loads(workflow_path.read_text())
            self.assertIn("name", workflow_content)
            self.assertIn("nodes", workflow_content)
            self.assertIn("connections", workflow_content)
            self.assertEqual(workflow_content["created_by"], "N8N Builder Project Manager")
    
    def test_create_duplicate_project(self):
        """Test creating a project with duplicate name."""
        # Create first project
        self.project_manager.create_project(name=self.sample_project_name)
        
        # Attempt to create duplicate should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.project_manager.create_project(name=self.sample_project_name)
        
        self.assertIn("already exists", str(context.exception))
    
    def test_list_projects(self):
        """Test listing projects."""
        # Initially no projects
        projects = self.project_manager.list_projects()
        self.assertEqual(len(projects), 0)
        
        # Create some projects
        project_names = ["project-one", "project-two", "project-three"]
        for name in project_names:
            self.project_manager.create_project(name=name, description=f"Description for {name}")
        
        # List projects
        projects = self.project_manager.list_projects(refresh_cache=True)
        self.assertEqual(len(projects), len(project_names))
        
        # Verify project names (sanitized)
        found_names = [p.name for p in projects]
        for name in project_names:
            self.assertIn(name, found_names)
    
    def test_get_project_info(self):
        """Test getting project information."""
        # Create project
        created_project = self.project_manager.create_project(
            name=self.sample_project_name,
            description=self.sample_description,
            initial_workflows=["test-workflow"]
        )
        
        # Get project info
        project_info = self.project_manager.get_project_info("test-project")
        
        self.assertIsNotNone(project_info)
        self.assertEqual(project_info.name, created_project.name)
        self.assertEqual(project_info.description, created_project.description)
        self.assertEqual(project_info.workflow_count, 1)
        
        # Test non-existent project
        non_existent = self.project_manager.get_project_info("non-existent")
        self.assertIsNone(non_existent)
    
    def test_list_project_workflows(self):
        """Test listing workflows in a project."""
        # Create project with workflows
        project_info = self.project_manager.create_project(
            name=self.sample_project_name,
            initial_workflows=self.sample_workflows
        )
        
        # List workflows
        workflows = self.project_manager.list_project_workflows(project_info.name)
        
        self.assertEqual(len(workflows), len(self.sample_workflows))
        for workflow_name in self.sample_workflows:
            expected_filename = f"{workflow_name}.json"
            self.assertIn(expected_filename, workflows)
        
        # Verify workflows are sorted
        self.assertEqual(workflows, sorted(workflows))
    
    def test_backup_file_detection(self):
        """Test backup file detection."""
        test_cases = [
            ("workflow.json", False),
            ("workflow_2024-01-15_14-30-25.json", True),
            ("email-notification_2023-12-01_09-15-00.json", True),
            ("invalid_backup.json", False),
            ("workflow_backup.json", False),
            ("test_2024-13-45_25-70-80.json", True)  # Invalid date but matches pattern
        ]
        
        for filename, expected_is_backup in test_cases:
            result = self.project_manager._is_backup_file(filename)
            self.assertEqual(result, expected_is_backup, 
                           f"Failed for filename: {filename}")
    
    def test_project_exists(self):
        """Test project existence check."""
        # Non-existent project
        self.assertFalse(self.project_manager.project_exists("non-existent"))
        
        # Create project
        project_info = self.project_manager.create_project(name=self.sample_project_name)
        
        # Existing project
        self.assertTrue(self.project_manager.project_exists(project_info.name))
    
    def test_delete_project(self):
        """Test project deletion."""
        # Create project
        project_info = self.project_manager.create_project(name=self.sample_project_name)
        project_name = project_info.name
        
        # Verify project exists
        self.assertTrue(self.project_manager.project_exists(project_name))
        self.assertTrue(project_info.path.exists())
        
        # Test deletion without confirmation
        with self.assertRaises(ValueError):
            self.project_manager.delete_project(project_name, confirm=False)
        
        # Delete with confirmation
        result = self.project_manager.delete_project(project_name, confirm=True)
        
        self.assertTrue(result)
        self.assertFalse(self.project_manager.project_exists(project_name))
        self.assertFalse(project_info.path.exists())
        
        # Test deleting non-existent project
        result2 = self.project_manager.delete_project("non-existent", confirm=True)
        self.assertFalse(result2)
    
    def test_get_project_stats(self):
        """Test project statistics."""
        # Initially no projects
        stats = self.project_manager.get_project_stats()
        self.assertEqual(stats['total_projects'], 0)
        self.assertEqual(stats['total_workflows'], 0)
        self.assertEqual(stats['average_workflows_per_project'], 0)
        
        # Create projects with different workflow counts
        projects_data = [
            ("project-one", [], 0),
            ("project-two", ["workflow1"], 1),
            ("project-three", ["workflow1", "workflow2", "workflow3"], 3)
        ]
        
        for name, workflows, expected_count in projects_data:
            self.project_manager.create_project(
                name=name,
                initial_workflows=workflows
            )
        
        # Get updated stats
        stats = self.project_manager.get_project_stats()
        
        self.assertEqual(stats['total_projects'], 3)
        self.assertEqual(stats['total_workflows'], 4)  # 0 + 1 + 3
        self.assertAlmostEqual(stats['average_workflows_per_project'], 4/3, places=2)
        self.assertEqual(len(stats['project_names']), 3)
        self.assertIn('project-one', stats['project_names'])
        self.assertEqual(stats['largest_project'], 'project-three')

class TestProjectInfo(unittest.TestCase):
    """Test ProjectInfo data class functionality."""
    
    def test_project_info_creation(self):
        """Test creating ProjectInfo objects."""
        path = Path("/test/path")
        project_info = ProjectInfo(
            name="test-project",
            path=path,
            description="Test description"
        )
        
        self.assertEqual(project_info.name, "test-project")
        self.assertEqual(project_info.path, path)
        self.assertEqual(project_info.description, "Test description")
        self.assertIsInstance(project_info.created_date, datetime)
        self.assertEqual(project_info.workflow_count, 0)
    
    def test_project_info_serialization(self):
        """Test ProjectInfo to/from dict conversion."""
        original = ProjectInfo(
            name="test-project",
            path=Path("/test/path"),
            description="Test description",
            workflow_count=3,
            workflows=["workflow1.json", "workflow2.json"],
            settings={"setting1": "value1"}
        )
        
        # Convert to dict
        data = original.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], "test-project")
        # Use Path to normalize for cross-platform compatibility
        self.assertEqual(Path(data['path']), Path("/test/path"))
        self.assertEqual(data['description'], "Test description")
        self.assertEqual(data['workflow_count'], 3)
        self.assertEqual(data['workflows'], ["workflow1.json", "workflow2.json"])
        
        # Convert back from dict
        restored = ProjectInfo.from_dict(data)
        
        self.assertEqual(restored.name, original.name)
        self.assertEqual(restored.path, original.path)
        self.assertEqual(restored.description, original.description)
        self.assertEqual(restored.workflow_count, original.workflow_count)
        self.assertEqual(restored.workflows, original.workflows)

class TestWorkflowInfo(unittest.TestCase):
    """Test WorkflowInfo data class functionality."""
    
    def test_workflow_info_creation(self):
        """Test creating WorkflowInfo objects."""
        workflow_info = WorkflowInfo(
            name="Test Workflow",
            filename="test-workflow.json",
            project_name="test-project",
            description="A test workflow",
            node_count=5,
            tags=["email", "automation"]
        )
        
        self.assertEqual(workflow_info.name, "Test Workflow")
        self.assertEqual(workflow_info.filename, "test-workflow.json")
        self.assertEqual(workflow_info.project_name, "test-project")
        self.assertEqual(workflow_info.node_count, 5)
        self.assertEqual(workflow_info.tags, ["email", "automation"])
    
    def test_workflow_info_serialization(self):
        """Test WorkflowInfo to dict conversion."""
        workflow_info = WorkflowInfo(
            name="Test Workflow",
            filename="test-workflow.json",
            project_name="test-project",
            description="A test workflow",
            version_count=3,
            file_size=1024,
            node_count=5,
            tags=["email", "automation"]
        )
        
        data = workflow_info.to_dict()
        
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], "Test Workflow")
        self.assertEqual(data['filename'], "test-workflow.json")
        self.assertEqual(data['project_name'], "test-project")
        self.assertEqual(data['version_count'], 3)
        self.assertEqual(data['file_size'], 1024)
        self.assertEqual(data['node_count'], 5)
        self.assertEqual(data['tags'], ["email", "automation"])

class TestProjectManagerIntegration(unittest.TestCase):
    """Test integration scenarios and edge cases."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.project_manager = ProjectManager(projects_root=self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
    
    def test_create_project_filesystem_error(self):
        """Test project creation with filesystem errors."""
        # Create a file where we want to create a project directory
        conflicting_file = self.temp_dir / "test-project"
        conflicting_file.write_text("This is a file, not a directory")
        
        # Attempt to create project should fail because the name already exists as a file
        with self.assertRaises(ValueError) as context:
            self.project_manager.create_project(name="test-project")
        
        # Verify it's the expected error about already existing
        self.assertIn("already exists", str(context.exception))
    
    def test_readme_generation_comprehensive(self):
        """Test comprehensive README generation."""
        # Create project with workflows
        project_info = self.project_manager.create_project(
            name="Comprehensive Test Project",
            description="A comprehensive test of README generation",
            initial_workflows=["email-sender", "data-processor", "error-handler"]
        )
        
        readme_path = project_info.path / "README.md"
        readme_content = readme_path.read_text(encoding='utf-8')
        
        # Verify all expected sections
        expected_sections = [
            "# Comprehensive Test Project",
            "## Project Information",
            "## Workflows",
            "## Getting Started",
            "## Project Structure",
            "## File Naming Conventions",
            "## Iteration History"
        ]
        
        for section in expected_sections:
            self.assertIn(section, readme_content)
        
        # Verify workflow listing
        for workflow in ["email-sender.json", "data-processor.json", "error-handler.json"]:
            self.assertIn(workflow, readme_content)
        
        # Verify generated timestamp
        self.assertIn("Generated by N8N Builder Project Manager", readme_content)
    
    def test_project_cache_functionality(self):
        """Test project caching behavior."""
        # Create project
        project_info = self.project_manager.create_project(name="Cache Test")
        
        # First call should populate cache
        projects1 = self.project_manager.list_projects()
        self.assertEqual(len(projects1), 1)
        
        # Second call should use cache
        projects2 = self.project_manager.list_projects()
        self.assertEqual(len(projects2), 1)
        self.assertEqual(projects1[0].name, projects2[0].name)
        
        # Force refresh should work
        projects3 = self.project_manager.list_projects(refresh_cache=True)
        self.assertEqual(len(projects3), 1)
    
    def test_edge_case_project_names(self):
        """Test edge cases in project naming."""
        edge_cases = [
            ("123", "123"),  # Numbers only
            ("A", "a"),      # Single character
            ("Mix3d_Ch4rs!", "mix3d-ch4rs"),  # Mixed with special chars
            ("                spaces                ", "spaces")  # Excessive spaces
        ]
        
        for input_name, expected_sanitized in edge_cases:
            try:
                project_info = self.project_manager.create_project(name=input_name)
                self.assertEqual(project_info.name, expected_sanitized)
                
                # Verify project was actually created
                self.assertTrue(project_info.path.exists())
                self.assertTrue(self.project_manager.project_exists(expected_sanitized))
                
                # Clean up for next iteration
                self.project_manager.delete_project(expected_sanitized, confirm=True)
            except Exception as e:
                self.fail(f"Edge case '{input_name}' failed: {str(e)}")

if __name__ == '__main__':
    # Run with increased verbosity to see detailed test output
    unittest.main(verbosity=2) 