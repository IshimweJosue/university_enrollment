#!/bin/bash

BACKUP_DIR="/home/ubuntu/projects/university_enrollment/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup MySQL database
mysqldump -u enrollment_user -ppassword123 university_enrollment > $BACKUP_FILE

# Compress the backup
gzip $BACKUP_FILE

echo "Database backup completed: $BACKUP_FILE.gz"

# Keep only last 7 backups
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete

echo "Old backups cleaned up"
