#!/bin/bash

# n8n Maintenance Script
# This script performs routine maintenance tasks for n8n Docker environment

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

show_help() {
    echo "n8n Docker Maintenance Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  -u, --update      Update n8n to latest version"
    echo "  -c, --cleanup     Clean up Docker system (images, containers, volumes)"
    echo "  -s, --status      Show n8n container status and health"
    echo "  -l, --logs        Show n8n container logs"
    echo "  -r, --restart     Restart n8n containers"
    echo "  -b, --backup      Create a backup"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --update       # Update n8n to latest version"
    echo "  $0 --status       # Check container status"
    echo "  $0 --cleanup      # Clean up Docker system"
}

update_n8n() {
    print_status "Updating n8n to latest version..."
    
    # Pull latest image
    docker pull n8nio/n8n:latest
    print_success "Latest n8n image pulled"
    
    # Stop current containers
    print_status "Stopping current containers..."
    docker-compose down 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    
    # Start containers with new image
    print_status "Starting containers with updated image..."
    if [ -f "../docker-compose.dev.yml" ]; then
        docker-compose -f docker-compose.dev.yml up -d
    else
        docker-compose up -d
    fi
    
    print_success "n8n updated successfully!"
    
    # Show version info
    sleep 5
    print_status "New version info:"
    docker exec $(docker ps --format "table {{.Names}}" | grep n8n | head -1) n8n --version 2>/dev/null || echo "Version info not available"
}

cleanup_docker() {
    print_status "Cleaning up Docker system..."
    
    print_warning "This will remove unused Docker images, containers, and networks"
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cleanup cancelled"
        return
    fi
    
    # Remove unused containers
    print_status "Removing unused containers..."
    docker container prune -f
    
    # Remove unused images
    print_status "Removing unused images..."
    docker image prune -f
    
    # Remove unused networks
    print_status "Removing unused networks..."
    docker network prune -f
    
    # Show disk space saved
    print_success "Docker cleanup completed!"
    print_status "Current Docker disk usage:"
    docker system df
}

show_status() {
    print_status "n8n Container Status:"
    echo ""
    
    # Show running containers
    if docker ps | grep -q "n8n"; then
        print_success "n8n containers are running:"
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep n8n
        echo ""
        
        # Show container health
        for container in $(docker ps --format "{{.Names}}" | grep n8n); do
            health=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null || echo "no healthcheck")
            if [ "$health" = "healthy" ]; then
                print_success "Container $container is healthy"
            elif [ "$health" = "unhealthy" ]; then
                print_error "Container $container is unhealthy"
            else
                print_status "Container $container: $health"
            fi
        done
        
        echo ""
        print_status "Access n8n at: http://localhost:5678"
    else
        print_warning "No n8n containers are currently running"
        print_status "To start n8n, run:"
        echo "  docker-compose -f docker-compose.dev.yml up -d  # For development"
        echo "  docker-compose up -d                            # For production"
    fi
    
    echo ""
    print_status "Docker volumes:"
    docker volume ls | grep n8n || echo "No n8n volumes found"
    
    echo ""
    print_status "Docker networks:"
    docker network ls | grep n8n || echo "No n8n networks found"
}

show_logs() {
    if docker ps | grep -q "n8n"; then
        container_name=$(docker ps --format "{{.Names}}" | grep n8n | head -1)
        print_status "Showing logs for container: $container_name"
        print_status "Press Ctrl+C to exit log view"
        echo ""
        docker logs -f "$container_name"
    else
        print_error "No n8n containers are running"
    fi
}

restart_containers() {
    print_status "Restarting n8n containers..."
    
    # Stop containers
    docker-compose down 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    
    # Start containers
    if [ -f "../docker-compose.dev.yml" ]; then
        docker-compose -f docker-compose.dev.yml up -d
    else
        docker-compose up -d
    fi
    
    print_success "Containers restarted successfully!"
}

create_backup() {
    print_status "Creating backup..."
    ./backup.sh
}

# Main script logic
case "${1:-}" in
    -u|--update)
        update_n8n
        ;;
    -c|--cleanup)
        cleanup_docker
        ;;
    -s|--status)
        show_status
        ;;
    -l|--logs)
        show_logs
        ;;
    -r|--restart)
        restart_containers
        ;;
    -b|--backup)
        create_backup
        ;;
    -h|--help)
        show_help
        ;;
    "")
        show_help
        ;;
    *)
        print_error "Unknown option: $1"
        show_help
        exit 1
        ;;
esac
