# N8N Workflow Builder

A Python-based tool for generating n8n workflows using natural language descriptions. This tool uses a local LLM (Mimo VL 7B) to convert plain English descriptions into valid n8n workflow JSON structures.

## Features

- Natural language to n8n workflow conversion
- Real-time workflow validation
- Best practices checking
- Improvement suggestions
- Command-line interface
- REST API with streaming responses
- Feedback tracking and history

## Prerequisites

- Python 3.8 or higher
- Local LLM server running Mimo VL 7B
- n8n instance for testing generated workflows

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
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

4. Create a `.env` file:
```bash
# LLM Configuration
MIMO_ENDPOINT=http://localhost:1234/v1/chat/completions
MIMO_MODEL=mimo-vl-7b
MIMO_TEMPERATURE=0.7
MIMO_MAX_TOKENS=2000
```

## Usage

### Command Line Interface

1. Start the API server:
```bash
# Windows
python -m n8n_builder.cli serve

# Linux/Mac
python -m n8n_builder.cli serve
```

2. Generate a workflow:
```bash
# Windows
python -m n8n_builder.cli generate "Create a workflow that sends an email when a new file is uploaded" -o workflow.json

# Linux/Mac
python -m n8n_builder.cli generate "Create a workflow that sends an email when a new file is uploaded" -o workflow.json
```

### API Usage

1. Start the server:
```bash
python -m n8n_builder.cli serve
```

2. Generate a workflow using the API:
```bash
# Windows PowerShell
$body = @{
    description = "Create a workflow that sends an email when a new file is uploaded"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/generate" -Method Post -Body $body -ContentType "application/json"

# Linux/Mac
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"description": "Create a workflow that sends an email when a new file is uploaded"}'
```

3. Check workflow feedback:
```bash
# Windows PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/feedback/{workflow_id}" -Method Get

# Linux/Mac
curl "http://localhost:8000/feedback/{workflow_id}"
```

## Project Structure

```
N8N_Builder/
├── n8n_builder/
│   ├── __init__.py
│   ├── app.py           # FastAPI application
│   ├── n8n_builder.py   # Core workflow generation
│   ├── validators.py    # Workflow validation
│   ├── cli.py          # Command-line interface
│   └── code_generation_patterns.py
├── requirements.txt
├── README.md
└── .env
```

## Development

### Adding New Features

1. **New Workflow Patterns**
   - Add new patterns in `code_generation_patterns.py`
   - Update validation rules in `validators.py`

2. **Custom Validators**
   - Extend `BaseWorkflowValidator` for specific workflow types
   - Implement custom validation rules

3. **API Endpoints**
   - Add new endpoints in `app.py`
   - Update CLI commands in `cli.py`

### Testing

```bash
# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=n8n_builder
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- n8n team for the workflow automation platform
- Mimo VL 7B team for the local LLM
- FastAPI for the web framework 