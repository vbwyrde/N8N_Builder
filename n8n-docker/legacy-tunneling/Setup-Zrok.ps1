# Setup-Zrok.ps1
# Initial setup script for zrok Docker installation
# Downloads images, creates volumes, and prepares environment

param(
    [switch]$Verbose,
    [switch]$SkipImagePull
)

$N8N_DOCKER_PATH = $PSScriptRoot
$ZROK_ENV_FILE = "$N8N_DOCKER_PATH\.env.zrok"

Write-Host "ZROK DOCKER SETUP" -ForegroundColor Green
Write-Host "=" * 30

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

# Function to pull required Docker images
function Get-ZrokImages {
    Write-Host "Pulling required Docker images..." -ForegroundColor Yellow

    $images = @(
        "openziti/ziti-controller:latest",
        "openziti/ziti-router:latest",
        "openziti/zrok:latest"
    )

    foreach ($image in $images) {
        Write-Host "Pulling $image..." -ForegroundColor Cyan
        try {
            docker pull $image
            if ($LASTEXITCODE -eq 0) {
                Write-Host "SUCCESS: Successfully pulled $image" -ForegroundColor Green
            }
            else {
                Write-Host "ERROR: Failed to pull $image" -ForegroundColor Red
                return $false
            }
        }
        catch {
            Write-Host "ERROR: Error pulling $image - $($_.Exception.Message)" -ForegroundColor Red
            return $false
        }
    }

    return $true
}

# Function to create Docker volumes
function New-ZrokVolumes {
    Write-Host "Creating Docker volumes..." -ForegroundColor Yellow
    
    $volumes = @(
        "zrok_ziti_controller_data",
        "zrok_ziti_router_data",
        "zrok_controller_data",
        "zrok_frontend_data",
        "zrok_share_data"
    )
    
    foreach ($volume in $volumes) {
        try {
            # Check if volume already exists
            $existing = docker volume ls --format "{{.Name}}" | Where-Object { $_ -eq $volume }
            
            if ($existing) {
                Write-Host "✓ Volume $volume already exists" -ForegroundColor Green
            }
            else {
                docker volume create $volume
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "SUCCESS: Created volume $volume" -ForegroundColor Green
                }
                else {
                    Write-Host "ERROR: Failed to create volume $volume" -ForegroundColor Red
                    return $false
                }
            }
        }
        catch {
            Write-Host "ERROR: Error creating volume $volume - $($_.Exception.Message)" -ForegroundColor Red
            return $false
        }
    }

    return $true
}

