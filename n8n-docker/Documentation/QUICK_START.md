# 🚀 n8n Docker Quick Start Guide

Get the **n8n execution environment** running with webhook support in under 5 minutes!

> **⚡ Even Faster?** Try [Lightning Start](../LIGHTNING_START.md) for 2-minute setup with no explanations!

**🏗️ Complete System Setup:**
- **🤖 [N8N_Builder Setup](../../README.md)**: Generate workflows with AI
- **🐳 n8n-docker Setup** (this guide): Execute workflows in production
- **📚 [Master Documentation](../../Documentation/DOCUMENTATION_INDEX.md)**: Complete system overview

## 📚 Documentation Navigation

- **📖 [Main README](README.md)** - Complete documentation hub
- **🔒 [Security Guide](SECURITY.md)** - Security best practices (READ FIRST!)
- **🔑 [Credentials Setup](CREDENTIALS_SETUP.md)** - Connect external services
- **🤖 [Automation Guide](AUTOMATION-README.md)** - Automation scripts
- **📋 [Complete Manual Guide](../RunSystem.md)** - Detailed manual operations

## 🎯 Prerequisites Check

Before starting, ensure you have:
- ✅ **Docker Desktop** installed and running
- ✅ **4GB+ RAM** available for Docker
- ✅ **20GB+ disk space** available
- ✅ **PowerShell** (Windows) or **Bash** (Linux/Mac)

**That's it!** No external services or accounts needed.

## 🚀 Choose Your Setup Method

### 🤖 Method A: Automated Setup (Recommended)

**Fastest way - Everything automated:**

1. **Navigate to n8n-docker folder**
2. **Double-click** `start-n8n.bat` **OR** run:
   ```powershell
   .\start-n8n.bat
   ```
3. **Wait 1-2 minutes** for automation to complete
4. **Access n8n** at http://localhost:8080 (stable URL that never changes!)

**✨ What gets automated:**
- ✅ Starts Docker containers (n8n + PostgreSQL)
- ✅ Starts stable URL proxy
- ✅ Configures permanent webhook URLs
- ✅ Shows all access URLs

### 📋 Method B: Manual Setup

**Step 1: Run Initial Setup**
```bash
# Navigate to n8n-docker directory first
cd n8n-docker

# Run setup script
powershell -ExecutionPolicy Bypass -File "setup.ps1"
```

**Step 2: Start n8n**
```bash
# For full features (recommended)
docker-compose up -d

# For development only (no PostgreSQL)
docker-compose -f docker-compose.dev.yml up -d
```

**Step 3: Access n8n**
- Open browser: http://localhost:5678
- Login with default credentials (⚠️ **CHANGE IMMEDIATELY**):
  - Username: `admin`
  - Password: `admin123`

## 🚨 CRITICAL: Security Configuration (Do This FIRST!)

**⚠️ DANGER**: Default credentials are publicly known and MUST be changed!

### 🔒 Step 1: Change Default Credentials (REQUIRED)

1. **Edit the `.env` file** (created by setup script):
   ```bash
   # Find these lines and change them:
   N8N_BASIC_AUTH_USER=admin                    # ❌ Change this
   N8N_BASIC_AUTH_PASSWORD=admin123             # ❌ Change this
   N8N_ENCRYPTION_KEY=CHANGE-THIS-TO-SECURE-KEY # ❌ Change this
   ```

2. **Use strong credentials:**
   ```bash
   # Example (use your own values):
   N8N_BASIC_AUTH_USER=myusername
   N8N_BASIC_AUTH_PASSWORD=MySecurePassword123!
   N8N_ENCRYPTION_KEY=your-32-character-random-key-here
   ```

3. **Restart n8n to apply changes:**
   ```bash
   docker-compose restart n8n
   ```

### 🔑 Step 2: Generate Secure Encryption Key

**Option A - PowerShell (Windows):**
```powershell
# Generate 32-character random key
[System.Web.Security.Membership]::GeneratePassword(32, 8)
```

**Option B - OpenSSL (Linux/Mac/Windows):**
```bash
# Generate base64 encoded key
openssl rand -base64 32
```

**Option C - Online Generator:**
- Visit: https://www.allkeysgenerator.com/Random/Security-Encryption-Key-Generator.aspx
- Generate 256-bit key
- Copy to `N8N_ENCRYPTION_KEY` in `.env`

### 🌍 Step 3: Configure Timezone (Optional)
```bash
# Edit .env file and set your timezone:
GENERIC_TIMEZONE=America/New_York    # Or your timezone
```

## ⚡ Essential Management Commands

### 🤖 Automated Commands (Recommended)
```bash
# Start everything (Docker + Stable URL Proxy)
start-n8n.bat

# Stop everything
stop-n8n.bat
```

