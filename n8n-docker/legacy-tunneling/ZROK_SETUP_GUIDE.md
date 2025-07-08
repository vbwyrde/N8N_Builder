# Zrok Self-Hosted Setup Guide

## 🎯 Overview

This guide sets up a **self-hosted zrok instance** that provides **stable URLs** for your n8n webhooks. Unlike ngrok's free tier that generates random URLs, zrok gives you consistent URLs that never change between restarts.

## 🏗️ Architecture

```
Internet → Zrok Frontend (localhost:8080) → Zrok Controller → OpenZiti Network → n8n (localhost:5678)
```

**Key Benefits:**
- ✅ **Stable URLs** - Never change between restarts
- ✅ **Self-hosted** - No external dependencies
- ✅ **Free** - No subscription costs
- ✅ **Secure** - Built on OpenZiti zero-trust networking
- ✅ **Docker-based** - Easy deployment and management

## 🚀 Quick Start

### 1. Initial Setup

```powershell
# Navigate to n8n-docker directory
cd n8n-docker

# Copy and customize zrok environment file
copy .env.zrok.template .env.zrok
# Edit .env.zrok and change the default tokens/passwords

# Start both n8n and zrok services
.\Start-N8N-Zrok.ps1
```

### 2. First-Time Configuration

The startup script will automatically:
1. Start OpenZiti controller and router
2. Start zrok controller and frontend
3. Initialize zrok environment
4. Create a reserved share for stable URLs
5. Update n8n webhook configuration

### 3. Access Your Services

- **n8n Interface**: http://localhost:5678
- **Stable Webhook URL**: http://localhost:8080
- **Zrok Controller API**: http://localhost:18080

## 📋 Detailed Setup Steps

### Step 1: Environment Configuration

Edit `.env.zrok` and customize these values:

```bash
# Change these default tokens for security
ZROK_ADMIN_TOKEN=your-secure-admin-token
ZROK_FRONTEND_TOKEN=your-secure-frontend-token
ZITI_PWD=your-secure-ziti-password

# Domain settings (can keep as localhost for local development)
ZROK_DOMAIN=localhost
ZROK_PUBLIC_PORT=8080
```

### Step 2: Start Services

```powershell
# Full startup (recommended)
.\Start-N8N-Zrok.ps1

# Or start components separately
.\Start-N8N-Zrok.ps1 -SkipDocker    # Only start zrok
.\Start-N8N-Zrok.ps1 -SkipZrok      # Only start n8n
```

### Step 3: Verify Setup

Check that all services are running:

```powershell
# Check service status
docker ps

# Test n8n access
curl http://localhost:5678/healthz

# Test zrok public access
curl http://localhost:8080/health

# Test zrok controller API
curl http://localhost:18080/api/v1/version
```

## 🔧 Configuration Details

### Zrok Controller Configuration

The controller is configured via `zrok-config/controller.yml`:

- **API Endpoint**: http://localhost:18080
- **Database**: SQLite (stored in Docker volume)
- **Frontend URL**: http://localhost:8080
- **Reserved Domains**: n8n-webhooks.localhost, stable.localhost

### Network Architecture

- **zrok-network**: Internal network for zrok components
- **n8n-network**: Shared with existing n8n setup
- **Cross-network access**: zrok-share connects to both networks

### Volume Management

Persistent data is stored in Docker volumes:
- `zrok_ziti_controller_data`: OpenZiti controller data
- `zrok_ziti_router_data`: OpenZiti router data
- `zrok_controller_data`: Zrok controller database
- `zrok_frontend_data`: Frontend configuration
- `zrok_share_data`: Share service data

## 🛠️ Management Commands

### Start/Stop Services

```powershell
# Start everything
.\Start-N8N-Zrok.ps1

# Stop everything
.\Stop-N8N-Zrok.ps1

# Keep n8n running, stop only zrok
.\Stop-N8N-Zrok.ps1 -KeepDocker

# Keep zrok running, stop only n8n
.\Stop-N8N-Zrok.ps1 -KeepZrok
```

### Manual Zrok Commands

```powershell
# Access zrok container for manual commands
docker exec -it zrok-share bash

# Inside container:
zrok status                    # Check environment status
zrok ls                       # List shares
zrok reserve public http://n8n:5678  # Create new reserved share
```

## 🔍 Troubleshooting

### Common Issues

**1. Services not starting**
```powershell
# Check Docker logs
docker-compose -f docker-compose.zrok.yml logs

# Check specific service
docker logs zrok-controller
```

**2. Zrok environment not initialized**
```powershell
# Manually initialize
docker exec -it zrok-share zrok enable http://zrok-controller:18080
```

**3. Reserved share creation fails**
```powershell
# Check zrok controller status
curl http://localhost:18080/api/v1/version

# Manually create share
docker exec -it zrok-share zrok reserve public --backend-mode proxy http://n8n:5678
```

**4. n8n can't access webhooks**
- Verify webhook URL in n8n settings: http://localhost:8080
- Check that zrok-frontend is running and accessible
- Test direct access: `curl http://localhost:8080`

### Health Checks

All services include health checks. Check status:

```powershell
# View health status
docker ps --format "table {{.Names}}\t{{.Status}}"

# Detailed health info
docker inspect zrok-controller --format='{{.State.Health.Status}}'
```

## 🔐 Security Considerations

### Default Security

- All services run in isolated Docker networks
- OpenZiti provides zero-trust networking
- Default tokens should be changed in production

### Production Hardening

1. **Change default passwords** in `.env.zrok`
2. **Enable HTTPS** by configuring SSL certificates
3. **Restrict network access** using Docker network policies
4. **Monitor logs** for suspicious activity

## 🎯 Next Steps

1. **Update OAuth Applications**: Use `http://localhost:8080` as your stable webhook URL
2. **Test Webhook Delivery**: Create test workflows to verify webhook reception
3. **Monitor Performance**: Check zrok controller logs for any issues
4. **Backup Configuration**: Save your `.env.zrok` and `zrok-config/` files

## 📚 Additional Resources

- **Zrok Documentation**: https://docs.zrok.io/
- **OpenZiti Documentation**: https://docs.openziti.io/
- **Docker Compose Reference**: https://docs.docker.com/compose/

---

**🎉 Congratulations!** You now have a stable, self-hosted tunneling solution that eliminates the ngrok URL change problem!
