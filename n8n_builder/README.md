# N8N_Builder Core Module

This is the core module of N8N_Builder, containing the main application logic for AI-powered workflow automation.

## 🏗️ Module Structure

### Core Application Files
- **`app.py`**: FastAPI application server and REST API endpoints
- **`n8n_builder.py`**: Main workflow generation logic and AI integration
- **`config.py`**: Configuration management and environment settings
- **`cli.py`**: Command-line interface for N8N_Builder

### AI and Processing
- **`enhanced_prompt_builder.py`**: Advanced prompt engineering for AI models
- **`code_generation_patterns.py`**: Patterns and templates for code generation
- **`performance_optimizer.py`**: Performance optimization utilities
- **`retry_manager.py`**: Intelligent retry logic for API calls

### Data Management
- **`knowledge_cache.py`**: Caching system for research and knowledge
- **`research_formatter.py`**: Format and structure research data
- **`research_validator.py`**: Validate research quality and accuracy
- **`mcp_research_tool.py`**: MCP (Model Context Protocol) research integration

### Validation and Quality
- **`validators.py`**: Input/output validation for workflows
- **`workflow_differ.py`**: Compare and analyze workflow differences
- **`error_handler.py`**: Comprehensive error handling and recovery

### System Management
- **`logging_config.py`**: Logging configuration and management
- **`log_rotation_manager.py`**: Automatic log rotation and cleanup
- **`project_manager.py`**: Project lifecycle management
- **`optional_integrations.py`**: Optional feature integration management

### Advanced Features
- **`agui_server.py`**: AG-UI protocol server implementation
- **`mcp_database_tool.py`**: Database integration via MCP protocol

## 🚀 Key Features

### AI Integration
- **Local LLM Support**: Integration with local AI models via LM Studio
- **Prompt Engineering**: Advanced prompt optimization for workflow generation
- **Context Management**: Intelligent context handling for complex workflows

### Workflow Generation
- **Natural Language Processing**: Convert plain English to n8n workflows
- **Template System**: Reusable workflow patterns and templates
- **Validation**: Comprehensive workflow validation and testing

### Performance & Reliability
- **Caching**: Intelligent caching for improved performance
- **Error Recovery**: Robust error handling and retry mechanisms
- **Logging**: Comprehensive logging and monitoring

### Integration Capabilities
- **REST API**: Full REST API for external integrations
- **AG-UI Protocol**: Advanced agent interaction protocol
- **Database Support**: Multiple database backend support
- **Docker Ready**: Container-friendly architecture

## 🔧 Configuration

The module uses configuration from:
- **Environment files**: `.env`, `.env.local`
- **YAML configuration**: `config_public.yaml`
- **Runtime parameters**: Command-line arguments and API parameters

## 📊 Usage Examples

### Basic Workflow Generation
```python
from n8n_builder import N8NBuilder

builder = N8NBuilder()
workflow = builder.generate_workflow("Send daily email reports")
```

### API Server
```python
from n8n_builder.app import app
import uvicorn

uvicorn.run(app, host="0.0.0.0", port=8002)
```

### CLI Usage
```bash
python -m n8n_builder.cli generate "Create a workflow for data backup"
```

## 🧪 Testing

The module includes comprehensive testing in the `../tests/` directory with:
- Unit tests for individual components
- Integration tests for complete workflows
- Performance benchmarks
- API endpoint testing

## 🔗 Dependencies

Core dependencies include:
- **FastAPI**: Web framework for API server
- **Pydantic**: Data validation and settings management
- **Requests**: HTTP client for external API calls
- **PyYAML**: YAML configuration file support
