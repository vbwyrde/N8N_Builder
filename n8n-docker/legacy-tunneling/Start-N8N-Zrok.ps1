# Start-N8N-Zrok.ps1
# Automated startup script for n8n Docker + Zrok tunnel
# Provides stable URLs that don't change between restarts

param(
    [switch]$SkipDocker,
    [switch]$SkipZrok,
    [switch]$Verbose,
    [switch]$SetupOnly
)

# Configuration
$N8N_DOCKER_PATH = $PSScriptRoot
$ZROK_ENV_FILE = "$N8N_DOCKER_PATH\.env.zrok"
$N8N_ENV_FILE = "$N8N_DOCKER_PATH\.env"
$ZROK_API_URL = "http://localhost:18080"
$ZROK_PUBLIC_URL = "http://localhost:8080"

Write-Host "STARTING n8n + Zrok Services" -ForegroundColor Green
Write-Host "=" * 40

# Function to check if Docker is running
function Test-DockerRunning {
    try {
        docker info | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to start n8n Docker services
function Start-N8NDocker {
    Write-Host "Starting n8n Docker services..." -ForegroundColor Yellow
    
    try {
        Set-Location $N8N_DOCKER_PATH
        
        # Start n8n services
        docker-compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SUCCESS: n8n Docker services started" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "ERROR: Failed to start n8n Docker services" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "ERROR: Docker startup failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to start Zrok services
function Start-ZrokServices {
    Write-Host "Starting Zrok services..." -ForegroundColor Yellow
    
    try {
        Set-Location $N8N_DOCKER_PATH
        
        # Start zrok services
        docker-compose -f docker-compose.zrok.yml --env-file .env.zrok up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SUCCESS: Zrok services started" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "ERROR: Failed to start Zrok services" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "ERROR: Zrok startup failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to wait for services to be ready
function Wait-ForServices {
    Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
    
    # Wait for n8n
    $n8nReady = $false
    $attempts = 0
    while (-not $n8nReady -and $attempts -lt 30) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:5678/healthz" -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                $n8nReady = $true
                Write-Host "✓ n8n is ready" -ForegroundColor Green
            }
        }
        catch {
            Start-Sleep -Seconds 2
            $attempts++
        }
    }
    
    # Wait for zrok controller
    $zrokReady = $false
    $attempts = 0
    while (-not $zrokReady -and $attempts -lt 30) {
        try {
            $response = Invoke-WebRequest -Uri "$ZROK_API_URL/api/v1/version" -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                $zrokReady = $true
                Write-Host "✓ Zrok controller is ready" -ForegroundColor Green
            }
        }
        catch {
            Start-Sleep -Seconds 2
            $attempts++
        }
    }
    
    return ($n8nReady -and $zrokReady)
}

# Function to setup zrok environment (first time only)
function Initialize-ZrokEnvironment {
    Write-Host "Initializing Zrok environment..." -ForegroundColor Yellow
    
    try {
        # Check if environment already exists
        $envToken = docker-compose -f docker-compose.zrok.yml exec -T zrok-share zrok status 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Zrok environment already initialized" -ForegroundColor Green
            return $true
        }
        
        # Enable zrok environment
        Write-Host "Creating new zrok environment..." -ForegroundColor Cyan
        $result = docker-compose -f docker-compose.zrok.yml exec -T zrok-share zrok enable http://zrok-controller:18080
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Zrok environment enabled" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "ERROR: Failed to enable zrok environment" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "ERROR: Zrok environment setup failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to create reserved share
function New-ZrokReservedShare {
    Write-Host "Creating reserved share for stable URL..." -ForegroundColor Yellow
    
    try {
        # Create reserved share
        $shareResult = docker-compose -f docker-compose.zrok.yml exec -T zrok-share zrok reserve public --backend-mode proxy http://n8n:5678
        
        if ($LASTEXITCODE -eq 0) {
            # Extract the share token from result
            $shareToken = ($shareResult | Select-String -Pattern "zrok://.*").Matches.Value
            
            if ($shareToken) {
                Write-Host "✓ Reserved share created: $shareToken" -ForegroundColor Green
                
                # Update environment file with share token
                Update-ZrokEnvironment -ShareToken $shareToken
                
                return $shareToken
            }
        }
        
        Write-Host "ERROR: Failed to create reserved share" -ForegroundColor Red
        return $null
    }
    catch {
        Write-Host "ERROR: Reserved share creation failed: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Function to update environment files
function Update-ZrokEnvironment {
    param([string]$ShareToken)
    
    if ($ShareToken) {
        # Update zrok environment file
        if (Test-Path $ZROK_ENV_FILE) {
            $content = Get-Content $ZROK_ENV_FILE
            $content = $content -replace "ZROK_RESERVED_SHARE_TOKEN=.*", "ZROK_RESERVED_SHARE_TOKEN=$ShareToken"
            $content = $content -replace "ZROK_STABLE_URL=.*", "ZROK_STABLE_URL=http://localhost:8080"
            $content | Set-Content $ZROK_ENV_FILE
        }
        
        # Update n8n environment file
        if (Test-Path $N8N_ENV_FILE) {
            $content = Get-Content $N8N_ENV_FILE
            $content = $content -replace "WEBHOOK_URL=.*", "WEBHOOK_URL=http://localhost:8080/"
            $content | Set-Content $N8N_ENV_FILE
            Write-Host "✓ Updated webhook URL in n8n configuration" -ForegroundColor Green
        }
    }
}

# Function to show service status
function Show-ServiceStatus {
    Write-Host "`nService Status:" -ForegroundColor Cyan
    Write-Host "=" * 20
    
    # Check n8n
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5678/healthz" -UseBasicParsing -TimeoutSec 5
        Write-Host "✓ n8n: Running (http://localhost:5678)" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ n8n: Not responding" -ForegroundColor Red
    }
    
    # Check zrok controller
    try {
        $response = Invoke-WebRequest -Uri "$ZROK_API_URL/api/v1/version" -UseBasicParsing -TimeoutSec 5
        Write-Host "✓ Zrok Controller: Running ($ZROK_API_URL)" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Zrok Controller: Not responding" -ForegroundColor Red
    }
    
    # Check zrok public access
    try {
        $response = Invoke-WebRequest -Uri "$ZROK_PUBLIC_URL/health" -UseBasicParsing -TimeoutSec 5
        Write-Host "✓ Zrok Public Access: Running ($ZROK_PUBLIC_URL)" -ForegroundColor Green
    }
    catch {
        Write-Host "✗ Zrok Public Access: Not responding" -ForegroundColor Red
    }
}

# Main execution
try {
    # Check Docker
    if (-not (Test-DockerRunning)) {
        Write-Host "ERROR: Docker is not running. Please start Docker Desktop." -ForegroundColor Red
        exit 1
    }
    
    # Start n8n services
    if (-not $SkipDocker) {
        if (-not (Start-N8NDocker)) {
            exit 1
        }
    }
    
    # Start zrok services
    if (-not $SkipZrok) {
        if (-not (Start-ZrokServices)) {
            exit 1
        }
    }
    
    # Wait for services
    if (-not (Wait-ForServices)) {
        Write-Host "WARNING: Some services may not be fully ready" -ForegroundColor Yellow
    }
    
    # Initialize zrok environment (first time setup)
    if (-not $SetupOnly) {
        Initialize-ZrokEnvironment | Out-Null
        
        # Create reserved share for stable URL
        $shareToken = New-ZrokReservedShare
        if (-not $shareToken) {
            Write-Host "WARNING: Could not create reserved share. Manual setup may be required." -ForegroundColor Yellow
        }
    }
    
    # Show final status
    Show-ServiceStatus
    
    Write-Host "`nSUCCESS: All services started!" -ForegroundColor Green
    Write-Host "n8n Interface: http://localhost:5678" -ForegroundColor Cyan
    Write-Host "Stable Webhook URL: http://localhost:8080" -ForegroundColor Cyan
    Write-Host "Zrok Controller: $ZROK_API_URL" -ForegroundColor Cyan
    
    Write-Host "`nIMPORTANT: Your webhook URL is now STABLE and won't change between restarts!" -ForegroundColor Yellow
}
catch {
    Write-Host "ERROR: Startup script failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
