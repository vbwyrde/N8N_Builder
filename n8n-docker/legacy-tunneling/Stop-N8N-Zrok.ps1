# Stop-N8N-Zrok.ps1
# Automated shutdown script for n8n Docker + Zrok services

param(
    [switch]$KeepDocker,
    [switch]$KeepZrok,
    [switch]$Verbose
)

$N8N_DOCKER_PATH = $PSScriptRoot

Write-Host "STOPPING n8n + Zrok Services" -ForegroundColor Red
Write-Host "=" * 40

# Function to stop Zrok services
function Stop-ZrokServices {
    Write-Host "Stopping Zrok services..." -ForegroundColor Yellow
    
    try {
        Set-Location $N8N_DOCKER_PATH
        
        # Stop zrok services
        docker-compose -f docker-compose.zrok.yml down
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SUCCESS: Zrok services stopped" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "ERROR: Failed to stop Zrok services" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "ERROR: Zrok shutdown failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to stop n8n Docker services
function Stop-N8NDocker {
    Write-Host "Stopping n8n Docker services..." -ForegroundColor Yellow
    
    try {
        Set-Location $N8N_DOCKER_PATH
        
        # Stop n8n services
        docker-compose down
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SUCCESS: n8n Docker services stopped" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "ERROR: Failed to stop n8n Docker services" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "ERROR: n8n shutdown failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to show final status
function Show-Status {
    Write-Host "`nFinal Status:" -ForegroundColor Cyan
    Write-Host "=" * 15
    
    # Check for running containers
    $runningContainers = docker ps --format "table {{.Names}}\t{{.Status}}" | Where-Object { $_ -match "n8n|zrok" }
    
    if ($runningContainers) {
        Write-Host "Still running:" -ForegroundColor Yellow
        $runningContainers | ForEach-Object { Write-Host "  $_" -ForegroundColor White }
    }
    else {
        Write-Host "✓ All services stopped" -ForegroundColor Green
    }
}

# Main execution
try {
    # Stop Zrok services first (unless keeping them)
    if (-not $KeepZrok) {
        Stop-ZrokServices | Out-Null
    }
    else {
        Write-Host "INFO: Keeping Zrok services running (-KeepZrok specified)" -ForegroundColor Cyan
    }

    # Stop n8n Docker services (unless keeping them)
    if (-not $KeepDocker) {
        Stop-N8NDocker | Out-Null
    }
    else {
        Write-Host "INFO: Keeping n8n Docker services running (-KeepDocker specified)" -ForegroundColor Cyan
    }

    # Show final status
    Show-Status

    Write-Host ""
    Write-Host "SUCCESS: Shutdown Complete!" -ForegroundColor Green

    if ($KeepDocker) {
        Write-Host "INFO: n8n is still accessible at: http://localhost:5678" -ForegroundColor Cyan
    }
    
    if ($KeepZrok) {
        Write-Host "INFO: Zrok services still running at: http://localhost:8080" -ForegroundColor Cyan
    }
}
catch {
    Write-Host "ERROR: Shutdown script failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
