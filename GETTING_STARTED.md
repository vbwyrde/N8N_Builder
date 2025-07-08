# 📖 Getting Started with N8N_Builder

**🎯 Goal**: Understand the system and customize for your needs (15 minutes)

## What is N8N_Builder?

N8N_Builder is an **AI-powered workflow generator** that creates n8n automation workflows from plain English descriptions. It consists of three parts:

1. **🤖 N8N_Builder** (this repo) - Generates JSON workflows using AI
2. **🔧 Automated System** - Automatic error detection and resolution system
3. **🐳 n8n-docker** - Executes workflows in production

## Quick Setup Overview

```mermaid
graph LR
    A[Install N8N_Builder] --> B[Configure LLM]
    B --> C[Start Generator]
    C --> D[Setup n8n-docker]
    D --> E[Generate & Deploy]
```

## Step 1: Setup N8N_Builder (Workflow Generator)

### Python Environment Requirements

**⚠️ CRITICAL**: N8N_Builder requires a properly configured Python virtual environment to function correctly.

#### Required Setup
```bash
git clone https://github.com/vbwyrde/N8N_Builder.git
cd N8N_Builder

# Create and activate virtual environment
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate

# Install dependencies in virtual environment
pip install -r requirements.txt
```

#### Why Virtual Environment is Required
- **Database Integration**: The MCP Database Tool requires `pyodbc` to be installed in the correct Python environment
- **Process Management**: Emergency shutdown logic depends on proper process isolation
- **Dependency Isolation**: Prevents conflicts with system Python packages
- **IDE Compatibility**: Ensures proper import resolution in development environments

#### Verification
Verify your environment is correctly configured:
```bash
# Check you're in the virtual environment (should show venv path)
which python  # Linux/Mac
where python   # Windows

# Test critical imports
python -c "import pyodbc; print('✅ pyodbc available')"
python -c "from n8n_builder.mcp_database_tool import get_mcp_database; print('✅ MCP Database tool ready')"
```

### Configure Your LLM
Create a `.env` file with your LLM settings:

**Option A: Local LLM (Recommended)**
```bash
echo "MIMO_ENDPOINT=http://localhost:1234/v1/chat/completions" > .env
echo "MIMO_MODEL=mimo-vl-7b" >> .env
echo "MIMO_IS_LOCAL=true" >> .env
```

**Option B: OpenAI API**
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
echo "MIMO_IS_LOCAL=false" >> .env
```

### Start the Generator

**⚠️ IMPORTANT**: Always run with the virtual environment activated or use the provided startup scripts.

**Method A: Using Startup Scripts (Recommended)**
```bash
# Windows PowerShell
.\Scripts\run_with_venv.ps1

# Windows Command Prompt
Scripts\run_with_venv.bat

# These scripts automatically:
# - Verify virtual environment is configured
# - Check dependencies are installed
# - Start with proper Python environment
```

**Method B: Manual with Virtual Environment**
```bash
# Activate virtual environment first
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# venv\Scripts\activate.bat   # Windows Command Prompt
# source venv/bin/activate    # Linux/Mac

