# n8n Docker Quick Start Guide

Get n8n running in Docker in under 5 minutes!

## 🎯 Prerequisites

- ✅ Docker Desktop installed and running
- ✅ 4GB+ RAM available
- ✅ 20GB+ disk space

## 🚀 3-Step Setup

### Step 1: Run Setup Script

**Windows:**
```cmd
cd n8n-docker\scripts
setup-docker.bat
```

**Linux/Mac:**
```bash
cd n8n-docker/scripts
./setup-docker.sh
```

### Step 2: Start n8n

**For Development (Recommended):**
```bash
cd n8n-docker
docker-compose -f docker-compose.dev.yml up -d
```

**For Production:**
```bash
cd n8n-docker
docker-compose up -d
```

### Step 3: Access n8n

1. Open browser: http://localhost:5678
2. **⚠️ SECURITY**: Login with default credentials (CHANGE IMMEDIATELY):
   - Username: `admin`
   - Password: `admin123`
3. **🔒 IMPORTANT**: Change these credentials immediately (see Configuration section below)
4. Start creating workflows! 🎉

## ⚡ Essential Commands

```bash
# Check status
docker-compose ps

# View logs
docker-compose logs -f n8n

# Stop n8n
docker-compose down

# Restart n8n
docker-compose restart n8n

# Create backup
./scripts/backup.sh    # Linux/Mac
scripts\backup.bat     # Windows
```

## � CRITICAL: Security Configuration (Do This First!)

**⚠️ WARNING**: The default credentials are publicly known and MUST be changed before use!

1. **🚨 IMMEDIATELY Change Default Password:**
   ```bash
   # Edit .env file and change:
   N8N_BASIC_AUTH_USER=your-username        # Change from 'admin'
   N8N_BASIC_AUTH_PASSWORD=your-secure-password  # Change from 'admin123'
   ```
   - Use a strong, unique password
   - Restart: `docker-compose restart n8n`

2. **🔑 Generate Secure Encryption Key:**
   ```bash
   # Generate a secure random key:
   openssl rand -base64 32

   # Or use PowerShell:
   [System.Web.Security.Membership]::GeneratePassword(32, 8)
   ```
   - Copy the generated key to `N8N_ENCRYPTION_KEY` in `.env`
   - Restart containers

3. **🌍 Configure Timezone:**
   - Edit `.env` file
   - Set `GENERIC_TIMEZONE=America/New_York` (or your timezone)

## 🆘 Quick Troubleshooting

**Can't access n8n?**
- Check if Docker is running: `docker info`
- Verify container is up: `docker-compose ps`
- Try different port: change `5678:5678` to `8080:5678` in docker-compose file

**Container won't start?**
- Check logs: `docker-compose logs n8n`
- Verify .env file syntax
- Ensure port 5678 isn't used by another app

**Need help?**
- Check full README.md
- Visit: https://community.n8n.io/

## 🎯 What's Next?

1. **Create Your First Workflow:**
   - Click "Add workflow" in n8n
   - Try the HTTP Request node
   - Connect to your favorite APIs

2. **Explore Integrations:**
   - 300+ built-in nodes
   - Connect Google Sheets, Slack, GitHub, etc.
   - Build powerful automations

3. **Set Up Backups:**
   - Run backup script weekly
   - Store backups safely
   - Test restore process

4. **Scale for Production:**
   - Switch to PostgreSQL
   - Enable HTTPS
   - Set up monitoring

---

**🎉 You're ready to automate everything with n8n!**
