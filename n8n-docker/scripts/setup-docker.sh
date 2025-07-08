#!/bin/bash

# n8n Docker Setup Script
# This script sets up Docker networks and volumes for n8n

set -e

echo "🚀 Setting up n8n Docker environment..."

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

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! docker info &> /dev/null; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

print_success "Docker is installed and running"

# Create Docker network for n8n
print_status "Creating Docker network 'n8n-network'..."
if docker network ls | grep -q "n8n-network"; then
    print_warning "Network 'n8n-network' already exists"
else
    docker network create n8n-network
    print_success "Created Docker network 'n8n-network'"
fi

# Create Docker network for development
print_status "Creating Docker network 'n8n-dev-network'..."
if docker network ls | grep -q "n8n-dev-network"; then
    print_warning "Network 'n8n-dev-network' already exists"
else
    docker network create n8n-dev-network
    print_success "Created Docker network 'n8n-dev-network'"
fi

# Create Docker volumes
print_status "Creating Docker volumes..."

volumes=("n8n_data" "n8n_dev_data" "n8n_postgres_data")

for volume in "${volumes[@]}"; do
    if docker volume ls | grep -q "$volume"; then
        print_warning "Volume '$volume' already exists"
    else
        docker volume create "$volume"
        print_success "Created Docker volume '$volume'"
    fi
done

# Pull n8n Docker image
print_status "Pulling n8n Docker image..."
docker pull n8nio/n8n:latest
print_success "n8n Docker image pulled successfully"

# Create data directories with proper permissions
print_status "Setting up data directories..."
mkdir -p ../data/workflows
mkdir -p ../data/credentials
mkdir -p ../backups
chmod 755 ../data
chmod 755 ../backups

print_success "Data directories created"

echo ""
print_success "🎉 n8n Docker environment setup complete!"
echo ""
print_status "Next steps:"
echo "  1. Review and customize the .env file"
echo "  2. Run 'docker-compose -f docker-compose.dev.yml up -d' for development"
echo "  3. Run 'docker-compose up -d' for full setup with PostgreSQL"
echo "  4. Access n8n at http://localhost:5678"
echo ""
print_status "Useful commands:"
echo "  - View logs: docker-compose logs -f n8n"
echo "  - Stop services: docker-compose down"
echo "  - Backup data: ./scripts/backup.sh"
echo ""
