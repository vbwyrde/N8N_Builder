# Start-N8N-Stable.ps1
# Unified startup script for n8n + Stable URL Proxy
# Provides stable localhost:8080 URL that never changes

param(
    [switch]$SkipProxy,
    [switch]$Verbose
)

Write-Host "STARTING N8N + STABLE URL PROXY" -ForegroundColor Green
Write-Host "=" * 45

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
Write-Host "Starting n8n services..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: n8n services started" -ForegroundColor Green
}
else {
    Write-Host "ERROR: Failed to start n8n services" -ForegroundColor Red
    exit 1
}

# Start stable proxy (unless skipped)
if (-not $SkipProxy) {
    Write-Host "Starting stable URL proxy..." -ForegroundColor Yellow
    docker-compose -f docker-compose.proxy.yml up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Stable proxy started" -ForegroundColor Green
    }
    else {
        Write-Host "ERROR: Failed to start stable proxy" -ForegroundColor Red
        exit 1
    }
}

# Wait for services to be ready
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check n8n direct access
Write-Host "Checking n8n direct access..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "SUCCESS: n8n is accessible at http://localhost:5678" -ForegroundColor Green
    }
}
catch {
    Write-Host "WARNING: n8n may still be starting up" -ForegroundColor Yellow
}

# Check stable proxy (if not skipped)
if (-not $SkipProxy) {
    Write-Host "Checking stable URL proxy..." -ForegroundColor Cyan
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8080/health" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Host "SUCCESS: Stable proxy is ready at http://localhost:8080" -ForegroundColor Green
            
            # Test actual n8n forwarding
            $n8nResponse = Invoke-WebRequest -Uri "http://localhost:8080" -UseBasicParsing -TimeoutSec 10
            if ($n8nResponse.StatusCode -eq 200 -and $n8nResponse.Content -match "n8n") {
                Write-Host "SUCCESS: n8n is accessible through stable URL" -ForegroundColor Green
            }
        }
    }
    catch {
        Write-Host "WARNING: Stable proxy may still be starting up" -ForegroundColor Yellow
    }
}

# Show service status
Write-Host "`nService Status:" -ForegroundColor Cyan
Write-Host "=" * 20

$containers = docker ps --format "table {{.Names}}\t{{.Status}}" | Where-Object { $_ -match "n8n|proxy" }
if ($containers) {
    Write-Host "Running containers:" -ForegroundColor Green
    $containers | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
}

Write-Host "`nSUCCESS: All Services Started!" -ForegroundColor Green
Write-Host "=" * 30

Write-Host "`nAccess Points:" -ForegroundColor Cyan
Write-Host "- n8n Direct Access: http://localhost:5678" -ForegroundColor White
if (-not $SkipProxy) {
    Write-Host "- STABLE WEBHOOK URL: http://localhost:8080" -ForegroundColor Yellow
    Write-Host "- Proxy Health Check: http://localhost:8080/health" -ForegroundColor White
}

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "1. Access n8n at http://localhost:5678 OR http://localhost:8080" -ForegroundColor White
if (-not $SkipProxy) {
    Write-Host "2. Configure OAuth apps to use http://localhost:8080 as webhook URL" -ForegroundColor White
    Write-Host "3. Test webhook delivery with your workflows" -ForegroundColor White
}

if (-not $SkipProxy) {
    Write-Host "`n🎯 IMPORTANT: Your webhook URL is now STABLE!" -ForegroundColor Green
    Write-Host "   http://localhost:8080 will NEVER change between restarts!" -ForegroundColor Green
    Write-Host "   No more OAuth credential updates needed!" -ForegroundColor Green
}

Write-Host "`nTo stop services: .\Stop-N8N-Stable.ps1" -ForegroundColor Cyan
