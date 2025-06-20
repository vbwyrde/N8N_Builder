# Update OAuth Redirect URLs Script
# Run this script whenever nGrok URL changes

param(
    [Parameter(Mandatory=$true)]
    [string]$NewNgrokUrl
)

Write-Host "🔄 Updating OAuth redirect URLs for new nGrok URL: $NewNgrokUrl" -ForegroundColor Green

# List of services that need URL updates
$Services = @{
    "Google Cloud Console (Drive/Blogger)" = "$NewNgrokUrl/rest/oauth2-credential/callback"
    "Twitter Developer Portal" = "$NewNgrokUrl/rest/oauth1-credential/callback"
    "Slack API" = "$NewNgrokUrl/rest/oauth2-credential/callback"
    "GitHub OAuth Apps" = "$NewNgrokUrl/rest/oauth2-credential/callback"
    "Microsoft Azure" = "$NewNgrokUrl/rest/oauth2-credential/callback"
}

Write-Host "`n📋 Manual Updates Required:" -ForegroundColor Yellow
Write-Host "Please update the following redirect URLs in each service:" -ForegroundColor White

foreach ($Service in $Services.GetEnumerator()) {
    Write-Host "`n🔗 $($Service.Key):" -ForegroundColor Cyan
    Write-Host "   Redirect URL: $($Service.Value)" -ForegroundColor White
}

Write-Host "`n⚠️  Important Notes:" -ForegroundColor Red
Write-Host "1. Update ALL OAuth applications with the new redirect URLs" -ForegroundColor White
Write-Host "2. Some services may take a few minutes to propagate changes" -ForegroundColor White
Write-Host "3. Test each credential in n8n after updating" -ForegroundColor White
Write-Host "4. Consider upgrading to nGrok paid plan for static URLs" -ForegroundColor White

# Update .env file
$EnvFile = Join-Path $PSScriptRoot "../.env"
if (Test-Path $EnvFile) {
    Write-Host "`n🔧 Updating .env file..." -ForegroundColor Green
    $Content = Get-Content $EnvFile
    $UpdatedContent = $Content -replace "WEBHOOK_URL=.*", "WEBHOOK_URL=$NewNgrokUrl/"
    $UpdatedContent | Set-Content $EnvFile
    Write-Host "✅ .env file updated with new webhook URL" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found at $EnvFile" -ForegroundColor Yellow
}

Write-Host "`n🚀 Next Steps:" -ForegroundColor Green
Write-Host "1. Update OAuth redirect URLs in all external services" -ForegroundColor White
Write-Host "2. Restart n8n container: docker-compose restart n8n" -ForegroundColor White
Write-Host "3. Test credentials in n8n interface" -ForegroundColor White
