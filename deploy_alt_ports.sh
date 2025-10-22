#!/bin/bash

# Emergency deployment with different ports to avoid conflicts
echo "🚑 Emergency deployment with alternative ports"
echo "This uses different ports to avoid conflicts with existing services"

# Stop the hanging script if it's running
pkill -f "docker-compose exec"

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --remove-orphans

# Use the alternative docker-compose file
echo "🐳 Using alternative ports to avoid conflicts..."
docker-compose -f docker-compose.ports-fixed.yml down --volumes
docker-compose -f docker-compose.ports-fixed.yml up -d --build

echo "⏳ Waiting for services to start..."
sleep 20

# Check if containers are running
echo "📊 Container status:"
docker-compose -f docker-compose.ports-fixed.yml ps

# Wait for database with alternative method
echo "🗄️ Waiting for database..."
until docker-compose -f docker-compose.ports-fixed.yml exec -T db pg_isready -U postgres -d build_db 2>/dev/null; do
    echo "Waiting for PostgreSQL on alternative port..."
    sleep 3
done

echo "✅ Database is ready!"

# Run Django setup
echo "📦 Running Django migrations..."
docker-compose -f docker-compose.ports-fixed.yml exec web python manage.py migrate_schemas --shared
docker-compose -f docker-compose.ports-fixed.yml exec web python manage.py migrate

echo "📦 Collecting static files..."
docker-compose -f docker-compose.ports-fixed.yml exec web python manage.py collectstatic --noinput

echo "🏢 Creating public tenant..."
docker-compose -f docker-compose.ports-fixed.yml exec web python manage.py create_public_tenant --domain build.justcodeworks.eu --name "Build Platform"

# Update Nginx to use port 8001
echo "🌐 Updating Nginx for alternative port..."
if [ -f "nginx-http-only.conf" ]; then
    # Create modified Nginx config for port 8001
    sed 's/proxy_pass http:\/\/127\.0\.0\.1:8000/proxy_pass http:\/\/127.0.0.1:8001/' nginx-http-only.conf > nginx-alt-port.conf
    
    sudo mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled
    sudo cp nginx-alt-port.conf /etc/nginx/sites-available/build.justcodeworks.eu
    sudo ln -sf /etc/nginx/sites-available/build.justcodeworks.eu /etc/nginx/sites-enabled/build.justcodeworks.eu
    sudo rm -f /etc/nginx/sites-enabled/default
    
    if sudo nginx -t; then
        sudo systemctl reload nginx
        echo "✅ Nginx updated for port 8001"
    fi
fi

echo ""
echo "🎉 Alternative port deployment completed!"
echo ""
echo "🌐 Your site is now available at:"
echo "   http://build.justcodeworks.eu (through Nginx)"
echo "   http://your-server-ip:8001 (direct access)"
echo "   Admin: http://build.justcodeworks.eu/admin/"
echo ""
echo "📋 Port usage:"
echo "   PostgreSQL: 5433 (external) -> 5432 (internal)"
echo "   Redis: 6380 (external) -> 6379 (internal)" 
echo "   Django: 8001 (external) -> 8000 (internal)"
echo ""
echo "🔧 Manage with:"
echo "   docker-compose -f docker-compose.ports-fixed.yml logs -f"
echo "   docker-compose -f docker-compose.ports-fixed.yml exec web python manage.py createsuperuser"