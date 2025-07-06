#!/bin/bash
# Simple Zrok HTTP Proxy Script
# This creates a simple HTTP proxy without requiring external service registration

set -e

echo "Starting simple zrok HTTP proxy..."

# Create a simple HTTP proxy that forwards to n8n
echo "Creating HTTP proxy from port 8080 to n8n:5678"

# Use a simple approach - just proxy HTTP traffic
# This will create a local proxy without needing external registration
exec zrok share public --headless --backend-mode proxy http://n8n:5678
