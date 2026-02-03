# Deployment Guide for Blog Site

## Development Setup

### 1. Initial Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and update the values:
- Change `SECRET_KEY` to a random string
- Set `DEBUG=True` for development
- Configure email settings if needed

### 3. Database Setup

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Load sample data (optional)
python setup_sample_data.py
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser

## Production Deployment

### Prerequisites
- Python 3.8 or higher
- PostgreSQL (recommended) or MySQL
- Web server (Nginx or Apache)
- WSGI server (Gunicorn or uWSGI)

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib

# Create project user
sudo useradd -m -s /bin/bash blogsite
sudo su - blogsite
```

### 2. Application Setup

```bash
# Clone or upload project
cd /home/blogsite
git clone <your-repo> blog_site
cd blog_site

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 3. Database Configuration

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE blogsite_db;
CREATE USER blogsite_user WITH PASSWORD 'your_secure_password';
ALTER ROLE blogsite_user SET client_encoding TO 'utf8';
ALTER ROLE blogsite_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE blogsite_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE blogsite_db TO blogsite_user;
\q
```

Update `settings.py` database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blogsite_db',
        'USER': 'blogsite_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4. Production Settings

Update `.env` file:

```
SECRET_KEY=your-very-long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Email settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Static Files

```bash
# Collect static files
python manage.py collectstatic --noinput
```

### 6. Gunicorn Configuration

Create `/etc/systemd/system/blogsite.service`:

```ini
[Unit]
Description=Blog Site Gunicorn daemon
After=network.target

[Service]
User=blogsite
Group=www-data
WorkingDirectory=/home/blogsite/blog_site
ExecStart=/home/blogsite/blog_site/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/home/blogsite/blog_site/blogsite.sock \
          blog_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start and enable service:

```bash
sudo systemctl start blogsite
sudo systemctl enable blogsite
```

### 7. Nginx Configuration

Create `/etc/nginx/sites-available/blogsite`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/blogsite/blog_site;
    }
    
    location /media/ {
        root /home/blogsite/blog_site;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/blogsite/blog_site/blogsite.sock;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/blogsite /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 8. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 9. Firewall Configuration

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## Maintenance

### Regular Updates

```bash
# Pull latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart blogsite
sudo systemctl restart nginx
```

### Backup Database

```bash
# Create backup
sudo -u postgres pg_dump blogsite_db > backup_$(date +%Y%m%d).sql

# Restore backup
sudo -u postgres psql blogsite_db < backup_20240101.sql
```

### Log Monitoring

```bash
# View Gunicorn logs
sudo journalctl -u blogsite -f

# View Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## Troubleshooting

### Common Issues

1. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check Nginx static file paths
   - Verify file permissions

2. **Email not sending**
   - Verify email settings in `.env`
   - Check firewall rules for SMTP
   - Use app-specific passwords for Gmail

3. **Database connection errors**
   - Check PostgreSQL is running
   - Verify database credentials
   - Ensure database exists

4. **Permission errors**
   - Check file ownership: `sudo chown -R blogsite:www-data /home/blogsite/blog_site`
   - Set proper permissions: `sudo chmod -R 755 /home/blogsite/blog_site`

## Performance Optimization

### 1. Enable Caching

Install Redis:
```bash
sudo apt install redis-server
pip install django-redis
```

Add to `settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 2. Database Optimization

- Create database indexes on frequently queried fields
- Use `select_related()` and `prefetch_related()` for queries
- Enable database connection pooling

### 3. Media File Optimization

- Use CDN for static and media files
- Compress images before upload
- Implement lazy loading for images

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Use HTTPS (SSL certificate)
- [ ] Keep dependencies updated
- [ ] Use strong database passwords
- [ ] Enable CSRF protection
- [ ] Configure secure cookies
- [ ] Regular backups
- [ ] Monitor logs for suspicious activity

## Support

For issues or questions:
- Check the README.md file
- Review Django documentation
- Check project logs
