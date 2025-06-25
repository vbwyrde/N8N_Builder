"""
Project Adapter - Generic interface for integrating Self-Healer with any project.

This module provides a configurable adapter that allows Self-Healer to work
with different project structures, dependencies, and conventions.
"""

import os
import sys
import importlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
import yaml
import glob
from dataclasses import dataclass, field


@dataclass
class ProjectConfig:
    """Configuration for a specific project."""
    name: str
    version: str
    description: str
    project_root: Path
    source_directories: List[str] = field(default_factory=list)
    documentation_directories: List[str] = field(default_factory=list)
    test_directories: List[str] = field(default_factory=list)
    config_directories: List[str] = field(default_factory=list)
    log_directories: List[str] = field(default_factory=list)
    backup_directory: str = "Self-Healer/backups"
    learning_data_directory: str = "Self-Healer/learning_data"


@dataclass
class DependencyConfig:
    """Configuration for external dependencies."""
    enabled: bool
    module_path: Optional[str] = None
    class_name: Optional[str] = None
    function_name: Optional[str] = None
    instance_name: Optional[str] = None
    fallback_to_builtin: bool = True
    fallback_config: Dict[str, Any] = field(default_factory=dict)


class ProjectAdapter:
    """
    Generic adapter for integrating Self-Healer with any project.
    
    This adapter reads project-specific configuration and provides a unified
    interface for Self-Healer components to interact with the host project.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the project adapter."""
        self.logger = self._setup_logging()
        
        # Load configuration
        self.config_path = config_path or Path(__file__).parent.parent / "config" / "project_config.yaml"
        self.config = self._load_config()
        
        # Project configuration
        self.project_config = self._parse_project_config()
        
        # Dependency configurations
        self.dependencies = self._parse_dependencies()
        
        # Cached instances
        self._cached_instances: Dict[str, Any] = {}
        
        # File type mappings
        self.file_types = self.config.get('file_types', {})
        
        # Solution templates
        self.solution_templates = self.config.get('solution_templates', {})
        
        self.logger.info(f"Project Adapter initialized for: {self.project_config.name}")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the adapter."""
        logger = logging.getLogger('self_healer.project_adapter')
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _load_config(self) -> Dict[str, Any]:
        """Load project configuration from YAML file."""
        try:
            if not self.config_path.exists():
                self.logger.warning(f"Config file not found: {self.config_path}")
                return self._get_default_config()
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            self.logger.info(f"Loaded configuration from: {self.config_path}")
            return config
            
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for generic projects."""
        return {
            'project': {
                'name': 'Generic_Project',
                'version': '1.0.0',
                'description': 'Generic project configuration'
            },
            'structure': {
                'project_root': '../',
                'source_directories': ['src', 'lib'],
                'documentation_directories': ['docs', 'README.md'],
                'test_directories': ['tests'],
                'log_directories': ['logs'],
                'backup_directory': 'Self-Healer/backups',
                'learning_data_directory': 'Self-Healer/learning_data'
            },
            'error_detection': {
                'log_files': ['logs/*.log'],
                'error_patterns': [
                    {'pattern': 'ERROR', 'severity': 'error', 'category': 'general'},
                    {'pattern': 'CRITICAL', 'severity': 'critical', 'category': 'system'}
                ]
            },
            'dependencies': {}
        }
    
    def _parse_project_config(self) -> ProjectConfig:
        """Parse project structure configuration."""
        project_info = self.config.get('project', {})
        structure = self.config.get('structure', {})
        
        # Resolve project root
        project_root_str = structure.get('project_root', '../')
        if os.path.isabs(project_root_str):
            project_root = Path(project_root_str)
        else:
            project_root = (Path(__file__).parent.parent / project_root_str).resolve()
        
        return ProjectConfig(
            name=project_info.get('name', 'Unknown_Project'),
            version=project_info.get('version', '1.0.0'),
            description=project_info.get('description', ''),
            project_root=project_root,
            source_directories=structure.get('source_directories', []),
            documentation_directories=structure.get('documentation_directories', []),
            test_directories=structure.get('test_directories', []),
            config_directories=structure.get('config_directories', []),
            log_directories=structure.get('log_directories', []),
            backup_directory=structure.get('backup_directory', 'Self-Healer/backups'),
            learning_data_directory=structure.get('learning_data_directory', 'Self-Healer/learning_data')
        )
    
    def _parse_dependencies(self) -> Dict[str, DependencyConfig]:
        """Parse dependency configurations."""
        dependencies = {}
        deps_config = self.config.get('dependencies', {})
        
        for dep_name, dep_config in deps_config.items():
            dependencies[dep_name] = DependencyConfig(
                enabled=dep_config.get('enabled', True),
                module_path=dep_config.get('module_path'),
                class_name=dep_config.get('class_name'),
                function_name=dep_config.get('logger_function'),
                instance_name=dep_config.get('manager_instance'),
                fallback_to_builtin=dep_config.get('fallback_to_builtin', True),
                fallback_config=dep_config.get('fallback_config', {})
            )
        
        return dependencies
    
    def get_project_root(self) -> Path:
        """Get the project root directory."""
        return self.project_config.project_root
    
    def get_log_files(self) -> List[Path]:
        """Get list of log files to monitor."""
        log_files = []
        error_detection = self.config.get('error_detection', {})
        log_file_patterns = error_detection.get('log_files', [])
        
        for pattern in log_file_patterns:
            if os.path.isabs(pattern):
                file_path = Path(pattern)
            else:
                file_path = self.project_config.project_root / pattern
            
            # Handle glob patterns
            if '*' in str(file_path):
                matching_files = glob.glob(str(file_path))
                log_files.extend([Path(f) for f in matching_files])
            else:
                if file_path.exists():
                    log_files.append(file_path)
        
        return log_files
    
    def get_source_directories(self) -> List[Path]:
        """Get list of source code directories."""
        directories = []
        for dir_name in self.project_config.source_directories:
            dir_path = self.project_config.project_root / dir_name
            if dir_path.exists():
                directories.append(dir_path)
        return directories
    
    def get_documentation_directories(self) -> List[Path]:
        """Get list of documentation directories."""
        directories = []
        for dir_pattern in self.project_config.documentation_directories:
            if dir_pattern.endswith('.md'):
                # Handle individual markdown files
                file_path = self.project_config.project_root / dir_pattern
                if file_path.exists():
                    directories.append(file_path.parent)
            else:
                dir_path = self.project_config.project_root / dir_pattern
                if dir_path.exists():
                    directories.append(dir_path)
        return directories
    
    def get_backup_directory(self) -> Path:
        """Get backup directory path."""
        backup_dir = self.project_config.project_root / self.project_config.backup_directory
        backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir
    
    def get_learning_data_directory(self) -> Path:
        """Get learning data directory path."""
        learning_dir = self.project_config.project_root / self.project_config.learning_data_directory
        learning_dir.mkdir(parents=True, exist_ok=True)
        return learning_dir
    
    def get_error_handler(self) -> Optional[Any]:
        """Get the project's error handler instance."""
        return self._get_dependency_instance('error_handler')
    
    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger instance using project's logging configuration."""
        logger_func = self._get_dependency_instance('logging')
        
        if logger_func and callable(logger_func):
            try:
                return logger_func(name)
            except Exception as e:
                self.logger.warning(f"Failed to use project logger: {e}")
        
        # Fallback to standard logging
        return logging.getLogger(name)
    
    def get_project_manager(self) -> Optional[Any]:
        """Get the project's project manager instance."""
        return self._get_dependency_instance('project_manager')
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration."""
        llm_config = self._get_dependency_instance('llm')
        
        if llm_config:
            return {
                'endpoint': getattr(llm_config, 'endpoint', 'http://localhost:1234/v1'),
                'model': getattr(llm_config, 'model', 'mimo-vl-7b-rl'),
                'api_key': getattr(llm_config, 'api_key', None)
            }
        
        # Fallback configuration
        llm_dep = self.dependencies.get('llm', DependencyConfig(enabled=False))
        return {
            'endpoint': llm_dep.fallback_config.get('endpoint', 'http://localhost:1234/v1'),
            'model': llm_dep.fallback_config.get('model', 'mimo-vl-7b-rl'),
            'api_key': None
        }
    
    def _get_dependency_instance(self, dep_name: str) -> Optional[Any]:
        """Get an instance of a dependency."""
        if dep_name in self._cached_instances:
            return self._cached_instances[dep_name]
        
        dep_config = self.dependencies.get(dep_name)
        if not dep_config or not dep_config.enabled:
            return None
        
        try:
            # Add project root to Python path
            project_root_str = str(self.project_config.project_root)
            if project_root_str not in sys.path:
                sys.path.insert(0, project_root_str)
            
            # Import the module
            module = importlib.import_module(dep_config.module_path)
            
            # Get the specific class, function, or instance
            if dep_config.class_name:
                cls = getattr(module, dep_config.class_name)
                instance = cls()
            elif dep_config.function_name:
                instance = getattr(module, dep_config.function_name)
            elif dep_config.instance_name:
                instance = getattr(module, dep_config.instance_name)
            else:
                instance = module
            
            self._cached_instances[dep_name] = instance
            self.logger.info(f"Successfully loaded dependency: {dep_name}")
            return instance
            
        except Exception as e:
            self.logger.warning(f"Failed to load dependency {dep_name}: {e}")
            
            if dep_config.fallback_to_builtin:
                self.logger.info(f"Using fallback for dependency: {dep_name}")
                return self._get_fallback_instance(dep_name)
            
            return None
    
    def _get_fallback_instance(self, dep_name: str) -> Optional[Any]:
        """Get a fallback instance for a dependency."""
        if dep_name == 'logging':
            return logging.getLogger
        elif dep_name == 'error_handler':
            return self._create_fallback_error_handler()
        # Add more fallbacks as needed
        return None
    
    def _create_fallback_error_handler(self) -> Any:
        """Create a fallback error handler."""
        class FallbackErrorHandler:
            def categorize_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
                return {
                    'category': 'general',
                    'severity': 'error',
                    'title': 'Error Detected',
                    'message': str(error),
                    'user_guidance': 'An error occurred. Please check the logs for details.',
                    'technical_details': str(error),
                    'context': context or {}
                }
        
        return FallbackErrorHandler()
    
    def get_error_patterns(self) -> List[Dict[str, Any]]:
        """Get error detection patterns."""
        error_detection = self.config.get('error_detection', {})
        return error_detection.get('error_patterns', [])
    
    def get_ignore_patterns(self) -> List[str]:
        """Get patterns to ignore during error detection."""
        error_detection = self.config.get('error_detection', {})
        return error_detection.get('ignore_patterns', [])
    
    def get_solution_templates(self) -> Dict[str, Any]:
        """Get solution templates configuration."""
        return self.solution_templates.get('patterns', {})
    
    def is_critical_file(self, file_path: Union[str, Path]) -> bool:
        """Check if a file is considered critical."""
        file_types = self.config.get('file_types', {})
        critical_files = file_types.get('critical_files', [])
        
        file_name = Path(file_path).name
        return any(
            file_name == critical or 
            (critical.startswith('*') and file_name.endswith(critical[1:]))
            for critical in critical_files
        )
    
    def get_custom_commands(self) -> Dict[str, Dict[str, Any]]:
        """Get custom commands configuration."""
        return self.config.get('custom_commands', {})
    
    def get_validation_rules(self) -> Dict[str, Any]:
        """Get validation rules."""
        return self.config.get('validation', {})
    
    def get_project_info(self) -> Dict[str, Any]:
        """Get project information summary."""
        return {
            'name': self.project_config.name,
            'version': self.project_config.version,
            'description': self.project_config.description,
            'root': str(self.project_config.project_root),
            'source_dirs': len(self.project_config.source_directories),
            'doc_dirs': len(self.project_config.documentation_directories),
            'dependencies_loaded': len(self._cached_instances),
            'config_path': str(self.config_path)
        }
