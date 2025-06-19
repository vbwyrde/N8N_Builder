# 🤖 n8n + nGrok Automation Scripts

## 🚀 Quick Start

### Easiest Method - Double Click
1. **Start**: Double-click `start-n8n.bat`
2. **Stop**: Double-click `stop-n8n.bat`

### Command Line Method
```powershell
# Start everything
powershell -ExecutionPolicy Bypass -File "Start-N8N-NgRok.ps1"

# Stop everything  
powershell -ExecutionPolicy Bypass -File "Stop-N8N-NgRok.ps1"
```

## ✨ What Gets Automated

### Starting (`Start-N8N-NgRok.ps1`):
1. ✅ **Checks Docker** - Verifies Docker Desktop is running
2. ✅ **Starts Containers** - Launches n8n and PostgreSQL via docker-compose
3. ✅ **Waits for n8n** - Monitors logs until n8n is ready
4. ✅ **Starts nGrok** - Launches tunnel in background
5. ✅ **Gets Public URL** - Extracts HTTPS URL from nGrok API
6. ✅ **Updates Config** - Automatically updates .env WEBHOOK_URL
7. ✅ **Restarts n8n** - Applies new configuration
8. ✅ **Shows Status** - Displays all access URLs

### Stopping (`Stop-N8N-NgRok.ps1`):
1. ✅ **Stops nGrok** - Terminates all nGrok processes
2. ✅ **Stops Docker** - Shuts down containers (optional)
3. ✅ **Shows Status** - Confirms what's stopped

## 🎛️ Advanced Options

### Start Script Parameters
```powershell
# Skip Docker startup (if containers already running)
Start-N8N-NgRok.ps1 -SkipDocker

# Skip nGrok startup (if tunnel already running)
Start-N8N-NgRok.ps1 -SkipNgrok

# Enable verbose output
Start-N8N-NgRok.ps1 -Verbose
```

### Stop Script Parameters
```powershell
# Keep Docker containers running (only stop nGrok)
Stop-N8N-NgRok.ps1 -KeepDocker

# Enable verbose output
Stop-N8N-NgRok.ps1 -Verbose
```

## 🔧 How It Works

### nGrok URL Detection
- Uses nGrok's REST API at `http://127.0.0.1:4040/api/tunnels`
- Automatically finds the HTTPS tunnel endpoint
- No manual copy/paste needed!

### Environment File Updates
- Reads current `.env` file
- Updates `WEBHOOK_URL=` line with new nGrok URL
- Preserves all other environment variables

### Smart Detection
- Checks if Docker containers are already running
- Detects existing nGrok tunnels
- Skips unnecessary steps to save time

## 🚨 Troubleshooting

### PowerShell Execution Policy
If you get execution policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Docker Not Running
```
❌ Docker is not running. Please start Docker Desktop first.
```
**Solution**: Start Docker Desktop and wait for it to be ready

### nGrok Timeout
```
⚠️ nGrok tunnel timeout - check manually
```
**Solution**: Check nGrok status at http://127.0.0.1:4040

### n8n Not Ready
```
⚠️ n8n startup timeout - check logs manually
```
**Solution**: Check container logs:
```bash
docker logs n8n-dev
```

## 📁 File Structure

```
n8n-docker/
├── start-n8n.bat              # Windows batch file (double-click)
├── stop-n8n.bat               # Windows batch file (double-click)
├── Start-N8N-NgRok.ps1        # Main PowerShell start script
├── Stop-N8N-NgRok.ps1         # Main PowerShell stop script
├── docker-compose.yml         # Docker configuration
├── .env                       # Environment variables (auto-updated)
└── RunSystem.md               # Complete manual instructions
```

## 🎯 Benefits

### Before Automation:
1. Start Docker Desktop
2. Open terminal, navigate to folder
3. Run `docker-compose up -d`
4. Wait for n8n to start
5. Open another terminal
6. Run nGrok command
7. Copy URL from terminal output
8. Edit .env file manually
9. Restart n8n container
10. Check everything works

### After Automation:
1. **Double-click `start-n8n.bat`**
2. ☕ Get coffee while it runs
3. ✅ Everything ready!

**Time saved**: ~5-10 minutes per startup
**Error reduction**: No manual copy/paste mistakes
**Consistency**: Same process every time

---

💡 **Pro Tip**: Create desktop shortcuts to the .bat files for even faster access!