### 📋 Manual Commands
```bash
# Check container status
docker-compose ps

# View n8n logs
docker-compose logs -f n8n

# Stop all services
docker-compose down

# Restart n8n only
docker-compose restart n8n

# Create backup
scripts\backup.bat     # Windows
./scripts/backup.sh    # Linux/Mac
```

## 🆘 Quick Troubleshooting

### 🐳 Docker Issues
```bash
# Check if Docker is running
docker info

# Check container status
docker-compose ps

# View error logs
docker-compose logs n8n
```

### 🌐 Access Issues
- **Can't access http://localhost:5678**:
  - Verify container is running: `docker-compose ps`
  - Check port isn't in use: `netstat -an | findstr 5678`
  - Try different port: Edit `docker-compose.yml`, change `5678:5678` to `8080:5678`

### 🔧 Common Fixes
- **Container won't start**: Check `.env` file syntax and Docker memory allocation
- **Permission errors**: Run PowerShell as Administrator
- **Port conflicts**: Ensure ports 5678 and 8080 are available
- **Proxy issues**: Check Docker containers are running (`docker ps`)

### 📚 Get More Help
- **📖 Full Documentation**: [README.md](README.md)
- **🔒 Security Guide**: [SECURITY.md](SECURITY.md)
- **🔑 Credentials Setup**: [CREDENTIALS_SETUP.md](CREDENTIALS_SETUP.md)
- **💬 Community Forum**: https://community.n8n.io/

## 🆘 Emergency Troubleshooting

### 🚨 Nothing Works - Start Here
```bash
# 1. Check if Docker is running
docker info
# If this fails: Start Docker Desktop and wait

# 2. Check if containers exist
docker-compose ps
# If empty: Run setup script first

# 3. Check n8n logs for errors
docker logs n8n-dev --tail 20
# Look for error messages

# 4. Check if port is blocked
netstat -an | findstr 5678
# If port in use: Change port or stop other service
```

### 🔧 Quick Fixes
- **PowerShell won't run scripts**: Run as Administrator
- **Docker won't start**: Restart Docker Desktop, check disk space
- **Can't access localhost:8080**: Check proxy health at `/health` endpoint
- **Stable URL not working**: Restart with `.\Stop-N8N-Stable-Fixed.ps1` then `.\Start-N8N-Stable.ps1`

### 🔄 Nuclear Option (Reset Everything)
```bash
# Stop everything
docker-compose down -v

# Remove all containers and data (⚠️ DESTROYS ALL DATA)
docker system prune -a

# Start fresh
powershell -ExecutionPolicy Bypass -File "../setup.ps1"
start-n8n.bat
```

## 🎯 What's Next?

### 🏃‍♂️ Immediate Next Steps
1. **🚨 SECURITY**: Change default credentials (see security section above)
2. **🔑 WEBHOOKS**: Set up external service credentials ([CREDENTIALS_SETUP.md](CREDENTIALS_SETUP.md))
3. **🤖 AUTOMATION**: Learn about automation scripts ([AUTOMATION-README.md](AUTOMATION-README.md))

### 🎨 Start Building

#### **🤖 Option A: Generate with AI (Recommended)**
1. **Setup N8N_Builder**: Follow the [N8N_Builder setup guide](../../README.md#installation--setup)
2. **Generate Workflow**: Open http://localhost:8000 and describe your automation
3. **Import to n8n**: Copy JSON → n8n Settings → Import from JSON
4. **Activate**: Toggle your AI-generated workflow active

#### **🔧 Option B: Build Manually**
1. **Create Your First Workflow:**
   - Click "Add workflow" in n8n interface
   - Try the HTTP Request node
   - Connect to your favorite APIs

2. **Explore 300+ Integrations:**
   - Google Sheets, Slack, GitHub, Discord
   - Blogger, Twitter, Email services
   - Build powerful automations

**📖 Complete Integration Guide**: [Master Documentation](../../DOCUMENTATION_INDEX.md#integration-guide)

3. **Set Up External Services:**
   - Follow [CREDENTIALS_SETUP.md](CREDENTIALS_SETUP.md) for OAuth setup
   - Configure webhooks for real-time triggers
   - Test with simple workflows first

### 🏭 Production Readiness
1. **Backups**: Run `scripts\backup.bat` weekly
2. **Monitoring**: Check logs regularly with `docker-compose logs n8n`
3. **Updates**: Update n8n monthly with `docker-compose pull`
4. **Security**: Review [SECURITY.md](SECURITY.md) for best practices

---

**🎉 You're ready to automate everything with n8n!**

**📖 Next recommended reading**: [CREDENTIALS_SETUP.md](CREDENTIALS_SETUP.md) for connecting external services
