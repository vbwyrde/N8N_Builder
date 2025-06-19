# 🔒 Security Guidelines

## ⚠️ Important Security Notes

This repository contains templates and automation scripts for n8n development. **Sensitive configuration files are excluded from version control** to protect your credentials and personal information.

## 🚫 Files NOT Included in Repository

The following files contain sensitive information and are **automatically excluded** via `.gitignore`:

### Configuration Files
- **`.env`** - Contains passwords, encryption keys, and API credentials
- **`config.ps1`** - Contains personal file paths and system-specific settings
- **`.env.local`**, **`.env.production`** - Environment-specific configurations

### Security Files
- **`*.key`**, **`*.pem`**, **`*.crt`** - SSL certificates and private keys
- **`ssl/*.key`**, **`ssl/*.pem`** - SSL certificate files

### Data Directories
- **`data/workflows/*`** - Your n8n workflows (may contain sensitive logic)
- **`data/credentials/*`** - Encrypted credential storage
- **`data/executions/*`** - Execution logs (may contain sensitive data)
- **`backups/*`** - Database backups (contain all your data)

## ✅ Safe Files in Repository

These files are **safe to include** in public repositories:

- **`.env.template`** - Template with placeholder values
- **`config.ps1.template`** - Template with example paths
- **`docker-compose.yml`** - Docker configuration (no secrets)
- **`*.md`** - Documentation files
- **`*.ps1`** - Automation scripts (use templates for config)
- **`*.bat`** - Batch files (reference config files)

## 🛡️ Security Best Practices

### 1. Change Default Credentials
```bash
# In your .env file, change these defaults:
N8N_BASIC_AUTH_USER=admin                    # ❌ Change this
N8N_BASIC_AUTH_PASSWORD=CHANGE-THIS-PASSWORD # ❌ Change this
N8N_ENCRYPTION_KEY=CHANGE-THIS-TO-A-SECURE-RANDOM-KEY # ❌ Change this
```

### 2. Generate Secure Encryption Key
```bash
# Use a secure random key generator:
openssl rand -base64 32

# Or use PowerShell:
[System.Web.Security.Membership]::GeneratePassword(32, 8)
```

### 3. Database Security
If using PostgreSQL:
```bash
# Change default database password:
DB_POSTGRESDB_PASSWORD=CHANGE-THIS-PASSWORD  # ❌ Change this
```

### 4. nGrok Security
- **Free Plan**: Shows warning page to visitors
- **Paid Plan**: Consider using custom domains
- **URLs Change**: Free plan URLs change on restart (good for security)

### 5. Network Security
- n8n runs on `localhost:5678` (not exposed externally)
- Only nGrok tunnel provides external access
- Basic auth protects the n8n interface

## 🔧 First-Time Setup

### 1. Run Setup Script
```powershell
# This creates .env and config.ps1 from templates
powershell -ExecutionPolicy Bypass -File "setup.ps1"
```

### 2. Customize Configuration
```bash
# Edit these files (they won't be committed):
.env          # Update passwords and keys
config.ps1    # Update file paths
```

### 3. Verify Security
```bash
# Check what would be committed:
git status

# These should NOT appear in git status:
# .env, config.ps1, data/, backups/
```

## 🚨 If You Accidentally Commit Secrets

### 1. Remove from Git History
```bash
# Remove file from git but keep locally
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from tracking"

# For files already in history, use git filter-branch or BFG
```

### 2. Rotate Compromised Credentials
- Change all passwords in `.env`
- Generate new encryption key
- Update any external service credentials

### 3. Update .gitignore
```bash
# Ensure .gitignore includes the file
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to .gitignore"
```

## 📋 Security Checklist

Before sharing or deploying:

- [ ] `.env` file is not in git repository
- [ ] `config.ps1` file is not in git repository
- [ ] Default passwords have been changed
- [ ] Encryption key has been generated
- [ ] SSL certificates (if any) are not in repository
- [ ] Backup files are not in repository
- [ ] Personal file paths are not hardcoded in scripts

## 🔍 Regular Security Maintenance

### Monthly
- [ ] Review and rotate passwords
- [ ] Check for exposed credentials in logs
- [ ] Update n8n to latest version
- [ ] Review workflow permissions

### Before Sharing
- [ ] Run `git status` to check for sensitive files
- [ ] Review commit history for accidentally committed secrets
- [ ] Verify `.gitignore` is working correctly

## 📞 Security Issues

If you discover a security vulnerability:

1. **Do NOT** create a public issue
2. Check if credentials were accidentally committed
3. Rotate any potentially compromised credentials
4. Update security practices

---

**Remember**: Security is a process, not a one-time setup. Regularly review and update your security practices!
