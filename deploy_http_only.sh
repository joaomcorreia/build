#!/bin/bash

# Emergency HTTP-only Deployment Script
# Use this when Let's Encrypt rate limits are hit

echo "🚑 Emergency HTTP-only deployment for build.justcodeworks.eu"
echo "⚠️  This will deploy without SSL - add HTTPS after rate limit resets"

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Please run this script from the Django project root directory"
    exit 1
fi

# Update .env for HTTP-only deployment
if [ -f ".env" ]; then
    echo "📝 Updating .env for HTTP deployment..."
    
    # Backup current .env
    cp .env .env.backup
    
    # Update security settings for HTTP
    sed -i 's/DEBUG=False/DEBUG=False/' .env
    sed -i 's/SECURE_SSL_REDIRECT=True/SECURE_SSL_REDIRECT=False/' .env
    sed -i 's/SESSION_COOKIE_SECURE=True/SESSION_COOKIE_SECURE=False/' .env
    sed -i 's/CSRF_COOKIE_SECURE=True/CSRF_COOKIE_SECURE=False/' .env
    
    echo "✅ Environment configured for HTTP deployment"
else
    echo "❌ .env file not found. Please create it from .env.example first"
    exit 1
fi

# Deploy the application
echo "🐳 Starting Docker deployment..."
docker-compose down
docker-compose up -d --build

echo "⏳ Waiting for services to start..."
sleep 30

echo "🗄️ Running migrations..."
docker-compose exec -T web python manage.py migrate_schemas --shared
docker-compose exec -T web python manage.py migrate

echo "📦 Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo "🏢 Creating public tenant..."
docker-compose exec -T web python manage.py create_public_tenant --domain build.justcodeworks.eu --name "Build Platform" || echo "Public tenant might already exist"

# Set up temporary Nginx configuration
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
sudo cp nginx-http-only.conf /etc/nginx/sites-available/build.justcodeworks.eu
sudo ln -sf /etc/nginx/sites-available/build.justcodeworks.eu /etc/nginx/sites-enabled/build.justcodeworks.eu

# Remove default Nginx site if it exists
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid"
    sudo systemctl reload nginx
    echo "🔄 Nginx reloaded"
else
    echo "❌ Nginx configuration error. Please check manually."
fi

echo ""
echo "✅ HTTP deployment completed!"
echo ""
echo "🌐 Your site is now available at:"
echo "   http://build.justcodeworks.eu"
echo "   Admin: http://build.justcodeworks.eu/admin/"
echo ""
echo "⚠️  IMPORTANT: This is HTTP-only deployment!"
echo ""
echo "🔒 To add SSL after rate limit resets (2025-10-22 12:59:23 UTC):"
echo "   sudo certbot --nginx -d build.justcodeworks.eu -d *.build.justcodeworks.eu"
echo ""
echo "📋 Next steps:"
echo "1. Test the site: curl -H 'Host: build.justcodeworks.eu' http://your-server-ip"
echo "2. Create superuser: docker-compose exec web python manage.py createsuperuser"
echo "3. Create first tenant: docker-compose exec web python manage.py create_tenant"
echo ""
echo "📊 Monitor with: docker-compose logs -f web"