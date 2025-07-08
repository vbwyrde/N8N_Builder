# OAuth Integration with Stable URL

## 🎯 Overview
With the new stable URL proxy, your webhook URL is now **http://localhost:8080** and will NEVER change between restarts!

## ✅ Key Benefits
- **No more URL updates**: Set once, works forever
- **No more OAuth credential changes**: Configure once and forget
- **Reliable webhooks**: Always accessible at the same URL
- **Simple setup**: Just use localhost:8080 everywhere

## 🔧 OAuth Provider Configuration

### Google OAuth Apps
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to APIs & Services > Credentials
3. Create or edit your OAuth 2.0 Client ID
4. **Set Authorized Redirect URIs to:**
   ```
   http://localhost:8080/rest/oauth2-credential/callback
   ```

### Twitter OAuth Apps  
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Navigate to your app settings
3. **Set Callback URL to:**
   ```
   http://localhost:8080/rest/oauth1-credential/callback
   ```

### GitHub OAuth Apps
1. Go to GitHub Settings > Developer settings > OAuth Apps
2. Create or edit your OAuth App
3. **Set Authorization callback URL to:**
   ```
   http://localhost:8080/rest/oauth2-credential/callback
   ```

### Generic OAuth 2.0 Pattern
For any OAuth 2.0 provider, use this callback URL pattern:
```
http://localhost:8080/rest/oauth2-credential/callback
```

For OAuth 1.0 providers, use:
```
http://localhost:8080/rest/oauth1-credential/callback
```

## 🧪 Testing OAuth Integration

### 1. Start n8n with Stable URL
```bash
# Use the main startup script
.\start-n8n.bat

# Or directly
.\Start-N8N-Stable.ps1
```

### 2. Access n8n
- **Primary URL**: http://localhost:8080
- **Direct URL**: http://localhost:5678 (with basic auth)
- **Health Check**: http://localhost:8080/health

### 3. Configure OAuth Credentials in n8n
1. Go to Settings > Credentials
2. Add new credential for your OAuth provider
3. The callback URL will automatically use your stable URL
4. Complete the OAuth flow - it will redirect to localhost:8080

### 4. Test Webhook Delivery
1. Create a workflow with a webhook trigger
2. The webhook URL will be: `http://localhost:8080/webhook/your-webhook-path`
3. Test the webhook from external services
4. Verify it works consistently across restarts

## 🔍 Troubleshooting

### Common Issues
1. **OAuth callback fails**: Ensure you've updated the callback URL in your OAuth app settings
2. **Webhook not receiving data**: Check that external services can reach localhost:8080
3. **SSL/HTTPS required**: Some providers require HTTPS - consider using ngrok for production

### Verification Steps
```powershell
# Test proxy health
Invoke-WebRequest -Uri "http://localhost:8080/health" -UseBasicParsing

# Test n8n access
Invoke-WebRequest -Uri "http://localhost:8080" -UseBasicParsing

# Check running containers
docker ps
```

## 📝 Migration from ngrok

### Before (ngrok - URL changes every restart)
```
https://abc123.ngrok-free.app/rest/oauth2-credential/callback
```

### After (Stable URL - NEVER changes)
```
http://localhost:8080/rest/oauth2-credential/callback
```

### Migration Steps
1. Update all OAuth app callback URLs to use localhost:8080
2. Update .env file WEBHOOK_URL to http://localhost:8080/
3. Restart n8n using the new stable startup process
4. Test all OAuth integrations
5. Remove ngrok dependencies

## 🎉 Success!
Once configured, your OAuth integrations will work reliably without any URL management overhead!
