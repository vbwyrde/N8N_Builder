# 🔒 Security Guidelines for n8n Docker Environment

## 📚 Related Documentation

- **🚀 [Quick Start](QUICK_START.md)** - Fast setup with security warnings
- **📖 [Main README](README.md)** - Complete documentation hub
- **🔑 [Credentials Setup](CREDENTIALS_SETUP.md)** - Secure external service setup
- **🤖 [Automation Guide](AUTOMATION-README.md)** - Secure automation practices
- **🔐 [SSL Guide](../ssl/README.md)** - SSL certificate management

## 🚨 CRITICAL SECURITY WARNING

**⚠️ DEFAULT CREDENTIALS ARE PUBLICLY KNOWN** - Change them immediately before use!

This repository contains templates and automation scripts for n8n development. **All sensitive configuration files are excluded from version control** to protect your credentials and personal information.

## 🚫 Files EXCLUDED from Repository (Protected)

The following files contain sensitive information and are **automatically excluded** via `.gitignore`:

### 🔑 Configuration Files (SENSITIVE)
- **`.env`** - Contains passwords, encryption keys, API credentials, database passwords
- **`config.ps1`** - Contains personal file paths, nGrok paths, system-specific settings
- **`.env.local`**, **`.env.production`**, **`.env.dev`** - Environment-specific configurations

### 🔐 Security & Certificate Files (SENSITIVE)
- **`*.key`**, **`*.pem`**, **`*.crt`** - SSL certificates and private keys
- **`ssl/*.key`**, **`ssl/*.pem`**, **`ssl/*.crt`** - SSL certificate files
- **`*.p12`**, **`*.pfx`** - Certificate bundles

### 📊 Data Directories (SENSITIVE)
- **`data/workflows/*`** - Your n8n workflows (may contain API keys, sensitive logic)
- **`data/credentials/*`** - Encrypted credential storage (OAuth tokens, API keys)
- **`data/executions/*`** - Execution logs (may contain sensitive data, API responses)
- **`data/database/*`** - Database files (SQLite databases with all data)
- **`backups/*`** - Database backups (contain ALL your data and credentials)
- **`logs/*`** - Log files (may contain sensitive information)

### 🔧 System Files (SENSITIVE)
- **`ngrok-config.yml`** - nGrok configuration with auth tokens
- **`*.log`** - Log files that may contain sensitive data

## ✅ Safe Files in Repository (Public)

These files are **safe to include** in public repositories:

- **`.env.template`** - Template with placeholder values only
- **`config.ps1.template`** - Template with example paths only
- **`docker-compose.yml`** - Docker configuration (no secrets embedded)
- **`docker-compose.dev.yml`** - Development Docker configuration
- **`*.md`** - Documentation files
- **`*.ps1`** - Automation scripts (reference config files, no hardcoded secrets)
- **`*.bat`** - Batch files (reference config files)
- **`*.sh`** - Shell scripts (reference config files)
- **`ssl/README.md`** - SSL documentation (no actual certificates)

## 🛡️ CRITICAL Security Best Practices

### 🚨 1. Change Default Credentials IMMEDIATELY

**⚠️ DANGER**: Default credentials are publicly known and used by attackers!

```bash
# In your .env file, change ALL of these:
N8N_BASIC_AUTH_USER=admin                           # ❌ CHANGE THIS
N8N_BASIC_AUTH_PASSWORD=admin123                    # ❌ CHANGE THIS
N8N_ENCRYPTION_KEY=CHANGE-THIS-TO-A-SECURE-RANDOM-KEY # ❌ CHANGE THIS
DB_POSTGRESDB_PASSWORD=CHANGE-THIS-PASSWORD         # ❌ CHANGE THIS
```

**✅ Use strong credentials:**
- **Username**: 8+ characters, avoid common names
- **Password**: 16+ characters, mix of letters/numbers/symbols
- **Encryption Key**: 32+ characters, cryptographically random

### 🔑 2. Generate Secure Encryption Key

**Option A - PowerShell (Recommended):**
```powershell
# Generate cryptographically secure 32-character key
[System.Web.Security.Membership]::GeneratePassword(32, 8)
```

**Option B - OpenSSL:**
```bash
# Generate base64 encoded key (Linux/Mac/Windows with OpenSSL)
openssl rand -base64 32
```

**Option C - Online (Use with caution):**
- Use only reputable generators
- Generate locally when possible
- Never use the same key across environments

### 🗄️ 3. Database Security

