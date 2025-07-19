# LocalTunnel for n8n OAuth Integrations

## 🚀 Quick Start (2 minutes)

### For Developers: Essential OAuth Setup

**When you need this**: Setting up Twitter, Google, GitHub, or any OAuth2 integration in n8n workflows.

**What this solves**: OAuth2 services require HTTPS callback URLs, but n8n runs on localhost:5678 (HTTP).

### 1. One-Command Setup
```powershell
cd n8n-docker
.\Start-LocalTunnel.ps1
```

**This script automatically:**
- ✅ Installs LocalTunnel if missing
- ✅ Starts n8n Docker if not running  
- ✅ Creates stable HTTPS tunnel
- ✅ Provides ready-to-use OAuth2 callback URL

### 2. Use This OAuth2 Callback URL
```
https://n8n-oauth-stable.loca.lt/rest/oauth2-credential/callback
```

**Copy this URL exactly** - it works for all OAuth2 services (Twitter, Google, GitHub, etc.)

## 📋 OAuth2 Service Setup Examples

### Twitter API
1. Go to: https://developer.twitter.com/
2. App Settings → Authentication settings
3. **Callback URL**: `https://n8n-oauth-stable.loca.lt/rest/oauth2-credential/callback`
4. **Website URL**: `https://n8n-oauth-stable.loca.lt`

### Google Cloud Console
1. Go to: https://console.cloud.google.com/
2. APIs & Services → Credentials → OAuth 2.0 Client IDs
3. **Authorized redirect URI**: `https://n8n-oauth-stable.loca.lt/rest/oauth2-credential/callback`

### GitHub OAuth Apps
1. Go to: https://github.com/settings/developers
2. New OAuth App
3. **Authorization callback URL**: `https://n8n-oauth-stable.loca.lt/rest/oauth2-credential/callback`

## 🔧 How to Use

### Step 1: Start Tunnel (Keep Running)
```powershell
cd n8n-docker
.\Start-LocalTunnel.ps1
```
**Keep this terminal open** - closing it stops the tunnel.

### Step 2: Setup OAuth2 in n8n
1. Open n8n: http://localhost:5678
2. Go to: Settings → Credentials → Add Credential
3. Choose your service (Twitter, Google, etc.)
4. **The callback URL will automatically show the tunnel URL**
5. Click "Connect my account" → Complete OAuth2 flow

### Step 3: Test Integration
- Create a workflow using your OAuth2 credential
- Test the connection
- **Once working, you can stop the tunnel** - OAuth2 tokens are permanent

## ⚠️ Important Notes

### For Daily Development
- **Tunnel only needed during initial OAuth2 setup**
- **OAuth2 tokens work permanently** after initial authorization
- **Regular workflows don't need the tunnel running**

### Browser Password Prompt
- LocalTunnel shows password prompt in browser - **this is normal**
- OAuth2 APIs bypass this prompt automatically
- For manual browser access, check terminal for password

### Troubleshooting
- **"Subdomain taken"**: Try again - script will retry with different name
- **"n8n not running"**: Script automatically starts Docker container
- **"Connection refused"**: Check Docker is running: `docker-compose ps`

## 📁 Files Created
- `package.json` - Node.js dependencies for LocalTunnel
- `node_modules/` - LocalTunnel installation
- `Start-LocalTunnel.ps1` - Main startup script

## 🔄 Alternative Methods

If LocalTunnel doesn't work, see [Documentation/ReadMe_TunnelSetup.md](../Documentation/ReadMe_TunnelSetup.md) for localhost.run SSH method.

---

**✅ That's it!** Your n8n now has stable OAuth2 integration capabilities for all major services.
