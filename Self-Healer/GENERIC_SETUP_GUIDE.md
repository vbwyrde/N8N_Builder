# Generic Self-Healer Setup Guide

This guide explains how to configure the Self-Healer system to work with any project, making it truly portable and reusable across different codebases.

## Overview

The Self-Healer system has been designed with a **Project Adapter** architecture that allows it to work with any project by configuring project-specific settings in a YAML configuration file. This eliminates hardcoded dependencies and makes the system truly generic.

## Key Components for Genericity

### 1. Project Adapter (`core/project_adapter.py`)
- **Purpose**: Provides a unified interface between Self-Healer and any project
- **Features**: 
  - Dynamic module loading
  - Fallback mechanisms for missing dependencies
  - Configurable path resolution
  - Generic error handling

### 2. Project Configuration (`config/project_config.yaml`)
- **Purpose**: Defines project-specific settings and structure
- **Configures**:
  - Directory structures
  - Log file locations
  - Error patterns
  - Dependencies
  - Solution templates

### 3. Generic Types (`core/generic_types.py`)
- **Purpose**: Provides project-agnostic data structures
- **Features**:
  - Generic error representations
  - Universal solution formats
  - Portable learning records

## Setting Up Self-Healer for a New Project

### Step 1: Copy Self-Healer to Your Project

```bash
# Copy the entire Self-Healer directory to your project root
cp -r /path/to/Self-Healer /your/project/root/

# Or clone as a submodule
git submodule add https://github.com/your-org/Self-Healer.git Self-Healer
```

### Step 2: Create Project Configuration

Create or customize `Self-Healer/config/project_config.yaml`:

```yaml
# Project Information
project:
  name: "YourProject"
  version: "1.0.0"
  description: "Your project description"

# Project Structure
structure:
  project_root: "../"  # Relative to Self-Healer directory
  source_directories:
    - "src"           # Your source code directories
    - "lib"
    - "app"
  documentation_directories:
    - "docs"          # Your documentation directories
    - "README.md"
  log_directories:
    - "logs"          # Your log directories
    - "var/log"

# Error Detection
error_detection:
  log_files:
    - "logs/app.log"  # Your specific log files
    - "logs/error.log"
  error_patterns:
    - pattern: "ERROR"
      severity: "error"
      category: "general"
    - pattern: "FATAL"
      severity: "critical"
      category: "system"

# Dependencies (optional - will use fallbacks if not available)
dependencies:
  error_handler:
    enabled: true
    module_path: "your_project.error_handler"  # Your error handler module
    class_name: "YourErrorHandler"
    fallback_to_builtin: true
  
  logging:
    enabled: true
    module_path: "your_project.logging"
    logger_function: "get_logger"
    fallback_to_builtin: true
```

### Step 3: Install Dependencies

```bash
# Install Self-Healer dependencies
pip install watchdog pyyaml psutil fastapi uvicorn websockets

# Or add to your requirements.txt
echo "watchdog>=2.1.0" >> requirements.txt
echo "pyyaml>=6.0" >> requirements.txt
echo "psutil>=5.8.0" >> requirements.txt
echo "fastapi>=0.68.0" >> requirements.txt
echo "uvicorn>=0.15.0" >> requirements.txt
echo "websockets>=10.0" >> requirements.txt
```

### Step 4: Initialize Self-Healer in Your Application

```python
# In your main application file
import asyncio
from pathlib import Path
from Self_Healer.core.healer_manager import GenericSelfHealerManager

async def main():
    # Initialize Self-Healer with your project configuration
    project_config_path = Path("Self-Healer/config/project_config.yaml")
    healer = GenericSelfHealerManager(project_config_path=project_config_path)
    
    try:
        # Start the self-healing system
        await healer.start()
        
        # Your application code here
        # ...
        
    finally:
        # Ensure proper shutdown
        await healer.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration Examples for Different Project Types

### Python Web Application (Flask/Django)

```yaml
project:
  name: "MyWebApp"
  version: "2.1.0"
  description: "Python web application"

