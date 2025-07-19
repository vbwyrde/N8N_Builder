# Tunnel Setup for OAuth2 Integration

## Overview
This document provides a complete step-by-step process for setting up SSH tunneling with localhost.run on Windows 11 to enable OAuth2 integrations (Twitter, Google, GitHub, etc.) with n8n.

## Prerequisites (Verify First)
- [ ] **Verify n8n is running**: `docker-compose ps` (should show n8n as "Up")
- [ ] **Verify n8n accessible**: http://localhost:5678 should load
- [ ] **Current working directory**: `C:\Users\...\source\Cursor_Workspaces\N8N_Builder`

## Step 1: Start SSH Tunnel (localhost.run)
- [ ] **Navigate to n8n-docker directory**: `cd n8n-docker`
- [ ] **Run SSH tunnel command**: `ssh -R 80:localhost:5678 nokey@localhost.run`
- [ ] **Record the tunnel URL**: Note the `https://xxxxxx.lhr.life` URL that appears
- [ ] **Keep terminal window open**: This maintains the tunnel

## Step 2: Update Docker Configuration
- [ ] **Edit docker-compose.yml**: Update these two lines with the new tunnel URL:
  ```yaml
  - N8N_EDITOR_BASE_URL=https://[NEW-TUNNEL-URL]
  - WEBHOOK_URL=https://[NEW-TUNNEL-URL]/
  ```
- [ ] **Save the file**

## Step 3: Restart n8n Container
- [ ] **Stop n8n completely**: `docker-compose stop n8n`
- [ ] **Start n8n fresh**: `docker-compose up -d n8n`
- [ ] **Verify restart**: `docker-compose ps` should show n8n as "Up"
- [ ] **Test access**: http://localhost:5678 should still work
- [ ] **Verify environment variables**: `docker-compose logs n8n --tail=10` should show the correct tunnel URL

**⚠️ Important**: Use `stop` then `up -d` instead of `restart` to ensure environment variables are properly loaded. A simple `restart` may not apply the new environment variables correctly.

## Step 4: Update OAuth Provider (Twitter Example)
- [ ] **Set Callback URL**: `https://[TUNNEL-URL]/rest/oauth2-credential/callback`
- [ ] **Set Website URL**: `https://[TUNNEL-URL]`

## Step 5: Complete OAuth in n8n
- [ ] **Access n8n**: http://localhost:5678
- [ ] **Create OAuth2 credential**: Settings → Credentials
- [ ] **Verify callback URL**: Should show tunnel URL
- [ ] **Connect account**: Click "Connect my account"
- [ ] **Authorize**: Complete OAuth authorization
- [ ] **Verify success**: Should redirect back successfully

## Step 6: Test and Cleanup
- [ ] **Test workflow**: Verify OAuth integration works
- [ ] **Document success**: Note that OAuth tokens are now permanent
- [ ] **Cleanup**: SSH tunnel can be stopped after OAuth completion

## Important Notes

### URL Behavior
- **localhost.run URLs change on each restart** - this is expected behavior
- **OAuth tokens are permanent** - once setup is complete, daily workflows don't need tunneling
- **Tunnel only needed for initial OAuth setup** - not for ongoing workflow execution

### Common Issues
- **Malwarebytes blocking**: Disable temporarily if SSH tunnels are blocked
- **URL must be updated**: Each new tunnel requires updating docker-compose.yml
- **Keep terminal open**: Closing the SSH command terminates the tunnel

### OAuth Provider URLs
For different OAuth providers, use these callback patterns:
- **Twitter OAuth2**: `https://[TUNNEL-URL]/rest/oauth2-credential/callback`
- **Twitter OAuth1**: `https://[TUNNEL-URL]/rest/oauth1-credential/callback`
- **Google OAuth2**: `https://[TUNNEL-URL]/rest/oauth2-credential/callback`
- **GitHub OAuth2**: `https://[TUNNEL-URL]/rest/oauth2-credential/callback`
- **Slack OAuth2**: `https://[TUNNEL-URL]/rest/oauth2-credential/callback`

### Security Considerations
- **Temporary exposure**: Tunnel exposes localhost:5678 to the internet
- **OAuth callbacks only**: External access requires password (OAuth APIs bypass this)
- **Close when done**: Terminate tunnel after OAuth setup is complete

## Alternative Tunneling Options
- **ngrok**: More stable URLs but requires account for custom subdomains
- **localtunnel (npm)**: Different service than localhost.run, uses loca.lt domain
- **cloudflared**: Cloudflare's tunneling solution

## Troubleshooting
- **Connection refused**: Verify n8n is running on localhost:5678
- **Invalid callback**: Check that tunnel URL is correctly updated in docker-compose.yml
- **Authorization failed**: Verify OAuth provider settings match tunnel URL exactly
- **Tunnel drops**: SSH connection may timeout; restart tunnel and update URLs
- **Wrong callback URL in n8n**: If n8n shows old URL after updating docker-compose.yml, use `docker-compose stop n8n` then `docker-compose up -d n8n` instead of `restart`
- **Environment variables not applied**: Check `docker-compose logs n8n --tail=10` to verify the correct tunnel URL is loaded

---
*Last updated: January 2025*
*For technical support, refer to n8n documentation or GitHub issues* 