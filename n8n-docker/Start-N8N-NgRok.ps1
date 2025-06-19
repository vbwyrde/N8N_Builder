# Start-N8N-NgRok.ps1
# Automated startup script for n8n Docker + nGrok tunnel
# This script automates the entire startup process and updates webhook URLs

param(
    [switch]$SkipDocker,
    [switch]$SkipNgrok,
    [switch]$Verbose
)

# Load configuration
$ConfigPath = Join-Path $PSScriptRoot "config.ps1"
if (Test-Path $ConfigPath) {
    . $ConfigPath
    $NGROK_PATH = $script:Config.NgrokPath
    $N8N_DOCKER_PATH = $script:Config.DockerPath
    $ENV_FILE = $script:Config.EnvFile
    $NGROK_API_URL = $script:Config.NgrokApiUrl
} else {
    Write-Host "ERROR: Configuration file not found at $ConfigPath" -ForegroundColor Red
    Write-Host "Please copy config.ps1.template to config.ps1 and customize it" -ForegroundColor Yellow
    exit 1
}

Write-Host "STARTING n8n + nGrok Automation Script" -ForegroundColor Green
Write-Host "=" * 50

# Function to check if Docker is running
function Test-DockerRunning {
    try {
        docker version 2>$null | Out-Null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

# Function to check if n8n container is running
function Test-N8NRunning {
    try {
        $containers = docker ps --filter "name=n8n" --format "{{.Names}}" 2>$null
        return $containers -contains "n8n-dev"
    }
    catch {
        return $false
    }
}

# Function to start Docker containers
function Start-DockerContainers {
    Write-Host "Starting Docker containers..." -ForegroundColor Yellow

    Set-Location $N8N_DOCKER_PATH

    # Start containers
    docker-compose up -d

    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Docker containers started successfully" -ForegroundColor Green

        # Wait for n8n to be ready
        Write-Host "Waiting for n8n to be ready..." -ForegroundColor Yellow
        $timeout = 60
        $elapsed = 0

        do {
            Start-Sleep -Seconds 2
            $elapsed += 2
            $logs = docker logs n8n-dev --tail 5 2>$null
            if ($logs -match "n8n ready on") {
                Write-Host "SUCCESS: n8n is ready!" -ForegroundColor Green
                return $true
            }
        } while ($elapsed -lt $timeout)

        Write-Host "WARNING: n8n startup timeout - check logs manually" -ForegroundColor Yellow
        return $true
    }
    else {
        Write-Host "ERROR: Failed to start Docker containers" -ForegroundColor Red
        return $false
    }
}

# Function to start nGrok tunnel
function Start-NgrokTunnel {
    Write-Host "Starting nGrok tunnel..." -ForegroundColor Yellow

    # Check if nGrok is already running
    try {
        $response = Invoke-RestMethod -Uri $NGROK_API_URL -ErrorAction SilentlyContinue
        if ($response.tunnels.Count -gt 0) {
            Write-Host "SUCCESS: nGrok tunnel already running" -ForegroundColor Green
            return $true
        }
    }
    catch {
        # nGrok not running, continue to start it
    }

    # Start nGrok in background
    Start-Job -ScriptBlock {
        param($ngrokPath)
        & $ngrokPath start n8n
    } -ArgumentList $NGROK_PATH | Out-Null

    # Wait for nGrok to start
    Write-Host "Waiting for nGrok tunnel to establish..." -ForegroundColor Yellow
    $timeout = 30
    $elapsed = 0

    do {
        Start-Sleep -Seconds 2
        $elapsed += 2
        try {
            $response = Invoke-RestMethod -Uri $NGROK_API_URL -ErrorAction SilentlyContinue
            if ($response.tunnels.Count -gt 0) {
                Write-Host "SUCCESS: nGrok tunnel established!" -ForegroundColor Green
                return $true
            }
        }
        catch {
            # Continue waiting
        }
    } while ($elapsed -lt $timeout)

    Write-Host "WARNING: nGrok tunnel timeout - check manually" -ForegroundColor Yellow
    return $false
}

# Function to get nGrok public URL
function Get-NgrokPublicUrl {
    try {
        $response = Invoke-RestMethod -Uri $NGROK_API_URL
        $httpsTunnel = $response.tunnels | Where-Object { $_.proto -eq "https" }
        
        if ($httpsTunnel) {
            return $httpsTunnel.public_url
        }
        else {
            Write-Host "ERROR: No HTTPS tunnel found" -ForegroundColor Red
            return $null
        }
    }
    catch {
        Write-Host "ERROR: Failed to get nGrok URL: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Function to update .env file with new webhook URL
function Update-WebhookUrl {
    param([string]$NewUrl)

    Write-Host "Updating webhook URL in .env file..." -ForegroundColor Yellow
    
    try {
        $envContent = Get-Content $ENV_FILE
        $updatedContent = @()
        $webhookUpdated = $false
        
        foreach ($line in $envContent) {
            if ($line -match "^WEBHOOK_URL=") {
                $updatedContent += "WEBHOOK_URL=$NewUrl/"
                $webhookUpdated = $true
                Write-Host "SUCCESS: Updated WEBHOOK_URL to: $NewUrl/" -ForegroundColor Green
            }
            else {
                $updatedContent += $line
            }
        }

        if (-not $webhookUpdated) {
            Write-Host "WARNING: WEBHOOK_URL not found in .env file" -ForegroundColor Yellow
        }

        $updatedContent | Set-Content $ENV_FILE
        return $true
    }
    catch {
        Write-Host "ERROR: Failed to update .env file: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to restart n8n container to apply new config
function Restart-N8NContainer {
    Write-Host "Restarting n8n container to apply new configuration..." -ForegroundColor Yellow

    Set-Location $N8N_DOCKER_PATH
    docker-compose restart n8n

    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: n8n container restarted successfully" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "ERROR: Failed to restart n8n container" -ForegroundColor Red
        return $false
    }
}

# Main execution
try {
    # Step 1: Check Docker
    if (-not $SkipDocker) {
        if (-not (Test-DockerRunning)) {
            Write-Host "ERROR: Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
            exit 1
        }

        if (-not (Test-N8NRunning)) {
            if (-not (Start-DockerContainers)) {
                exit 1
            }
        }
        else {
            Write-Host "SUCCESS: n8n container already running" -ForegroundColor Green
        }
    }

    # Step 2: Start nGrok
    if (-not $SkipNgrok) {
        if (-not (Start-NgrokTunnel)) {
            Write-Host "WARNING: nGrok tunnel may not be ready, continuing..." -ForegroundColor Yellow
        }
    }

    # Step 3: Get public URL and update config
    Start-Sleep -Seconds 3  # Give nGrok a moment to stabilize

    $publicUrl = Get-NgrokPublicUrl
    if ($publicUrl) {
        Write-Host "nGrok Public URL: $publicUrl" -ForegroundColor Cyan

        if (Update-WebhookUrl -NewUrl $publicUrl) {
            Restart-N8NContainer | Out-Null
        }
    }
    else {
        Write-Host "WARNING: Could not retrieve nGrok URL automatically" -ForegroundColor Yellow
        Write-Host "INFO: Check nGrok status manually at: http://127.0.0.1:4040" -ForegroundColor Cyan
    }

    # Final status
    Write-Host ""
    Write-Host "SUCCESS: Startup Complete!" -ForegroundColor Green
    Write-Host "=" * 50
    Write-Host "Local n8n:     http://localhost:5678" -ForegroundColor Cyan
    Write-Host "nGrok Monitor: http://127.0.0.1:4040" -ForegroundColor Cyan
    if ($publicUrl) {
        Write-Host "Public URL:    $publicUrl" -ForegroundColor Cyan
    }
    Write-Host ""
    Write-Host "INFO: Use Ctrl+C to stop nGrok tunnel when done" -ForegroundColor Yellow
}
catch {
    Write-Host "ERROR: Script failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
