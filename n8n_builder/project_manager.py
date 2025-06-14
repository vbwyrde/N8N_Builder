#!/usr/bin/env python3
"""
Project Management System for N8N Builder
Handles project folder structure, workflow file management, and README generation.

Task 2.0.1: Create project folder structure and management
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
import shutil
import re

logger = logging.getLogger(__name__)
project_logger = logging.getLogger('n8n_builder.project')

@dataclass
class ProjectInfo:
    """Information about a project."""
    name: str
    path: Path
    description: str = ""
    created_date: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    workflow_count: int = 0
    workflows: List[str] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert project info to dictionary for serialization."""
        return {
            'name': self.name,
            'path': str(self.path),
            'description': self.description,
            'created_date': self.created_date.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'workflow_count': self.workflow_count,
            'workflows': self.workflows,
            'settings': self.settings
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectInfo':
        """Create ProjectInfo from dictionary."""
        return cls(
            name=data['name'],
            path=Path(data['path']),
            description=data.get('description', ''),
            created_date=datetime.fromisoformat(data['created_date']),
            last_modified=datetime.fromisoformat(data['last_modified']),
            workflow_count=data.get('workflow_count', 0),
            workflows=data.get('workflows', []),
            settings=data.get('settings', {})
        )

@dataclass
class WorkflowInfo:
    """Information about a workflow within a project."""
    name: str
    filename: str
    project_name: str
    description: str = ""
    created_date: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    version_count: int = 1
    file_size: int = 0
    node_count: int = 0
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow info to dictionary."""
        return {
            'name': self.name,
            'filename': self.filename,
            'project_name': self.project_name,
            'description': self.description,
            'created_date': self.created_date.isoformat(),
            'last_modified': self.last_modified.isoformat(),
            'version_count': self.version_count,
            'file_size': self.file_size,
            'node_count': self.node_count,
            'tags': self.tags
        }

class ProjectManager:
    """
    Manages N8N Builder project folder structure and file operations.
    
    Handles:
    - Project creation and management
    - Workflow file operations
    - README.md generation and updates
    - File system error handling
    - Project metadata tracking
    """
    
    def __init__(self, projects_root: Optional[Union[str, Path]] = None):
        """
        Initialize the project manager.
        
        Args:
            projects_root: Root directory for projects. Defaults to 'projects' in current dir.
        """
        if projects_root is None:
            self.projects_root = Path.cwd() / "projects"
        else:
            self.projects_root = Path(projects_root)
        
        # Ensure projects root directory exists
        self._ensure_projects_root()
        
        # Project cache for performance
        self._project_cache: Dict[str, ProjectInfo] = {}
        self._cache_valid = False
        
        project_logger.info(f"Project manager initialized with root: {self.projects_root}")
    
    def _ensure_projects_root(self) -> None:
        """Ensure the projects root directory exists."""
        try:
            self.projects_root.mkdir(parents=True, exist_ok=True)
            project_logger.info(f"Ensured projects root directory exists: {self.projects_root}")
        except Exception as e:
            error_msg = f"Failed to create projects root directory {self.projects_root}: {str(e)}"
            project_logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def _sanitize_project_name(self, name: str) -> str:
        """
        Sanitize project name for filesystem use.
        
        Args:
            name: Raw project name
            
        Returns:
            Sanitized name safe for filesystem
        """
        # Replace spaces and underscores with hyphens, remove special characters
        sanitized = re.sub(r'[^\w\s-]', '', name.strip())
        sanitized = re.sub(r'[-\s_]+', '-', sanitized)  # Convert underscores to hyphens
        sanitized = sanitized.lower().strip('-')
        
        # Ensure name is not empty
        if not sanitized:
            sanitized = f"project-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        return sanitized
    
    def _validate_project_name(self, name: str) -> None:
        """
        Validate project name.
        
        Args:
            name: Project name to validate
            
        Raises:
            ValueError: If project name is invalid
        """
        if not name or not name.strip():
            raise ValueError("Project name cannot be empty")
        
        if len(name) > 100:
            raise ValueError("Project name too long (max 100 characters)")
        
        sanitized = self._sanitize_project_name(name)
        if len(sanitized) < 1:
            raise ValueError("Project name contains no valid characters")
    
    def create_project(self, name: str, description: str = "", 
                      initial_workflows: Optional[List[str]] = None) -> ProjectInfo:
        """
        Create a new project with folder structure and README.
        
        Args:
            name: Project name (will be sanitized for filesystem)
            description: Project description
            initial_workflows: List of initial workflow names to create
            
        Returns:
            ProjectInfo object for the created project
            
        Raises:
            ValueError: If project name is invalid
            RuntimeError: If project creation fails
        """
        try:
            # Validate and sanitize name
            self._validate_project_name(name)
            sanitized_name = self._sanitize_project_name(name)
            
            project_path = self.projects_root / sanitized_name
            
            # Check if project already exists
            if project_path.exists():
                raise ValueError(f"Project '{sanitized_name}' already exists")
            
            project_logger.info(f"Creating new project: {sanitized_name}", extra={'project_name': sanitized_name, 'operation': 'create_project'})
            
            # Create project directory
            project_path.mkdir(parents=True)
            
            # Create project info
            project_info = ProjectInfo(
                name=sanitized_name,
                path=project_path,
                description=description
            )
            
            # Create initial workflows if specified
            if initial_workflows:
                for workflow_name in initial_workflows:
                    self._create_placeholder_workflow(project_info, workflow_name)
            
            # Update project info with workflow count
            project_info.workflows = self.list_project_workflows(sanitized_name)
            project_info.workflow_count = len(project_info.workflows)
            
            # Generate README after workflows are created (so count is accurate)
            self._generate_project_readme(project_info)
            
            # Update cache
            self._project_cache[sanitized_name] = project_info
            
            project_logger.info(f"Successfully created project '{sanitized_name}' at {project_path}", extra={'project_name': sanitized_name, 'operation': 'create_project'})
            
            return project_info
            
        except Exception as e:
            error_msg = f"Failed to create project '{name}': {str(e)}"
            project_logger.error(error_msg, extra={'project_name': name, 'operation': 'create_project'})
            
            # Cleanup on failure
            try:
                if 'project_path' in locals() and project_path.exists():
                    shutil.rmtree(project_path)
            except Exception as cleanup_error:
                project_logger.error(f"Failed to cleanup failed project creation: {cleanup_error}", extra={'project_name': name, 'operation': 'create_project'})
            
            if isinstance(e, ValueError):
                raise
            else:
                raise RuntimeError(error_msg)
    
    def _generate_project_readme(self, project_info: ProjectInfo) -> None:
        """
        Generate a comprehensive README.md file for a project.
        
        Args:
            project_info: Project information
        """
        readme_content = f"""# {project_info.name.replace('-', ' ').title()}

{project_info.description if project_info.description else 'N8N workflow automation project'}

## Project Information

- **Created**: {project_info.created_date.strftime('%Y-%m-%d %H:%M:%S')}
- **Last Modified**: {project_info.last_modified.strftime('%Y-%m-%d %H:%M:%S')}
- **Workflows**: {project_info.workflow_count}

## Workflows

{self._generate_workflow_list_for_readme(project_info)}

## Getting Started

1. **Load workflows**: Import any `.json` files into N8N
2. **Test workflows**: Run workflows in N8N to verify functionality
3. **Iterate**: Use N8N Builder to modify and improve workflows based on testing feedback

## Project Structure

```
{project_info.name}/
├── README.md                    # This file
├── workflow-name.json          # Main workflow files
└── workflow-name_YYYY-MM-DD_HH-MM-SS.json  # Versioned backups
```

## File Naming Conventions

- **Original workflows**: `workflow-name.json`
- **Versioned backups**: `workflow-name_YYYY-MM-DD_HH-MM-SS.json`
- **Project documentation**: `README.md`

## Iteration History

This section will be updated automatically as workflows are modified through N8N Builder.

---

*Generated by N8N Builder Project Manager on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        readme_path = project_info.path / "README.md"
        try:
            readme_path.write_text(readme_content, encoding='utf-8')
            project_logger.info(f"Generated README for project {project_info.name}", extra={'project_name': project_info.name, 'operation': 'generate_readme'})
        except Exception as e:
            project_logger.error(f"Failed to generate README for project {project_info.name}: {str(e)}", extra={'project_name': project_info.name, 'operation': 'generate_readme'})
            raise RuntimeError(f"Failed to generate README: {str(e)}")
    
    def _generate_workflow_list_for_readme(self, project_info: ProjectInfo) -> str:
        """Generate workflow list section for README."""
        if not project_info.workflows:
            return "*No workflows yet. Create your first workflow using N8N Builder.*"
        
        workflow_list = []
        for workflow_name in project_info.workflows:
            workflow_list.append(f"- **{workflow_name}**: [Description will be added after analysis]")
        
        return "\n".join(workflow_list)
    
    def _create_placeholder_workflow(self, project_info: ProjectInfo, workflow_name: str) -> None:
        """
        Create a placeholder workflow file.
        
        Args:
            project_info: Project information
            workflow_name: Name of the workflow to create
        """
        sanitized_name = re.sub(r'[^\w\s-]', '', workflow_name.strip())
        sanitized_name = re.sub(r'[-\s]+', '-', sanitized_name).lower().strip('-')
        
        if not sanitized_name:
            sanitized_name = f"workflow-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        filename = f"{sanitized_name}.json"
        filepath = project_info.path / filename
        
        # Create basic workflow structure
        placeholder_workflow = {
            "name": workflow_name,
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
            "version": 1,
            "created_by": "N8N Builder Project Manager",
            "created_date": datetime.now().isoformat()
        }
        
        try:
            filepath.write_text(json.dumps(placeholder_workflow, indent=2), encoding='utf-8')
            project_logger.info(f"Created placeholder workflow {filename} in project {project_info.name}", extra={'project_name': project_info.name, 'operation': 'create_placeholder_workflow'})
        except Exception as e:
            project_logger.error(f"Failed to create placeholder workflow {filename}: {str(e)}", extra={'project_name': project_info.name, 'operation': 'create_placeholder_workflow'})
            raise RuntimeError(f"Failed to create placeholder workflow: {str(e)}")
    
    def list_projects(self, refresh_cache: bool = False) -> List[ProjectInfo]:
        """
        List all projects in the projects directory.
        
        Args:
            refresh_cache: Whether to refresh the project cache
            
        Returns:
            List of ProjectInfo objects
        """
        if refresh_cache or not self._cache_valid:
            self._refresh_project_cache()
        
        return list(self._project_cache.values())
    
    def _refresh_project_cache(self) -> None:
        """Refresh the project cache by scanning the filesystem."""
        self._project_cache.clear()
        
        try:
            if not self.projects_root.exists():
                self._ensure_projects_root()
                self._cache_valid = True
                return
            
            for item in self.projects_root.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    try:
                        project_info = self._load_project_info(item.name)
                        self._project_cache[item.name] = project_info
                    except Exception as e:
                        project_logger.warning(f"Failed to load project info for {item.name}: {str(e)}", extra={'project_name': item.name, 'operation': 'refresh_project_cache'})
                        continue
            
            self._cache_valid = True
            project_logger.info(f"Refreshed project cache: {len(self._project_cache)} projects found", extra={'project_name': None, 'operation': 'refresh_project_cache'})
            
        except Exception as e:
            project_logger.error(f"Failed to refresh project cache: {str(e)}", extra={'project_name': None, 'operation': 'refresh_project_cache'})
            self._cache_valid = False
    
    def _load_project_info(self, project_name: str) -> ProjectInfo:
        """
        Load project information from filesystem.
        
        Args:
            project_name: Name of the project
            
        Returns:
            ProjectInfo object
        """
        project_path = self.projects_root / project_name
        
        if not project_path.exists() or not project_path.is_dir():
            raise ValueError(f"Project {project_name} does not exist")
        
        # Get basic info from filesystem
        stat = project_path.stat()
        created_date = datetime.fromtimestamp(stat.st_ctime)
        last_modified = datetime.fromtimestamp(stat.st_mtime)
        
        # Get workflows
        workflows = self.list_project_workflows(project_name)
        
        # Try to extract description from README if it exists
        description = ""
        readme_path = project_path / "README.md"
        if readme_path.exists():
            try:
                readme_content = readme_path.read_text(encoding='utf-8')
                # Extract description from README (first paragraph after title)
                lines = readme_content.split('\n')
                for i, line in enumerate(lines[1:], 1):  # Skip title
                    if line.strip() and not line.startswith('#'):
                        description = line.strip()
                        break
            except Exception as e:
                project_logger.warning(f"Failed to read README for project {project_name}: {str(e)}", extra={'project_name': project_name, 'operation': 'load_project_info'})
        
        return ProjectInfo(
            name=project_name,
            path=project_path,
            description=description,
            created_date=created_date,
            last_modified=last_modified,
            workflow_count=len(workflows),
            workflows=workflows
        )
    
    def get_project_info(self, project_name: str) -> Optional[ProjectInfo]:
        """
        Get information about a specific project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            ProjectInfo object or None if not found
        """
        try:
            if project_name in self._project_cache and self._cache_valid:
                return self._project_cache[project_name]
            
            return self._load_project_info(project_name)
        except Exception as e:
            project_logger.error(f"Failed to get project info for {project_name}: {str(e)}", extra={'project_name': project_name, 'operation': 'get_project_info'})
            return None
    
    def list_project_workflows(self, project_name: str) -> List[str]:
        """
        List all workflow files in a project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            List of workflow filenames (without path)
        """
        project_path = self.projects_root / project_name
        
        if not project_path.exists():
            return []
        
        workflows = []
        try:
            for item in project_path.iterdir():
                if (item.is_file() and 
                    item.suffix == '.json' and 
                    not self._is_backup_file(item.name)):
                    workflows.append(item.name)
            
            workflows.sort()  # Sort alphabetically
            return workflows
            
        except Exception as e:
            project_logger.error(f"Failed to list workflows for project {project_name}: {str(e)}", extra={'project_name': project_name, 'operation': 'list_project_workflows'})
            return []
    
    def _is_backup_file(self, filename: str) -> bool:
        """
        Check if a filename is a backup file.
        
        Args:
            filename: Name of the file
            
        Returns:
            True if it's a backup file
        """
        # Backup files follow pattern: workflow-name_YYYY-MM-DD_HH-MM-SS.json
        # or workflow-name_YYYY-MM-DD_HH-MM-SS-NNN.json (with counter)
        backup_pattern = r'.*_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(-\d{3})?\.json$'
        return bool(re.match(backup_pattern, filename))
    
    def project_exists(self, project_name: str) -> bool:
        """
        Check if a project exists.
        
        Args:
            project_name: Name of the project
            
        Returns:
            True if project exists
        """
        project_path = self.projects_root / project_name
        return project_path.exists() and project_path.is_dir()
    
    def delete_project(self, project_name: str, confirm: bool = False) -> bool:
        """
        Delete a project and all its contents.
        
        Args:
            project_name: Name of the project to delete
            confirm: Confirmation flag to prevent accidental deletion
            
        Returns:
            True if deletion was successful
            
        Raises:
            ValueError: If confirmation is not provided
            RuntimeError: If deletion fails
        """
        if not confirm:
            raise ValueError("Project deletion requires explicit confirmation")
        
        project_path = self.projects_root / project_name
        
        if not project_path.exists():
            project_logger.warning(f"Project {project_name} does not exist", extra={'project_name': project_name, 'operation': 'delete_project'})
            return False
        
        try:
            shutil.rmtree(project_path)
            
            # Remove from cache
            if project_name in self._project_cache:
                del self._project_cache[project_name]
            
            project_logger.info(f"Successfully deleted project {project_name}", extra={'project_name': project_name, 'operation': 'delete_project'})
            return True
            
        except Exception as e:
            error_msg = f"Failed to delete project {project_name}: {str(e)}"
            project_logger.error(error_msg, extra={'project_name': project_name, 'operation': 'delete_project'})
            raise RuntimeError(error_msg)
    
    def get_project_stats(self) -> Dict[str, Any]:
        """
        Get statistics about all projects.
        
        Returns:
            Dictionary with project statistics
        """
        projects = self.list_projects(refresh_cache=True)
        
        total_workflows = sum(p.workflow_count for p in projects)
        
        stats = {
            'total_projects': len(projects),
            'total_workflows': total_workflows,
            'projects_root': str(self.projects_root),
            'average_workflows_per_project': total_workflows / len(projects) if projects else 0,
            'project_names': [p.name for p in projects],
            'largest_project': max(projects, key=lambda p: p.workflow_count).name if projects else None,
            'most_recent_project': max(projects, key=lambda p: p.last_modified).name if projects else None
        }
        
        return stats

# Global project manager instance
project_manager = ProjectManager()

class FileSystemUtilities:
    """
    Enhanced file system utilities for workflow management.
    Extends ProjectManager with advanced workflow file operations.
    
    Task 2.0.2: Implement file system utilities for workflow management
    """
    
    def __init__(self, project_manager_instance: ProjectManager):
        """
        Initialize file system utilities.
        
        Args:
            project_manager_instance: The project manager to extend
        """
        self.project_manager = project_manager_instance
        self.logger = logging.getLogger('n8n_builder.filesystem')
    
    def read_workflow_file(self, project_name: str, workflow_filename: str) -> Dict[str, Any]:
        """
        Read and parse a workflow JSON file.
        
        Args:
            project_name: Name of the project
            workflow_filename: Name of the workflow file (with .json extension)
            
        Returns:
            Dictionary containing the workflow data
            
        Raises:
            ValueError: If project or file doesn't exist
            RuntimeError: If file cannot be read or parsed
        """
        try:
            if not self.project_manager.project_exists(project_name):
                raise ValueError(f"Project '{project_name}' does not exist")
            
            project_path = self.project_manager.projects_root / project_name
            workflow_path = project_path / workflow_filename
            
            if not workflow_path.exists():
                raise ValueError(f"Workflow file '{workflow_filename}' not found in project '{project_name}'")
            
            if not workflow_path.is_file():
                raise ValueError(f"'{workflow_filename}' is not a file")
            
            # Read and parse JSON
            workflow_content = workflow_path.read_text(encoding='utf-8')
            workflow_data = json.loads(workflow_content)
            
            self.logger.info(f"Successfully read workflow {workflow_filename} from project {project_name}", extra={'project_name': project_name, 'operation': 'read_workflow_file'})
            return workflow_data
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in workflow file '{workflow_filename}': {str(e)}"
            self.logger.error(error_msg, extra={'project_name': project_name, 'operation': 'read_workflow_file'})
            raise RuntimeError(error_msg)
        except Exception as e:
            error_msg = f"Failed to read workflow '{workflow_filename}' from project '{project_name}': {str(e)}"
            self.logger.error(error_msg, extra={'project_name': project_name, 'operation': 'read_workflow_file'})
            if isinstance(e, ValueError):
                raise
            else:
                raise RuntimeError(error_msg)
    
    def write_workflow_file(self, project_name: str, workflow_filename: str, 
                          workflow_data: Dict[str, Any], create_backup: bool = True) -> bool:
        """
        Write workflow data to a JSON file with optional backup.
        
        Args:
            project_name: Name of the project
            workflow_filename: Name of the workflow file (with .json extension)
            workflow_data: Dictionary containing the workflow data
            create_backup: Whether to create a backup before writing
            
        Returns:
            True if write was successful
            
        Raises:
            ValueError: If project doesn't exist or data is invalid
            RuntimeError: If file cannot be written
        """
        try:
            if not self.project_manager.project_exists(project_name):
                raise ValueError(f"Project '{project_name}' does not exist")
            
            project_path = self.project_manager.projects_root / project_name
            workflow_path = project_path / workflow_filename
            
            # Validate workflow data
            if not isinstance(workflow_data, dict):
                raise ValueError("Workflow data must be a dictionary")
            
            # Create backup if file exists and backup is requested
            if create_backup and workflow_path.exists():
                self._create_workflow_backup(project_name, workflow_filename)
            
            # Write workflow data
            workflow_json = json.dumps(workflow_data, indent=2, ensure_ascii=False)
            workflow_path.write_text(workflow_json, encoding='utf-8')
            
            # Update project info if this is a new workflow
            project_info = self.project_manager.get_project_info(project_name)
            if project_info and workflow_filename not in project_info.workflows:
                # Refresh project cache to include new workflow
                self.project_manager._refresh_project_cache()
            
            self.logger.info(f"Successfully wrote workflow {workflow_filename} to project {project_name}", extra={'project_name': project_name, 'operation': 'write_workflow_file'})
            return True
            
        except Exception as e:
            error_msg = f"Failed to write workflow '{workflow_filename}' to project '{project_name}': {str(e)}"
            self.logger.error(error_msg, extra={'project_name': project_name, 'operation': 'write_workflow_file'})
            if isinstance(e, ValueError):
                raise
            else:
                raise RuntimeError(error_msg)
    
    def _create_workflow_backup(self, project_name: str, workflow_filename: str) -> str:
        """
        Create a timestamped backup of a workflow file.
        
        Args:
            project_name: Name of the project
            workflow_filename: Name of the workflow file
            
        Returns:
            Name of the backup file created
        """
        project_path = self.project_manager.projects_root / project_name
        workflow_path = project_path / workflow_filename
        
        if not workflow_path.exists():
            return ""
        
        # Generate backup filename with timestamp - ensure uniqueness
        base_timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        name_without_ext = workflow_filename.replace('.json', '')
        backup_filename = f"{name_without_ext}_{base_timestamp}.json"
        backup_path = project_path / backup_filename
        
        # If backup already exists, add microseconds for uniqueness
        counter = 0
        while backup_path.exists():
            counter += 1
            timestamp_with_counter = f"{base_timestamp}-{counter:03d}"
            backup_filename = f"{name_without_ext}_{timestamp_with_counter}.json"
            backup_path = project_path / backup_filename
        
        # Copy file to backup
        import shutil
        shutil.copy2(workflow_path, backup_path)
        
        self.logger.info(f"Created backup: {backup_filename}", extra={'project_name': project_name, 'operation': 'create_workflow_backup'})
        return backup_filename
    
    def list_workflow_versions(self, project_name: str, workflow_filename: str) -> List[str]:
        """
        List all versions (backups) of a workflow file.
        
        Args:
            project_name: Name of the project
            workflow_filename: Name of the workflow file
            
        Returns:
            List of backup filenames sorted by creation time (newest first)
        """
        try:
            if not self.project_manager.project_exists(project_name):
                return []
            
            project_path = self.project_manager.projects_root / project_name
            name_without_ext = workflow_filename.replace('.json', '')
            
            # Find all backup files for this workflow
            backup_files = []
            for file_path in project_path.iterdir():
                if (file_path.is_file() and 
                    file_path.name.startswith(f"{name_without_ext}_") and
                    file_path.name.endswith('.json') and
                    self.project_manager._is_backup_file(file_path.name)):
                    backup_files.append((file_path.name, file_path.stat().st_mtime))
            
            # Sort by modification time (newest first)
            backup_files.sort(key=lambda x: x[1], reverse=True)
            return [filename for filename, _ in backup_files]
            
        except Exception as e:
            self.logger.error(f"Failed to list workflow versions for {workflow_filename}: {str(e)}", extra={'project_name': project_name, 'operation': 'list_workflow_versions'})
            return []
    
    def cleanup_old_versions(self, project_name: str, workflow_filename: str, 
                           keep_versions: int = 10) -> int:
        """
        Clean up old versions of a workflow, keeping only the specified number.
        
        Args:
            project_name: Name of the project
            workflow_filename: Name of the workflow file
            keep_versions: Number of versions to keep (default: 10)
            
        Returns:
            Number of files deleted
        """
        try:
            versions = self.list_workflow_versions(project_name, workflow_filename)
            
            if len(versions) <= keep_versions:
                return 0
            
            project_path = self.project_manager.projects_root / project_name
            files_to_delete = versions[keep_versions:]  # Keep the newest ones
            deleted_count = 0
            
            for filename in files_to_delete:
                file_path = project_path / filename
                try:
                    file_path.unlink()
                    deleted_count += 1
                    self.logger.info(f"Deleted old version: {filename}", extra={'project_name': project_name, 'operation': 'cleanup_old_versions'})
                except Exception as e:
                    self.logger.warning(f"Failed to delete old version {filename}: {str(e)}", extra={'project_name': project_name, 'operation': 'cleanup_old_versions'})
            
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup old versions for {workflow_filename}: {str(e)}", extra={'project_name': project_name, 'operation': 'cleanup_old_versions'})
            return 0
    
    def get_version_info(self, project_name: str, workflow_filename: str, version_filename: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific workflow version.
        
        Args:
            project_name: Name of the project
            workflow_filename: Name of the main workflow file
            version_filename: Name of the version file
            
        Returns:
            Dictionary with version information
        """
        try:
            if not self.project_manager.project_exists(project_name):
                raise ValueError(f"Project '{project_name}' does not exist")
            
            project_path = self.project_manager.projects_root / project_name
            version_path = project_path / version_filename
            
            if not version_path.exists():
                raise ValueError(f"Version file '{version_filename}' not found")
            
            # Extract timestamp from filename
            import re
            timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', version_filename)
            timestamp_str = timestamp_match.group(1) if timestamp_match else "unknown"
            
            # Get file stats
            file_stats = version_path.stat()
            
            # Read workflow data for analysis
            try:
                with open(version_path, 'r', encoding='utf-8') as f:
                    workflow_data = json.load(f)
                
                node_count = len(workflow_data.get('nodes', []))
                workflow_name = workflow_data.get('name', 'Unknown')
                tags = workflow_data.get('tags', [])
            except Exception as e:
                self.logger.warning(f"Failed to analyze workflow data in version {version_filename}: {str(e)}", extra={'project_name': project_name, 'operation': 'get_version_info'})
                node_count = 0
                workflow_name = "Unknown"
                tags = []
            
            return {
                'filename': version_filename,
                'timestamp': timestamp_str,
                'created_date': datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
                'modified_date': datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                'file_size': file_stats.st_size,
                'file_size_mb': round(file_stats.st_size / (1024 * 1024), 3),
                'workflow_name': workflow_name,
                'node_count': node_count,
                'tags': tags,
                'is_backup': True
            }
            
        except Exception as e:
            error_msg = f"Failed to get version info for {version_filename}: {str(e)}"
            self.logger.error(error_msg, extra={'project_name': project_name, 'operation': 'get_version_info'})
            if isinstance(e, ValueError):
                raise
            else:
                raise RuntimeError(error_msg)
    
    def restore_workflow_version(self, project_name: str, workflow_filename: str, 
                               version_filename: str, create_backup: bool = True) -> bool:
        """
        Restore a workflow from a specific version.
        
        Args:
            project_name: Name of the project
            workflow_filename: Name of the main workflow file
            version_filename: Name of the version file to restore from
            create_backup: Whether to create a backup of current version before restoring
            
        Returns:
            True if restoration was successful
        """
        try:
            if not self.project_manager.project_exists(project_name):
                raise ValueError(f"Project '{project_name}' does not exist")
            
            project_path = self.project_manager.projects_root / project_name
            version_path = project_path / version_filename
            workflow_path = project_path / workflow_filename
            
            if not version_path.exists():
                raise ValueError(f"Version file '{version_filename}' not found")
            
            # Read version data
            with open(version_path, 'r', encoding='utf-8') as f:
                version_data = json.load(f)
            
            # Validate the version data
            validation_errors = self.validate_workflow_json(version_data)
            if validation_errors:
                raise ValueError(f"Version file contains invalid workflow data: {'; '.join(validation_errors)}")
            
            # Create backup of current version if requested and file exists
            if create_backup and workflow_path.exists():
                backup_filename = self._create_workflow_backup(project_name, workflow_filename)
                self.logger.info(f"Created backup before restoration: {backup_filename}", extra={'project_name': project_name, 'operation': 'restore_workflow_version'})
            
            # Write the version data to the main workflow file
            success = self.write_workflow_file(project_name, workflow_filename, version_data, create_backup=False)
            
            if success:
                self.logger.info(f"Successfully restored workflow '{workflow_filename}' from version '{version_filename}'", extra={'project_name': project_name, 'operation': 'restore_workflow_version'})
                return True
            else:
                raise RuntimeError("Failed to write restored workflow data")
            
        except Exception as e:
            error_msg = f"Failed to restore workflow from version {version_filename}: {str(e)}"
            self.logger.error(error_msg, extra={'project_name': project_name, 'operation': 'restore_workflow_version'})
            if isinstance(e, ValueError):
                raise
            else:
                raise RuntimeError(error_msg)
    
    def compare_workflow_versions(self, project_name: str, workflow_filename: str, 
                                version1: str, version2: str) -> Dict[str, Any]:
        """
        Compare two workflow versions and return differences.
        
        Args:
            project_name: Name of the project
            workflow_filename: Name of the main workflow file
            version1: First version filename (or 'current' for main file)
            version2: Second version filename (or 'current' for main file)
            
        Returns:
            Dictionary with comparison results
        """
        try:
            if not self.project_manager.project_exists(project_name):
                raise ValueError(f"Project '{project_name}' does not exist")
            
            project_path = self.project_manager.projects_root / project_name
            
            # Read first version
            if version1 == 'current':
                version1_path = project_path / workflow_filename
                version1_label = 'Current Version'
            else:
                version1_path = project_path / version1
                version1_label = version1
            
            # Read second version
            if version2 == 'current':
                version2_path = project_path / workflow_filename
                version2_label = 'Current Version'
            else:
                version2_path = project_path / version2
                version2_label = version2
            
            if not version1_path.exists():
                raise ValueError(f"Version file '{version1}' not found")
            if not version2_path.exists():
                raise ValueError(f"Version file '{version2}' not found")
            
            # Read workflow data
            with open(version1_path, 'r', encoding='utf-8') as f:
                data1 = json.load(f)
            with open(version2_path, 'r', encoding='utf-8') as f:
                data2 = json.load(f)
            
            # Compare basic properties
            comparison = {
                'version1': {
                    'label': version1_label,
                    'filename': version1,
                    'name': data1.get('name', 'Unknown'),
                    'node_count': len(data1.get('nodes', [])),
                    'tags': data1.get('tags', []),
                    'active': data1.get('active', False)
                },
                'version2': {
                    'label': version2_label,
                    'filename': version2,
                    'name': data2.get('name', 'Unknown'),
                    'node_count': len(data2.get('nodes', [])),
                    'tags': data2.get('tags', []),
                    'active': data2.get('active', False)
                },
                'differences': {
                    'name_changed': data1.get('name') != data2.get('name'),
                    'node_count_changed': len(data1.get('nodes', [])) != len(data2.get('nodes', [])),
                    'tags_changed': set(data1.get('tags', [])) != set(data2.get('tags', [])),
                    'active_changed': data1.get('active', False) != data2.get('active', False),
                    'nodes_changed': data1.get('nodes', []) != data2.get('nodes', []),
                    'connections_changed': data1.get('connections', {}) != data2.get('connections', {}),
                    'settings_changed': data1.get('settings', {}) != data2.get('settings', {})
                },
                'summary': {
                    'has_changes': False,
                    'change_count': 0,
                    'major_changes': [],
                    'minor_changes': []
                }
            }
            
            # Analyze changes
            major_changes = []
            minor_changes = []
            
            if comparison['differences']['name_changed']:
                minor_changes.append(f"Name changed from '{data1.get('name')}' to '{data2.get('name')}'")
            
            if comparison['differences']['node_count_changed']:
                node_diff = len(data2.get('nodes', [])) - len(data1.get('nodes', []))
                if node_diff > 0:
                    major_changes.append(f"Added {node_diff} node(s)")
                else:
                    major_changes.append(f"Removed {abs(node_diff)} node(s)")
            
            if comparison['differences']['tags_changed']:
                tags1 = set(data1.get('tags', []))
                tags2 = set(data2.get('tags', []))
                added_tags = tags2 - tags1
                removed_tags = tags1 - tags2
                if added_tags:
                    minor_changes.append(f"Added tags: {', '.join(added_tags)}")
                if removed_tags:
                    minor_changes.append(f"Removed tags: {', '.join(removed_tags)}")
            
            if comparison['differences']['active_changed']:
                status = "activated" if data2.get('active', False) else "deactivated"
                minor_changes.append(f"Workflow {status}")
            
            if comparison['differences']['nodes_changed']:
                major_changes.append("Node configuration changed")
            
            if comparison['differences']['connections_changed']:
                major_changes.append("Node connections changed")
            
            if comparison['differences']['settings_changed']:
                minor_changes.append("Workflow settings changed")
            
            comparison['summary']['major_changes'] = major_changes
            comparison['summary']['minor_changes'] = minor_changes
            comparison['summary']['change_count'] = len(major_changes) + len(minor_changes)
            comparison['summary']['has_changes'] = comparison['summary']['change_count'] > 0
            
            return comparison
            
        except Exception as e:
            error_msg = f"Failed to compare workflow versions: {str(e)}"
            self.logger.error(error_msg, extra={'project_name': project_name, 'operation': 'compare_workflow_versions'})
            if isinstance(e, ValueError):
                raise
            else:
                raise RuntimeError(error_msg)
    
    def delete_workflow_version(self, project_name: str, workflow_filename: str, 
                              version_filename: str, confirm: bool = False) -> bool:
        """
        Delete a specific workflow version.
        
        Args:
            project_name: Name of the project
            workflow_filename: Name of the main workflow file
            version_filename: Name of the version file to delete
            confirm: Confirmation flag to prevent accidental deletion
            
        Returns:
            True if deletion was successful
        """
        if not confirm:
            raise ValueError("Version deletion requires explicit confirmation")
        
        try:
            if not self.project_manager.project_exists(project_name):
                raise ValueError(f"Project '{project_name}' does not exist")
            
            project_path = self.project_manager.projects_root / project_name
            version_path = project_path / version_filename
            
            if not version_path.exists():
                raise ValueError(f"Version file '{version_filename}' not found")
            
            # Verify it's actually a backup file
            if not self.project_manager._is_backup_file(version_filename):
                raise ValueError(f"File '{version_filename}' is not a valid backup file")
            
            # Delete the version file
            version_path.unlink()
            
            self.logger.info(f"Successfully deleted version '{version_filename}' for workflow '{workflow_filename}'", extra={'project_name': project_name, 'operation': 'delete_workflow_version'})
            return True
            
        except Exception as e:
            error_msg = f"Failed to delete version {version_filename}: {str(e)}"
            self.logger.error(error_msg, extra={'project_name': project_name, 'operation': 'delete_workflow_version'})
            if isinstance(e, ValueError):
                raise
            else:
                raise RuntimeError(error_msg)
    
    def copy_workflow(self, source_project: str, source_workflow: str,
                     dest_project: str, dest_workflow: str, 
                     overwrite: bool = False) -> bool:
        """
        Copy a workflow from one project to another.
        
        Args:
            source_project: Source project name
            source_workflow: Source workflow filename
            dest_project: Destination project name
            dest_workflow: Destination workflow filename
            overwrite: Whether to overwrite if destination exists
            
        Returns:
            True if copy was successful
        """
        try:
            # Read source workflow
            workflow_data = self.read_workflow_file(source_project, source_workflow)
            
            # Check if destination exists
            if not overwrite:
                try:
                    self.read_workflow_file(dest_project, dest_workflow)
                    raise ValueError(f"Destination workflow '{dest_workflow}' already exists in project '{dest_project}'")
                except ValueError as e:
                    if "already exists" in str(e):
                        raise
                    # File doesn't exist, which is what we want
                    pass
            
            # Update workflow name if it exists in the data
            if 'name' in workflow_data:
                workflow_data['name'] = dest_workflow.replace('.json', '')
            
            # Write to destination
            self.write_workflow_file(dest_project, dest_workflow, workflow_data, create_backup=overwrite)
            
            self.logger.info(f"Successfully copied workflow from {source_project}/{source_workflow} to {dest_project}/{dest_workflow}", extra={'project_name': dest_project, 'operation': 'copy_workflow'})
            return True
            
        except Exception as e:
            error_msg = f"Failed to copy workflow: {str(e)}"
            self.logger.error(error_msg, extra={'project_name': dest_project, 'operation': 'copy_workflow'})
            if isinstance(e, ValueError):
                raise
            else:
                raise RuntimeError(error_msg)
    
    def move_workflow(self, source_project: str, source_workflow: str,
                     dest_project: str, dest_workflow: str,
                     overwrite: bool = False) -> bool:
        """
        Move a workflow from one project to another.
        
        Args:
            source_project: Source project name
            source_workflow: Source workflow filename
            dest_project: Destination project name
            dest_workflow: Destination workflow filename
            overwrite: Whether to overwrite if destination exists
            
        Returns:
            True if move was successful
        """
        try:
            # Copy to destination
            self.copy_workflow(source_project, source_workflow, dest_project, dest_workflow, overwrite)
            
            # Delete source
            self.delete_workflow_file(source_project, source_workflow, confirm=True)
            
            self.logger.info(f"Successfully moved workflow from {source_project}/{source_workflow} to {dest_project}/{dest_workflow}", extra={'project_name': dest_project, 'operation': 'move_workflow'})
            return True
            
        except Exception as e:
            error_msg = f"Failed to move workflow: {str(e)}"
            self.logger.error(error_msg, extra={'project_name': dest_project, 'operation': 'move_workflow'})
            if isinstance(e, ValueError):
                raise
            else:
                raise RuntimeError(error_msg)
    
    def rename_workflow(self, project_name: str, old_filename: str, new_filename: str) -> bool:
        """
        Rename a workflow file within a project.
        
        Args:
            project_name: Name of the project
            old_filename: Current workflow filename
            new_filename: New workflow filename
            
        Returns:
            True if rename was successful
        """
        try:
            if not self.project_manager.project_exists(project_name):
                raise ValueError(f"Project '{project_name}' does not exist")
            
            project_path = self.project_manager.projects_root / project_name
            old_path = project_path / old_filename
            new_path = project_path / new_filename
            
            if not old_path.exists():
                raise ValueError(f"Workflow file '{old_filename}' not found")
            
            if new_path.exists():
                raise ValueError(f"Destination file '{new_filename}' already exists")
            
            # Rename the file
            old_path.rename(new_path)
            
            # Update workflow name in the JSON if it contains a name field
            try:
                workflow_data = self.read_workflow_file(project_name, new_filename)
                if 'name' in workflow_data:
                    workflow_data['name'] = new_filename.replace('.json', '')
                    self.write_workflow_file(project_name, new_filename, workflow_data, create_backup=False)
            except Exception as e:
                self.logger.warning(f"Failed to update workflow name in JSON: {str(e)}", extra={'project_name': project_name, 'operation': 'rename_workflow'})
            
            # Refresh project cache
            self.project_manager._refresh_project_cache()
            
            self.logger.info(f"Successfully renamed workflow from {old_filename} to {new_filename}", extra={'project_name': project_name, 'operation': 'rename_workflow'})
            return True
            
        except Exception as e:
            error_msg = f"Failed to rename workflow '{old_filename}' to '{new_filename}': {str(e)}"
            self.logger.error(error_msg, extra={'project_name': project_name, 'operation': 'rename_workflow'})
            if isinstance(e, ValueError):
                raise
            else:
                raise RuntimeError(error_msg)
    
    def delete_workflow_file(self, project_name: str, workflow_filename: str, 
                           confirm: bool = False, keep_backups: bool = True) -> bool:
        """
        Delete a workflow file with optional backup preservation.
        
        Args:
            project_name: Name of the project
            workflow_filename: Name of the workflow file to delete
            confirm: Confirmation flag to prevent accidental deletion
            keep_backups: Whether to keep backup files
            
        Returns:
            True if deletion was successful
        """
        if not confirm:
            raise ValueError("Workflow deletion requires explicit confirmation")
        
        try:
            if not self.project_manager.project_exists(project_name):
                raise ValueError(f"Project '{project_name}' does not exist")
            
            project_path = self.project_manager.projects_root / project_name
            workflow_path = project_path / workflow_filename
            
            if not workflow_path.exists():
                self.logger.warning(f"Workflow file {workflow_filename} does not exist", extra={'project_name': project_name, 'operation': 'delete_workflow_file'})
                return False
            
            # Delete the main workflow file
            workflow_path.unlink()
            
            # Optionally delete backup files
            if not keep_backups:
                versions = self.list_workflow_versions(project_name, workflow_filename)
                for version_file in versions:
                    version_path = project_path / version_file
                    try:
                        version_path.unlink()
                        self.logger.info(f"Deleted backup: {version_file}", extra={'project_name': project_name, 'operation': 'delete_workflow_file'})
                    except Exception as e:
                        self.logger.warning(f"Failed to delete backup {version_file}: {str(e)}", extra={'project_name': project_name, 'operation': 'delete_workflow_file'})
            
            # Refresh project cache
            self.project_manager._refresh_project_cache()
            
            self.logger.info(f"Successfully deleted workflow {workflow_filename} from project {project_name}", extra={'project_name': project_name, 'operation': 'delete_workflow_file'})
            return True
            
        except Exception as e:
            error_msg = f"Failed to delete workflow '{workflow_filename}': {str(e)}"
            self.logger.error(error_msg, extra={'project_name': project_name, 'operation': 'delete_workflow_file'})
            if isinstance(e, ValueError):
                raise
            else:
                raise RuntimeError(error_msg)
    
    def get_workflow_info(self, project_name: str, workflow_filename: str) -> WorkflowInfo:
        """
        Get detailed information about a workflow file.
        
        Args:
            project_name: Name of the project
            workflow_filename: Name of the workflow file
            
        Returns:
            WorkflowInfo object with detailed information
        """
        try:
            if not self.project_manager.project_exists(project_name):
                raise ValueError(f"Project '{project_name}' does not exist")
            
            project_path = self.project_manager.projects_root / project_name
            workflow_path = project_path / workflow_filename
            
            if not workflow_path.exists():
                raise ValueError(f"Workflow file '{workflow_filename}' not found")
            
            # Get file stats
            stat = workflow_path.stat()
            file_size = stat.st_size
            created_date = datetime.fromtimestamp(stat.st_ctime)
            last_modified = datetime.fromtimestamp(stat.st_mtime)
            
            # Get workflow data
            workflow_data = self.read_workflow_file(project_name, workflow_filename)
            
            # Extract workflow information
            workflow_name = workflow_data.get('name', workflow_filename.replace('.json', ''))
            description = workflow_data.get('description', '')
            node_count = len(workflow_data.get('nodes', []))
            
            # Get version count
            versions = self.list_workflow_versions(project_name, workflow_filename)
            version_count = len(versions) + 1  # +1 for current version
            
            # Extract tags if present
            tags = workflow_data.get('tags', [])
            if not isinstance(tags, list):
                tags = []
            
            return WorkflowInfo(
                name=workflow_name,
                filename=workflow_filename,
                project_name=project_name,
                description=description,
                created_date=created_date,
                last_modified=last_modified,
                version_count=version_count,
                file_size=file_size,
                node_count=node_count,
                tags=tags
            )
            
        except Exception as e:
            error_msg = f"Failed to get workflow info for '{workflow_filename}': {str(e)}"
            self.logger.error(error_msg, extra={'project_name': project_name, 'operation': 'get_workflow_info'})
            if isinstance(e, ValueError):
                raise
            else:
                raise RuntimeError(error_msg)
    
    def validate_workflow_json(self, workflow_data: Dict[str, Any]) -> List[str]:
        """
        Validate workflow JSON structure and return any issues found.
        
        Args:
            workflow_data: Dictionary containing workflow data
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        try:
            # Check required top-level fields
            required_fields = ['nodes', 'connections']
            for field in required_fields:
                if field not in workflow_data:
                    errors.append(f"Missing required field: '{field}'")
                elif not isinstance(workflow_data[field], (list, dict)):
                    errors.append(f"Field '{field}' must be a list or dict")
            
            # Validate nodes if present
            node_ids = set()
            if 'nodes' in workflow_data:
                nodes = workflow_data['nodes']
                if isinstance(nodes, list):
                    for i, node in enumerate(nodes):
                        if not isinstance(node, dict):
                            errors.append(f"Node {i} must be a dictionary")
                            continue
                        # Check for required node fields
                        node_required = ['id', 'name', 'type']
                        for field in node_required:
                            if field not in node:
                                errors.append(f"Node {i} missing required field: '{field}'")
                        node_id = node.get('id')
                        if node_id:
                            node_ids.add(node_id)
            
            # DEBUG LOGGING
            self.logger.debug(f"[VALIDATION DEBUG] Node IDs: {node_ids}")
            
            # Validate connections if present
            if 'connections' in workflow_data:
                connections = workflow_data['connections']
                if not isinstance(connections, dict):
                    errors.append("Connections must be a dictionary")
                else:
                    # Check that all connection keys are valid node IDs
                    for source_id, connection_data in connections.items():
                        if source_id not in node_ids:
                            self.logger.debug(f"[VALIDATION DEBUG] Connection key '{source_id}' is not a valid node ID. node_ids={node_ids}")
                            errors.append(f"Connection references non-existent node '{source_id}'")
                        if not isinstance(connection_data, dict):
                            errors.append(f"Invalid connection data structure for node '{source_id}'")
                            continue
                        for connection_type, targets in connection_data.items():
                            if not isinstance(targets, list):
                                errors.append(f"Invalid targets structure for node '{source_id}'")
                                continue
                            for target_list in targets:
                                if not isinstance(target_list, list):
                                    errors.append(f"Invalid target list structure for node '{source_id}'")
                                    continue
                                for target in target_list:
                                    if not isinstance(target, dict):
                                        errors.append(f"Invalid target structure for node '{source_id}'")
                                        continue
                                    target_node = target.get('node')
                                    if not target_node:
                                        errors.append(f"Missing target node in connection from '{source_id}'")
                                        continue
                                    if target_node not in node_ids:
                                        self.logger.debug(f"[VALIDATION DEBUG] Connection from '{source_id}' references non-existent target node '{target_node}'. node_ids={node_ids}")
                                        errors.append(f"Connection references non-existent node '{target_node}'")
            
            # Check for common optional fields
            optional_fields = {
                'name': str,
                'active': bool,
                'settings': dict,
                'tags': list
            }
            
            for field, expected_type in optional_fields.items():
                if field in workflow_data:
                    if not isinstance(workflow_data[field], expected_type):
                        errors.append(f"Field '{field}' should be of type {expected_type.__name__}")
            
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
        
        return errors
    
    def get_file_system_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive file system statistics.
        
        Returns:
            Dictionary with file system statistics
        """
        try:
            projects = self.project_manager.list_projects(refresh_cache=True)
            
            total_workflows = 0
            total_versions = 0
            total_file_size = 0
            largest_workflow = {'name': '', 'size': 0, 'project': ''}
            
            for project_info in projects:
                workflows = self.project_manager.list_project_workflows(project_info.name)
                total_workflows += len(workflows)
                
                for workflow_filename in workflows:
                    try:
                        workflow_info = self.get_workflow_info(project_info.name, workflow_filename)
                        total_file_size += workflow_info.file_size
                        total_versions += workflow_info.version_count
                        
                        if workflow_info.file_size > largest_workflow['size']:
                            largest_workflow = {
                                'name': workflow_filename,
                                'size': workflow_info.file_size,
                                'project': project_info.name
                            }
                    except Exception as e:
                        self.logger.warning(f"Failed to get info for {workflow_filename}: {str(e)}", extra={'project_name': project_info.name, 'operation': 'get_file_system_stats'})
                        continue
            
            stats = {
                'total_projects': len(projects),
                'total_workflows': total_workflows,
                'total_versions': total_versions,
                'total_file_size_bytes': total_file_size,
                'total_file_size_mb': round(total_file_size / (1024 * 1024), 3) if total_file_size > 0 else 0,
                'average_file_size_kb': round((total_file_size / total_workflows / 1024), 2) if total_workflows > 0 else 0,
                'largest_workflow': largest_workflow,
                'projects_root': str(self.project_manager.projects_root)
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Failed to get file system stats: {str(e)}", extra={'project_name': None, 'operation': 'get_file_system_stats'})
            return {'error': str(e)}

# Global file system utilities instance
filesystem_utils = FileSystemUtilities(project_manager) 