#!/bin/bash

# Quick deployment status check for build.justcodeworks.eu

echo "🔍 Checking Build Platform deployment status..."
echo ""

# Check if Docker containers are running
echo "📦 Docker Container Status:"
docker-compose ps

echo ""
echo "🌐 Network Connectivity Tests:"

# Test internal connection
echo "Testing internal Django server..."
curl -s -o /dev/null -w "Django server (localhost:8000): %{http_code}\n" http://localhost:8000 || echo "Django server: Not responding"

# Test with domain header
echo "Testing with domain header..."
curl -s -o /dev/null -w "Domain header test: %{http_code}\n" -H "Host: build.justcodeworks.eu" http://localhost:8000 || echo "Domain header test: Failed"

# Test Nginx (if configured)
echo "Testing Nginx (port 80)..."
curl -s -o /dev/null -w "Nginx (port 80): %{http_code}\n" http://localhost || echo "Nginx: Not responding"

echo ""
echo "📊 Service Logs (last 10 lines):"
echo "--- Django Web Server ---"
docker-compose logs --tail=10 web

echo ""
echo "--- Database ---"
docker-compose logs --tail=5 db

echo ""
echo "📋 Quick Commands:"
echo "View full logs: docker-compose logs -f"
echo "Restart Django: docker-compose restart web"
echo "Access Django shell: docker-compose exec web python manage.py shell"
echo "Create superuser: docker-compose exec web python manage.py createsuperuser"
echo ""

# Check if the public tenant exists
echo "🏢 Tenant Status:"
docker-compose exec -T web python manage.py shell -c "
from tenants.models import Client, Domain
try:
    public = Client.objects.get(schema_name='public')
    domains = Domain.objects.filter(tenant=public)
    print(f'Public tenant: {public.name}')
    for domain in domains:
        print(f'Domain: {domain.domain}')
except:
    print('No public tenant found - run: docker-compose exec web python manage.py create_public_tenant')
" 2>/dev/null || echo "Could not check tenant status"

echo ""
echo "✅ Status check complete!"