# Troubleshooting Guide - Build Platform

## Rate Limit Issues (Let's Encrypt)

### Problem
```
too many new registrations (10) from this IP address in the last 3h0m0s
```

### Solutions

#### 1. Wait for Rate Limit Reset
- Rate limit resets at: **2025-10-22 12:59:23 UTC**
- After reset, run: `sudo certbot --nginx -d build.justcodeworks.eu -d *.build.justcodeworks.eu`

#### 2. Deploy HTTP-Only (Immediate)
```bash
chmod +x deploy_http_only.sh
./deploy_http_only.sh
```

#### 3. Use Existing Certificate
If you have other domains with Let's Encrypt certificates:
```bash
# Copy existing certificate
sudo cp /etc/letsencrypt/live/otherdomain.com/fullchain.pem /etc/ssl/certs/build.crt
sudo cp /etc/letsencrypt/live/otherdomain.com/privkey.pem /etc/ssl/private/build.key

# Update Nginx configuration to use these certificates
```

#### 4. Use Staging Environment (Testing)
```bash
# Test with Let's Encrypt staging (doesn't count toward rate limit)
sudo certbot --staging --nginx -d build.justcodeworks.eu
```

## Common Deployment Issues

### Django Not Starting
```bash
# Check logs
docker-compose logs web

# Common fixes
docker-compose down
docker-compose up -d --build

# Check environment
docker-compose exec web python manage.py check --deploy
```

### Database Connection Issues
```bash
# Check database container
docker-compose logs db

# Reset database
docker-compose down
docker volume rm build_postgres_data
docker-compose up -d
```

### Domain Not Resolving

#### Check DNS
```bash
# Test DNS resolution
nslookup build.justcodeworks.eu
dig build.justcodeworks.eu

# Expected result: Should point to your server IP
```

#### Check A Record
- Ensure A record points to your server IP
- Allow 5-60 minutes for DNS propagation
- Test from different locations: https://www.whatsmydns.net/

### Nginx Issues

#### Configuration Test
```bash
sudo nginx -t
sudo nginx -s reload
```

#### Check Nginx Status
```bash
sudo systemctl status nginx
sudo systemctl restart nginx
```

#### Port Conflicts
```bash
# Check what's using port 80/443
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443
```

## Quick Status Checks

### Run Status Script
```bash
chmod +x check_status.sh
./check_status.sh
```

### Manual Checks
```bash
# Test Django directly
curl -H "Host: build.justcodeworks.eu" http://localhost:8000

# Test through Nginx
curl http://build.justcodeworks.eu

# Check containers
docker-compose ps

# Check logs
docker-compose logs -f web
```

## Emergency Recovery

### Complete Reset
```bash
# Stop everything
docker-compose down

# Remove volumes (⚠️ DELETES DATA)
docker volume prune -f

# Rebuild from scratch
docker-compose up -d --build

# Run migrations
docker-compose exec web python manage.py migrate_schemas --shared
docker-compose exec web python manage.py migrate
```

### Backup Before Reset
```bash
# Backup database
docker-compose exec db pg_dump -U postgres build_db > backup.sql

# Backup media files
tar -czf media_backup.tar.gz media/
```

## SSL Certificate Solutions

### Temporary Self-Signed
```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/temp-build.key \
    -out /etc/ssl/certs/temp-build.crt \
    -subj "/CN=build.justcodeworks.eu"
```

### CloudFlare SSL (Alternative)
1. Add domain to CloudFlare
2. Set SSL mode to "Full (Strict)"
3. Use CloudFlare's origin certificates
4. Update Nginx to use CloudFlare IPs

### After Rate Limit Reset
```bash
# Full SSL setup
sudo certbot --nginx -d build.justcodeworks.eu -d *.build.justcodeworks.eu

# Auto-renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
```

## Performance Issues

### Check Resources
```bash
# Memory usage
docker stats

# Disk space
df -h
docker system df
```

### Optimize Database
```bash
# Run inside Django container
docker-compose exec web python manage.py dbshell
# Then: VACUUM; ANALYZE;
```

## Support Resources

- **Django Logs**: `docker-compose logs web`
- **Let's Encrypt Logs**: `/var/log/letsencrypt/letsencrypt.log`
- **Nginx Logs**: `/var/log/nginx/error.log`
- **Rate Limit Info**: https://letsencrypt.org/docs/rate-limits/

---

**Need immediate help?** Run the HTTP-only deployment to get your site working while troubleshooting SSL issues.