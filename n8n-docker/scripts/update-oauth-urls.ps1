# OAuth Redirect URLs Reference Script
# With stable URL proxy, OAuth URLs NEVER change!
# This script shows the permanent URLs to use in OAuth app configurations

Write-Host "🎯 Stable OAuth Redirect URLs (NEVER change!)" -ForegroundColor Green
Write-Host "Use these permanent URLs in your OAuth app configurations:" -ForegroundColor Cyan

# Permanent stable URLs for OAuth services
$StableUrl = "http://localhost:8080"
$Services = @{
    "Google Cloud Console (Drive/Blogger)" = "$StableUrl/rest/oauth2-credential/callback"
    "Twitter Developer Portal" = "$StableUrl/rest/oauth1-credential/callback"
    "Slack API" = "$StableUrl/rest/oauth2-credential/callback"
    "GitHub OAuth Apps" = "$StableUrl/rest/oauth2-credential/callback"
    "Microsoft Azure" = "$StableUrl/rest/oauth2-credential/callback"
}

Write-Host "`n📋 Permanent OAuth Redirect URLs:" -ForegroundColor Yellow
Write-Host "Configure these URLs ONCE in your OAuth applications:" -ForegroundColor White

foreach ($Service in $Services.GetEnumerator()) {
    Write-Host "`n🔗 $($Service.Key):" -ForegroundColor Cyan
    Write-Host "   Redirect URL: $($Service.Value)" -ForegroundColor White
}

Write-Host "`n✅ Benefits of Stable URLs:" -ForegroundColor Green
Write-Host "1. Set OAuth URLs ONCE - they never change!" -ForegroundColor White
Write-Host "2. No more manual updates after restarts" -ForegroundColor White
Write-Host "3. No external service dependencies" -ForegroundColor White
Write-Host "4. Reliable local networking with Docker" -ForegroundColor White

# Verify .env file configuration
$EnvFile = Join-Path $PSScriptRoot "../.env"
if (Test-Path $EnvFile) {
    Write-Host "`n🔧 Checking .env file configuration..." -ForegroundColor Green
    $Content = Get-Content $EnvFile
    $WebhookLine = $Content | Where-Object { $_ -match "WEBHOOK_URL=" }
    if ($WebhookLine -match "http://localhost:8080") {
        Write-Host "✅ .env file correctly configured with stable URL" -ForegroundColor Green
    } else {
        Write-Host "⚠️  .env file may need updating to use stable URL" -ForegroundColor Yellow
        Write-Host "   Expected: WEBHOOK_URL=http://localhost:8080/" -ForegroundColor Cyan
    }
} else {
    Write-Host "⚠️  .env file not found at $EnvFile" -ForegroundColor Yellow
}

Write-Host "`n🚀 Next Steps:" -ForegroundColor Green
Write-Host "1. Update OAuth redirect URLs in all external services" -ForegroundColor White
Write-Host "2. Restart n8n container: docker-compose restart n8n" -ForegroundColor White
Write-Host "3. Test credentials in n8n interface" -ForegroundColor White
