# 🔑 External Service Credentials Setup Guide

This guide covers setting up credentials for external services with your local n8n instance using nGrok tunneling for webhook access.

## 📚 Related Documentation

- **🚀 [Quick Start](QUICK_START.md)** - Get n8n running first
- **📖 [Main README](README.md)** - Complete documentation hub
- **🔒 [Security Guide](SECURITY.md)** - Security best practices for credentials
- **🤖 [Automation Guide](AUTOMATION-README.md)** - Automated URL management
- **📋 [Manual Operations](../RunSystem.md)** - Manual nGrok setup

## 🌐 Dynamic Configuration System

### Current URLs (Auto-Updated)
- **N8N Local URL**: http://localhost:5678
- **N8N Public URL**: `https://YOUR-CURRENT-NGROK-URL/` (⚠️ Changes each restart)
- **OAuth2 Callback**: `https://YOUR-CURRENT-NGROK-URL/rest/oauth2-credential/callback`
- **OAuth1 Callback**: `https://YOUR-CURRENT-NGROK-URL/rest/oauth1-credential/callback`

### 🔍 How to Find Your Current nGrok URL

**Method 1: Automation Script Output**
```bash
# Run the start script and look for the URLs in output:
start-n8n.bat
# OR
powershell -ExecutionPolicy Bypass -File "Start-N8N-NgRok.ps1"
```

**Method 2: nGrok Web Interface**
- Open: http://127.0.0.1:4040
- Click "Status" tab
- Copy the HTTPS forwarding URL

**Method 3: nGrok API**
```bash
# Query the nGrok API directly:
curl http://127.0.0.1:4040/api/tunnels
```

⚠️ **CRITICAL**: nGrok URL changes on each restart (free plan). You MUST update all OAuth redirect URLs when this happens.

## 🔑 Service-Specific Setup Instructions

### 🔧 Before You Start

1. **Get your current nGrok URL** (see methods above)
2. **Have your nGrok URL ready** - you'll need it for each service
3. **Keep nGrok running** while setting up OAuth applications

### 📊 Google Drive / Google Services

**Step 1: Google Cloud Console Setup**
1. Visit: https://console.cloud.google.com/
2. Create new project or select existing one
3. **Enable APIs** (APIs & Services → Library):
   - Google Drive API
   - Google Sheets API (if needed)
   - Gmail API (if needed)

**Step 2: OAuth Consent Screen**
1. Go to: APIs & Services → OAuth consent screen
2. **User Type**: External (unless you have Google Workspace)
3. **App Information**:
   - App name: "n8n Local Development"
   - User support email: Your email
   - Developer contact: Your email
4. **Scopes**: Add when prompted during credential creation
5. **Test users**: Add your email for testing

**Step 3: Create OAuth Credentials**
1. APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID
2. **Application type**: Web application
3. **Name**: "n8n Google Services"
4. **Authorized redirect URIs** (⚠️ **REPLACE WITH YOUR NGROK URL**):
   ```
   https://YOUR-CURRENT-NGROK-URL/rest/oauth2-credential/callback
   ```
   Example: `https://abc123-45-67-89-012.ngrok-free.app/rest/oauth2-credential/callback`

**Step 4: n8n Configuration**
1. Open n8n → Settings → Credentials
2. Add "Google Drive OAuth2 API" (or "Google OAuth2 API")
3. Enter **Client ID** and **Client Secret** from Google Cloud Console
4. **Scopes** (add as needed):
   ```
   https://www.googleapis.com/auth/drive
   https://www.googleapis.com/auth/drive.file
   ```
5. Complete OAuth authorization flow

### 📝 Google Blogger (Detailed Setup)

**Step 1: Enable Blogger API**
1. In same Google Cloud Console project as above
2. APIs & Services → Library → Search "Blogger"
3. **Enable "Blogger API v3"**

**Step 2: OAuth Credentials (Reuse or Create New)**

**Option A: Reuse Google Drive Credentials (Recommended)**
- Use the same OAuth 2.0 Client ID created above
- Just add Blogger scopes in n8n

