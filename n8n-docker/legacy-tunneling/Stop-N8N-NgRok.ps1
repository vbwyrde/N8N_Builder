# Stop-N8N-NgRok.ps1
# Automated shutdown script for n8n Docker + nGrok tunnel

param(
    [switch]$KeepDocker,
    [switch]$Verbose
)

# Load configuration
$ConfigPath = Join-Path $PSScriptRoot "config.ps1"
if (Test-Path $ConfigPath) {
    . $ConfigPath
    $N8N_DOCKER_PATH = $script:Config.DockerPath
} else {
    Write-Host "ERROR: Configuration file not found at $ConfigPath" -ForegroundColor Red
    Write-Host "Please copy config.ps1.template to config.ps1 and customize it" -ForegroundColor Yellow
    exit 1
}

Write-Host "STOPPING n8n + nGrok Services" -ForegroundColor Red
Write-Host "=" * 40

# Function to stop nGrok processes
function Stop-NgrokProcesses {
    Write-Host "Stopping nGrok processes..." -ForegroundColor Yellow
    
    try {
        # Find and stop nGrok processes
        $ngrokProcesses = Get-Process -Name "ngrok" -ErrorAction SilentlyContinue
        
        if ($ngrokProcesses) {
            foreach ($process in $ngrokProcesses) {
                Write-Host "Stopping nGrok process (PID: $($process.Id))" -ForegroundColor Yellow
                Stop-Process -Id $process.Id -Force
            }
            Write-Host "SUCCESS: nGrok processes stopped" -ForegroundColor Green
        }
        else {
            Write-Host "INFO: No nGrok processes found running" -ForegroundColor Cyan
        }
        
        return $true
    }
    catch {
        Write-Host "ERROR: Error stopping nGrok: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to stop Docker containers
function Stop-DockerContainers {
    Write-Host "Stopping Docker containers..." -ForegroundColor Yellow
    
    try {
        Set-Location $N8N_DOCKER_PATH
        
        # Stop containers
        docker-compose down
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SUCCESS: Docker containers stopped successfully" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "ERROR: Failed to stop Docker containers" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "ERROR: Error stopping Docker containers: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to show final status
function Show-Status {
    Write-Host ""
    Write-Host "FINAL STATUS:" -ForegroundColor Cyan
    Write-Host "-" * 20

    # Check nGrok
    $ngrokRunning = Get-Process -Name "ngrok" -ErrorAction SilentlyContinue
    if ($ngrokRunning) {
        Write-Host "nGrok: Still running" -ForegroundColor Yellow
    }
    else {
        Write-Host "nGrok: Stopped" -ForegroundColor Green
    }

    # Check Docker containers
    try {
        $n8nRunning = docker ps --filter "name=n8n" --format "{{.Names}}" 2>$null
        if ($n8nRunning -contains "n8n-dev") {
            Write-Host "n8n Docker: Still running" -ForegroundColor Yellow
        }
        else {
            Write-Host "n8n Docker: Stopped" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "n8n Docker: Status unknown" -ForegroundColor Gray
    }
}

# Main execution
try {
    # Stop nGrok first
    Stop-NgrokProcesses | Out-Null

    # Stop Docker containers (unless keeping them)
    if (-not $KeepDocker) {
        Stop-DockerContainers | Out-Null
    }
    else {
        Write-Host "INFO: Keeping Docker containers running (-KeepDocker specified)" -ForegroundColor Cyan
    }

    # Show final status
    Show-Status

    Write-Host ""
    Write-Host "SUCCESS: Shutdown Complete!" -ForegroundColor Green

    if ($KeepDocker) {
        Write-Host "INFO: n8n is still accessible at: http://localhost:5678" -ForegroundColor Cyan
    }
}
catch {
    Write-Host "ERROR: Shutdown script failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