# Function to create Docker networks
function New-ZrokNetworks {
    Write-Host "Creating Docker networks..." -ForegroundColor Yellow
    
    try {
        # Check if zrok-network exists
        $existing = docker network ls --format "{{.Name}}" | Where-Object { $_ -eq "zrok-network" }
        
        if ($existing) {
            Write-Host "✓ Network zrok-network already exists" -ForegroundColor Green
        }
        else {
            docker network create zrok-network
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Created network zrok-network" -ForegroundColor Green
            }
            else {
                Write-Host "✗ Failed to create network zrok-network" -ForegroundColor Red
                return $false
            }
        }
        
        # Check if n8n-network exists (should exist from n8n setup)
        $n8nNetwork = docker network ls --format "{{.Name}}" | Where-Object { $_ -eq "n8n-network" }
        
        if ($n8nNetwork) {
            Write-Host "✓ Network n8n-network found" -ForegroundColor Green
        }
        else {
            Write-Host "⚠️  Network n8n-network not found - will be created when n8n starts" -ForegroundColor Yellow
        }
        
        return $true
    }
    catch {
        Write-Host "✗ Error creating networks: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to setup environment file
function Initialize-ZrokEnvironment {
    Write-Host "Setting up environment configuration..." -ForegroundColor Yellow
    
    if (-not (Test-Path $ZROK_ENV_FILE)) {
        Write-Host "✗ Environment file not found: $ZROK_ENV_FILE" -ForegroundColor Red
        Write-Host "Please copy .env.zrok.template to .env.zrok and customize it" -ForegroundColor Yellow
        return $false
    }
    
    # Check if default tokens are still in use
    $content = Get-Content $ZROK_ENV_FILE -Raw
    
    if ($content -match "zrok-admin-token-change-this" -or $content -match "admin123-change-this") {
        Write-Host "⚠️  WARNING: Default tokens detected in .env.zrok" -ForegroundColor Yellow
        Write-Host "For security, please change the default tokens:" -ForegroundColor Yellow
        Write-Host "  - ZROK_ADMIN_TOKEN" -ForegroundColor White
        Write-Host "  - ZROK_FRONTEND_TOKEN" -ForegroundColor White
        Write-Host "  - ZITI_PWD" -ForegroundColor White
        Write-Host ""
        
        $response = Read-Host "Continue with default tokens? (y/N)"
        if ($response -ne "y" -and $response -ne "Y") {
            Write-Host "Please edit $ZROK_ENV_FILE and run setup again" -ForegroundColor Yellow
            return $false
        }
    }
    
    Write-Host "✓ Environment configuration ready" -ForegroundColor Green
    return $true
}

# Function to verify setup
function Test-ZrokSetup {
    Write-Host "Verifying setup..." -ForegroundColor Yellow
    
    # Check images
    $images = @("openziti/ziti-controller", "openziti/ziti-router", "openziti/zrok")
    foreach ($image in $images) {
        $found = docker images --format "{{.Repository}}" | Where-Object { $_ -eq $image }
        if ($found) {
            Write-Host "✓ Image $image available" -ForegroundColor Green
        }
        else {
            Write-Host "✗ Image $image missing" -ForegroundColor Red
            return $false
        }
    }
    
    # Check volumes
    $volumes = @("zrok_ziti_controller_data", "zrok_controller_data", "zrok_share_data")
    foreach ($volume in $volumes) {
        $found = docker volume ls --format "{{.Name}}" | Where-Object { $_ -eq $volume }
        if ($found) {
            Write-Host "✓ Volume $volume exists" -ForegroundColor Green
        }
        else {
            Write-Host "✗ Volume $volume missing" -ForegroundColor Red
            return $false
        }
    }
    
    # Check networks
    $network = docker network ls --format "{{.Name}}" | Where-Object { $_ -eq "zrok-network" }
    if ($network) {
        Write-Host "✓ Network zrok-network exists" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Network zrok-network missing" -ForegroundColor Red
        return $false
    }
    
    # Check configuration files
    if (Test-Path "$N8N_DOCKER_PATH\docker-compose.zrok.yml") {
        Write-Host "✓ Docker Compose file exists" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Docker Compose file missing" -ForegroundColor Red
        return $false
    }
    
    if (Test-Path $ZROK_ENV_FILE) {
        Write-Host "✓ Environment file exists" -ForegroundColor Green
    }
    else {
        Write-Host "✗ Environment file missing" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# Function to show next steps
function Show-NextSteps {
    Write-Host "`n🎯 SETUP COMPLETE!" -ForegroundColor Green
    Write-Host "=" * 20
    
    Write-Host "`nNext Steps:" -ForegroundColor Cyan
    Write-Host "1. Review and customize .env.zrok (change default tokens)" -ForegroundColor White
    Write-Host "2. Start services: .\Start-N8N-Zrok.ps1" -ForegroundColor White
    Write-Host "3. Access n8n: http://localhost:5678" -ForegroundColor White
    Write-Host "4. Use stable webhook URL: http://localhost:8080" -ForegroundColor White
    
    Write-Host "`nConfiguration Files:" -ForegroundColor Cyan
    Write-Host "- Docker Compose: docker-compose.zrok.yml" -ForegroundColor White
    Write-Host "- Environment: .env.zrok" -ForegroundColor White
    Write-Host "- Controller Config: zrok-config/controller.yml" -ForegroundColor White
    
    Write-Host "`nManagement Scripts:" -ForegroundColor Cyan
    Write-Host "- Start: .\Start-N8N-Zrok.ps1" -ForegroundColor White
    Write-Host "- Stop: .\Stop-N8N-Zrok.ps1" -ForegroundColor White
    Write-Host "- Setup Guide: ZROK_SETUP_GUIDE.md" -ForegroundColor White
}

# Main execution
try {
    Set-Location $N8N_DOCKER_PATH
    
    # Check Docker
    if (-not (Test-DockerRunning)) {
        Write-Host "ERROR: Docker is not running. Please start Docker Desktop." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✓ Docker is running" -ForegroundColor Green
    
    # Pull Docker images
    if (-not $SkipImagePull) {
        if (-not (Get-ZrokImages)) {
            Write-Host "ERROR: Failed to pull required Docker images" -ForegroundColor Red
            exit 1
        }
    }
    else {
        Write-Host "Skipping image pull (-SkipImagePull specified)" -ForegroundColor Yellow
    }
    
    # Create volumes
    if (-not (New-ZrokVolumes)) {
        Write-Host "ERROR: Failed to create Docker volumes" -ForegroundColor Red
        exit 1
    }
    
    # Create networks
    if (-not (New-ZrokNetworks)) {
        Write-Host "ERROR: Failed to create Docker networks" -ForegroundColor Red
        exit 1
    }
    
    # Setup environment
    if (-not (Initialize-ZrokEnvironment)) {
        Write-Host "ERROR: Environment setup failed" -ForegroundColor Red
        exit 1
    }
    
    # Verify everything
    if (-not (Test-ZrokSetup)) {
        Write-Host "ERROR: Setup verification failed" -ForegroundColor Red
        exit 1
    }
    
    # Show next steps
    Show-NextSteps
    
}
catch {
    Write-Host "ERROR: Setup failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
