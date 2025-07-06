# Start-N8N-Zrok-Simple.ps1
# Simplified startup script for n8n Docker + Zrok services

param(
    [switch]$SkipDocker,
    [switch]$SkipZrok
)

Write-Host "STARTING n8n + Zrok Services" -ForegroundColor Green
Write-Host "=" * 40

# Check Docker
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    docker info | Out-Null
    Write-Host "SUCCESS: Docker is running" -ForegroundColor Green
}
catch {
    Write-Host "ERROR: Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}

# Start n8n services
if (-not $SkipDocker) {
    Write-Host "Starting n8n Docker services..." -ForegroundColor Yellow
    
    docker-compose up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: n8n Docker services started" -ForegroundColor Green
    }
    else {
        Write-Host "ERROR: Failed to start n8n Docker services" -ForegroundColor Red
        exit 1
    }
}

# Start zrok services
if (-not $SkipZrok) {
    Write-Host "Starting Zrok services..." -ForegroundColor Yellow
    
    docker-compose -f docker-compose.zrok.yml --env-file .env.zrok up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Zrok services started" -ForegroundColor Green
    }
    else {
        Write-Host "ERROR: Failed to start Zrok services" -ForegroundColor Red
        exit 1
    }
}

# Wait for services to be ready
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check n8n
Write-Host "Checking n8n status..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678/healthz" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "SUCCESS: n8n is ready at http://localhost:5678" -ForegroundColor Green
    }
}
catch {
    Write-Host "WARNING: n8n may still be starting up" -ForegroundColor Yellow
}

# Check zrok controller
Write-Host "Checking zrok controller status..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:18080/api/v1/version" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "SUCCESS: Zrok controller is ready at http://localhost:18080" -ForegroundColor Green
    }
}
catch {
    Write-Host "WARNING: Zrok controller may still be starting up" -ForegroundColor Yellow
}

# Check zrok public access
Write-Host "Checking zrok public access..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8080" -UseBasicParsing -TimeoutSec 10
    Write-Host "SUCCESS: Zrok public access is ready at http://localhost:8080" -ForegroundColor Green
}
catch {
    Write-Host "WARNING: Zrok public access may still be starting up" -ForegroundColor Yellow
}

# Show service status
Write-Host "`nService Status:" -ForegroundColor Cyan
Write-Host "=" * 20

$containers = docker ps --format "table {{.Names}}\t{{.Status}}" | Where-Object { $_ -match "n8n|zrok" }
if ($containers) {
    Write-Host "Running containers:" -ForegroundColor Green
    $containers | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
}

Write-Host "`nSUCCESS: Services Started!" -ForegroundColor Green
Write-Host "=" * 25

Write-Host "`nAccess Points:" -ForegroundColor Cyan
Write-Host "- n8n Interface: http://localhost:5678" -ForegroundColor White
Write-Host "- Stable Webhook URL: http://localhost:8080" -ForegroundColor White
Write-Host "- Zrok Controller: http://localhost:18080" -ForegroundColor White

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "1. Access n8n at http://localhost:5678" -ForegroundColor White
Write-Host "2. Configure OAuth apps to use http://localhost:8080 as webhook URL" -ForegroundColor White
Write-Host "3. Test webhook delivery" -ForegroundColor White

Write-Host "`nIMPORTANT: Your webhook URL (http://localhost:8080) is now STABLE!" -ForegroundColor Green
Write-Host "It will not change between restarts, eliminating the OAuth update problem." -ForegroundColor Green