**Option B: Create Separate Blogger Credentials**
1. Create new OAuth 2.0 Client ID
2. **Authorized redirect URIs** (⚠️ **REPLACE WITH YOUR NGROK URL**):
   ```
   https://YOUR-CURRENT-NGROK-URL/rest/oauth2-credential/callback
   ```

**Step 3: n8n Configuration**
1. Settings → Credentials → Add "Google OAuth2 API"
2. Enter **Client ID** and **Client Secret**
3. **Scopes** (⚠️ **CRITICAL - Add these specific scopes**):
   ```
   https://www.googleapis.com/auth/blogger
   https://www.googleapis.com/auth/blogger.readonly
   ```
4. Complete OAuth authorization flow

**Step 4: Test Blogger Access**
1. Create simple workflow with Blogger node
2. Test "Get Blog Info" operation
3. Verify you can see your blogs

**🎯 Blogger-Specific Notes:**
- ✅ Same OAuth2 credentials work for multiple Google services
- ✅ Blogger API requires explicit scope configuration
- ✅ Can manage multiple blogs with single credential
- ✅ Supports both read and write operations
- ⚠️ Blogger API has rate limits - monitor usage

### 🐦 Twitter/X API

**Step 1: Developer Account Setup**
1. Apply for developer account: https://developer.twitter.com/
2. **Wait for approval** (can take 1-7 days)
3. Create new app in developer portal

**Step 2: App Configuration**
1. **App Details**:
   - App name: "n8n Local Development"
   - Description: "Local n8n automation testing"
   - Website URL: Your current nGrok URL
2. **App Permissions**: Set as needed:
   - Read only
   - Read and Write
   - Read, Write, and Direct Messages
3. **Callback URL** (⚠️ **REPLACE WITH YOUR NGROK URL**):
   ```
   https://YOUR-CURRENT-NGROK-URL/rest/oauth1-credential/callback
   ```

**Step 3: Get API Keys**
1. Go to app settings → Keys and Tokens
2. **Copy these values**:
   - API Key (Consumer Key)
   - API Secret Key (Consumer Secret)
   - Access Token
   - Access Token Secret

**Step 4: n8n Configuration**
1. Settings → Credentials → Add "Twitter OAuth1 API"
2. Enter all four keys/tokens from step 3
3. Test connection with a simple tweet read operation

**⚠️ Twitter API Notes:**
- Free tier has limited requests per month
- Rate limits apply to all operations
- Some features require paid API access

### 💬 Slack

**Step 1: Create Slack App**
1. Visit: https://api.slack.com/apps
2. **Create New App** → "From scratch"
3. **App Name**: "n8n Local Development"
4. **Choose workspace** where you want to install the app

**Step 2: OAuth Configuration**
1. **OAuth & Permissions** → Redirect URLs:
   ```
   https://YOUR-CURRENT-NGROK-URL/rest/oauth2-credential/callback
   ```
2. **Scopes** - Add required bot token scopes:
   ```
   channels:read      # Read channel information
   chat:write         # Send messages
   files:read         # Read file information
   users:read         # Read user information
   ```
3. **Install App** to your workspace

**Step 3: n8n Setup**
1. Get **Client ID** and **Client Secret** from app settings
2. Settings → Credentials → Add "Slack OAuth2 API"
3. Enter Client ID and Client Secret
4. Complete OAuth flow

### 🐙 GitHub

**Step 1: OAuth App Setup**
1. GitHub → Settings → Developer settings → OAuth Apps
2. **Register new application**:
   - Application name: "n8n Local Development"
   - Homepage URL: Your current nGrok URL
   - **Authorization callback URL** (⚠️ **REPLACE WITH YOUR NGROK URL**):
     ```
     https://YOUR-CURRENT-NGROK-URL/rest/oauth2-credential/callback
     ```

**Step 2: n8n Configuration**
1. Copy **Client ID** and **Client Secret** from GitHub
2. Settings → Credentials → Add "GitHub OAuth2 API"
3. Enter credentials and complete OAuth flow

## 📝 Blogger Integration Deep Dive

### Blogger API Setup Details

