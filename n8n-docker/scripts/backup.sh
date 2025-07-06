#!/bin/bash

# n8n Backup Script
# This script creates a backup of n8n data including workflows, credentials, and settings

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration
BACKUP_DIR="../backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="n8n_backup_${TIMESTAMP}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

print_status "Starting n8n backup process..."
print_status "Backup will be saved to: ${BACKUP_PATH}"

# Check if n8n container is running
if docker ps | grep -q "n8n"; then
    CONTAINER_RUNNING=true
    CONTAINER_NAME=$(docker ps --format "table {{.Names}}" | grep n8n | head -1)
    print_status "n8n container '${CONTAINER_NAME}' is running"
else
    CONTAINER_RUNNING=false
    print_warning "n8n container is not running"
fi

# Create backup directory
mkdir -p "$BACKUP_PATH"

# Backup Docker volumes
print_status "Backing up Docker volumes..."

# Backup n8n data volume
if docker volume ls | grep -q "n8n_data"; then
    print_status "Backing up n8n_data volume..."
    docker run --rm -v n8n_data:/source -v "$(pwd)/${BACKUP_PATH}:/backup" alpine cp -r /source/. /backup/n8n_data
    print_success "n8n_data volume backed up"
fi

# Backup n8n dev data volume
if docker volume ls | grep -q "n8n_dev_data"; then
    print_status "Backing up n8n_dev_data volume..."
    docker run --rm -v n8n_dev_data:/source -v "$(pwd)/${BACKUP_PATH}:/backup" alpine cp -r /source/. /backup/n8n_dev_data
    print_success "n8n_dev_data volume backed up"
fi

# Backup PostgreSQL data if it exists
if docker volume ls | grep -q "n8n_postgres_data"; then
    print_status "Backing up PostgreSQL data..."
    docker run --rm -v n8n_postgres_data:/source -v "$(pwd)/${BACKUP_PATH}:/backup" alpine cp -r /source/. /backup/postgres_data
    print_success "PostgreSQL data backed up"
fi

# Backup configuration files
print_status "Backing up configuration files..."
cp -r ../config "$BACKUP_PATH/" 2>/dev/null || true
cp ../.env "$BACKUP_PATH/" 2>/dev/null || true
cp ../docker-compose.yml "$BACKUP_PATH/" 2>/dev/null || true
cp ../docker-compose.dev.yml "$BACKUP_PATH/" 2>/dev/null || true
print_success "Configuration files backed up"

# Create backup metadata
cat > "${BACKUP_PATH}/backup_info.txt" << EOF
n8n Backup Information
=====================
Backup Date: $(date)
Backup Name: ${BACKUP_NAME}
Container Running: ${CONTAINER_RUNNING}
Container Name: ${CONTAINER_NAME:-N/A}
Docker Version: $(docker --version)
n8n Image: $(docker images n8nio/n8n:latest --format "table {{.Repository}}:{{.Tag}}\t{{.ID}}\t{{.CreatedAt}}" | tail -1)

Volumes Backed Up:
$(docker volume ls | grep n8n)

Files Included:
- n8n data volumes
- Configuration files (.env, docker-compose files)
- PostgreSQL data (if exists)
EOF

# Compress the backup
print_status "Compressing backup..."
cd "$BACKUP_DIR"
tar -czf "${BACKUP_NAME}.tar.gz" "$BACKUP_NAME"
rm -rf "$BACKUP_NAME"
cd - > /dev/null

# Calculate backup size
BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" | cut -f1)

print_success "Backup completed successfully!"
print_status "Backup file: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
print_status "Backup size: ${BACKUP_SIZE}"

# Clean up old backups (keep last 7 days)
print_status "Cleaning up old backups (keeping last 7 days)..."
find "$BACKUP_DIR" -name "n8n_backup_*.tar.gz" -type f -mtime +7 -delete 2>/dev/null || true
print_success "Old backups cleaned up"

echo ""
print_success "🎉 Backup process completed!"
echo ""
print_status "To restore from this backup, use: ./restore.sh ${BACKUP_NAME}.tar.gz"
