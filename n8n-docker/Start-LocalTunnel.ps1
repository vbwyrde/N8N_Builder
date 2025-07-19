# LocalTunnel for n8n OAuth Integrations
# Provides stable HTTPS URLs for OAuth2 callbacks
# Independent of N8N_Builder - works directly with n8n Docker

Write-Host "🌐 LocalTunnel for n8n OAuth Integrations" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Configuration
$PORT = 5678
$SUBDOMAIN = "n8n-oauth-stable"
$PUBLIC_URL = "https://$SUBDOMAIN.loca.lt"

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Local n8n: http://localhost:$PORT" -ForegroundColor White
Write-Host "  Public URL: $PUBLIC_URL" -ForegroundColor White
Write-Host "  OAuth Callback: $PUBLIC_URL/rest/oauth2-credential/callback" -ForegroundColor Cyan
Write-Host ""

# Check if n8n is running
Write-Host "Checking n8n status..." -ForegroundColor Yellow
$dockerStatus = docker-compose ps --services --filter "status=running" 2>$null
if ($dockerStatus -notcontains "n8n") {
    Write-Host "⚠️  n8n is not running. Starting n8n first..." -ForegroundColor Yellow
    docker-compose up -d n8n
    Write-Host "Waiting for n8n to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
}

# Check if LocalTunnel is installed
if (-not (Test-Path ".\node_modules\.bin\lt")) {
    Write-Host "❌ LocalTunnel not found. Installing..." -ForegroundColor Red
    if (-not (Test-Path ".\package.json")) {
        Write-Host "Creating package.json..." -ForegroundColor Yellow
        npm init -y
    }
    npm install localtunnel
}

Write-Host "🚀 Starting LocalTunnel..." -ForegroundColor Green
Write-Host ""
Write-Host "📋 OAuth Callback URLs:" -ForegroundColor Cyan
Write-Host "  Twitter OAuth2: $PUBLIC_URL/rest/oauth2-credential/callback" -ForegroundColor White
Write-Host "  Twitter OAuth1: $PUBLIC_URL/rest/oauth1-credential/callback" -ForegroundColor White
Write-Host "  Google OAuth2:  $PUBLIC_URL/rest/oauth2-credential/callback" -ForegroundColor White
Write-Host "  GitHub OAuth2:  $PUBLIC_URL/rest/oauth2-credential/callback" -ForegroundColor White
Write-Host "  Slack OAuth2:   $PUBLIC_URL/rest/oauth2-credential/callback" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Webhook URLs:" -ForegroundColor Cyan
Write-Host "  Base: $PUBLIC_URL/webhook/" -ForegroundColor White
Write-Host "  Test: $PUBLIC_URL/webhook-test/" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Keep this window open to maintain the tunnel" -ForegroundColor Yellow
Write-Host "⚠️  Browser access requires password (OAuth2 APIs bypass this)" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎯 For n8n workflow development:" -ForegroundColor Green
Write-Host "  - Direct access: http://localhost:5678" -ForegroundColor White
Write-Host "  - Through tunnel: $PUBLIC_URL (requires password)" -ForegroundColor White
Write-Host "  - Add OAuth credentials: Settings → Credentials" -ForegroundColor White
Write-Host ""
Write-Host "💡 IMPORTANT: For OAuth1 credentials, create them via tunnel URL!" -ForegroundColor Yellow
Write-Host "   OAuth2 credentials can be created from either URL" -ForegroundColor Yellow
Write-Host ""

# Start LocalTunnel
& ".\node_modules\.bin\lt" --port $PORT --subdomain $SUBDOMAIN 