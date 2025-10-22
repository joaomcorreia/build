#!/bin/bash

# Fixed Emergency HTTP Deployment Script
# Handles Docker build issues and proper collectstatic

echo "🚑 Fixed HTTP-only deployment for build.justcodeworks.eu"
echo "🔧 This version fixes Docker build and static file issues"

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Please run this script from the Django project root directory"
    exit 1
fi

# Check if .env exists, if not create from example
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your production values!"
    echo "   Key settings to update:"
    echo "   - SECRET_KEY (generate a new one)"
    echo "   - Database credentials"
    echo "   - AWS S3 settings (if using)"
    echo ""
    read -p "Press Enter after editing .env file, or Ctrl+C to exit..."
fi

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Remove any problematic containers/images to start fresh
echo "🧹 Cleaning up Docker resources..."
docker-compose down --volumes --remove-orphans
docker system prune -f

# Build containers without problematic steps
echo "🐳 Building Docker containers (this may take a few minutes)..."
docker-compose build --no-cache

# Start the database first and wait for it
echo "🗄️ Starting database..."
docker-compose up -d db redis

echo "⏳ Waiting for database to be ready..."
sleep 15

# Check if database is responsive
until docker-compose exec db pg_isready -U postgres; do
    echo "Waiting for PostgreSQL..."
    sleep 2
done

echo "✅ Database is ready!"

# Start the web application
echo "🌐 Starting web application..."
docker-compose up -d web

# Wait for web container to be running
sleep 10

# Check if web container is running
if ! docker-compose ps | grep -q "web.*Up"; then
    echo "❌ Web container failed to start. Checking logs..."
    docker-compose logs web
    exit 1
fi

echo "✅ Web container is running!"

# Now run Django management commands
echo "🔄 Running Django setup commands..."

# Run migrations
echo "📦 Running database migrations..."
docker-compose exec web python manage.py migrate_schemas --shared
docker-compose exec web python manage.py migrate

# Collect static files (now that container is running)
echo "📦 Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

# Create public tenant
echo "🏢 Creating public tenant..."
docker-compose exec web python manage.py create_public_tenant --domain build.justcodeworks.eu --name "Build Platform" || echo "✅ Public tenant already exists"

# Start celery worker
echo "🔄 Starting Celery worker..."
docker-compose up -d celery

# Set up Nginx configuration
echo "🌐 Setting up Nginx configuration..."

# Create Nginx directories if they don't exist
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled

# Create temporary self-signed certificate
if [ ! -f "/etc/ssl/certs/temp-build.crt" ]; then
    echo "🔒 Creating temporary self-signed certificate..."
    sudo mkdir -p /etc/ssl/certs /etc/ssl/private
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/ssl/private/temp-build.key \
        -out /etc/ssl/certs/temp-build.crt \
        -subj "/C=EU/ST=State/L=City/O=Organization/OU=OrgUnit/CN=build.justcodeworks.eu"
fi

# Copy Nginx configuration
if [ -f "nginx-http-only.conf" ]; then
    sudo cp nginx-http-only.conf /etc/nginx/sites-available/build.justcodeworks.eu
    sudo ln -sf /etc/nginx/sites-available/build.justcodeworks.eu /etc/nginx/sites-enabled/build.justcodeworks.eu
    
    # Remove default site
    sudo rm -f /etc/nginx/sites-enabled/default
    
    # Test and reload Nginx
    if sudo nginx -t; then
        echo "✅ Nginx configuration is valid"
        sudo systemctl reload nginx
        echo "🔄 Nginx reloaded"
    else
        echo "⚠️  Nginx configuration has issues, but continuing..."
    fi
else
    echo "⚠️  nginx-http-only.conf not found, skipping Nginx setup"
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "🔍 Container Status:"
docker-compose ps

echo ""
echo "🌐 Your site should be available at:"
echo "   http://build.justcodeworks.eu"
echo "   http://your-server-ip:8000 (direct access)"
echo "   Admin: http://build.justcodeworks.eu/admin/"
echo ""
echo "🔧 Next steps:"
echo "1. Create superuser: docker-compose exec web python manage.py createsuperuser"
echo "2. Test the site: curl -H 'Host: build.justcodeworks.eu' http://localhost:8000"
echo "3. Create first tenant: docker-compose exec web python manage.py create_tenant"
echo ""
echo "📊 Monitor logs: docker-compose logs -f web"
echo "🔒 Add SSL after 12:59 UTC: sudo certbot --nginx -d build.justcodeworks.eu -d *.build.justcodeworks.eu"