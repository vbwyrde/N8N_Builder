# 🔒 Essential Security Setup

**🎯 Goal**: Secure your n8n installation for safe operation (15 minutes)

## 🚨 Critical First Steps

### 1. Change Default Credentials (REQUIRED)
**⚠️ Default credentials are publicly known - change immediately!**

```bash
# Default credentials (INSECURE):
Username: admin
Password: admin
```

**To Change:**
1. **Login** to n8n: http://localhost:5678
2. **Go to**: Settings → Users
3. **Click** your user profile
4. **Change password** to something strong
5. **Update email** if needed

### 2. Verify Protected Files
These files contain sensitive data and are automatically protected:

**✅ Protected (never committed to git):**
- `.env` - Passwords, API keys, encryption keys
- `config.ps1` - Personal paths and settings
- `*.key`, `*.pem`, `*.crt` - SSL certificates

**Check protection:**
```bash
# These commands should show "not found" (good!)
git status | findstr ".env"
git status | findstr "config.ps1"
```

## 🔐 Essential Security Configuration

### Generate Secure Encryption Key
n8n uses an encryption key to protect sensitive data:

```bash
# Generate a secure 32-character key
# Use a password generator or:
openssl rand -hex 32
```

**Update .env file:**
```bash
N8N_ENCRYPTION_KEY=your-32-character-key-here
```

### Configure Basic Authentication
Add an extra layer of security:

```bash
# In .env file:
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=your-username
N8N_BASIC_AUTH_PASSWORD=your-strong-password
```

### Set Secure Database Password
```bash
# In .env file:
POSTGRES_PASSWORD=your-secure-database-password
POSTGRES_USER=n8n_user
```

## 🌐 nGrok Security

### Free Tier Limitations
- **Public URLs** - Anyone with URL can access
- **Changing URLs** - New URL each restart
- **No authentication** - Built-in nGrok auth not available

### Secure nGrok Usage
```bash
# Use authentication (paid plans)
ngrok http 5678 --auth="username:password"

# Use custom domains (paid plans)
ngrok http 5678 --hostname=your-domain.ngrok.io
```

### Production Recommendations
- **Upgrade to paid nGrok** for custom domains and auth
- **Use VPN** for internal access only
- **Implement IP whitelisting** where possible
- **Monitor access logs** regularly

## 🔒 File System Security

### Secure Permissions
```bash
# Windows - Restrict .env file access
icacls .env /grant:r "%USERNAME%:F" /inheritance:r

# Linux/Mac - Restrict .env file access  
chmod 600 .env
```

### Backup Security
```bash
# Secure backup location (not in project folder)
# Update config.ps1:
$BackupPath = "C:\SecureBackups\n8n"
```

## 🛡️ Network Security

### Local Network Only
For maximum security, disable external access:

```bash
# In docker-compose.yml, remove nGrok and use:
ports:
  - "127.0.0.1:5678:5678"  # Only localhost access
```

### Firewall Configuration
```bash
# Windows Firewall - Block external access to n8n port
netsh advfirewall firewall add rule name="Block n8n External" dir=in action=block protocol=TCP localport=5678 remoteip=!127.0.0.1
```

## 🔍 Security Monitoring

### Check Running Services
```bash
# Verify only expected services are running
docker-compose ps
netstat -an | findstr "5678 5432"
```

### Monitor Access Logs
```bash
# Check n8n logs for suspicious activity
docker logs n8n-dev | findstr "login\|auth\|error"

# Check nGrok access logs
# Open: http://127.0.0.1:4040
```

### Regular Security Checks
- **Weekly**: Review access logs
- **Monthly**: Update passwords and keys
- **Quarterly**: Review user permissions
- **As needed**: Update Docker images

## 🚨 Security Incident Response

### If Credentials Compromised
1. **Immediately change** all passwords
2. **Regenerate** encryption keys
3. **Review** all workflows for sensitive data
4. **Check** access logs for unauthorized activity
5. **Update** external service credentials

### If System Compromised
1. **Stop** all services immediately
2. **Disconnect** from network
3. **Backup** current state for analysis
4. **Restore** from clean backup
5. **Investigate** compromise vector

## ✅ Security Checklist

**Initial Setup:**
- [ ] Changed default admin password
- [ ] Generated secure encryption key
- [ ] Set strong database password
- [ ] Verified protected files are excluded from git

**Network Security:**
- [ ] Configured nGrok authentication (if using paid plan)
- [ ] Set up firewall rules
- [ ] Limited network access as needed

**Ongoing Security:**
- [ ] Regular password updates
- [ ] Access log monitoring
- [ ] Backup security verification
- [ ] Docker image updates

## 🆘 Security Help

### Common Security Issues
- **"Can't login after password change"**: Check browser cache, try incognito mode
- **"Encryption key errors"**: Ensure key is exactly 32 characters
- **"nGrok tunnel exposed"**: Consider paid plan with authentication

### Security Resources
- **📖 [n8n Security Docs](https://docs.n8n.io/hosting/security/)**
- **🔒 [Docker Security Guide](https://docs.docker.com/engine/security/)**
- **🌐 [nGrok Security](https://ngrok.com/docs/security/)**

---

**🎉 Security Setup Complete!** Your n8n installation now has essential security measures in place.

**Next Steps:**
- **[Credentials Setup](CREDENTIALS_SETUP.md)** - Connect external services securely
- **[Automation Setup](AUTOMATION_SETUP.md)** - Secure automation practices
- **[Advanced Security](../technical/ADVANCED_SECURITY.md)** - Production hardening
