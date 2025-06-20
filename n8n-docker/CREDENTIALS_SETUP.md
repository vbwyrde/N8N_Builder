# External Service Credentials Setup Guide

This guide covers setting up credentials for external services with your local N8N instance using nGrok tunneling.

## 🌐 Current Configuration

- **N8N Local URL**: http://localhost:5678
- **N8N Public URL**: https://4da5-24-187-157-188.ngrok-free.app/
- **OAuth Callback Base**: `https://4da5-24-187-157-188.ngrok-free.app/rest/`

⚠️ **Important**: nGrok URL changes on each restart (free plan). Update all OAuth redirect URLs when this happens.

## 🔑 Service-Specific Setup Instructions

### Google Drive / Google Services

1. **Google Cloud Console Setup**:
   - Visit: https://console.cloud.google.com/
   - Create/select project
   - Enable Google Drive API (APIs & Services → Library)

2. **OAuth Consent Screen**:
   - APIs & Services → OAuth consent screen
   - User Type: External
   - App name: "N8N Local Instance"
   - Add your email as user support and developer contact

3. **Create Credentials**:
   - APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID
   - Application type: Web application
   - Name: "N8N Google Services"
   - **Authorized redirect URIs**:
     ```
     https://4da5-24-187-157-188.ngrok-free.app/rest/oauth2-credential/callback
     ```

4. **N8N Configuration**:
   - Open N8N → Settings → Credentials
   - Add "Google Drive OAuth2 API"
   - Enter Client ID and Client Secret
   - Complete OAuth authorization

### Google Blogger

1. **Google Cloud Console Setup** (Same project as Google Drive):
   - Visit: https://console.cloud.google.com/
   - Use same project as Google Drive or create new one
   - Enable Blogger API v3 (APIs & Services → Library → Search "Blogger")

2. **OAuth Credentials** (Can reuse Google Drive credentials):
   - Use same OAuth 2.0 Client ID as Google Drive
   - Or create separate one with same redirect URI:
     ```
     https://4da5-24-187-157-188.ngrok-free.app/rest/oauth2-credential/callback
     ```

3. **N8N Configuration**:
   - Settings → Credentials → Add "Google OAuth2 API"
   - Enter Client ID and Client Secret
   - **Scopes**: Add Blogger-specific scopes:
     ```
     https://www.googleapis.com/auth/blogger
     https://www.googleapis.com/auth/blogger.readonly
     ```
   - Complete OAuth authorization

4. **Blogger-Specific Notes**:
   - Same OAuth2 credentials work for multiple Google services
   - Blogger API requires explicit scope configuration
   - Can manage multiple blogs with single credential

### Twitter/X API

1. **Developer Portal Setup**:
   - Apply for developer account: https://developer.twitter.com/
   - Create new app in developer portal

2. **App Configuration**:
   - App permissions: Set as needed (Read/Write/DM)
   - **Callback URL**:
     ```
     https://4da5-24-187-157-188.ngrok-free.app/rest/oauth1-credential/callback
     ```
   - Website URL: Your nGrok URL

3. **Get API Keys**:
   - API Key (Consumer Key)
   - API Secret Key (Consumer Secret)  
   - Access Token
   - Access Token Secret

4. **N8N Configuration**:
   - Settings → Credentials → Add "Twitter OAuth1 API"
   - Enter all four keys/tokens

### Slack

1. **Create Slack App**:
   - Visit: https://api.slack.com/apps
   - Create new app → From scratch
   - Choose workspace

2. **OAuth Configuration**:
   - OAuth & Permissions → Redirect URLs:
     ```
     https://4da5-24-187-157-188.ngrok-free.app/rest/oauth2-credential/callback
     ```
   - Add required scopes (channels:read, chat:write, etc.)

3. **N8N Setup**:
   - Get Client ID and Client Secret from app settings
   - Add "Slack OAuth2 API" credential in N8N

### GitHub

1. **OAuth App Setup**:
   - GitHub → Settings → Developer settings → OAuth Apps
   - Register new application
   - **Authorization callback URL**:
     ```
     https://4da5-24-187-157-188.ngrok-free.app/rest/oauth2-credential/callback
     ```

2. **N8N Configuration**:
   - Use Client ID and Client Secret in N8N GitHub OAuth2 credential

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

## 🔄 Managing nGrok URL Changes

### When nGrok URL Changes:

1. **Get New URL**:
   ```bash
   # From nGrok terminal output or web interface (http://127.0.0.1:4040)
   ```

2. **Run Update Script**:
   ```powershell
   .\scripts\update-oauth-urls.ps1 -NewNgrokUrl "https://new-url.ngrok-free.app"
   ```

3. **Update Each Service**:
   - Google Cloud Console → Credentials → Edit OAuth client
   - Twitter Developer Portal → App settings → Authentication settings
   - Slack API → OAuth & Permissions → Redirect URLs
   - GitHub → OAuth Apps → Edit application

4. **Restart N8N**:
   ```bash
   docker-compose restart n8n
   ```

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

- **Current nGrok URL**: https://4da5-24-187-157-188.ngrok-free.app/
- **OAuth2 Callback**: `/rest/oauth2-credential/callback`
- **OAuth1 Callback**: `/rest/oauth1-credential/callback`
- **nGrok Web Interface**: http://127.0.0.1:4040
- **N8N Local Interface**: http://localhost:5678

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

## 🛠️ Helper Scripts

Run these scripts from the `n8n-docker/scripts/` directory:

```powershell
# Update all OAuth URLs when nGrok changes
.\update-oauth-urls.ps1 -NewNgrokUrl "https://new-url.ngrok-free.app"

# Get step-by-step Blogger setup guide
.\setup-blogger-credentials.ps1

# Auto-detect current nGrok URL and show Blogger setup
.\setup-blogger-credentials.ps1
```
