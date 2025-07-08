# Migration Guide: From ngrok to Stable URL Solution

## 🎯 Overview

This guide helps you migrate from the old ngrok-based setup to the new **Stable URL Proxy** solution that provides permanent webhook URLs.

## ✅ Benefits of Migration

### Before (ngrok)
- ❌ URL changes every restart: `https://abc123.ngrok-free.app`
- ❌ Manual OAuth credential updates required
- ❌ External service dependency
- ❌ Complex setup and maintenance

### After (Stable URL)
- ✅ URL never changes: `http://localhost:8080`
- ✅ Zero maintenance required
- ✅ No external dependencies
- ✅ Simple one-command startup

## 🚀 Quick Migration (5 minutes)

### Step 1: Update Your Startup Process
**Old way:**
```bash
.\Start-N8N-NgRok.ps1
```

**New way:**
```bash
.\start-n8n.bat
# OR directly:
.\Start-N8N-Stable.ps1
```

### Step 2: Update OAuth Applications
Replace all ngrok URLs in your OAuth apps with the stable URL:

| Service | Old URL Pattern | New Stable URL |
|---------|----------------|----------------|
| **Google OAuth** | `https://xyz.ngrok-free.app/rest/oauth2-credential/callback` | `http://localhost:8080/rest/oauth2-credential/callback` |
| **Twitter OAuth** | `https://xyz.ngrok-free.app/rest/oauth1-credential/callback` | `http://localhost:8080/rest/oauth1-credential/callback` |
| **GitHub OAuth** | `https://xyz.ngrok-free.app/rest/oauth2-credential/callback` | `http://localhost:8080/rest/oauth2-credential/callback` |

### Step 3: Verify Configuration
```powershell
# Check that stable URL is working
Invoke-WebRequest -Uri "http://localhost:8080/health" -UseBasicParsing

# Verify n8n access
Invoke-WebRequest -Uri "http://localhost:8080" -UseBasicParsing
```

## 📋 Detailed Migration Steps

### 1. Stop Current ngrok Setup
```powershell
# Stop old ngrok-based system
.\Stop-N8N-NgRok.ps1
# OR
docker-compose down
```

### 2. Update Environment Configuration
Your `.env` file should now contain:
```env
# OLD (ngrok-based)
WEBHOOK_URL=https://abc123.ngrok-free.app/

# NEW (stable URL)
WEBHOOK_URL=http://localhost:8080/
```

### 3. Start New Stable URL System
```powershell
# Start with stable URL proxy
.\start-n8n.bat
```

### 4. Update OAuth Applications

#### Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to APIs & Services > Credentials
3. Edit your OAuth 2.0 Client ID
4. Update Authorized Redirect URIs to: `http://localhost:8080/rest/oauth2-credential/callback`

#### Twitter Developer Portal
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Navigate to your app settings
3. Update Callback URL to: `http://localhost:8080/rest/oauth1-credential/callback`

#### GitHub OAuth Apps
1. Go to GitHub Settings > Developer settings > OAuth Apps
2. Edit your OAuth App
3. Update Authorization callback URL to: `http://localhost:8080/rest/oauth2-credential/callback`

### 5. Test Your Migration
```powershell
# 1. Verify stable URL health
Invoke-WebRequest -Uri "http://localhost:8080/health"

# 2. Test n8n access
# Open: http://localhost:8080
# Login with your credentials

# 3. Test OAuth credentials in n8n
# Go to Settings > Credentials
# Test each OAuth credential

# 4. Test webhook workflows
# Create a test workflow with webhook trigger
# Verify webhook URL uses localhost:8080
```

## 🔧 Troubleshooting Migration Issues

### Issue: "Can't access http://localhost:8080"
**Solution:**
```powershell
# Check if containers are running
docker ps

# Restart if needed
.\Stop-N8N-Stable-Fixed.ps1
.\Start-N8N-Stable.ps1
```

### Issue: "OAuth callback fails"
**Solution:**
1. Verify you updated the callback URL in your OAuth app
2. Ensure you're using the exact URL: `http://localhost:8080/rest/oauth2-credential/callback`
3. Clear browser cache and try again

### Issue: "Webhooks not working"
**Solution:**
1. Check webhook URL in n8n workflow uses `http://localhost:8080`
2. Verify external services can reach localhost (may need port forwarding for external testing)

## 📚 What Happens to Old Files?

### Moved to `legacy-tunneling/` folder:
- `Start-N8N-NgRok.ps1`
- `Stop-N8N-NgRok.ps1`
- All zrok-related files
- Old docker-compose configurations

### Updated files:
- `start-n8n.bat` - Now uses stable URL
- `stop-n8n.bat` - Now uses stable URL
- `setup.ps1` - Updated descriptions
- All documentation files

## 🎉 Migration Complete!

Once migrated, you'll enjoy:
- **Permanent URLs** that never change
- **Zero maintenance** webhook management
- **Reliable local networking**
- **Simple one-command startup**

**Welcome to the stable URL future!** 🚀

---
*For questions or issues, see [STABLE_URL_ASSESSMENT.md](STABLE_URL_ASSESSMENT.md) for technical details.*