structure:
  project_root: "../"
  source_directories:
    - "app"
    - "models"
    - "views"
    - "controllers"
  log_directories:
    - "logs"
    - "var/log/app"

error_detection:
  log_files:
    - "logs/app.log"
    - "logs/django.log"
    - "logs/gunicorn.log"
  error_patterns:
    - pattern: "ERROR"
      severity: "error"
      category: "application"
    - pattern: "500 Internal Server Error"
      severity: "critical"
      category: "web"

dependencies:
  error_handler:
    enabled: true
    module_path: "app.utils.error_handler"
    class_name: "AppErrorHandler"
  logging:
    enabled: true
    module_path: "app.utils.logging"
    logger_function: "get_logger"
```

### Node.js Application

```yaml
project:
  name: "NodeApp"
  version: "1.5.0"
  description: "Node.js application"

structure:
  project_root: "../"
  source_directories:
    - "src"
    - "lib"
    - "routes"
  log_directories:
    - "logs"

error_detection:
  log_files:
    - "logs/app.log"
    - "logs/error.log"
    - "logs/pm2.log"
  error_patterns:
    - pattern: "Error:"
      severity: "error"
      category: "javascript"
    - pattern: "UnhandledPromiseRejectionWarning"
      severity: "critical"
      category: "async"

# No dependencies - will use built-in fallbacks
dependencies: {}

custom_commands:
  restart_service:
    command: "pm2 restart app"
    timeout: 30
  run_tests:
    command: "npm test"
    working_directory: "{project_root}"
    timeout: 300
```

### Microservice Architecture

```yaml
project:
  name: "MicroserviceCluster"
  version: "3.0.0"
  description: "Microservice cluster"

structure:
  project_root: "../"
  source_directories:
    - "services/*/src"
    - "shared/lib"
  log_directories:
    - "logs"
    - "services/*/logs"

error_detection:
  log_files:
    - "logs/*.log"
    - "services/*/logs/*.log"
  error_patterns:
    - pattern: "SERVICE_ERROR"
      severity: "error"
      category: "service"
    - pattern: "CIRCUIT_BREAKER_OPEN"
      severity: "critical"
      category: "resilience"

solution_templates:
  patterns:
    service_down:
      title: "Restart Failed Service"
      applicable_errors: ["service_error", "connection_refused"]
      steps:
        - action: "check_service_health"
        - action: "restart_service"
        - action: "verify_service_up"
      confidence: 0.9
```

## Advanced Configuration Options

### Custom Error Patterns

```yaml
error_detection:
  error_patterns:
    - pattern: "OutOfMemoryError"
      severity: "critical"
      category: "memory"
      keywords: ["memory", "heap", "allocation"]
    - pattern: "ConnectionTimeout"
      severity: "error"
      category: "network"
      keywords: ["timeout", "connection", "network"]
    - pattern: "ValidationError"
      severity: "warning"
      category: "data"
      keywords: ["validation", "invalid", "format"]
```

### Custom Solution Templates

```yaml
solution_templates:
  patterns:
    memory_leak:
      title: "Address Memory Leak"
      applicable_errors: ["memory", "heap", "oom"]
      steps:
        - action: "analyze_memory_usage"
        - action: "identify_leak_source"
        - action: "restart_service"
        - action: "monitor_memory"
      confidence: 0.7
      risk_level: "medium"
    
    database_connection_lost:
      title: "Restore Database Connection"
      applicable_errors: ["database", "connection", "lost"]
      steps:
        - action: "check_database_status"
        - action: "restart_connection_pool"
        - action: "verify_connectivity"
      confidence: 0.8
      risk_level: "low"
