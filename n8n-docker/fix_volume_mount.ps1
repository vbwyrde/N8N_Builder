# Fix N8N Volume Mount for DNS Reports
# This script properly restarts N8N with the shared volume mount

Write-Host "🔧 Fixing N8N Volume Mount for DNS Reports" -ForegroundColor Cyan
Write-Host "=" * 50

# We're already in the n8n-docker directory
Write-Host "📂 Working in: $(Get-Location)" -ForegroundColor Green

# Show current container status
Write-Host "`n📊 Current Container Status:" -ForegroundColor Yellow
docker-compose ps

# Stop all containers completely
Write-Host "`n🛑 Stopping all N8N containers..." -ForegroundColor Yellow
docker-compose down --remove-orphans
Start-Sleep -Seconds 5

# Remove any existing containers (force cleanup)
Write-Host "`n🧹 Cleaning up containers..." -ForegroundColor Yellow
docker-compose rm -f

# Verify the volume mount is in docker-compose.yml
Write-Host "`n🔍 Checking docker-compose.yml for volume mount..." -ForegroundColor Yellow
$composeContent = Get-Content "docker-compose.yml" -Raw
if ($composeContent -match "../data:/home/node/shared") {
    Write-Host "✅ Volume mount found in docker-compose.yml" -ForegroundColor Green
} else {
    Write-Host "❌ Volume mount NOT found in docker-compose.yml" -ForegroundColor Red
    Write-Host "Please ensure this line is in the volumes section:" -ForegroundColor Yellow
    Write-Host "      - ../data:/home/node/shared" -ForegroundColor White
    exit 1
}

# Create the data directory if it doesn't exist
$dataDir = "../data"
if (-not (Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir -Force
    Write-Host "✅ Created data directory: $dataDir" -ForegroundColor Green
} else {
    Write-Host "✅ Data directory exists: $dataDir" -ForegroundColor Green
}

# Start containers with fresh configuration
Write-Host "`n🚀 Starting N8N with volume mount..." -ForegroundColor Yellow
docker-compose up -d

# Wait for containers to start
Write-Host "`n⏳ Waiting for containers to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Check final status
Write-Host "`n📊 Final Container Status:" -ForegroundColor Cyan
docker-compose ps

# Test the volume mount
Write-Host "`n🧪 Testing volume mount..." -ForegroundColor Yellow
try {
    # Create a test file from the container
    docker-compose exec n8n touch /home/node/shared/test_volume_mount.txt
    
    # Check if it appears on the host
    if (Test-Path "../data/test_volume_mount.txt") {
        Write-Host "✅ Volume mount working! Test file created successfully." -ForegroundColor Green
        Remove-Item "../data/test_volume_mount.txt" -Force
        Write-Host "✅ Test file cleaned up." -ForegroundColor Green
    } else {
        Write-Host "❌ Volume mount not working - test file not found on host" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠️  Could not test volume mount: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Check N8N health
Write-Host "`n🏥 Checking N8N health..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5678/healthz" -TimeoutSec 10 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ N8N is healthy and responding" -ForegroundColor Green
    } else {
        Write-Host "⚠️  N8N responded but may not be fully ready" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  N8N health check failed - may still be starting" -ForegroundColor Yellow
}

Write-Host "`n🎉 N8N Volume Mount Fix Complete!" -ForegroundColor Green
Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Wait 30 seconds for N8N to fully start" -ForegroundColor White
Write-Host "2. Open N8N: http://localhost:5678" -ForegroundColor White
Write-Host "3. Import the DNS Security workflow" -ForegroundColor White
Write-Host "4. Run the workflow to test file creation" -ForegroundColor White
Write-Host "5. Check ../data/ directory for generated files" -ForegroundColor White

Write-Host "`n🔗 Volume Mount Details:" -ForegroundColor Cyan
Write-Host "   Container: /home/node/shared" -ForegroundColor White
Write-Host "   Host: ../data" -ForegroundColor White
Write-Host "   Files saved by N8N will appear in ../data/" -ForegroundColor White
