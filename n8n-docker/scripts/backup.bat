@echo off
REM n8n Backup Script for Windows
REM This script creates a backup of n8n data including workflows, credentials, and settings

setlocal enabledelayedexpansion

REM Configuration
set BACKUP_DIR=..\backups
set TIMESTAMP=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_NAME=n8n_backup_%TIMESTAMP%
set BACKUP_PATH=%BACKUP_DIR%\%BACKUP_NAME%

REM Create backup directory if it doesn't exist
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo [INFO] Starting n8n backup process...
echo [INFO] Backup will be saved to: %BACKUP_PATH%

REM Check if n8n container is running
docker ps | findstr "n8n" >nul
if %errorlevel% equ 0 (
    set CONTAINER_RUNNING=true
    for /f "tokens=*" %%i in ('docker ps --format "table {{.Names}}" ^| findstr n8n') do set CONTAINER_NAME=%%i
    echo [INFO] n8n container '!CONTAINER_NAME!' is running
) else (
    set CONTAINER_RUNNING=false
    echo [WARNING] n8n container is not running
)

REM Create backup directory
mkdir "%BACKUP_PATH%"

REM Backup Docker volumes
echo [INFO] Backing up Docker volumes...

REM Backup n8n data volume
docker volume ls | findstr "n8n_data" >nul
if %errorlevel% equ 0 (
    echo [INFO] Backing up n8n_data volume...
    docker run --rm -v n8n_data:/source -v "%CD%\%BACKUP_PATH%:/backup" alpine cp -r /source/. /backup/n8n_data
    echo [SUCCESS] n8n_data volume backed up
)

REM Backup n8n dev data volume
docker volume ls | findstr "n8n_dev_data" >nul
if %errorlevel% equ 0 (
    echo [INFO] Backing up n8n_dev_data volume...
    docker run --rm -v n8n_dev_data:/source -v "%CD%\%BACKUP_PATH%:/backup" alpine cp -r /source/. /backup/n8n_dev_data
    echo [SUCCESS] n8n_dev_data volume backed up
)

REM Backup PostgreSQL data if it exists
docker volume ls | findstr "n8n_postgres_data" >nul
if %errorlevel% equ 0 (
    echo [INFO] Backing up PostgreSQL data...
    docker run --rm -v n8n_postgres_data:/source -v "%CD%\%BACKUP_PATH%:/backup" alpine cp -r /source/. /backup/postgres_data
    echo [SUCCESS] PostgreSQL data backed up
)

REM Backup configuration files
echo [INFO] Backing up configuration files...
if exist "..\config" xcopy "..\config" "%BACKUP_PATH%\config\" /E /I /Q >nul 2>&1
if exist "..\.env" copy "..\.env" "%BACKUP_PATH%\" >nul 2>&1
if exist "..\docker-compose.yml" copy "..\docker-compose.yml" "%BACKUP_PATH%\" >nul 2>&1
if exist "..\docker-compose.dev.yml" copy "..\docker-compose.dev.yml" "%BACKUP_PATH%\" >nul 2>&1
echo [SUCCESS] Configuration files backed up

REM Create backup metadata
echo n8n Backup Information > "%BACKUP_PATH%\backup_info.txt"
echo ===================== >> "%BACKUP_PATH%\backup_info.txt"
echo Backup Date: %date% %time% >> "%BACKUP_PATH%\backup_info.txt"
echo Backup Name: %BACKUP_NAME% >> "%BACKUP_PATH%\backup_info.txt"
echo Container Running: %CONTAINER_RUNNING% >> "%BACKUP_PATH%\backup_info.txt"
echo Container Name: %CONTAINER_NAME% >> "%BACKUP_PATH%\backup_info.txt"
docker --version >> "%BACKUP_PATH%\backup_info.txt"
echo. >> "%BACKUP_PATH%\backup_info.txt"
echo Volumes Backed Up: >> "%BACKUP_PATH%\backup_info.txt"
docker volume ls | findstr n8n >> "%BACKUP_PATH%\backup_info.txt"

REM Note: Windows doesn't have tar by default, so we'll use PowerShell to compress
echo [INFO] Compressing backup...
powershell -command "Compress-Archive -Path '%BACKUP_PATH%' -DestinationPath '%BACKUP_DIR%\%BACKUP_NAME%.zip' -Force"
rmdir /s /q "%BACKUP_PATH%"

echo [SUCCESS] Backup completed successfully!
echo [INFO] Backup file: %BACKUP_DIR%\%BACKUP_NAME%.zip

REM Clean up old backups (keep last 7 days)
echo [INFO] Cleaning up old backups (keeping last 7 days)...
forfiles /p "%BACKUP_DIR%" /m "n8n_backup_*.zip" /d -7 /c "cmd /c del @path" 2>nul

echo.
echo [SUCCESS] 🎉 Backup process completed!
echo.
echo [INFO] To restore from this backup, use: scripts\restore.bat %BACKUP_NAME%.zip
pause