**PostgreSQL Security:**
```bash
# Strong database password (16+ characters)
DB_POSTGRESDB_PASSWORD=YourSecureDBPassword123!

# Database user (avoid 'postgres' for production)
DB_POSTGRESDB_USER=n8n_user
```

### 🌐 4. nGrok Security Considerations

**Free Plan Limitations:**
- ⚠️ Shows warning page to visitors
- ⚠️ URLs change on restart (can break webhooks)
- ⚠️ Limited to 1 tunnel at a time

**Security Benefits:**
- ✅ URLs change frequently (harder to target)
- ✅ HTTPS termination handled by nGrok
- ✅ Basic auth still protects n8n interface

**Paid Plan Benefits:**
- ✅ Custom/static subdomains
- ✅ No warning page
- ✅ Multiple tunnels
- ✅ Better for production use

### 🔒 5. Network Security

**Local Security:**
- ✅ n8n runs on `localhost:5678` (not exposed externally)
- ✅ Only nGrok tunnel provides external access
- ✅ Basic auth protects the n8n interface
- ✅ Docker network isolation

**External Access:**
- ⚠️ nGrok tunnel bypasses local firewall
- ⚠️ Basic auth is your primary protection
- ⚠️ Monitor nGrok access logs regularly

## 🔧 Secure First-Time Setup Process

### 🚀 Step 1: Run Setup Script
```powershell
# Navigate to n8n-docker directory first
cd n8n-docker

# Run setup script (creates .env and config.ps1 from templates)
powershell -ExecutionPolicy Bypass -File "setup.ps1"
```

**What this creates:**
- ✅ `.env` file with default values (⚠️ **MUST CHANGE DEFAULTS**)
- ✅ `config.ps1` file with template paths
- ✅ Required directory structure

### 🔒 Step 2: Secure Configuration (CRITICAL)
```bash
# Edit these files immediately (they won't be committed):
.env          # ⚠️ CHANGE ALL DEFAULT PASSWORDS AND KEYS
config.ps1    # Update nGrok path and system-specific settings
```

**Required changes in `.env`:**
```bash
# CHANGE THESE IMMEDIATELY:
N8N_BASIC_AUTH_USER=your-secure-username
N8N_BASIC_AUTH_PASSWORD=your-secure-password-16-chars-min
N8N_ENCRYPTION_KEY=your-32-character-random-encryption-key
DB_POSTGRESDB_PASSWORD=your-secure-database-password
```

### 🔍 Step 3: Verify Security Setup
```bash
# Check what would be committed to git:
git status

# These files should NOT appear in git status (protected by .gitignore):
# ❌ .env
# ❌ config.ps1
# ❌ data/
# ❌ backups/
# ❌ logs/
# ❌ ssl/*.key, ssl/*.pem

# If any sensitive files appear, they are NOT protected!
```

### 🛡️ Step 4: Test Security
```bash
# Verify basic auth works:
# 1. Start n8n: docker-compose up -d
# 2. Visit: http://localhost:5678
# 3. Should prompt for username/password
# 4. Should NOT accept default admin/admin123

# Verify encryption key works:
# 1. Create a credential in n8n
# 2. Check it's encrypted in data/credentials/
```

## 🚨 EMERGENCY: If You Accidentally Commit Secrets

### 🔥 Immediate Actions (Do These NOW)

1. **🚨 STOP**: Don't push to remote if you haven't already
2. **🔄 Rotate ALL compromised credentials immediately**
3. **🗑️ Remove from Git history**

### 🛠️ Step 1: Remove from Git History
```bash
# Remove file from git tracking but keep locally
git rm --cached .env
git rm --cached config.ps1

# Commit the removal
git commit -m "Remove sensitive files from tracking"

# For files already in history, use BFG Repo-Cleaner:
# Download from: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files .env
java -jar bfg.jar --delete-files config.ps1
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

### 🔄 Step 2: Rotate ALL Compromised Credentials
```bash
# Change EVERYTHING in .env:
N8N_BASIC_AUTH_USER=new-username
N8N_BASIC_AUTH_PASSWORD=new-secure-password
N8N_ENCRYPTION_KEY=new-32-character-key
DB_POSTGRESDB_PASSWORD=new-database-password

# Update external service credentials:
# - Google OAuth credentials
# - nGrok auth token
# - Any API keys used in workflows
```

### 🛡️ Step 3: Update .gitignore
```bash
# Ensure .gitignore includes all sensitive files
echo ".env" >> .gitignore
echo "config.ps1" >> .gitignore
echo "data/" >> .gitignore
echo "backups/" >> .gitignore
echo "logs/" >> .gitignore
echo "ssl/*.key" >> .gitignore
echo "ssl/*.pem" >> .gitignore

