# RunSystem.md - n8n + nGrok Startup Guide

This document provides step-by-step instructions to start your n8n Docker environment with nGrok tunneling for webhook access.

## 🚀 Quick Start Options

### Option A: Automated Script (Recommended)
```bash
# Double-click or run from command line:
start-n8n.bat

# Or run PowerShell script directly:
powershell -ExecutionPolicy Bypass -File "Start-N8N-NgRok.ps1"
```
**What it does automatically:**
- ✅ Starts Docker containers
- ✅ Starts nGrok tunnel
- ✅ Extracts public URL from nGrok API
- ✅ Updates .env file with new webhook URL
- ✅ Restarts n8n to apply changes
- ✅ Shows all access URLs

### Option B: Manual Commands

### 1. Start Docker Desktop
- Ensure Docker Desktop is running on your system
- Wait for Docker to fully initialize

### 2. Start n8n Docker Container
```bash
cd C:\Users\mabramsR\source\Cursor_Workspaces\N8N_Builder\n8n-docker
docker-compose up -d
```

### 3. Verify n8n is Running
```bash
docker ps
docker logs n8n-dev --tail 10
```
- Look for: `n8n ready on 0.0.0.0, port 5678`
- Local access: http://localhost:5678

### 4. Start nGrok Tunnel
```bash
powershell "& 'C:\Installation\ngrok.exe' start n8n"
```

### 5. Get nGrok Public URL

**Method 1: From nGrok Terminal Output**
- After running the nGrok command, look at the terminal output
- Find the line that says `Forwarding`
- Example output:
```
Session Status                online
Account                       vbwyrde (Plan: Free)
Version                       3.23.1
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://9c83-24-187-157-188.ngrok-free.app -> http://localhost:5678
```
- Copy the HTTPS URL: `https://9c83-24-187-157-188.ngrok-free.app`

**Method 2: From nGrok Web Interface**
- Open browser: http://127.0.0.1:4040
- Click on the **"Status"** tab (next to "Inspect")
- The public URL will be shown in the tunnel status information
- Look for the tunnel endpoint URL

**Method 3: Command Line Query**
```bash
# Get tunnel info in JSON format
powershell "& 'C:\Installation\ngrok.exe' api tunnels"

# Or use curl to query the local API
curl http://127.0.0.1:4040/api/tunnels
```

### 6. Update n8n Webhook Configuration (if needed)
```bash
# Edit the .env file to update WEBHOOK_URL with new nGrok URL
# File: C:\Users\mabramsR\source\Cursor_Workspaces\N8N_Builder\n8n-docker\.env
# Update line: WEBHOOK_URL=https://YOUR-NEW-NGROK-URL/
```

## 📋 Detailed Step-by-Step Instructions

### Prerequisites Check
1. **Docker Desktop**: Must be installed and running
2. **nGrok**: Installed at `C:\Installation\ngrok.exe`
3. **nGrok Authentication**: Already configured with your account

### Step 1: Start Docker Services
```bash
# Navigate to n8n-docker directory
cd C:\Users\mabramsR\source\Cursor_Workspaces\N8N_Builder\n8n-docker

# Start n8n and PostgreSQL containers
docker-compose up -d

# Alternative: Start with development setup (SQLite)
# docker-compose -f docker-compose.dev.yml up -d
```

### Step 2: Verify Container Status
```bash
# Check if containers are running
docker ps

# Check n8n logs for startup confirmation
docker logs n8n-dev --tail 20

# Expected output should include:
# "n8n ready on 0.0.0.0, port 5678"
# "Editor is now accessible via: http://localhost:5678"
```

### Step 3: Test Local n8n Access
- Open browser: http://localhost:5678
- You should see the n8n login/setup page
- Complete initial setup if first time

### Step 4: Start nGrok Tunnel
```bash
# Start nGrok tunnel using configured profile
powershell "& 'C:\Installation\ngrok.exe' start n8n"

# Alternative: Start with simple command
# powershell "& 'C:\Installation\ngrok.exe' http 5678"
```

### Step 5: Monitor nGrok Status and Get Public URL

**A. Terminal Output Method**
- nGrok will display a live dashboard in terminal
- Look for this section in the output:
```
ngrok                                                    (Ctrl+C to quit)

Session Status                online
Account                       vbwyrde (Plan: Free)
Version                       3.23.1
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123-45-67-89-012.ngrok-free.app -> http://localhost:5678

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```
- **Copy this URL**: `https://abc123-45-67-89-012.ngrok-free.app`

**B. Web Interface Method**
- Open browser: http://127.0.0.1:4040
- By default, you'll see the "Inspect" tab with request logs
- **Click on the "Status" tab** (next to "Inspect" at the top)
- On the Status page, you'll see:
  - Tunnel information
  - Public URL/endpoint
  - Connection details
