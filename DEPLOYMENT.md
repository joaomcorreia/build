# Deployment Guide for build.justcodeworks.eu

## Prerequisites
- Server with Docker and Docker Compose installed
- Domain `build.justcodeworks.eu` pointing to your server IP
- SSL certificate (Let's Encrypt recommended)

## Step 1: Clone Repository
```bash
cd /var/www
git clone https://github.com/joaomcorreia/build.git
cd build
```

## Step 2: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your production values:
```env
DEBUG=False
SECRET_KEY=your-actual-secret-key-here
ALLOWED_HOSTS=build.justcodeworks.eu,.build.justcodeworks.eu
MAIN_DOMAIN=build.justcodeworks.eu

# Database
DATABASE_URL=postgresql://build_user:secure_password@db:5432/build_db

# Redis
REDIS_URL=redis://redis:6379/0

# AWS S3 (for media storage)
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_STORAGE_BUCKET_NAME=build-justcodeworks-media
AWS_S3_REGION_NAME=eu-central-1

# OpenAI
OPENAI_API_KEY=your_openai_key

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@justcodeworks.eu
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=noreply@justcodeworks.eu
```

## Step 3: Update Database Credentials
Edit `docker-compose.yml` to use secure database credentials:
```yaml
environment:
  POSTGRES_DB: build_db
  POSTGRES_USER: build_user
  POSTGRES_PASSWORD: your_secure_db_password
```

## Step 4: Set Up SSL with Nginx
Create `/etc/nginx/sites-available/build.justcodeworks.eu`:
```nginx
server {
    listen 80;
    server_name build.justcodeworks.eu *.build.justcodeworks.eu;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name build.justcodeworks.eu *.build.justcodeworks.eu;

    ssl_certificate /path/to/your/ssl/cert.pem;
    ssl_certificate_key /path/to/your/ssl/private.key;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/build/staticfiles/;
    }

    location /media/ {
        alias /var/www/build/media/;
    }
}
```

Enable the site:
```bash
ln -s /etc/nginx/sites-available/build.justcodeworks.eu /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

## Step 5: Deploy with Docker
```bash
# Build and start services
docker-compose up -d --build

# Wait for database to be ready, then run migrations
sleep 30
docker-compose exec web python manage.py migrate_schemas --shared
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Create public tenant (main domain)
docker-compose exec web python manage.py create_public_tenant

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

## Step 6: Create Your First Tenant
```bash
docker-compose exec web python manage.py create_tenant
```

When prompted:
- Schema name: `demo` (or your preferred name)
- Domain: `demo.build.justcodeworks.eu`
- Name: `Demo Tenant`
- Description: `Demo tenant for testing`

## Step 7: Test the Deployment

1. **Main domain**: https://build.justcodeworks.eu
2. **Admin panel**: https://build.justcodeworks.eu/admin/
3. **Tenant subdomain**: https://demo.build.justcodeworks.eu

## Step 8: Set Up SSL Certificate (Let's Encrypt)
```bash
# Install certbot
apt install certbot python3-certbot-nginx

# Get certificate for main domain and wildcard
certbot --nginx -d build.justcodeworks.eu -d *.build.justcodeworks.eu

# Auto-renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
```

## Monitoring and Maintenance

### View logs
```bash
docker-compose logs -f web
docker-compose logs -f celery
```

### Update application
```bash
git pull origin main
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
```

### Backup database
```bash
docker-compose exec db pg_dump -U build_user build_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

## Troubleshooting

### Check container status
```bash
docker-compose ps
```

### Restart services
```bash
docker-compose restart web
docker-compose restart celery
```

### Check Django settings
```bash
docker-compose exec web python manage.py check --deploy
```

---

Your Django multi-tenant platform should now be running at https://build.justcodeworks.eu! 🚀