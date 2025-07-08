# 🔧 n8n-docker Troubleshooting Guide

**Quick fixes for common n8n-docker and nGrok issues**

## 🚨 Emergency Quick Fixes

### Complete System Reset
```bash
# Stop everything
stop-n8n.bat

# Clean Docker
docker-compose down
docker system prune -f

# Restart fresh
start-n8n.bat
```

### Port Conflicts
```bash
# Find what's using n8n port
netstat -ano | findstr 5678
taskkill /F /PID <process-id>

# Find what's using PostgreSQL port
netstat -ano | findstr 5432
taskkill /F /PID <process-id>
```

## 🐳 Docker Issues

### Docker Version Compatibility

**Recommended Docker Version:**
- **Docker Desktop 4.40.0** - Confirmed stable version
- Newer versions may have compatibility issues
- If experiencing Docker startup problems, consider downgrading to 4.40.0

**Check Your Docker Version:**
```bash
docker --version
# Should show: Docker version 4.40.0 or similar
```

### "Docker not found" or "Docker not running"

**Check Docker Status:**
```bash
docker info
# Should show Docker system information
```

**Solutions:**
- **Start Docker Desktop** and wait 2-3 minutes
- **Restart Docker Desktop** if it's unresponsive
- **Check Windows Services**: Docker Desktop Service should be running
- **Verify installation**: Reinstall Docker Desktop if needed
- **Version issues**: Try Docker Desktop 4.40.0 if newer versions fail

### "Container won't start"

**Check Container Status:**
```bash
docker-compose ps
# Should show containers as "Up"
```

**Check Logs:**
```bash
docker logs n8n-dev
docker logs postgres-dev
```

**Common Solutions:**
- **Port conflicts**: Change ports in docker-compose.yml
- **Permission issues**: Run as administrator
- **Disk space**: Clean up Docker images and volumes
- **Memory issues**: Increase Docker memory allocation

### "External volumes not found" Error

**Create Required Docker Volumes:**
```bash
# Create n8n data volume
docker volume create n8n_data

# Create PostgreSQL data volume
docker volume create n8n_postgres_data

# Verify volumes exist
docker volume ls
```

**Then restart containers:**
```bash
docker-compose up -d
```

### "Database connection errors"

**Check PostgreSQL Container:**
```bash
docker logs postgres-dev
```

**Reset Database:**
```bash
docker-compose down
docker volume rm n8n-docker_postgres_data
docker-compose up -d
```

**Verify Database Connection:**
```bash
# Connect to database directly
docker exec -it postgres-dev psql -U n8n_user -d n8n
```

## 🌐 nGrok Issues

### "nGrok not found" or "nGrok authentication failed"

**Check nGrok Installation:**
```bash
ngrok version
# Should show version number
```

**Check Authentication:**
```bash
ngrok config check
# Should show valid auth token
```

**Solutions:**
- **Install nGrok**: Download from https://ngrok.com/download
- **Authenticate**: `ngrok config add-authtoken YOUR_TOKEN`
- **Update PATH**: Add nGrok to system PATH
- **Check config.ps1**: Verify nGrok path is correct

### "Tunnel won't start" or "Tunnel disconnects"

**Check nGrok Status:**
```bash
curl http://127.0.0.1:4040/api/tunnels
# Should show active tunnel
```

**Common Solutions:**
- **Free tier limits**: Only 1 tunnel allowed on free tier
- **Network issues**: Check internet connection
- **Firewall blocking**: Allow nGrok through firewall
- **Account limits**: Check nGrok dashboard for usage

### "Webhook URLs not updating"

**Manual URL Check:**
```bash
# Get current nGrok URL
curl http://127.0.0.1:4040/api/tunnels | findstr "public_url"
```

**Force URL Update:**
```bash
# Restart automation with force
Start-N8N-NgRok.ps1 -Force
```

## 🔗 n8n Web Interface Issues

### "Can't access n8n web interface"

**Check n8n Container:**
```bash
docker logs n8n-dev
# Look for startup errors
```

**Test Connectivity:**
```bash
curl http://localhost:5678/healthz
# Should return "ok"
```

