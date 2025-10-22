#!/bin/bash

# Deployment Diagnostic Script
# Run this to diagnose current deployment issues

echo "🔍 Build Platform Deployment Diagnostics"
echo "======================================="

echo ""
echo "📦 Docker System Info:"
docker --version
docker-compose --version

echo ""
echo "🐳 Container Status:"
docker-compose ps

echo ""
echo "📊 Docker Resources:"
docker system df

echo ""
echo "🔄 Recent Container Logs:"
echo "--- Web Container (last 20 lines) ---"
docker-compose logs --tail=20 web 2>/dev/null || echo "Web container not found or not running"

echo ""
echo "--- Database Container (last 10 lines) ---"
docker-compose logs --tail=10 db 2>/dev/null || echo "Database container not found or not running"

echo ""
echo "--- Celery Container (last 10 lines) ---"
docker-compose logs --tail=10 celery 2>/dev/null || echo "Celery container not found or not running"

echo ""
echo "🌐 Network Tests:"
echo "Testing Django server on port 8000..."
if curl -s --connect-timeout 5 http://localhost:8000 >/dev/null 2>&1; then
    echo "✅ Django server responds on localhost:8000"
    
    # Test with domain header
    RESPONSE=$(curl -s -w "%{http_code}" -H "Host: build.justcodeworks.eu" http://localhost:8000 2>/dev/null | tail -c 3)
    echo "Domain header test response: $RESPONSE"
else
    echo "❌ Django server not responding on localhost:8000"
fi

echo ""
echo "Testing Nginx on port 80..."
if curl -s --connect-timeout 5 http://localhost >/dev/null 2>&1; then
    echo "✅ Nginx responds on port 80"
else
    echo "❌ Nginx not responding on port 80"
fi

echo ""
echo "🗂️ File System Checks:"
echo "Static files directory:"
ls -la staticfiles/ 2>/dev/null || echo "staticfiles directory not found"

echo ""
echo "Media files directory:"
ls -la media/ 2>/dev/null || echo "media directory not found"

echo ""
echo "Environment file:"
if [ -f ".env" ]; then
    echo "✅ .env file exists"
    echo "Key settings (without sensitive values):"
    grep -E "^(DEBUG|ALLOWED_HOSTS|MAIN_DOMAIN)" .env 2>/dev/null || echo "Could not read .env settings"
else
    echo "❌ .env file missing"
fi

echo ""
echo "🔧 Nginx Configuration:"
if [ -f "/etc/nginx/sites-available/build.justcodeworks.eu" ]; then
    echo "✅ Nginx site configuration exists"
    if sudo nginx -t >/dev/null 2>&1; then
        echo "✅ Nginx configuration is valid"
    else
        echo "❌ Nginx configuration has errors:"
        sudo nginx -t 2>&1
    fi
else
    echo "❌ Nginx site configuration missing"
fi

echo ""
echo "🎯 Quick Fixes:"
echo "1. If containers aren't running: ./deploy_fixed.sh"
echo "2. If static files missing: docker-compose exec web python manage.py collectstatic --noinput"
echo "3. If database issues: docker-compose exec web python manage.py migrate"
echo "4. If Nginx issues: sudo systemctl status nginx"

echo ""
echo "🆘 Emergency Commands:"
echo "Complete restart: docker-compose down && docker-compose up -d --build"
echo "View all logs: docker-compose logs -f"
echo "Clean slate: docker-compose down --volumes && docker system prune -f"

echo ""
echo "✅ Diagnostic complete!"