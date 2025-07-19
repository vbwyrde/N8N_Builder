# 🔧 Troubleshooting Guide

**Quick fixes for common N8N_Builder and n8n-docker issues**

## 🚨 Emergency Quick Fixes

### System Won't Start
```bash
# Check if ports are in use
netstat -an | findstr "8002 5678"

# Kill processes using ports
# Windows
taskkill /F /PID <process-id>
# Linux/Mac  
kill -9 <process-id>

# Restart everything
cd N8N_Builder
python run.py
cd n8n-docker
docker-compose restart
```

### Complete Reset
```bash
# Stop everything
docker-compose down
pkill -f "python run.py"

# Clean Docker
docker system prune -f

# Restart fresh
docker-compose up -d
python run.py
```

## 🤖 N8N_Builder Issues

### "N8N_Builder won't start"

**Check Python Version**
```bash
python --version  # Must be 3.8+
```

**Install Dependencies**
```bash
pip install -r requirements.txt
```

**Check LLM Connection**
```bash
curl http://localhost:1234/v1/models
# Should return model list
```

**Common Solutions:**
- Ensure local LLM server (LM Studio) is running
- Check `.env` file exists with correct settings
- Try different port: `python -m n8n_builder.cli serve --port 8001`

### "Workflow generation fails"

**Check Logs**
```bash
tail -f logs/n8n_builder.log
```

**Common Causes:**
- LLM server not responding
- Invalid description (too vague/complex)
- Network connectivity issues

**Solutions:**
- Restart LLM server
- Simplify workflow description
- Check firewall settings

### "API returns errors"

**Test Health Endpoint**
```bash
curl http://localhost:8002/health
```

**Check API Status**
```bash
curl http://localhost:8002/status
```

**Common Solutions:**
- Restart N8N_Builder: `python run.py`
- Check port conflicts
- Verify `.env` configuration

## 🐳 n8n-docker Issues

### "n8n won't start"

**Check Docker**
```bash
docker info
# Should show Docker running
```

**Check Ports**
```bash
netstat -an | findstr 5678
# Should be empty or show n8n
```

**Check Logs**
```bash
docker logs n8n-dev
```

**Common Solutions:**
- Start Docker Desktop
- Free port 5678: `taskkill /F /PID <process-using-5678>`
- Restart containers: `docker-compose restart`

### "Can't access n8n web interface"

**Verify Container Status**
```bash
docker-compose ps
# Should show n8n-dev as "Up"
```

**Check Network**
```bash
curl http://localhost:5678/healthz
```

**Solutions:**
- Wait 2-3 minutes for full startup
- Check Windows Firewall
- Try: http://127.0.0.1:5678

### "Database connection errors"

**Check PostgreSQL**
```bash
docker logs postgres-dev
```

**Reset Database**
```bash
docker-compose down
docker volume rm n8n-docker_postgres_data
docker-compose up -d
```

## 🔗 Integration Issues

### "Workflows won't import"

**Verify JSON Format**
- Copy exact output from N8N_Builder
- Check for truncated JSON
- Validate JSON syntax online

**Check n8n Version**
- Ensure n8n version supports generated nodes
- Update n8n: `docker-compose pull`

**Solutions:**
- Regenerate workflow in N8N_Builder
- Try importing smaller workflow first
- Check n8n logs during import

### "Nodes show errors"

**Missing Node Types**
- Check if custom nodes are installed
- Verify n8n version compatibility

**Configuration Issues**
- Check node credentials
- Verify external service connections
- Test with manual execution

### "Webhooks not working"

**Check LocalTunnel**
```bash
# Verify LocalTunnel SSH process is running
Get-Process -Name "ssh" | Where-Object { $_.CommandLine -like "*localhost.run*" }

# Check if n8n is accessible locally
curl http://localhost:5678
```

**Update Webhook URLs**
- Get current LocalTunnel URL from SSH terminal output
- Update external service webhook settings with new URL
- Test webhook with curl using the LocalTunnel URL

**Solutions:**
- Restart LocalTunnel: `ssh -R 80:localhost:5678 nokey@localhost.run`
- Update docker-compose.yml with new tunnel URL
- Restart n8n container: `docker-compose stop n8n && docker-compose up -d n8n`
- Verify webhook URL format: `https://[tunnel-id].lhr.life/webhook/[path]`

## 🔍 Diagnostic Commands

### System Health Check
```bash
# N8N_Builder
curl http://localhost:8002/health

# n8n
curl http://localhost:5678/healthz

# Docker
docker-compose ps

# nGrok (if running)
curl http://127.0.0.1:4040/api/tunnels
```

### Log Locations
```bash
# N8N_Builder logs
tail -f logs/n8n_builder.log

# n8n logs  
docker logs n8n-dev -f

# PostgreSQL logs
docker logs postgres-dev -f

# Docker compose logs
docker-compose logs -f
```

### Port Usage Check
```bash
# Windows
netstat -an | findstr "8002 8003 5678 5432"

# Linux/Mac
netstat -an | grep -E "(8002|8003|5678|5432)"
```

## 🆘 Getting Help

### Before Asking for Help
1. **Check this troubleshooting guide**
2. **Review relevant logs**
3. **Try the emergency quick fixes**
4. **Document error messages exactly**

### Where to Get Help
- **📖 Documentation**: [Architecture Overview](../Architecture.md)
- **💬 n8n Community**: https://community.n8n.io/
- **🐛 GitHub Issues**: https://github.com/vbwyrde/N8N_Builder/issues
- **📧 Email Support**: Include logs and error messages

### Information to Include
- Operating system and version
- Python version (`python --version`)
- Docker version (`docker --version`)
- Exact error messages
- Steps to reproduce
- Relevant log excerpts

---

**💡 Pro Tip**: Most issues are resolved by restarting services and checking logs. When in doubt, try the "Complete Reset" procedure above.
