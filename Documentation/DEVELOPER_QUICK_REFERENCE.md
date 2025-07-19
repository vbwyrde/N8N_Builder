# N8N_Builder Developer Quick Reference

## 🚀 Essential Commands (Copy & Paste Ready)

### Initial Setup
```bash
# Clone and setup
git clone https://github.com/vbwyrde/N8N_Builder.git
cd N8N_Builder
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Start N8N_Builder
python run.py
# Opens: http://localhost:8002 (main) + http://localhost:8081 (dashboard)
```

### OAuth2 Setup (Twitter, Google, GitHub, etc.)
```bash
# In separate terminal
cd n8n-docker
.\Start-LocalTunnel.ps1
# Use callback URL: https://n8n-oauth-stable.loca.lt/rest/oauth2-credential/callback
```

### Daily Workflow
```bash
# Start n8n Docker
cd n8n-docker
.\start-n8n.bat

# Start N8N_Builder  
python run.py

# Generate workflow at: http://localhost:8002
# Import to n8n at: http://localhost:5678
```

## 📚 Key Documentation

| Need | File | Time |
|------|------|------|
| **Complete setup** | [GETTING_STARTED.md](GETTING_STARTED.md) | 15 min |
| **OAuth2 setup** | [n8n-docker/README-LocalTunnel.md](n8n-docker/README-LocalTunnel.md) | 5 min |
| **Architecture** | [Documentation/ARCHITECTURE.md](Documentation/ARCHITECTURE.md) | 10 min |
| **API usage** | [Documentation/api/API_Reference.md](Documentation/api/API_Reference.md) | Reference |
| **Troubleshooting** | [Documentation/guides/Troubleshooting.md](Documentation/guides/Troubleshooting.md) | As needed |

## 🔧 Common Issues & Solutions

### "Import pyodbc could not be resolved"
```bash
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "OAuth2 callback URL not working"
```bash
# Start LocalTunnel for OAuth2 setup
cd n8n-docker
.\Start-LocalTunnel.ps1
# Use: https://n8n-oauth-stable.loca.lt/rest/oauth2-credential/callback
```

### "n8n won't start"
```bash
# Check Docker and restart
docker-compose ps
cd n8n-docker
.\Stop-N8N-Stable.ps1
.\Start-N8N-Stable.ps1
```

---
**Updated**: {datetime.now().strftime('%Y-%m-%d')}
