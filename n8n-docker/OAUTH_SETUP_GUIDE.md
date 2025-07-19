# OAuth2 Setup Guide for n8n

## Overview
This guide helps you set up OAuth2 integrations (Twitter, Google, GitHub, etc.) with your n8n Docker instance using LocalTunnel for free, stable HTTPS URLs.

## Prerequisites
- ✅ n8n running in Docker
- ✅ Node.js installed
- ✅ Internet connection

## Step 1: Start LocalTunnel

In your `n8n-docker` directory, run:
```powershell
.\Start-LocalTunnel.ps1
```

You'll see output like:
```
🌐 LocalTunnel for n8n OAuth Integrations
=========================================
Configuration:
  Local n8n: http://localhost:5678
  Public URL: https://n8n-oauth-stable.loca.lt
  OAuth Callback: https://n8n-oauth-stable.loca.lt/rest/oauth2-credential/callback

your url is: https://n8n-oauth-stable.loca.lt
```

## Step 2: Configure OAuth2 Services

### Twitter OAuth2
1. **Go to**: https://developer.twitter.com/
2. **Select your app** → **Settings** → **Authentication settings**
3. **Add Callback URL**: `https://n8n-oauth-stable.loca.lt/rest/oauth2-credential/callback`
4. **Website URL**: `https://n8n-oauth-stable.loca.lt`
5. **Save changes**

### Google OAuth2
1. **Go to**: https://console.cloud.google.com/
2. **APIs & Services** → **Credentials**
3. **Select your OAuth 2.0 Client ID**
4. **Add Authorized redirect URI**: `https://n8n-oauth-stable.loca.lt/rest/oauth2-credential/callback`
5. **Save**

### GitHub OAuth2
1. **Go to**: https://github.com/settings/developers
2. **Select your OAuth App** (or create new)
3. **Authorization callback URL**: `https://n8n-oauth-stable.loca.lt/rest/oauth2-credential/callback`
4. **Homepage URL**: `https://n8n-oauth-stable.loca.lt`
5. **Update application**

## Step 3: Configure n8n Credentials

1. **Access n8n**: http://localhost:5678
2. **Go to**: Settings → Credentials
3. **Add New Credential**: Choose your service (e.g., "Twitter OAuth2 API")
4. **Enter your credentials**:
   - Client ID: From your OAuth2 app
   - Client Secret: From your OAuth2 app
5. **Click "Connect"** - n8n will redirect to the service for authorization
6. **Complete authorization** - you'll be redirected back to n8n

## Step 4: Test Your Integration

1. **Create a new workflow**
2. **Add a node** for your OAuth2 service (e.g., Twitter, Google Sheets)
3. **Select your credential** from the dropdown
4. **Test the connection** - should work seamlessly!

## Important Notes

### Keep LocalTunnel Running
- **OAuth2 callbacks require the tunnel to be active**
- **Keep the PowerShell window open** while using OAuth2 integrations
- **Restart if needed**: Just run `.\Start-LocalTunnel.ps1` again

### Browser Password Prompt
- **Normal behavior**: LocalTunnel shows password prompt for browser access
- **OAuth2 unaffected**: API calls bypass the password completely
- **For manual testing**: Use direct access at http://localhost:5678

### Workflow Development
- **Direct n8n access**: http://localhost:5678 (no password needed)
- **Import workflows**: Use n8n's Settings → Import/Export
- **N8N_Builder compatible**: Import generated JSON files normally

## Troubleshooting

### "Subdomain not available"
- **Error**: `subdomain "n8n-oauth-stable" is not available`
- **Solution**: Edit `Start-LocalTunnel.ps1` and change `$SUBDOMAIN` to something unique like `n8n-oauth-yourname`

### "Connection refused"
- **Check n8n**: Run `docker-compose ps` to verify n8n is running
- **Start n8n**: Run `docker-compose up -d n8n`
- **Wait**: n8n takes ~10 seconds to start

### "OAuth2 callback failed"
- **Check tunnel**: Ensure LocalTunnel is still running
- **Verify URL**: Make sure you used the exact callback URL shown in the script
- **Check service**: Verify the OAuth2 app configuration in the external service

### "LocalTunnel not found"
- **Auto-install**: The script automatically installs LocalTunnel
- **Manual install**: Run `npm install localtunnel` in the n8n-docker directory

## File Structure

After setup, your n8n-docker directory will have:
```
n8n-docker/
├── Start-LocalTunnel.ps1       # Main script
├── package.json                # Node.js dependencies
├── node_modules/               # LocalTunnel installation
├── docker-compose.yml          # n8n Docker config
└── data/                       # n8n data
```

## Security Notes

- **OAuth2 credentials**: Stored securely in n8n's credential system
- **Public tunnel**: The LocalTunnel URL is publicly accessible
- **Production**: Consider paid tunneling services for production use

## Summary

This setup provides:
- ✅ **Free HTTPS URLs** for OAuth2 integrations
- ✅ **Stable subdomains** - same URL every time
- ✅ **Auto-installation** - script handles dependencies
- ✅ **Docker integration** - works with n8n containers
- ✅ **Independent operation** - works with any n8n setup

Your n8n instance now has reliable OAuth2 integration capabilities without requiring paid services! 