- Copy the public HTTPS URL from the tunnel information

**C. Command Line API Method**
```bash
# Query nGrok API for tunnel information
curl http://127.0.0.1:4040/api/tunnels

# This returns JSON with tunnel details including public_url
```

**Important Notes**:
- The URL format will be: `https://[random-string].ngrok-free.app`
- **Terminal method is most reliable** - the URL is always clearly shown there
- If you see the "Inspect" tab by default at http://127.0.0.1:4040, click "Status" tab to find tunnel info
- The terminal output is the easiest and most consistent way to get the URL

### Step 6: Update Webhook Configuration
```bash
# If nGrok URL changed, update n8n environment
# Edit file: n8n-docker\.env
# Find line: WEBHOOK_URL=https://old-url/
# Replace with: WEBHOOK_URL=https://new-ngrok-url/

# Restart n8n container to apply changes
docker-compose restart n8n
```

## 🛑 Stopping Services

### Automated Stop
```bash
# Double-click or run:
stop-n8n.bat

# Or PowerShell directly:
powershell -ExecutionPolicy Bypass -File "Stop-N8N-NgRok.ps1"
```

### Manual Stop
```bash
# Stop nGrok (Ctrl+C in nGrok terminal)
# Stop Docker containers
docker-compose down
```

## 🤖 Automation Features

The PowerShell automation scripts provide:

### Start-N8N-NgRok.ps1 Features:
- **Smart Detection**: Checks if services are already running
- **Automatic URL Extraction**: Uses nGrok API to get public URL
- **Environment Updates**: Automatically updates .env with new webhook URL
- **Service Coordination**: Restarts n8n after config changes
- **Error Handling**: Graceful handling of failures with clear messages
- **Status Reporting**: Shows all access URLs at completion

### Script Parameters:
```powershell
# Skip Docker startup (if already running)
Start-N8N-NgRok.ps1 -SkipDocker

# Skip nGrok startup (if already running)
Start-N8N-NgRok.ps1 -SkipNgrok

# Keep Docker running when stopping
Stop-N8N-NgRok.ps1 -KeepDocker
```

### Troubleshooting Automation:
- **PowerShell Execution Policy**: Scripts handle bypass automatically
- **nGrok API Access**: Uses http://127.0.0.1:4040/api/tunnels for URL extraction
- **Docker Detection**: Checks container status before starting
- **Timeout Handling**: 60s for n8n startup, 30s for nGrok tunnel

## 🔧 Management Commands

### Check System Status
```bash
# Check Docker containers
docker ps

# Check n8n logs
docker logs n8n-dev

# Check nGrok status (if running)
# Visit: http://127.0.0.1:4040
```

### Stop Services
```bash
# Stop nGrok (Ctrl+C in nGrok terminal)

# Stop Docker containers
docker-compose down

# Stop specific container
docker stop n8n-dev
```

### Restart Services
```bash
# Restart n8n container
docker-compose restart n8n

# Restart all services
docker-compose down && docker-compose up -d
```

## 🌐 Access URLs

### Local Access
- **n8n Interface**: http://localhost:5678
- **nGrok Monitor**: http://127.0.0.1:4040

### Public Access (via nGrok)
- **Public n8n**: https://YOUR-NGROK-URL (changes each restart)
- **Webhook Endpoint**: https://YOUR-NGROK-URL/webhook/YOUR-WEBHOOK-ID

## ⚠️ Important Notes

### nGrok URL Changes
- **Free Plan**: URL changes every time nGrok restarts
- **Paid Plan**: Can use static subdomains
- **Always update** webhook URLs in external services when nGrok restarts

### Security Considerations
- n8n basic auth is maintained through nGrok tunnel
- Default credentials: admin/admin123 (change these!)
- nGrok free plan shows warning page to visitors

### Troubleshooting
- **n8n not accessible**: Check Docker container status
- **nGrok connection refused**: Ensure n8n is running first
- **Webhook not working**: Verify nGrok URL is updated in n8n settings

## 📝 Configuration Files

### Key Files
- **Docker Compose**: `docker-compose.yml`
- **Environment**: `.env`
- **nGrok Config**: `C:\Users\mabramsR\AppData\Local\ngrok\ngrok.yml`

### Current Configuration
- **n8n Container**: n8n-dev
- **Database**: PostgreSQL (n8n-postgres)
- **nGrok Profile**: n8n (configured tunnel)
- **nGrok Location**: C:\Installation\ngrok.exe

---

**Last Updated**: Created during nGrok integration setup
**nGrok Account**: vbwyrde (Free Plan)
**Docker Environment**: Development setup with PostgreSQL
