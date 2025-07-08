# Setup script for n8n + Stable URL Proxy
# This script helps configure the environment for first-time use

Write-Host "n8n + Stable URL Proxy Setup Script" -ForegroundColor Green
Write-Host "=" * 30

# Check if .env exists
$envFile = ".env"
$envTemplate = ".env.template"

if (-not (Test-Path $envFile)) {
    if (Test-Path $envTemplate) {
        Write-Host "Creating .env file from template..." -ForegroundColor Yellow
        Copy-Item $envTemplate $envFile
        Write-Host "SUCCESS: .env file created" -ForegroundColor Green
        Write-Host "IMPORTANT: Please edit .env and update the following:" -ForegroundColor Red
        Write-Host "  - N8N_ENCRYPTION_KEY (generate a secure random key)" -ForegroundColor Yellow
        Write-Host "  - N8N_BASIC_AUTH_PASSWORD (change from default)" -ForegroundColor Yellow
        Write-Host "  - Any database passwords if using PostgreSQL" -ForegroundColor Yellow
    } else {
        Write-Host "ERROR: .env.template not found" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "INFO: .env file already exists" -ForegroundColor Cyan
}

# Check if config.ps1 exists
$configFile = "config.ps1"
$configTemplate = "config.ps1.template"

if (-not (Test-Path $configFile)) {
    if (Test-Path $configTemplate) {
        Write-Host "Creating config.ps1 from template..." -ForegroundColor Yellow
        Copy-Item $configTemplate $configFile
        Write-Host "SUCCESS: config.ps1 file created" -ForegroundColor Green
        Write-Host "IMPORTANT: Please edit config.ps1 and update:" -ForegroundColor Red
        Write-Host "  - NGROK_PATH (path to your ngrok.exe)" -ForegroundColor Yellow
    } else {
        Write-Host "ERROR: config.ps1.template not found" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "INFO: config.ps1 file already exists" -ForegroundColor Cyan
}

# Check if nGrok is installed and accessible
Write-Host ""
Write-Host "Checking nGrok installation..." -ForegroundColor Yellow

# Try to load config to get nGrok path
if (Test-Path $configFile) {
    . ".\config.ps1"
    $ngrokPath = $script:Config.NgrokPath
    
    if (Test-Path $ngrokPath) {
        Write-Host "SUCCESS: nGrok found at $ngrokPath" -ForegroundColor Green
        
        # Test nGrok version
        try {
            $version = & $ngrokPath version 2>$null
            Write-Host "nGrok version: $($version[0])" -ForegroundColor Cyan
        } catch {
            Write-Host "WARNING: Could not get nGrok version" -ForegroundColor Yellow
        }
    } else {
        Write-Host "ERROR: nGrok not found at $ngrokPath" -ForegroundColor Red
        Write-Host "Please update the NGROK_PATH in config.ps1" -ForegroundColor Yellow
    }
} else {
    Write-Host "WARNING: config.ps1 not found, skipping nGrok check" -ForegroundColor Yellow
}

# Check Docker
Write-Host ""
Write-Host "Checking Docker installation..." -ForegroundColor Yellow

try {
    $dockerVersion = docker version --format "{{.Client.Version}}" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Docker found, version $dockerVersion" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Docker not found or not running" -ForegroundColor Red
        Write-Host "Please install Docker Desktop and ensure it's running" -ForegroundColor Yellow
    }
} catch {
    Write-Host "ERROR: Docker not found" -ForegroundColor Red
    Write-Host "Please install Docker Desktop" -ForegroundColor Yellow
}

# Check Docker Compose
try {
    $composeVersion = docker-compose version --short 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Docker Compose found, version $composeVersion" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Docker Compose not found (may be integrated with Docker)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "WARNING: Docker Compose check failed" -ForegroundColor Yellow
}

# Final instructions
Write-Host ""
Write-Host "Setup Summary:" -ForegroundColor Green
Write-Host "-" * 20

if (Test-Path $envFile) {
    Write-Host "✓ .env file ready" -ForegroundColor Green
} else {
    Write-Host "✗ .env file missing" -ForegroundColor Red
}

if (Test-Path $configFile) {
    Write-Host "✓ config.ps1 file ready" -ForegroundColor Green
} else {
    Write-Host "✗ config.ps1 file missing" -ForegroundColor Red
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file and change default passwords" -ForegroundColor White
Write-Host "2. Edit config.ps1 and set correct nGrok path" -ForegroundColor White
Write-Host "3. Run: start-n8n.bat or Start-N8N-NgRok.ps1" -ForegroundColor White
Write-Host ""
Write-Host "For help, see: README.md or AUTOMATION-README.md" -ForegroundColor Yellow