Since you're planning to create custom Blogger nodes, here are the specific details:

1. **API Capabilities**:
   - Read blog information and posts
   - Create, update, delete posts
   - Manage comments
   - Handle multiple blogs per account

2. **Required Scopes**:
   ```
   https://www.googleapis.com/auth/blogger          # Full access
   https://www.googleapis.com/auth/blogger.readonly # Read-only access
   ```

3. **Common API Endpoints** (for custom node development):
   ```
   GET  /v3/blogs/{blogId}                    # Get blog info
   GET  /v3/blogs/{blogId}/posts              # List posts
   POST /v3/blogs/{blogId}/posts              # Create post
   PUT  /v3/blogs/{blogId}/posts/{postId}     # Update post
   DELETE /v3/blogs/{blogId}/posts/{postId}   # Delete post
   ```

4. **Authentication Flow**:
   - Uses same OAuth2 as other Google services
   - Token includes Blogger scopes
   - Can be combined with Drive/Gmail credentials

### Custom Blogger Node Development

If you're creating custom Blogger nodes, you'll need:

1. **Node Structure**:
   - Resource: Blog, Post, Comment
   - Operations: Create, Read, Update, Delete, List
   - Credential: Google OAuth2 API (with Blogger scopes)

2. **API Base URL**: `https://www.googleapis.com/blogger/v3`

3. **Common Parameters**:
   - `blogId`: Blog identifier (can be URL or numeric ID)
   - `postId`: Post identifier
   - `maxResults`: Pagination limit
   - `pageToken`: Pagination token

## 🔄 Managing nGrok URL Changes (CRITICAL PROCESS)

### 🚨 When nGrok URL Changes (Every Restart on Free Plan):

**Step 1: Get New nGrok URL**
```bash
# Method 1: From automation script output
start-n8n.bat
# Look for: "✅ Public URL: https://new-url.ngrok-free.app"

# Method 2: From nGrok web interface
# Open: http://127.0.0.1:4040 → Status tab

# Method 3: From nGrok API
curl http://127.0.0.1:4040/api/tunnels
```

**Step 2: Run Automated Update Script (If Available)**
```powershell
# Navigate to scripts directory
cd n8n-docker\scripts

# Run update script with new URL
.\update-oauth-urls.ps1 -NewNgrokUrl "https://YOUR-NEW-NGROK-URL.ngrok-free.app"
```

**Step 3: Manual Updates (If Script Not Available)**
Update redirect URLs in each service:

1. **Google Cloud Console**:
   - Console → APIs & Services → Credentials
   - Edit OAuth 2.0 Client ID
   - Update Authorized redirect URIs

2. **Twitter Developer Portal**:
   - App settings → Authentication settings
   - Update Callback URLs

3. **Slack API**:
   - OAuth & Permissions → Redirect URLs
   - Update redirect URL

4. **GitHub**:
   - Settings → Developer settings → OAuth Apps
   - Edit application → Update Authorization callback URL

**Step 4: Restart n8n (Apply Changes)**
```bash
docker-compose restart n8n
```

**Step 5: Test All Credentials**
- Go to n8n → Settings → Credentials
- Test each credential to ensure they work with new URL

## 🛠️ Troubleshooting

### Common Issues:

1. **OAuth Redirect Mismatch**:
   - Ensure exact URL match including trailing slashes
   - Check for HTTP vs HTTPS mismatches

2. **nGrok Warning Page**:
   - Free nGrok shows warning page to visitors
   - Click "Visit Site" to proceed
   - Consider paid plan to remove warning

3. **SSL Certificate Issues**:
   - Most services require HTTPS (nGrok provides this)
   - Ensure N8N_PROTOCOL=http in .env (nGrok handles SSL termination)

4. **Credential Test Failures**:
   - Verify OAuth URLs are updated in external service
   - Check that APIs are enabled (Google services)
   - Confirm app permissions are sufficient

### Testing Credentials:

1. **In N8N Interface**:
   - Go to credential settings
   - Click "Test" button on each credential
   - Should show green checkmark if successful

