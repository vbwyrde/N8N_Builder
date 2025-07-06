# ⚡ Lightning Start - N8N_Builder

**🎯 Goal**: Working AI workflow generator in 2 minutes

## Prerequisites
- Python 3.8+
- Git

## Commands
```bash
# 1. Get the code
git clone https://github.com/vbwyrde/N8N_Builder.git
cd N8N_Builder

# 2. Install
pip install -r requirements.txt

# 3. Configure (create .env file)
echo MIMO_ENDPOINT=http://localhost:1234/v1/chat/completions > .env
echo MIMO_MODEL=mimo-vl-7b >> .env
echo MIMO_IS_LOCAL=true >> .env

# 4. Start
python run.py
```

## Success
- ✅ Open: http://localhost:8002
- ✅ Type: "Send email when file uploaded"
- ✅ Click: "Generate Workflow"
- ✅ See: JSON workflow output

## Next Steps
- **Need n8n execution?** → [n8n Lightning Start](n8n-docker/LIGHTNING_START.md)
- **Want to understand more?** → [Getting Started Guide](GETTING_STARTED.md)
- **Having issues?** → [Troubleshooting](Documentation/TROUBLESHOOTING.md)

---
*⚡ Lightning Start gets you running fast. For explanations and options, see [Getting Started](GETTING_STARTED.md).*
