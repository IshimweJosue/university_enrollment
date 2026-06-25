# University Enrollment System - Production Deployment

## 📊 System Information

- **Server OS:** Ubuntu 24.04 LTS
- **Web Server:** Nginx 1.24.0
- **Application Server:** Gunicorn
- **Database:** MySQL
- **Python:** 3.12
- **Django:** 4.2

## 🚀 Running Application

**Visit your application:**
http://192.168.1.200/
**Admin Panel:**
http://192.168.1.200/admin
**API Endpoints:**
http://192.168.1.200/api/
## 📋 Service Management

### Check Service Status
```bash
sudo systemctl status gunicorn_enrollment
sudo systemctl status nginx
sudo systemctl status mysql
```

### Restart Services
```bash
# Restart Gunicorn
sudo systemctl restart gunicorn_enrollment

# Restart Nginx
sudo systemctl restart nginx

# Restart all
sudo systemctl restart gunicorn_enrollment nginx
```

### View Logs
```bash
# Application logs
sudo journalctl -u gunicorn_enrollment -n 50 -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

## 💾 Database Backup

### Manual Backup
```bash
cd /home/ubuntu/projects/university_enrollment
./backup_database.sh
```

### View Backups
```bash
ls -lh /home/ubuntu/projects/university_enrollment/backups/
```

### Restore from Backup
```bash
gunzip < /path/to/backup.sql.gz | mysql -u enrollment_user -p university_enrollment
```

### Automatic Backups
- Configured to run daily at 2 AM
- Keeps last 7 days of backups
- Logs saved to: `backup.log`

## 🔧 Common Tasks

### Collect Static Files (after code updates)
```bash
cd /home/ubuntu/projects/university_enrollment
source venv/bin/activate
python3 manage.py collectstatic --noinput
sudo systemctl restart gunicorn_enrollment
```

### Create Superuser
```bash
cd /home/ubuntu/projects/university_enrollment
source venv/bin/activate
python3 manage.py createsuperuser
```

### Create Sample Data
Access admin panel: `http://your-server-ip/admin/`
- Add Professors
- Add Students
- Add Courses
- Add Enrollments

### Migrate Database
```bash
cd /home/ubuntu/projects/university_enrollment
source venv/bin/activate
python3 manage.py migrate
```

## 📊 Monitoring

### System Resources
```bash
# CPU and Memory Usage
top

# Disk Usage
df -h

# Check if services are running
sudo netstat -tuln | grep -E ':(80|8001|3306)'
```

### Application Health
```bash
# Test home page
curl -I http://localhost/

# Test API
curl http://localhost/api/students/ | python -m json.tool
```

## 🔍 Troubleshooting

### 502 Bad Gateway
```bash
# Check Gunicorn status
sudo systemctl status gunicorn_enrollment

# View error logs
sudo journalctl -u gunicorn_enrollment -n 100
```

### Nginx Not Working
```bash
# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Check error logs
sudo tail -f /var/log/nginx/error.log
```

### Database Connection Issues
```bash
# Check MySQL status
sudo systemctl status mysql

# Test connection
mysql -u enrollment_user -p university_enrollment -e "SELECT 1;"
```

### Permission Denied Errors
```bash
# Fix project permissions
sudo chown -R ubuntu:www-data /home/ubuntu/projects/university_enrollment

# Restart services
sudo systemctl restart gunicorn_enrollment nginx
```

## 📁 Directory Structure
/home/ubuntu/projects/university_enrollment/

├── venv/                          # Virtual environment

├── enrollment_system/             # Django project settings

├── core/                          # Main application

├── api/                           # REST API

├── accounts/                      # Authentication

├── templates/                     # HTML templates

├── static/                        # CSS, JS, images

├── media/                         # Uploaded files

├── manage.py                      # Django management

├── requirements.txt               # Python dependencies

├── backup_database.sh             # Backup script

├── backups/                       # Database backups

└── DEPLOYMENT_README.md           # This file
## 🔐 Security Notes

- DEBUG is disabled in production
- CSRF protection enabled
- Static files served via Nginx
- Database credentials in environment variables
- Regular automated backups
- Firewall (UFW) configured

## 🎯 Performance Optimizations

- Gzip compression enabled
- Static file caching (30 days)
- Media file caching (7 days)
- Database query optimization
- Connection pooling configured

## 📞 Support & Maintenance

### Regular Maintenance
- Check logs weekly
- Verify backups are running
- Monitor disk space
- Update system packages monthly

### Update Django/Dependencies
```bash
cd /home/ubuntu/projects/university_enrollment
source venv/bin/activate
pip install --upgrade Django djangorestframework
sudo systemctl restart gunicorn_enrollment
```

## 📈 Future Enhancements

- [ ] SSL/HTTPS with Let's Encrypt
- [ ] Email notifications
- [ ] Monitoring dashboard
- [ ] Rate limiting
- [ ] CDN for static files
- [ ] Database replication
- [ ] Load balancing
