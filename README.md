# N8N Workflow Builder

A Python-based tool for generating n8n workflows using natural language descriptions. This tool uses a local LLM (Mimo VL 7B) to convert plain English descriptions into valid n8n workflow JSON structures.

## Features

- **Natural Language Processing** - Convert plain English to n8n workflows
- **Real-time Workflow Validation** - Comprehensive validation with intelligent error handling
- **Workflow Modification** - Modify existing workflows based on feedback and requirements
- **Best Practices Checking** - Automated workflow optimization suggestions
- **Command-line Interface** - Full CLI support for automation
- **REST API with Streaming** - Server-sent events for real-time updates
- **Feedback Tracking** - Learning system with iteration history
- **Agent-Based Architecture** - Extensible system for custom workflow processing
- **Performance Optimization** - Intelligent handling of large workflows
- **Enhanced Error Recovery** - Robust retry mechanisms with fallback strategies

## Prerequisites

- Python 3.8 or higher
- Local LLM server running Mimo VL 7B (or compatible reasoning model)
- n8n instance for testing generated workflows

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vbwyrde/N8N_Builder.git
cd N8N_Builder
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Create .env file or set environment variables

# LLM Configuration
MIMO_ENDPOINT=http://localhost:1234/v1/chat/completions
MIMO_MODEL=mimo-vl-7b
MIMO_TEMPERATURE=0.7
MIMO_MAX_TOKENS=4000
MIMO_IS_LOCAL=true

# For external LLM services (set MIMO_IS_LOCAL=false)
# MIMO_API_KEY=your_api_key_here

# Application Settings
API_HOST=localhost
API_PORT=8000
DEBUG_MODE=true
LOG_LEVEL=INFO
```

## Usage

### Command Line Interface

1. Start the API server:
```bash
python -m n8n_builder.cli serve
```

2. Generate a workflow:
```bash
python -m n8n_builder.cli generate "Create a workflow that sends an email when a new file is uploaded" -o workflow.json
```

3. Modify an existing workflow:
```bash
python -m n8n_builder.cli modify existing_workflow.json "Add an email notification step" -o modified_workflow.json
```

### Web Interface

1. Start the server:
```bash
python -m n8n_builder.cli serve
```

2. Open your browser to `http://localhost:8000`

3. Use the web interface to:
   - Generate new workflows from descriptions
   - Modify existing workflows
   - View workflow validation results
   - Track iteration history

### API Usage

#### Generate New Workflow
```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"description": "Create a workflow that sends an email when a new file is uploaded"}'
```

#### Modify Existing Workflow
```bash
curl -X POST "http://localhost:8000/modify" \
     -H "Content-Type: application/json" \
     -d '{
       "existing_workflow": "...",
       "modification_description": "Add email notification",
       "workflow_id": "my-workflow"
     }'
```

#### Check System Health
```bash
curl "http://localhost:8000/health"
```

## Project Structure

```
N8N_Builder/
├── n8n_builder/
│   ├── __init__.py
│   ├── app.py                    # FastAPI application with streaming
│   ├── n8n_builder.py           # Core workflow generation engine
│   ├── config.py                # Configuration management
│   ├── validators.py            # Enhanced workflow validation
│   ├── cli.py                   # Command-line interface
│   ├── error_handler.py         # Comprehensive error handling
│   ├── retry_manager.py         # Intelligent retry logic
│   ├── performance_optimizer.py # Performance optimization
│   ├── workflow_differ.py       # Workflow comparison and diffing
│   ├── project_manager.py       # Project and workflow management
│   └── code_generation_patterns.py
├── agents/
│   ├── base_agent.py            # Agent architecture foundation
│   └── ...                     # Extensible agent implementations
├── static/
│   └── index.html              # Web interface
├── logs/                       # Comprehensive logging
├── tests/                      # Test suite
├── Documentation/              # Detailed documentation
├── requirements.txt
├── setup.py
└── README.md
```