2. **In Workflows**:
   - Create simple test workflow
   - Use credential in a basic node operation
   - Execute to verify functionality

## 📝 Best Practices

1. **Document Your Setup**:
   - Keep record of all OAuth applications created
   - Note which services are configured

2. **Regular Updates**:
   - Update redirect URLs promptly when nGrok restarts
   - Test credentials after URL changes

3. **Security**:
   - Use strong passwords for OAuth applications
   - Regularly review and rotate credentials
   - Limit OAuth scopes to minimum required

4. **Consider nGrok Paid Plan**:
   - Static subdomain eliminates URL change issues
   - Removes warning page for better user experience
   - More reliable for production workflows

## 🔗 Quick Reference URLs

### 🌐 Dynamic URLs (Change with each nGrok restart)
- **Current nGrok URL**: `https://YOUR-CURRENT-NGROK-URL/` (⚠️ **Get from nGrok interface**)
- **OAuth2 Callback**: `https://YOUR-CURRENT-NGROK-URL/rest/oauth2-credential/callback`
- **OAuth1 Callback**: `https://YOUR-CURRENT-NGROK-URL/rest/oauth1-credential/callback`

### 🔧 Static URLs (Always the same)
- **nGrok Web Interface**: http://127.0.0.1:4040
- **n8n Local Interface**: http://localhost:5678

### 📋 URL Templates for Copy/Paste
```
# OAuth2 Callback Template (Google, Slack, GitHub, etc.)
https://YOUR-CURRENT-NGROK-URL/rest/oauth2-credential/callback

# OAuth1 Callback Template (Twitter/X)
https://YOUR-CURRENT-NGROK-URL/rest/oauth1-credential/callback

# Replace YOUR-CURRENT-NGROK-URL with actual URL from nGrok
```

## 📚 Google Services API Reference

### Required APIs to Enable in Google Cloud Console:
- **Google Drive**: Google Drive API
- **Blogger**: Blogger API v3
- **Gmail**: Gmail API
- **Google Sheets**: Google Sheets API
- **Google Calendar**: Google Calendar API

### Common OAuth Scopes:
```
# Blogger
https://www.googleapis.com/auth/blogger
https://www.googleapis.com/auth/blogger.readonly

# Drive
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/drive.readonly

# Gmail
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/gmail.readonly
```

### API Base URLs:
- **Blogger**: `https://www.googleapis.com/blogger/v3`
- **Drive**: `https://www.googleapis.com/drive/v3`
- **Gmail**: `https://www.googleapis.com/gmail/v1`

## 🛠️ Helper Scripts and Automation

### 📁 Available Scripts
Run these scripts from the `n8n-docker/scripts/` directory:

```powershell
# Update all OAuth URLs when nGrok changes
.\update-oauth-urls.ps1 -NewNgrokUrl "https://YOUR-NEW-NGROK-URL.ngrok-free.app"

# Get step-by-step Blogger setup guide
.\setup-blogger-credentials.ps1

# Auto-detect current nGrok URL and show setup instructions
.\setup-blogger-credentials.ps1 -AutoDetect
```

### 🤖 Automation Integration
The main automation scripts handle URL updates automatically:

```bash
# Start script automatically updates WEBHOOK_URL in .env
start-n8n.bat

# Manual URL update if needed
powershell -ExecutionPolicy Bypass -File "Start-N8N-NgRok.ps1" -UpdateUrlsOnly
```

### 📝 Manual Process Checklist
If automation scripts aren't available, follow this checklist:

1. **[ ]** Get new nGrok URL from http://127.0.0.1:4040
2. **[ ]** Update Google Cloud Console OAuth redirect URIs
3. **[ ]** Update Twitter/X app callback URLs
4. **[ ]** Update Slack app redirect URLs
5. **[ ]** Update GitHub OAuth app callback URLs
6. **[ ]** Update any other service redirect URLs
7. **[ ]** Restart n8n: `docker-compose restart n8n`
8. **[ ]** Test all credentials in n8n interface

---

**🎯 Pro Tip**: Consider upgrading to nGrok paid plan for static URLs to eliminate the need for constant URL updates!