# Then start normally
python run.py
# Opens TWO interfaces:
# N8N Builder: http://localhost:8002
# System Dashboard: http://localhost:8081
```

**Method C: Direct Virtual Environment Python**
```bash
# Use venv Python directly (no activation needed)
.\venv\Scripts\python.exe run.py  # Windows
# ./venv/bin/python run.py        # Linux/Mac
```

**Method D: CLI Mode**
```bash
# Ensure virtual environment is activated first
python -m n8n_builder.cli serve
# Opens at http://localhost:8000
```

## Step 2: Setup n8n-docker (Workflow Executor)

### Quick Start
```bash
cd n8n-docker
# Windows
.\start-n8n.bat
# Linux/Mac
docker-compose up -d
```

### Access n8n
- Open: http://localhost:5678
- Default login: admin / admin
- **⚠️ Change password immediately!**

## Step 3: Create Your First Workflow

### Generate with AI
1. Open N8N_Builder: http://localhost:8002
2. Monitor system health: http://localhost:8081 (System Dashboard)
2. Describe your automation:
   - *"Send me an email when a new file is uploaded to a folder"*
   - *"Post to Twitter when I publish a blog article"*
   - *"Convert CSV files to JSON and send to webhook"*
3. Click "Generate Workflow"
4. Copy the JSON output

### Deploy to n8n
1. Open n8n: http://localhost:5678
2. Go to: Settings → Import from JSON
3. Paste the JSON from N8N_Builder
4. Click "Import"
5. Activate the workflow (toggle switch)

## Understanding the System

### N8N_Builder Features
- **AI Generation**: Converts plain English to n8n workflows
- **MCP Research**: Real-time research of n8n documentation
- **Dual APIs**: Standard REST + AG-UI Protocol
- **Workflow Modification**: Update existing workflows
- **Validation**: Ensures workflows meet n8n standards

### n8n-docker Features
- **Production Environment**: Docker-based n8n with PostgreSQL
- **Webhook Support**: nGrok tunneling for external integrations
- **Automated Scripts**: Easy startup/shutdown
- **Security**: Authentication and encryption ready

## Common Customizations

### Change Ports
Edit `.env` file:
```bash
STANDARD_API_PORT=8002
AGUI_SERVER_PORT=8003
```

### Enable Webhooks
For external service integration:
1. Install nGrok: https://ngrok.com/download
2. Run: `ngrok http 5678`
3. Use the https URL for webhook endpoints

### Production Security
See: [Technical Specifications](Documentation/technical/Specifications.md)
- Change default passwords
- Generate encryption keys
- Configure authentication

## Next Steps

### I Want To...
| Goal | Guide | Time |
|------|-------|------|
| Connect external services | [Integration Guide](Documentation/guides/Integration.md) | 15 min |
| Understand the architecture | [Architecture Overview](Documentation/Architecture.md) | 10 min |
| Learn design principles | [Design Principles](Documentation/DesignPrinciples.md) | 10 min |
| Use the API | [API Reference](Documentation/api/API_Reference.md) | Reference |

### Troubleshooting

#### Environment Issues
- **"Import pyodbc could not be resolved"**: Virtual environment not activated or pyodbc not installed in venv
- **"Process kills itself on startup"**: Using system Python instead of virtual environment Python
- **"Dependencies not found"**: Run `pip install -r requirements.txt` inside activated virtual environment
- **"Virtual environment broken"**: Recreate with `python -m venv venv --clear` then reinstall requirements

#### General Issues
- **N8N_Builder won't start**: Check Python version (3.8+), ensure virtual environment is activated
- **n8n won't start**: Check Docker is running, port 5678 is free
- **Workflows won't import**: Verify JSON format, check n8n version compatibility
- **LLM connection issues**: Verify endpoint URL and model availability

#### Environment Recovery Commands
```bash
# If virtual environment is corrupted, recreate it:
python -m venv venv --clear
.\venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt

# Verify everything works:
.\venv\Scripts\python.exe -c "import pyodbc; print('✅ Environment ready')"
```

**📖 Complete troubleshooting**: [Troubleshooting Guide](Documentation/guides/Troubleshooting.md)

## Success Indicators

✅ **N8N_Builder Working**: Web interface loads at http://localhost:8002  
✅ **n8n Working**: Login screen at http://localhost:5678  
✅ **Integration Working**: Can import JSON from N8N_Builder to n8n  
✅ **Workflow Working**: Activated workflow shows in n8n dashboard  

---

**🎉 Congratulations!** You now have a complete AI-powered workflow automation system running locally.

**Next**: Try creating different types of workflows or explore the [User Guides](Documentation/guides/) for specific use cases.