git add .gitignore
git commit -m "Add comprehensive .gitignore for sensitive files"
```

### 🔍 Step 4: Verify Clean History
```bash
# Search for any remaining sensitive data
git log --all --full-history -- .env
git log --all --full-history -- config.ps1

# Should return no results if properly cleaned
```

## 📋 Pre-Deployment Security Checklist

**Before sharing code or deploying:**

### 🔍 Repository Security
- [ ] `.env` file is NOT in git repository
- [ ] `config.ps1` file is NOT in git repository
- [ ] `data/` directory is NOT in git repository
- [ ] `backups/` directory is NOT in git repository
- [ ] `logs/` directory is NOT in git repository
- [ ] SSL certificates are NOT in git repository
- [ ] No hardcoded passwords in any files
- [ ] No hardcoded API keys in any files
- [ ] No personal file paths in committed scripts

### 🔒 Credential Security
- [ ] Default passwords have been changed
- [ ] Encryption key has been generated (32+ characters)
- [ ] Database password is strong (16+ characters)
- [ ] Basic auth credentials are strong
- [ ] All external service credentials are configured
- [ ] OAuth applications use correct redirect URLs

### 🌐 Network Security
- [ ] nGrok authentication is configured
- [ ] Basic auth is enabled and working
- [ ] SSL certificates are valid (if using HTTPS)
- [ ] Firewall rules are appropriate
- [ ] Access logs are being monitored

## 🔍 Regular Security Maintenance Schedule

### 📅 Weekly Tasks
- [ ] Review access logs for suspicious activity
- [ ] Check nGrok tunnel usage and connections
- [ ] Verify all containers are running latest security patches
- [ ] Monitor disk space (logs and backups can grow large)

### 📅 Monthly Tasks
- [ ] **Rotate passwords** (basic auth, database, encryption key)
- [ ] **Update n8n** to latest version: `docker-compose pull && docker-compose up -d`
- [ ] **Review workflow permissions** and credential usage
- [ ] **Check for exposed credentials** in logs and execution history
- [ ] **Audit external service connections** and OAuth applications
- [ ] **Clean up old backups** and log files

### 📅 Quarterly Tasks
- [ ] **Full security audit** of all configurations
- [ ] **Review and update** all external service credentials
- [ ] **Test backup and restore** procedures
- [ ] **Update SSL certificates** (if using HTTPS)
- [ ] **Review nGrok account** and consider upgrading plan

### 📅 Before Sharing/Deploying
- [ ] Run `git status` to check for sensitive files
- [ ] Review commit history: `git log --oneline -10`
- [ ] Verify `.gitignore` is working: `git check-ignore .env config.ps1`
- [ ] Test with fresh clone to ensure no sensitive data
- [ ] Verify all default credentials have been changed

## 🚨 Security Incident Response

### If You Discover a Security Issue:

1. **🛑 IMMEDIATE**: Stop any running services if actively compromised
2. **🔍 ASSESS**: Determine scope of potential exposure
3. **🔄 ROTATE**: Change all potentially compromised credentials
4. **📝 DOCUMENT**: Record what happened and how it was fixed
5. **🛡️ PREVENT**: Update procedures to prevent recurrence

### If Credentials Are Exposed:

1. **🚨 URGENT**: Rotate ALL credentials immediately
2. **🔍 AUDIT**: Check all external services for unauthorized access
3. **📊 MONITOR**: Watch for unusual activity in connected services
4. **🗑️ CLEAN**: Remove from git history if committed
5. **📚 LEARN**: Update security practices and documentation

## 📞 Getting Security Help

### Internal Resources
- **📖 Documentation**: Review all security sections in this guide
- **🔍 Troubleshooting**: Check [README.md](README.md) troubleshooting section
- **🤖 Automation**: Use [AUTOMATION-README.md](AUTOMATION-README.md) for script security

### External Resources
- **💬 n8n Community**: https://community.n8n.io/ (for n8n-specific security)
- **🐳 Docker Security**: https://docs.docker.com/engine/security/
- **🌐 nGrok Security**: https://ngrok.com/docs/security/
- **🔒 OWASP Guidelines**: https://owasp.org/www-project-top-ten/

### Emergency Contacts
- **🚨 If credentials are actively being misused**: Contact the affected service providers immediately
- **🔍 If unsure about exposure**: Err on the side of caution and rotate credentials

---

**🛡️ Remember**: Security is an ongoing process, not a one-time setup. Stay vigilant and keep your security practices up to date!
