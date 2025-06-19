# n8n Docker Development Environment

This directory contains a complete Docker-based development environment for n8n workflow automation. The setup follows best practices from the [official n8n Docker hosting guide](https://osher.com.au/blog/how-to-host-n8n-with-docker/).

## 📁 Directory Structure

```
n8n-docker/
├── README.md                    # This file
├── .env                        # Environment configuration
├── docker-compose.yml          # Full production setup with PostgreSQL
├── docker-compose.dev.yml      # Simplified development setup with SQLite
├── config/                     # Configuration files
├── data/                       # Local data directory
├── ssl/                        # SSL certificates (for HTTPS)
├── backups/                    # Backup storage
└── scripts/                    # Utility scripts
    ├── setup-docker.sh         # Initial setup script (Linux/Mac)
    ├── setup-docker.bat        # Initial setup script (Windows)
    ├── backup.sh               # Backup script (Linux/Mac)
    ├── backup.bat              # Backup script (Windows)
    ├── restore.sh              # Restore script (Linux/Mac)
    └── maintenance.sh           # Maintenance utilities (Linux/Mac)
```

## 🔒 Security First

**IMPORTANT**: This repository excludes sensitive files for security. Before starting:

1. **Run setup**: `powershell -ExecutionPolicy Bypass -File "setup.ps1"`
2. **Edit `.env`**: Change default passwords and encryption key
3. **Edit `config.ps1`**: Set your nGrok path

See [SECURITY.md](SECURITY.md) for complete security guidelines.

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed and running
- At least 4GB RAM and 20GB storage available
- Basic familiarity with command line

### 1. Initial Setup

**On Windows:**
```cmd
cd n8n-docker/scripts
setup-docker.bat
```

**On Linux/Mac:**
```bash
cd n8n-docker/scripts
./setup-docker.sh
```

### 2. Configure Environment

Edit the `.env` file to customize your setup:
- Change `N8N_ENCRYPTION_KEY` to a secure random string
- Update `N8N_BASIC_AUTH_USER` and `N8N_BASIC_AUTH_PASSWORD`
- Modify other settings as needed

### 3. Start n8n

**For Development (SQLite):**
```bash
docker-compose -f docker-compose.dev.yml up -d
```

**For Production (PostgreSQL):**
```bash
docker-compose up -d
```

### 4. Access n8n

Open your browser and navigate to: http://localhost:5678

Default credentials (if basic auth is enabled):
- Username: admin
- Password: admin123 (change this!)

## 🔧 Configuration Options

### Environment Variables

Key variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `N8N_HOST` | Host name for n8n | localhost |
| `N8N_PORT` | Port for n8n web interface | 5678 |
| `N8N_PROTOCOL` | Protocol (http/https) | http |
| `N8N_ENCRYPTION_KEY` | Encryption key for sensitive data | (change this!) |
| `DB_TYPE` | Database type (sqlite/postgresdb) | sqlite |
| `N8N_BASIC_AUTH_ACTIVE` | Enable basic authentication | true |

### Docker Compose Files

- **docker-compose.dev.yml**: Lightweight setup with SQLite, perfect for development
- **docker-compose.yml**: Full production setup with PostgreSQL and Redis support

## 📊 Management Commands

### View Container Status
```bash
docker-compose ps
```

### View Logs
```bash
docker-compose logs -f n8n
```

### Stop Services
```bash
docker-compose down
```

### Update n8n
```bash
# Linux/Mac
./scripts/maintenance.sh --update

# Windows
docker-compose pull
docker-compose up -d
```

## 💾 Backup and Restore

### Create Backup

**Linux/Mac:**
```bash
./scripts/backup.sh
```

**Windows:**
```cmd
scripts\backup.bat
```

### Restore from Backup

**Linux/Mac:**
```bash
./scripts/restore.sh backup_filename.tar.gz
```

Backups include:
- All workflow data
- Credentials and settings
- Database content
- Configuration files

## 🔒 Security Considerations

### Development Environment
- Basic authentication is enabled by default
- Uses HTTP (not HTTPS)
- SQLite database (single file)

### Production Environment
- Change default passwords immediately
- Use strong encryption keys
- Consider enabling HTTPS with SSL certificates
- Use PostgreSQL for better performance
- Implement proper firewall rules

### SSL/HTTPS Setup

1. Place SSL certificates in the `ssl/` directory
2. Update `.env` file:
   ```
   N8N_PROTOCOL=https
   N8N_SSL_KEY=/etc/ssl/certs/privkey.pem
   N8N_SSL_CERT=/etc/ssl/certs/fullchain.pem
   ```
3. Restart containers

## 🔧 Troubleshooting

### Container Won't Start
1. Check Docker is running: `docker info`
2. View logs: `docker-compose logs n8n`
3. Verify port 5678 is not in use
4. Check environment variables in `.env`

### Can't Access n8n Web Interface
1. Verify container is running: `docker-compose ps`
2. Check port mapping: `docker port n8n`
3. Try accessing via container IP
4. Check firewall settings

### Database Connection Issues
1. For PostgreSQL: ensure database container is running
2. Check database credentials in `.env`
3. Verify network connectivity between containers

### Performance Issues
1. Increase Docker memory allocation
2. Monitor resource usage: `docker stats`
3. Consider switching to PostgreSQL for better performance

## 📚 Additional Resources

- [n8n Official Documentation](https://docs.n8n.io/)
- [n8n Community Forum](https://community.n8n.io/)
- [Docker Documentation](https://docs.docker.com/)
- [n8n Docker Hub](https://hub.docker.com/r/n8nio/n8n)

## 🤝 Integration with N8N_Builder Project

This Docker environment is designed to work seamlessly with the main N8N_Builder project:

- The `../projects` directory is mounted as `/home/node/projects` in the container
- Workflows created in n8n can reference files in the projects directory
- The N8N_Builder application can interact with n8n via its REST API
- Shared data directory for easy file exchange

## 📝 Maintenance Schedule

### Daily
- Monitor container health
- Check log files for errors

### Weekly
- Create backups
- Update n8n image
- Clean up old Docker images

### Monthly
- Review security settings
- Update SSL certificates (if applicable)
- Archive old backups

---

**Need Help?** Check the troubleshooting section above or consult the n8n community forums.
