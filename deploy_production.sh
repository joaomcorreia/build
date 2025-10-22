#!/bin/bash

# Production Deployment Script for build.justcodeworks.eu
# Run this script on your server after cloning the repository

echo "🚀 Deploying Build Platform to build.justcodeworks.eu"

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
   echo "⚠️  This script should not be run as root. Run as a regular user with sudo access."
   exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your production values before continuing!"
    echo "   - Set SECRET_KEY to a secure random string"
    echo "   - Configure DATABASE_URL with secure credentials"
    echo "   - Add your AWS S3 credentials"
    echo "   - Add your OpenAI API key"
    echo "   - Configure email settings"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
mkdir -p logs
mkdir -p media
mkdir -p staticfiles

# Set proper permissions
sudo chown -R www-data:www-data logs media staticfiles

echo "🐳 Building Docker containers..."
docker-compose down
docker-compose up -d --build

echo "⏳ Waiting for database to be ready..."
sleep 30

echo "🗄️  Running database migrations..."
docker-compose exec -T web python manage.py migrate_schemas --shared
docker-compose exec -T web python manage.py migrate

echo "📦 Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo "🏢 Creating public tenant..."
docker-compose exec -T web python manage.py create_public_tenant --domain build.justcodeworks.eu --name "Build Platform"

echo "✅ Deployment completed!"
echo ""
echo "🌐 Your platform is now available at:"
echo "   Main site: https://build.justcodeworks.eu"
echo "   Admin: https://build.justcodeworks.eu/admin/"
echo ""
echo "📋 Next steps:"
echo "1. Create a superuser: docker-compose exec web python manage.py createsuperuser"
echo "2. Create your first tenant: docker-compose exec web python manage.py create_tenant"
echo "3. Set up SSL certificate with Let's Encrypt"
echo "4. Configure Nginx (see DEPLOYMENT.md for details)"
echo ""
echo "📊 Monitor logs with: docker-compose logs -f"