```

### Integration Hooks

```yaml
integration_hooks:
  pre_healing:
    - hook: "notify_team"
      enabled: true
      config:
        webhook_url: "https://hooks.slack.com/your-webhook"
    - hook: "create_incident"
      enabled: false
  
  post_healing:
    - hook: "update_monitoring"
      enabled: true
    - hook: "generate_report"
      enabled: true
```

## Testing Your Configuration

### 1. Validate Configuration

```python
# Test script to validate your configuration
from Self_Healer.core.project_adapter import ProjectAdapter

def test_configuration():
    try:
        adapter = ProjectAdapter()
        project_info = adapter.get_project_info()
        print(f"Project: {project_info['name']}")
        print(f"Root: {project_info['root']}")
        print(f"Dependencies loaded: {project_info['dependencies_loaded']}")
        
        # Test log file detection
        log_files = adapter.get_log_files()
        print(f"Log files found: {len(log_files)}")
        
        # Test error handler
        error_handler = adapter.get_error_handler()
        print(f"Error handler: {'Available' if error_handler else 'Using fallback'}")
        
        print("Configuration is valid!")
        
    except Exception as e:
        print(f"Configuration error: {e}")

if __name__ == "__main__":
    test_configuration()
```

### 2. Run Self-Healer in Test Mode

```python
# Test the complete Self-Healer system
import asyncio
from Self_Healer.core.healer_manager import GenericSelfHealerManager

async def test_self_healer():
    healer = GenericSelfHealerManager()
    
    try:
        await healer.start()
        
        # Wait for initialization
        await asyncio.sleep(5)
        
        # Check status
        status = await healer.get_status()
        print(f"Self-Healer Status: {status['status']}")
        print(f"Is Running: {status['is_running']}")
        
        # Test for 30 seconds
        await asyncio.sleep(30)
        
    finally:
        await healer.stop()

if __name__ == "__main__":
    asyncio.run(test_self_healer())
```

## Migration from Project-Specific to Generic

If you have an existing Self-Healer installation that's project-specific:

### 1. Backup Current Installation

```bash
cp -r Self-Healer Self-Healer-backup
```

### 2. Update to Generic Version

```bash
# Replace with generic version
git pull origin generic-version
# or
cp -r /path/to/generic/Self-Healer/* Self-Healer/
```

### 3. Create Project Configuration

Extract your project-specific settings into `project_config.yaml`:

```python
# Migration helper script
def migrate_to_generic():
    # Extract hardcoded paths from old version
    old_paths = {
        'logs': 'logs/errors.log',
        'docs': 'Documentation',
        'source': 'n8n_builder'
    }
    
    # Create new project_config.yaml
    config = {
        'project': {
            'name': 'YourProject',
            'version': '1.0.0'
        },
        'structure': {
            'project_root': '../',
            'source_directories': [old_paths['source']],
            'documentation_directories': [old_paths['docs']],
            'log_directories': ['logs']
        },
        'error_detection': {
            'log_files': [old_paths['logs']]
        }
    }
    
    import yaml
    with open('Self-Healer/config/project_config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
```

## Benefits of Generic Self-Healer

1. **Portability**: Works with any project structure
2. **Flexibility**: Configurable for different languages and frameworks
3. **Maintainability**: Single codebase for all projects
4. **Scalability**: Easy to add new project types
5. **Robustness**: Fallback mechanisms for missing dependencies
6. **Consistency**: Same healing capabilities across all projects

## Troubleshooting

### Common Issues

1. **Configuration not found**: Ensure `project_config.yaml` exists and is valid YAML
2. **Import errors**: Check that module paths in dependencies are correct
3. **Permission errors**: Ensure Self-Healer has read/write access to log and backup directories
4. **Log files not found**: Verify log file paths in configuration

### Debug Mode

Enable debug logging to troubleshoot issues:

```yaml
logging:
  level: "DEBUG"
```

This generic approach makes Self-Healer truly reusable across any project while maintaining all its powerful self-healing capabilities!
