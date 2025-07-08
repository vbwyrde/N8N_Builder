#!/bin/bash

# n8n Restore Script
# This script restores n8n data from a backup

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

# Check if backup file is provided
if [ $# -eq 0 ]; then
    print_error "Usage: $0 <backup_file.tar.gz>"
    print_status "Available backups:"
    ls -la ../backups/n8n_backup_*.tar.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

BACKUP_FILE="$1"
BACKUP_DIR="../backups"
RESTORE_DIR="/tmp/n8n_restore_$$"

# Check if backup file exists
if [ ! -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    if [ ! -f "$BACKUP_FILE" ]; then
        print_error "Backup file not found: $BACKUP_FILE"
        exit 1
    else
        BACKUP_FILE_PATH="$BACKUP_FILE"
    fi
else
    BACKUP_FILE_PATH="$BACKUP_DIR/$BACKUP_FILE"
fi

print_status "Starting n8n restore process..."
print_status "Restoring from: $BACKUP_FILE_PATH"

# Warning about data loss
print_warning "⚠️  WARNING: This will replace all current n8n data!"
print_warning "Make sure to backup current data before proceeding."
echo ""
read -p "Do you want to continue? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_status "Restore cancelled by user"
    exit 0
fi

# Stop n8n containers
print_status "Stopping n8n containers..."
docker-compose down 2>/dev/null || true
docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
print_success "Containers stopped"

# Create temporary restore directory
mkdir -p "$RESTORE_DIR"

# Extract backup
print_status "Extracting backup..."
tar -xzf "$BACKUP_FILE_PATH" -C "$RESTORE_DIR"
BACKUP_NAME=$(basename "$BACKUP_FILE_PATH" .tar.gz)
EXTRACT_DIR="$RESTORE_DIR/$BACKUP_NAME"

if [ ! -d "$EXTRACT_DIR" ]; then
    print_error "Invalid backup file structure"
    rm -rf "$RESTORE_DIR"
    exit 1
fi

print_success "Backup extracted"

# Display backup information
if [ -f "$EXTRACT_DIR/backup_info.txt" ]; then
    print_status "Backup Information:"
    cat "$EXTRACT_DIR/backup_info.txt"
    echo ""
fi

# Restore Docker volumes
print_status "Restoring Docker volumes..."

# Restore n8n data volume
if [ -d "$EXTRACT_DIR/n8n_data" ]; then
    print_status "Restoring n8n_data volume..."
    docker volume rm n8n_data 2>/dev/null || true
    docker volume create n8n_data
    docker run --rm -v n8n_data:/destination -v "$EXTRACT_DIR/n8n_data:/backup" alpine cp -r /backup/. /destination
    print_success "n8n_data volume restored"
fi

# Restore n8n dev data volume
if [ -d "$EXTRACT_DIR/n8n_dev_data" ]; then
    print_status "Restoring n8n_dev_data volume..."
    docker volume rm n8n_dev_data 2>/dev/null || true
    docker volume create n8n_dev_data
    docker run --rm -v n8n_dev_data:/destination -v "$EXTRACT_DIR/n8n_dev_data:/backup" alpine cp -r /backup/. /destination
    print_success "n8n_dev_data volume restored"
fi

# Restore PostgreSQL data
if [ -d "$EXTRACT_DIR/postgres_data" ]; then
    print_status "Restoring PostgreSQL data..."
    docker volume rm n8n_postgres_data 2>/dev/null || true
    docker volume create n8n_postgres_data
    docker run --rm -v n8n_postgres_data:/destination -v "$EXTRACT_DIR/postgres_data:/backup" alpine cp -r /backup/. /destination
    print_success "PostgreSQL data restored"
fi

# Restore configuration files
print_status "Restoring configuration files..."
if [ -f "$EXTRACT_DIR/.env" ]; then
    cp "$EXTRACT_DIR/.env" ../ 2>/dev/null || true
    print_success ".env file restored"
fi

if [ -f "$EXTRACT_DIR/docker-compose.yml" ]; then
    cp "$EXTRACT_DIR/docker-compose.yml" ../ 2>/dev/null || true
    print_success "docker-compose.yml restored"
fi

if [ -f "$EXTRACT_DIR/docker-compose.dev.yml" ]; then
    cp "$EXTRACT_DIR/docker-compose.dev.yml" ../ 2>/dev/null || true
    print_success "docker-compose.dev.yml restored"
fi

if [ -d "$EXTRACT_DIR/config" ]; then
    cp -r "$EXTRACT_DIR/config" ../ 2>/dev/null || true
    print_success "Configuration directory restored"
fi

# Clean up temporary files
rm -rf "$RESTORE_DIR"

print_success "Restore completed successfully!"
echo ""
print_status "Next steps:"
echo "  1. Review the restored .env file"
echo "  2. Start n8n with: docker-compose up -d"
echo "  3. Or for development: docker-compose -f docker-compose.dev.yml up -d"
echo "  4. Access n8n at http://localhost:5678"
echo ""
print_warning "Note: You may need to recreate user accounts if authentication settings changed"
