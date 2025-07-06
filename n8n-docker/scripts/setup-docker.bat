@echo off
REM n8n Docker Setup Script for Windows
REM This script sets up Docker networks and volumes for n8n

echo 🚀 Setting up n8n Docker environment...

REM Check if Docker is installed and running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo [SUCCESS] Docker is installed and running

REM Create Docker network for n8n
echo [INFO] Creating Docker network 'n8n-network'...
docker network ls | findstr "n8n-network" >nul
if %errorlevel% equ 0 (
    echo [WARNING] Network 'n8n-network' already exists
) else (
    docker network create n8n-network
    echo [SUCCESS] Created Docker network 'n8n-network'
)

REM Create Docker network for development
echo [INFO] Creating Docker network 'n8n-dev-network'...
docker network ls | findstr "n8n-dev-network" >nul
if %errorlevel% equ 0 (
    echo [WARNING] Network 'n8n-dev-network' already exists
) else (
    docker network create n8n-dev-network
    echo [SUCCESS] Created Docker network 'n8n-dev-network'
)

REM Create Docker volumes
echo [INFO] Creating Docker volumes...

docker volume ls | findstr "n8n_data" >nul
if %errorlevel% equ 0 (
    echo [WARNING] Volume 'n8n_data' already exists
) else (
    docker volume create n8n_data
    echo [SUCCESS] Created Docker volume 'n8n_data'
)

docker volume ls | findstr "n8n_dev_data" >nul
if %errorlevel% equ 0 (
    echo [WARNING] Volume 'n8n_dev_data' already exists
) else (
    docker volume create n8n_dev_data
    echo [SUCCESS] Created Docker volume 'n8n_dev_data'
)

docker volume ls | findstr "n8n_postgres_data" >nul
if %errorlevel% equ 0 (
    echo [WARNING] Volume 'n8n_postgres_data' already exists
) else (
    docker volume create n8n_postgres_data
    echo [SUCCESS] Created Docker volume 'n8n_postgres_data'
)

REM Pull n8n Docker image
echo [INFO] Pulling n8n Docker image...
docker pull n8nio/n8n:latest
echo [SUCCESS] n8n Docker image pulled successfully

REM Create data directories
echo [INFO] Setting up data directories...
if not exist "..\data" mkdir "..\data"
if not exist "..\data\workflows" mkdir "..\data\workflows"
if not exist "..\data\credentials" mkdir "..\data\credentials"
if not exist "..\backups" mkdir "..\backups"
echo [SUCCESS] Data directories created

echo.
echo [SUCCESS] 🎉 n8n Docker environment setup complete!
echo.
echo [INFO] Next steps:
echo   1. Review and customize the .env file
echo   2. Run 'docker-compose -f docker-compose.dev.yml up -d' for development
echo   3. Run 'docker-compose up -d' for full setup with PostgreSQL
echo   4. Access n8n at http://localhost:5678
echo.
echo [INFO] Useful commands:
echo   - View logs: docker-compose logs -f n8n
echo   - Stop services: docker-compose down
echo   - Backup data: scripts\backup.bat
echo.
pause
