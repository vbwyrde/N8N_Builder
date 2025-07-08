# Setup-Zrok-Simple.ps1
# Simplified setup script for zrok Docker installation

param(
    [switch]$SkipImagePull
)

Write-Host "ZROK DOCKER SETUP" -ForegroundColor Green
Write-Host "=" * 30

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

# Pull Docker images
if (-not $SkipImagePull) {
    Write-Host "Pulling required Docker images..." -ForegroundColor Yellow
    
    $images = @(
        "openziti/ziti-controller:latest",
        "openziti/ziti-router:latest", 
        "openziti/zrok:latest"
    )
    
    foreach ($image in $images) {
        Write-Host "Pulling $image..." -ForegroundColor Cyan
        docker pull $image
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SUCCESS: Pulled $image" -ForegroundColor Green
        }
        else {
            Write-Host "ERROR: Failed to pull $image" -ForegroundColor Red
            exit 1
        }
    }
}

# Create Docker volumes
Write-Host "Creating Docker volumes..." -ForegroundColor Yellow

$volumes = @(
    "zrok_ziti_controller_data",
    "zrok_ziti_router_data",
    "zrok_controller_data",
    "zrok_frontend_data",
    "zrok_share_data"
)

foreach ($volume in $volumes) {
    $existing = docker volume ls --format "{{.Name}}" | Where-Object { $_ -eq $volume }
    
    if ($existing) {
        Write-Host "SUCCESS: Volume $volume already exists" -ForegroundColor Green
    }
    else {
        docker volume create $volume
        if ($LASTEXITCODE -eq 0) {
            Write-Host "SUCCESS: Created volume $volume" -ForegroundColor Green
        }
        else {
            Write-Host "ERROR: Failed to create volume $volume" -ForegroundColor Red
            exit 1
        }
    }
}

# Create Docker networks
Write-Host "Creating Docker networks..." -ForegroundColor Yellow

$existing = docker network ls --format "{{.Name}}" | Where-Object { $_ -eq "zrok-network" }

if ($existing) {
    Write-Host "SUCCESS: Network zrok-network already exists" -ForegroundColor Green
}
else {
    docker network create zrok-network
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Created network zrok-network" -ForegroundColor Green
    }
    else {
        Write-Host "ERROR: Failed to create network zrok-network" -ForegroundColor Red
        exit 1
    }
}

# Check environment file
Write-Host "Checking environment configuration..." -ForegroundColor Yellow

$envFile = "$PSScriptRoot\.env.zrok"
if (-not (Test-Path $envFile)) {
    Write-Host "ERROR: Environment file not found: $envFile" -ForegroundColor Red
    Write-Host "Please copy .env.zrok.template to .env.zrok and customize it" -ForegroundColor Yellow
    exit 1
}

$content = Get-Content $envFile -Raw
if ($content -match "change-this") {
    Write-Host "WARNING: Default tokens detected in .env.zrok" -ForegroundColor Yellow
    Write-Host "For security, please change the default tokens" -ForegroundColor Yellow
}

Write-Host "SUCCESS: Environment file ready" -ForegroundColor Green

# Final verification
Write-Host "Verifying setup..." -ForegroundColor Yellow

$allGood = $true

# Check images
$images = @("openziti/ziti-controller", "openziti/ziti-router", "openziti/zrok")
foreach ($image in $images) {
    $found = docker images --format "{{.Repository}}" | Where-Object { $_ -eq $image }
    if ($found) {
        Write-Host "SUCCESS: Image $image available" -ForegroundColor Green
    }
    else {
        Write-Host "ERROR: Image $image missing" -ForegroundColor Red
        $allGood = $false
    }
}

# Check key volumes
$volumes = @("zrok_controller_data", "zrok_share_data")
foreach ($volume in $volumes) {
    $found = docker volume ls --format "{{.Name}}" | Where-Object { $_ -eq $volume }
    if ($found) {
        Write-Host "SUCCESS: Volume $volume exists" -ForegroundColor Green
    }
    else {
        Write-Host "ERROR: Volume $volume missing" -ForegroundColor Red
        $allGood = $false
    }
}

if ($allGood) {
    Write-Host "`nSETUP COMPLETE!" -ForegroundColor Green
    Write-Host "=" * 20
    Write-Host "`nNext Steps:" -ForegroundColor Cyan
    Write-Host "1. Review and customize .env.zrok (change default tokens)" -ForegroundColor White
    Write-Host "2. Start services: .\Start-N8N-Zrok.ps1" -ForegroundColor White
    Write-Host "3. Access n8n: http://localhost:5678" -ForegroundColor White
    Write-Host "4. Use stable webhook URL: http://localhost:8080" -ForegroundColor White
}
else {
    Write-Host "`nSETUP FAILED!" -ForegroundColor Red
    Write-Host "Please check the errors above and try again." -ForegroundColor Yellow
    exit 1
}
