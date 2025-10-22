#!/bin/bash

# Build and Deploy Script for Build Platform
# Usage: ./deploy.sh [environment]
# Environments: dev, staging, production

set -e

ENVIRONMENT=${1:-dev}
PROJECT_NAME="build-platform"

echo "🚀 Starting deployment for environment: $ENVIRONMENT"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Environment-specific configurations
case $ENVIRONMENT in
    "dev")
        COMPOSE_FILE="docker-compose.dev.yml"
        print_status "Using development configuration"
        ;;
    "staging")
        COMPOSE_FILE="docker-compose.yml"
        export DEBUG=False
        print_status "Using staging configuration"
        ;;
    "production")
        COMPOSE_FILE="docker-compose.yml"
        export DEBUG=False
        print_status "Using production configuration"
        ;;
    *)
        print_error "Unknown environment: $ENVIRONMENT"
        print_warning "Available environments: dev, staging, production"
        exit 1
        ;;
esac

# Build and start services
print_status "Building Docker images..."
docker-compose -f $COMPOSE_FILE build

print_status "Starting services..."
docker-compose -f $COMPOSE_FILE up -d

# Wait for database to be ready
print_status "Waiting for database to be ready..."
sleep 10

# Run migrations
print_status "Running database migrations..."
docker-compose -f $COMPOSE_FILE exec -T web python manage.py migrate_schemas --shared

# Create public tenant if it doesn't exist
print_status "Setting up public tenant..."
docker-compose -f $COMPOSE_FILE exec -T web python manage.py create_public_tenant --domain=build.justcodeworks.eu || true

# Collect static files (for production)
if [ "$ENVIRONMENT" != "dev" ]; then
    print_status "Collecting static files..."
    docker-compose -f $COMPOSE_FILE exec -T web python manage.py collectstatic --noinput
fi

# Show running containers
print_status "Deployment complete! Running containers:"
docker-compose -f $COMPOSE_FILE ps

# Show logs
print_warning "Showing recent logs (last 50 lines):"
docker-compose -f $COMPOSE_FILE logs --tail=50

print_status "Access the application at:"
if [ "$ENVIRONMENT" = "dev" ]; then
    echo "  🌐 http://localhost:8000"
else
    echo "  🌐 https://build.justcodeworks.eu"
fi

print_warning "To view logs: docker-compose -f $COMPOSE_FILE logs -f"
print_warning "To stop services: docker-compose -f $COMPOSE_FILE down"

# Create superuser reminder
print_warning ""
print_warning "Don't forget to create a superuser:"
print_warning "docker-compose -f $COMPOSE_FILE exec web python manage.py createsuperuser"