# Quick Commands Reference

## 🚀 Start/Stop Services
```bash
sudo systemctl start gunicorn_enrollment
sudo systemctl stop gunicorn_enrollment
sudo systemctl restart gunicorn_enrollment
sudo systemctl status gunicorn_enrollment
```

## 📊 View Logs
```bash
sudo journalctl -u gunicorn_enrollment -f        # Follow logs
sudo journalctl -u gunicorn_enrollment -n 50     # Last 50 lines
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 💾 Backup
```bash
cd /home/ubuntu/projects/university_enrollment
./backup_database.sh                  # Manual backup
ls -lh backups/                       # View backups
```

## 🔍 Check Status
```bash
sudo systemctl status gunicorn_enrollment nginx mysql
sudo netstat -tuln | grep -E ':(80|8001|3306)'
curl -I http://localhost/
```

## 🔧 Maintenance
```bash
# Collect static files
cd /home/ubuntu/projects/university_enrollment
source venv/bin/activate
python3 manage.py collectstatic --noinput
sudo systemctl restart gunicorn_enrollment

# Check disk space
df -h

# Check memory
free -h
```

## 🌐 Access Application
Website:    http://192.168.1.200/

Admin:      http://192.168.1.200/admin/

API:        http://192.168.1.200/api/