**Solutions:**
- **Wait for startup**: n8n takes 1-2 minutes to fully start
- **Check firewall**: Allow port 5678
- **Try different browser**: Clear cache or use incognito
- **Check Docker networking**: Restart Docker Desktop

### "Login issues" or "Authentication errors"

**Reset Admin Password:**
```bash
# Stop n8n
docker-compose stop n8n

# Reset password via environment variable
# Add to .env file:
N8N_OWNER_EMAIL=admin@example.com
N8N_OWNER_PASSWORD=newpassword

# Restart n8n
docker-compose start n8n
```

### "Workflows won't import"

**Check JSON Format:**
- Verify JSON is valid (use online JSON validator)
- Ensure complete JSON (not truncated)
- Check for special characters

**Check n8n Version:**
```bash
docker exec n8n-dev n8n --version
```

**Solutions:**
- **Update n8n**: `docker-compose pull && docker-compose up -d`
- **Check node compatibility**: Some nodes require specific n8n versions
- **Try smaller workflow**: Test with simple workflow first

## 🔧 Configuration Issues

### "Environment variables not loading"

**Check .env File:**
```bash
# Verify .env file exists and has correct format
type .env
```

**Common Issues:**
- **No spaces around =**: Use `KEY=value` not `KEY = value`
- **No quotes needed**: Use `KEY=value` not `KEY="value"`
- **File encoding**: Save as UTF-8 without BOM

### "Config.ps1 errors"

**Check PowerShell Execution Policy:**
```bash
Get-ExecutionPolicy
# Should be RemoteSigned or Unrestricted
```

**Fix Execution Policy:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Verify Config File:**
```bash
# Test config file syntax
powershell -File config.ps1 -WhatIf
```

## 📊 Performance Issues

### "n8n running slowly"

**Check Resource Usage:**
```bash
docker stats
# Monitor CPU and memory usage
```

**Solutions:**
- **Increase Docker memory**: Docker Desktop → Settings → Resources
- **Clean up workflows**: Remove unused/large workflows
- **Optimize database**: Regular maintenance and cleanup
- **Check disk space**: Ensure adequate free space

### "Database performance issues"

**Check Database Size:**
```bash
docker exec postgres-dev psql -U n8n_user -d n8n -c "SELECT pg_size_pretty(pg_database_size('n8n'));"
```

**Database Maintenance:**
```bash
# Vacuum and analyze database
docker exec postgres-dev psql -U n8n_user -d n8n -c "VACUUM ANALYZE;"
```

## 🔍 Diagnostic Commands

### System Health Check
```bash
# Check all services
docker-compose ps
curl http://localhost:5678/healthz
curl http://127.0.0.1:4040/api/tunnels

# Check disk space
docker system df

# Check logs
docker logs n8n-dev --tail 50
docker logs postgres-dev --tail 50
```

### Network Diagnostics
```bash
# Check port usage
netstat -an | findstr "5678 5432 4040"

# Test internal connectivity
docker exec n8n-dev curl http://postgres:5432

# Test external connectivity
curl -I https://api.n8n.io
```

## 🆘 Getting Help

### Before Asking for Help
1. **Try emergency quick fixes** above
2. **Check relevant logs** for error messages
3. **Document exact steps** to reproduce issue
4. **Note system information** (OS, Docker version, etc.)

### Information to Include
- **Operating system** and version
- **Docker version**: `docker --version`
- **nGrok version**: `ngrok version`
- **Error messages** (exact text)
- **Steps to reproduce**
- **Log excerpts** from Docker containers

### Where to Get Help
- **📖 [n8n Community](https://community.n8n.io/)** - Active community support
- **🐛 [GitHub Issues](https://github.com/vbwyrde/N8N_Builder/issues)** - Bug reports
- **📚 [n8n Documentation](https://docs.n8n.io/)** - Official documentation
- **💬 [Discord](https://discord.gg/n8n)** - Real-time chat support

---

**💡 Pro Tip**: Most issues are resolved by restarting services and checking logs. When in doubt, try the "Complete System Reset" procedure above.
