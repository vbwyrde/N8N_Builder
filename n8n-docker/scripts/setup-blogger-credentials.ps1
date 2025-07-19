# Blogger Credentials Setup Helper Script
# This script provides step-by-step guidance for setting up Blogger API credentials

param(
    [string]$TunnelUrl = ""
)

# Get current LocalTunnel URL if not provided
if (-not $TunnelUrl) {
    try {
        # Check if LocalTunnel is running by looking for the SSH process
        $sshProcess = Get-Process -Name "ssh" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*localhost.run*" }

        if ($sshProcess) {
            Write-Host "⚠️  LocalTunnel SSH process detected, but URL must be provided manually." -ForegroundColor Yellow
            Write-Host "💡 LocalTunnel URLs are displayed in the SSH terminal when you run:" -ForegroundColor Cyan
            Write-Host "   ssh -R 80:localhost:5678 nokey@localhost.run" -ForegroundColor Cyan
            Write-Host "   Look for a URL like: https://7cf5d5df8e061d.lhr.life" -ForegroundColor Cyan
        } else {
            Write-Host "⚠️  LocalTunnel not detected. Please start it first:" -ForegroundColor Yellow
            Write-Host "   ssh -R 80:localhost:5678 nokey@localhost.run" -ForegroundColor Cyan
        }

        $TunnelUrl = Read-Host "Enter your current LocalTunnel URL (e.g., https://7cf5d5df8e061d.lhr.life)"
    } catch {
        Write-Host "⚠️  Could not detect LocalTunnel. Please provide it manually." -ForegroundColor Yellow
        $TunnelUrl = Read-Host "Enter your current LocalTunnel URL (e.g., https://7cf5d5df8e061d.lhr.life)"
    }
}

$CallbackUrl = "$TunnelUrl/rest/oauth2-credential/callback"

Write-Host "🚀 Blogger API Credentials Setup Guide" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

Write-Host "`n📋 Step 1: Google Cloud Console Setup" -ForegroundColor Yellow
Write-Host "1. Open: https://console.cloud.google.com/" -ForegroundColor White
Write-Host "2. Create new project or select existing one" -ForegroundColor White
Write-Host "3. Go to: APIs & Services → Library" -ForegroundColor White
Write-Host "4. Search for 'Blogger API v3' and enable it" -ForegroundColor White

Write-Host "`n📋 Step 2: OAuth Consent Screen (if not done)" -ForegroundColor Yellow
Write-Host "1. Go to: APIs & Services → OAuth consent screen" -ForegroundColor White
Write-Host "2. User Type: External" -ForegroundColor White
Write-Host "3. App name: 'N8N Local Instance'" -ForegroundColor White
Write-Host "4. Add your email for support and developer contact" -ForegroundColor White
Write-Host "5. Add test users (your email) in Test users section" -ForegroundColor White

Write-Host "`n📋 Step 3: Create OAuth Credentials" -ForegroundColor Yellow
Write-Host "1. Go to: APIs & Services → Credentials" -ForegroundColor White
Write-Host "2. Click: Create Credentials → OAuth 2.0 Client ID" -ForegroundColor White
Write-Host "3. Application type: Web application" -ForegroundColor White
Write-Host "4. Name: 'N8N Blogger API'" -ForegroundColor White
Write-Host "5. Authorized redirect URIs:" -ForegroundColor White
Write-Host "   $CallbackUrl" -ForegroundColor Cyan

Write-Host "`n📋 Step 4: N8N Configuration" -ForegroundColor Yellow
Write-Host "1. Open N8N: $TunnelUrl" -ForegroundColor White
Write-Host "2. Go to: Settings → Credentials" -ForegroundColor White
Write-Host "3. Add new credential: 'Google OAuth2 API'" -ForegroundColor White
Write-Host "4. Enter Client ID and Client Secret from Google Console" -ForegroundColor White
Write-Host "5. Scopes (add these manually):" -ForegroundColor White
Write-Host "   https://www.googleapis.com/auth/blogger" -ForegroundColor Cyan
Write-Host "   https://www.googleapis.com/auth/blogger.readonly" -ForegroundColor Cyan
Write-Host "6. Complete OAuth authorization flow" -ForegroundColor White

Write-Host "`n📋 Step 5: Test the Setup" -ForegroundColor Yellow
Write-Host "1. Create a test workflow in N8N" -ForegroundColor White
Write-Host "2. Add an HTTP Request node with these settings:" -ForegroundColor White
Write-Host "   Method: GET" -ForegroundColor White
Write-Host "   URL: https://www.googleapis.com/blogger/v3/users/self/blogs" -ForegroundColor Cyan
Write-Host "   Authentication: Use your new Google OAuth2 credential" -ForegroundColor White
Write-Host "3. Execute the workflow to test" -ForegroundColor White

Write-Host "`n🔧 Blogger API Quick Reference" -ForegroundColor Green
Write-Host "Base URL: https://www.googleapis.com/blogger/v3" -ForegroundColor White
Write-Host "Common Endpoints:" -ForegroundColor White
Write-Host "  GET /users/self/blogs                    # List your blogs" -ForegroundColor Cyan
Write-Host "  GET /blogs/{blogId}/posts                # List posts" -ForegroundColor Cyan
Write-Host "  POST /blogs/{blogId}/posts               # Create post" -ForegroundColor Cyan
Write-Host "  PUT /blogs/{blogId}/posts/{postId}       # Update post" -ForegroundColor Cyan
Write-Host "  DELETE /blogs/{blogId}/posts/{postId}    # Delete post" -ForegroundColor Cyan

Write-Host "`n💡 Pro Tips:" -ForegroundColor Green
Write-Host "• You can use the same OAuth credentials for multiple Google services" -ForegroundColor White
Write-Host "• Blog ID can be found in your Blogger dashboard URL or API response" -ForegroundColor White
Write-Host "• Use 'self' as user ID to access your own blogs" -ForegroundColor White
Write-Host "• Test with readonly scope first, then add full access if needed" -ForegroundColor White

Write-Host "`n⚠️  Important Notes:" -ForegroundColor Red
Write-Host "• Blogger API has rate limits (requests per day/per 100 seconds)" -ForegroundColor White
Write-Host "• OAuth consent screen must be configured for external users" -ForegroundColor White
Write-Host "• Add your email as a test user during development" -ForegroundColor White
Write-Host "• Update redirect URI when LocalTunnel URL changes (URLs change on each restart)" -ForegroundColor White
Write-Host "• LocalTunnel URLs are temporary - OAuth tokens persist after setup" -ForegroundColor White

Write-Host "`n🔗 Useful Links:" -ForegroundColor Blue
Write-Host "• Google Cloud Console: https://console.cloud.google.com/" -ForegroundColor White
Write-Host "• Blogger API Documentation: https://developers.google.com/blogger" -ForegroundColor White
Write-Host "• OAuth 2.0 Playground: https://developers.google.com/oauthplayground/" -ForegroundColor White
Write-Host "• Current LocalTunnel URL: $TunnelUrl" -ForegroundColor White
Write-Host "• LocalTunnel Setup Guide: Documentation\ReadMe_TunnelSetup.md" -ForegroundColor White

Write-Host "`n✅ Setup Complete!" -ForegroundColor Green
Write-Host "After completing these steps, you'll be able to create custom Blogger nodes in N8N." -ForegroundColor White
