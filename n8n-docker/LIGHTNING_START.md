# ⚡ Lightning Start - n8n Docker

**🎯 Goal**: Working n8n execution environment in 2 minutes

## Prerequisites
- Docker Desktop running (recommended: version 4.40.0)
- Windows PowerShell OR Linux/Mac Terminal

## Commands

### Windows
```powershell
cd n8n-docker
.\start-n8n.bat
```

### Linux/Mac
```bash
cd n8n-docker
docker-compose up -d
```

### First-Time Setup (If Volumes Don't Exist)
If you get "external volumes not found" error:
```bash
# Create required Docker volumes
docker volume create n8n_data
docker volume create n8n_postgres_data

# Then start normally
docker-compose up -d
```

## Success
- ✅ Open: http://localhost:8080 (Stable URL) OR http://localhost:5678 (Direct)
- ✅ See: n8n login screen
- ✅ Login: MarkA / abc123def* (configured in .env)
- ✅ Ready: Import workflows from N8N_Builder
- ✅ Stable webhook URL: http://localhost:8080 (NEVER changes!)

## Import Your First Workflow
1. **Generate workflow** in N8N_Builder (http://localhost:8002)
2. **Copy the JSON** output
3. **In n8n**: Settings → Import from JSON
4. **Paste JSON** and click Import
5. **Activate workflow** (toggle switch)

## Next Steps
- **Need webhooks?** → [Getting Started Guide](Documentation/GETTING_STARTED.md)
- **Want security?** → [Security Setup](Documentation/SECURITY.md)
- **Having issues?** → [Troubleshooting](Documentation/TROUBLESHOOTING.md)

---
*⚡ Lightning Start gets you running fast. For webhooks, security, and options, see [Getting Started](Documentation/GETTING_STARTED.md).*
