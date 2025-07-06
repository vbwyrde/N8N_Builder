# 🐳 Docker Setup Guide for N8N_Builder

**Complete Docker installation and configuration guide for n8n workflow automation**

## 🎯 Overview

This guide covers Docker installation, version management, and n8n container setup for the N8N_Builder project.

## 📋 Docker Version Requirements

### Recommended Version
- **Docker Desktop 4.40.0** - Confirmed stable and reliable
- **Why this version?** Newer versions may have startup issues and container management problems
- **Compatibility:** Tested with Windows 11, works reliably with n8n containers

### Version Check
```bash
# Check your current Docker version
docker --version

# Expected output: Docker version 4.40.0, build...
```

## 🚀 Docker Installation

### Fresh Installation
1. **Download Docker Desktop 4.40.0**
   - Visit [Docker Desktop releases](https://docs.docker.com/desktop/release-notes/)
   - Download version 4.40.0 specifically
   - Avoid latest versions if experiencing issues

2. **Install Docker Desktop**
   - Run installer as Administrator
   - Enable WSL 2 integration (Windows)
   - Restart computer when prompted

3. **Verify Installation**
   ```bash
   docker --version
   docker info
   ```

### Downgrading from Newer Version
If you have Docker issues with newer versions:

1. **Uninstall Current Docker**
   - Windows: Apps & Features → Docker Desktop → Uninstall
   - Remove all Docker data if prompted

2. **Install Docker 4.40.0**
   - Download specific version 4.40.0
   - Install as Administrator
   - Restart system

3. **Verify Downgrade**
   ```bash
   docker --version
   # Should show: Docker version 4.40.0
   ```

## 🔧 N8N Container Setup

### Step 1: Create Required Docker Volumes
```bash
# Create n8n data volume
docker volume create n8n_data

# Create PostgreSQL data volume  
docker volume create n8n_postgres_data

# Verify volumes exist
docker volume ls
```

### Step 2: Start N8N Containers
```bash
# Navigate to n8n-docker directory
cd n8n-docker

# Start containers
docker-compose up -d

# Check status
docker-compose ps
```

### Step 3: Verify Installation
```bash
# Check container logs
docker logs n8n-dev --tail 20
docker logs postgres-dev --tail 20

# Test web access
curl http://localhost:5678
```

## 🔍 Troubleshooting

### Docker Won't Start
```bash
# Check Docker service status
docker info

# If fails, restart Docker Desktop
# Windows: Right-click Docker icon → Restart
```

### Containers Won't Start
```bash
# Check for port conflicts
netstat -ano | findstr "5678 5432"

# Kill conflicting processes if needed
taskkill /F /PID <process-id>
```

### Volume Errors
```bash
# If "external volumes not found" error:
docker volume create n8n_data
docker volume create n8n_postgres_data

# Then restart containers
docker-compose up -d
```

### Memory Issues
```bash
# Check Docker resource usage
docker stats

# Increase Docker memory allocation:
# Docker Desktop → Settings → Resources → Memory
# Recommended: 4GB minimum
```

## 📊 Container Management

### Essential Commands
```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# View logs
docker-compose logs -f n8n
docker-compose logs -f postgres

# Check status
docker-compose ps
```

### Maintenance Commands
```bash
# Update n8n image
docker pull n8nio/n8n:latest
docker-compose up -d

# Clean up unused resources
docker system prune -f

# Backup volumes
docker run --rm -v n8n_data:/data -v $(pwd):/backup alpine tar czf /backup/n8n_backup.tar.gz /data
```

## 🔒 Security Considerations

### Default Credentials
- **Default login:** admin / admin
- **⚠️ CRITICAL:** Change immediately after first login
- **Location:** n8n web interface → Settings → Users

### Network Security
- **Local access only:** http://localhost:5678
- **External access:** Use nGrok tunneling (see automation guides)
- **Production:** Configure HTTPS and authentication

## 🎯 Quick Reference

### Successful Setup Checklist
- ✅ Docker Desktop 4.40.0 installed and running
- ✅ Docker volumes created (n8n_data, n8n_postgres_data)
- ✅ Containers running (docker-compose ps shows "Up")
- ✅ Web interface accessible (http://localhost:5678)
- ✅ Default credentials changed

### Common File Locations
- **Docker Compose:** `n8n-docker/docker-compose.yml`
- **Environment:** `n8n-docker/.env`
- **Logs:** `docker logs n8n-dev` and `docker logs postgres-dev`
- **Data:** Docker volumes (persistent across restarts)

## 🆘 Getting Help

### Before Asking for Help
1. Check Docker version: `docker --version`
2. Verify containers: `docker-compose ps`
3. Check logs: `docker logs n8n-dev`
4. Try system reset: `docker-compose down && docker-compose up -d`

### Include This Information
- Operating system and version
- Docker version (`docker --version`)
- Error messages (exact text)
- Container status (`docker-compose ps`)
- Log excerpts (`docker logs n8n-dev --tail 50`)

---

**💡 Pro Tip:** Most Docker issues are resolved by using the stable version 4.40.0 and ensuring proper volume creation before starting containers.
