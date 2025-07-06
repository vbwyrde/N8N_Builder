# Stop-N8N-Stable.ps1
# Unified shutdown script for n8n + Stable URL Proxy

param(
    [switch]$KeepProxy,
    [switch]$KeepN8N
)

Write-Host "STOPPING N8N + STABLE URL PROXY" -ForegroundColor Red
Write-Host "=" * 40

# Stop stable proxy (unless keeping it)
if (-not $KeepProxy) {
    Write-Host "Stopping stable URL proxy..." -ForegroundColor Yellow
    docker-compose -f docker-compose.proxy.yml down
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Stable proxy stopped" -ForegroundColor Green
    }
    else {
        Write-Host "ERROR: Failed to stop stable proxy" -ForegroundColor Red
    }
}
else {
    Write-Host "INFO: Keeping stable proxy running (-KeepProxy specified)" -ForegroundColor Cyan
}

# Stop n8n services (unless keeping them)
if (-not $KeepN8N) {
    Write-Host "Stopping n8n services..." -ForegroundColor Yellow
    docker-compose down
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: n8n services stopped" -ForegroundColor Green
    }
    else {
        Write-Host "ERROR: Failed to stop n8n services" -ForegroundColor Red
    }
}
else {
    Write-Host "INFO: Keeping n8n services running (-KeepN8N specified)" -ForegroundColor Cyan
}

# Show final status
Write-Host "`nFinal Status:" -ForegroundColor Cyan
Write-Host "=" * 15

$runningContainers = docker ps --format "table {{.Names}}\t{{.Status}}" | Where-Object { $_ -match "n8n|proxy" }

if ($runningContainers) {
    Write-Host "Still running:" -ForegroundColor Yellow
    $runningContainers | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
}
else {
    Write-Host "All services stopped" -ForegroundColor Green
}

Write-Host ""
Write-Host "SUCCESS: Shutdown Complete!" -ForegroundColor Green

if ($KeepN8N) {
    Write-Host "INFO: n8n is still accessible at: http://localhost:5678" -ForegroundColor Cyan
}

if ($KeepProxy) {
    Write-Host "INFO: Stable URL still accessible at: http://localhost:8080" -ForegroundColor Cyan
}