## Key Components

### Core Engine (`n8n_builder.py`)
- **Workflow Generation** - AI-powered workflow creation
- **Workflow Modification** - Intelligent workflow updates
- **Validation System** - Multi-layer validation with smart error handling
- **LLM Integration** - Robust handling of reasoning models

### Enhanced Features
- **Agent Architecture** - Extensible processing agents
- **Performance Optimization** - Handles large workflows efficiently  
- **Error Recovery** - Intelligent retry with fallback strategies
- **Workflow Diffing** - Compare and track workflow changes
- **Project Management** - Organize workflows by project

## Development

### Adding New Features

1. **Custom Agents**
   ```python
   from agents.base_agent import BaseAgent, AgentResult
   
   class CustomAgent(BaseAgent):
       async def process(self, request):
           # Your custom logic
           return AgentResult(success=True, data=result)
   ```

2. **New Workflow Patterns**
   - Add patterns in `code_generation_patterns.py`
   - Update validation rules in `validators.py`

3. **API Endpoints**
   - Extend `app.py` with new endpoints
   - Update CLI commands in `cli.py`

### Testing

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=n8n_builder

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
```

### Debugging

- **Logs Location**: `logs/` directory with separate files for different components
- **Debug Mode**: Set `LOG_LEVEL=DEBUG` for detailed logging
- **Health Check**: Use `/health` endpoint to check system status
- **Validation Details**: Check `logs/n8n_builder.validation.log` for validation issues

## Configuration

### Environment Variables

```bash
# LLM Settings
MIMO_ENDPOINT=http://localhost:1234/v1/chat/completions
MIMO_MODEL=mimo-vl-7b
MIMO_TEMPERATURE=0.7
MIMO_MAX_TOKENS=4000
MIMO_IS_LOCAL=true
MIMO_TIMEOUT=30

# Application Settings  
API_HOST=localhost
API_PORT=8000
DEBUG_MODE=true
LOG_LEVEL=INFO

# Agent Configuration
MAX_CONCURRENT_AGENTS=5
AGENT_TIMEOUT=300
ENABLE_MONITORING=true
```

### Advanced Configuration

See `DOCUMENTATION.md` for detailed configuration options including:
- Custom agent development
- Performance tuning
- Security settings
- Monitoring and analytics

## Troubleshooting

### Common Issues

1. **LLM Connection Issues**
   - Check if your local LLM server is running
   - Verify `MIMO_ENDPOINT` is correct
   - Check logs in `logs/n8n_builder.llm.log`

2. **Validation Failures**
   - Recent fixes resolved most validation issues
   - Check `logs/n8n_builder.validation.log` for details
   - Ensure workflow has proper node connections

3. **Performance Issues**
   - Large workflows are automatically optimized
   - Check `logs/n8n_builder.performance.log`
   - Adjust `MIMO_MAX_TOKENS` if needed

## 🚀 Recent Updates (June 2025)

**Major Bug Fixes & Improvements:**
- ✅ **Fixed Critical Validation Bugs** - Workflow modifications now apply successfully
- ✅ **Enhanced LLM Response Parsing** - Robust handling of reasoning models with `<think>` tags
- ✅ **Intelligent Isolated Node Validation** - Allows acceptable isolated nodes (e.g., webhook responses)
- ✅ **Conflict Resolution** - Prevents duplicate connection actions
- ✅ **Comprehensive Error Handling** - Enhanced retry logic and fallback strategies

**Result:** Email nodes, database connections, and other workflow modifications now work reliably!

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow the agent-based architecture patterns
- Add comprehensive tests for new features
- Update documentation for API changes
- Use the logging system for debugging information

## License

MIT License - See LICENSE file for details

## Acknowledgments

- n8n team for the workflow automation platform
- Mimo VL 7B team for the local LLM capabilities
- FastAPI for the excellent web framework
- The open-source community for inspiration and contributions 