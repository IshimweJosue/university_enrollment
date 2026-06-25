# University Course Enrollment & Grades Management System

A full-stack Django web application for managing university course enrollments, student grades, and professor assignments.

## 📋 Project Overview

This is a complete CRUD (Create, Read, Update, Delete) application built with Django 4.x and Django REST Framework, designed to handle:

- **Student Management** - Register and manage student profiles
- **Professor Management** - Manage faculty and their courses
- **Course Management** - Create courses, manage capacity, upload syllabi
- **Enrollment System** - Enroll students in courses and track grades
- **Grade Reporting** - View student grades, GPAs, and academic progress
- **REST API** - Full API for integration with other systems

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────┐

│                    Frontend (HTML/CSS/JS)               │

└────────────────────┬────────────────────────────────────┘

│ HTTP Requests

┌────────────────────▼────────────────────────────────────┐

│                  Nginx (Reverse Proxy)                  │

│              Static & Media File Server                 │

└────────────────────┬────────────────────────────────────┘

│ WSGI

┌────────────────────▼────────────────────────────────────┐

│            Gunicorn (Application Server)                │

│         Django 4.x + Django REST Framework              │

└────────────────────┬────────────────────────────────────┘

│ SQL Queries

┌────────────────────▼────────────────────────────────────┐

│                 MySQL Database                          │

│    (Professor, Student, Course, Enrollment Models)      │

└─────────────────────────────────────────────────────────┘
## 🛠️ Technology Stack

### Backend
- **Framework:** Django 4.2.0
- **API:** Django REST Framework 3.14.0
- **Database:** MySQL 8.0
- **Server:** Gunicorn 21.2.0
- **Proxy:** Nginx 1.24.0
- **Language:** Python 3.12

### Frontend
- **Markup:** HTML5
- **Styling:** CSS3
- **Interactivity:** Vanilla JavaScript
- **No admin templates** - custom responsive UI

### Deployment
- **OS:** Ubuntu 24.04 LTS
- **Hosting:** University Server (Nextcloud Infrastructure)
- **Backup:** Automated daily MySQL backups

## 📦 Installation & Setup

### Prerequisites
- Ubuntu 24.04 LTS
- Python 3.12
- MySQL Server
- Pip & Virtual Environment

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/university_enrollment.git
cd university_enrollment

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << 'ENVFILE'
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_ENGINE=django.db.backends.mysql
DB_NAME=university_enrollment
DB_USER=enrollment_user
DB_PASSWORD=password123
DB_HOST=localhost
DB_PORT=3306
ENVFILE

# Create database and tables
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser

# Run development server
python3 manage.py runserver 0.0.0.0:8000
```

Visit: `http://localhost:8000/`

## 🚀 Production Deployment

### Quick Start
```bash
# All services running
sudo systemctl status gunicorn_enrollment nginx mysql

# Access application
http://your-server-ip/
```

### Detailed Deployment Guide
See `DEPLOYMENT_README.md` for complete production setup instructions.

## 📊 Database Schema

### Models & Relationships
┌──────────────────────────────────────────────────────┐

│                    Professor                         │

├──────────────────────────────────────────────────────┤

│ • id (PK)                                            │

│ • user_id (FK → User)                               │

│ • employee_id (unique)                              │

│ • department                                        │

│ • phone                                             │

│ • office_location                                   │

│ • profile_picture                                   │

│ • bio                                               │

│ • created_at, updated_at                            │

└──────────────┬───────────────────────────────────────┘

│ One-to-Many

│ (1 Professor → M Courses)

▼

┌──────────────────────────────────────────────────────┐

│                     Course                           │

├──────────────────────────────────────────────────────┤

│ • id (PK)                                            │

│ • course_code (unique)                              │

│ • title                                             │

│ • description                                       │

│ • credits                                           │

│ • professor_id (FK → Professor)                     │

│ • semester                                          │

│ • max_students                                      │

│ • syllabus (PDF file)                               │

│ • created_at, updated_at                            │

└──────────────┬────────┬──────────────────────────────┘

│        │

│        │ Many-to-Many (via Enrollment)

│        │

│        ▼

│    ┌──────────────────────────────────┐

│    │    Enrollment (Join Table)       │

│    ├──────────────────────────────────┤

│    │ • id (PK)                        │

│    │ • student_id (FK → Student)      │

│    │ • course_id (FK → Course)        │

│    │ • grade (A-F)                    │

│    │ • enrolled_date                  │

│    │ • updated_at                     │

│    └──────────────────────────────────┘

│

│ One-to-Many

│ (1 Student ← M Enrollments)

▼

┌──────────────────────────────────────────────────────┐

│                     Student                          │

├──────────────────────────────────────────────────────┤

│ • id (PK)                                            │

│ • user_id (FK → User)                               │

│ • student_id (unique)                               │

│ • major                                             │

│ • enrollment_year                                   │

│ • phone                                             │

│ • profile_picture                                   │

│ • bio                                               │

│ • created_at, updated_at                            │

└──────────────────────────────────────────────────────┘

## 🔌 API Endpoints

### Base URL
http://192.168.1.200/api/
### Professors
GET    /api/professors/              - List all professors

POST   /api/professors/              - Create professor

GET    /api/professors/{id}/         - Get professor details

PUT    /api/professors/{id}/         - Update professor

DELETE /api/professors/{id}/         - Delete professor
### Students
GET    /api/students/                - List all students

POST   /api/students/                - Create student

GET    /api/students/{id}/           - Get student details

PUT    /api/students/{id}/           - Update student

DELETE /api/students/{id}/           - Delete student

GET    /api/students/{id}/grade_report/ - Get grade report
### Courses
GET    /api/courses/                 - List all courses

POST   /api/courses/                 - Create course

GET    /api/courses/{id}/            - Get course details

PUT    /api/courses/{id}/            - Update course

DELETE /api/courses/{id}/            - Delete course

GET    /api/courses/{id}/students/   - Get enrolled students
### Enrollments
GET    /api/enrollments/             - List all enrollments

POST   /api/enrollments/             - Create enrollment

GET    /api/enrollments/{id}/        - Get enrollment details

PUT    /api/enrollments/{id}/        - Update enrollment (grade)

DELETE /api/enrollments/{id}/        - Delete enrollment
### Example: Get Student Grade Report
```bash
curl http://localhost/api/students/1/grade_report/
```

**Response:**
```json
{
  "id": 1,
  "user": {
    "id": 3,
    "username": "alice_johnson",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Johnson"
  },
  "student_id": "STU001",
  "major": "Computer Science",
  "enrollment_year": 2024,
  "gpa": 3.5,
  "total_credits": 7,
  "total_credits_earned": 7,
  "courses": [
    {
      "course_code": "CS101",
      "title": "Introduction to Programming",
      "credits": 3,
      "professor": "Dr. John Smith",
      "grade": "A",
      "grade_value": 4.0
    }
  ]
}
```

## 🔐 Authentication

### Frontend
- Django session-based authentication
- Login/Register/Logout views
- User roles: Student, Professor, Admin

### API
- Token-based authentication
- Session authentication
- Permission classes: `IsAuthenticatedOrReadOnly`

### Login
cat > README.md << 'EOF'
# University Course Enrollment & Grades Management System

A full-stack Django web application for managing university course enrollments, student grades, and professor assignments.

## 📋 Project Overview

This is a complete CRUD (Create, Read, Update, Delete) application built with Django 4.x and Django REST Framework, designed to handle:

- **Student Management** - Register and manage student profiles
- **Professor Management** - Manage faculty and their courses
- **Course Management** - Create courses, manage capacity, upload syllabi
- **Enrollment System** - Enroll students in courses and track grades
- **Grade Reporting** - View student grades, GPAs, and academic progress
- **REST API** - Full API for integration with other systems

## 🏗️ Architecture
┌─────────────────────────────────────────────────────────┐

│                    Frontend (HTML/CSS/JS)               │

└────────────────────┬────────────────────────────────────┘

│ HTTP Requests

┌────────────────────▼────────────────────────────────────┐

│                  Nginx (Reverse Proxy)                  │

│              Static & Media File Server                 │

└────────────────────┬────────────────────────────────────┘

│ WSGI

┌────────────────────▼────────────────────────────────────┐

│            Gunicorn (Application Server)                │

│         Django 4.x + Django REST Framework              │

└────────────────────┬────────────────────────────────────┘

│ SQL Queries

┌────────────────────▼────────────────────────────────────┐

│                 MySQL Database                          │

│    (Professor, Student, Course, Enrollment Models)      │

└─────────────────────────────────────────────────────────┘
## 🛠️ Technology Stack

### Backend
- **Framework:** Django 4.2.0
- **API:** Django REST Framework 3.14.0
- **Database:** MySQL 8.0
- **Server:** Gunicorn 21.2.0
- **Proxy:** Nginx 1.24.0
- **Language:** Python 3.12

### Frontend
- **Markup:** HTML5
- **Styling:** CSS3
- **Interactivity:** Vanilla JavaScript
- **No admin templates** - custom responsive UI

### Deployment
- **OS:** Ubuntu 24.04 LTS
- **Hosting:** University Server (Nextcloud Infrastructure)
- **Backup:** Automated daily MySQL backups

## 📦 Installation & Setup

### Prerequisites
- Ubuntu 24.04 LTS
- Python 3.12
- MySQL Server
- Pip & Virtual Environment

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/university_enrollment.git
cd university_enrollment

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << 'ENVFILE'
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_ENGINE=django.db.backends.mysql
DB_NAME=university_enrollment
DB_USER=enrollment_user
DB_PASSWORD=password123
DB_HOST=localhost
DB_PORT=3306
ENVFILE

# Create database and tables
python3 manage.py migrate

# Create superuser
python3 manage.py createsuperuser

# Run development server
python3 manage.py runserver 0.0.0.0:8000
```

Visit: `http://localhost:8000/`

## 🚀 Production Deployment

### Quick Start
```bash
# All services running
sudo systemctl status gunicorn_enrollment nginx mysql

# Access application
http://your-server-ip/
```

### Detailed Deployment Guide
See `DEPLOYMENT_README.md` for complete production setup instructions.

## 📊 Database Schema

### Models & Relationships
┌──────────────────────────────────────────────────────┐

│                    Professor                         │

├──────────────────────────────────────────────────────┤

│ • id (PK)                                            │

│ • user_id (FK → User)                               │

│ • employee_id (unique)                              │

│ • department                                        │

│ • phone                                             │

│ • office_location                                   │

│ • profile_picture                                   │

│ • bio                                               │

│ • created_at, updated_at                            │

└──────────────┬───────────────────────────────────────┘

│ One-to-Many

│ (1 Professor → M Courses)

▼

┌──────────────────────────────────────────────────────┐

│                     Course                           │

├──────────────────────────────────────────────────────┤

│ • id (PK)                                            │

│ • course_code (unique)                              │

│ • title                                             │

│ • description                                       │

│ • credits                                           │

│ • professor_id (FK → Professor)                     │

│ • semester                                          │

│ • max_students                                      │

│ • syllabus (PDF file)                               │

│ • created_at, updated_at                            │

└──────────────┬────────┬──────────────────────────────┘

│        │

│        │ Many-to-Many (via Enrollment)

│        │

│        ▼

│    ┌──────────────────────────────────┐

│    │    Enrollment (Join Table)       │

│    ├──────────────────────────────────┤

│    │ • id (PK)                        │

│    │ • student_id (FK → Student)      │

│    │ • course_id (FK → Course)        │

│    │ • grade (A-F)                    │

│    │ • enrolled_date                  │

│    │ • updated_at                     │

│    └──────────────────────────────────┘

│

│ One-to-Many

│ (1 Student ← M Enrollments)

▼

┌──────────────────────────────────────────────────────┐

│                     Student                          │

├──────────────────────────────────────────────────────┤

│ • id (PK)                                            │

│ • user_id (FK → User)                               │

│ • student_id (unique)                               │

│ • major                                             │

│ • enrollment_year                                   │

│ • phone                                             │

│ • profile_picture                                   │

│ • bio                                               │

│ • created_at, updated_at                            │

└──────────────────────────────────────────────────────┘

## 🔌 API Endpoints

### Base URL
http://192.168.1.200/api/
### Professors
GET    /api/professors/              - List all professors

POST   /api/professors/              - Create professor

GET    /api/professors/{id}/         - Get professor details

PUT    /api/professors/{id}/         - Update professor

DELETE /api/professors/{id}/         - Delete professor
### Students
GET    /api/students/                - List all students

POST   /api/students/                - Create student

GET    /api/students/{id}/           - Get student details

PUT    /api/students/{id}/           - Update student

DELETE /api/students/{id}/           - Delete student

GET    /api/students/{id}/grade_report/ - Get grade report
### Courses
GET    /api/courses/                 - List all courses

POST   /api/courses/                 - Create course

GET    /api/courses/{id}/            - Get course details

PUT    /api/courses/{id}/            - Update course

DELETE /api/courses/{id}/            - Delete course

GET    /api/courses/{id}/students/   - Get enrolled students
### Enrollments
GET    /api/enrollments/             - List all enrollments

POST   /api/enrollments/             - Create enrollment

GET    /api/enrollments/{id}/        - Get enrollment details

PUT    /api/enrollments/{id}/        - Update enrollment (grade)

DELETE /api/enrollments/{id}/        - Delete enrollment
### Example: Get Student Grade Report
```bash
curl http://localhost/api/students/1/grade_report/
```

**Response:**
```json
{
  "id": 1,
  "user": {
    "id": 3,
    "username": "alice_johnson",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Johnson"
  },
  "student_id": "STU001",
  "major": "Computer Science",
  "enrollment_year": 2024,
  "gpa": 3.5,
  "total_credits": 7,
  "total_credits_earned": 7,
  "courses": [
    {
      "course_code": "CS101",
      "title": "Introduction to Programming",
      "credits": 3,
      "professor": "Dr. John Smith",
      "grade": "A",
      "grade_value": 4.0
    }
  ]
}
```

## 🔐 Authentication

### Frontend
- Django session-based authentication
- Login/Register/Logout views
- User roles: Student, Professor, Admin

### API
- Token-based authentication
- Session authentication
- Permission classes: `IsAuthenticatedOrReadOnly`

### Login

http://192.168.1.200/login/

Username:admin

Password:Password123!
## 🔍 Search & Filtering

### Students - Search by:
- First name
- Last name
- Student ID
- Major
- Enrollment year

### Courses - Filter by:
- Semester
- Professor
- Credits
- Course code

### Enrollments - Filter by:
- Course
- Student
- Grade

## 📁 Project Structure
university_enrollment/

├── venv/                          # Python virtual environment

├── enrollment_system/             # Django project configuration

│   ├── settings.py               # Project settings

│   ├── urls.py                   # URL routing

│   ├── wsgi.py                   # WSGI configuration

│   └── asgi.py                   # ASGI configuration

├── core/                         # Main application

│   ├── models.py                 # Database models

│   ├── views.py                  # View classes

│   ├── forms.py                  # Django forms

│   ├── urls.py                   # App URLs

│   ├── admin.py                  # Admin configuration

│   └── templates/core/           # HTML templates

├── api/                          # REST API

│   ├── serializers.py            # DRF serializers

│   ├── views.py                  # ViewSets

│   └── urls.py                   # API URLs

├── accounts/                     # Authentication

│   ├── views.py                  # Auth views

│   └── urls.py                   # Auth URLs

├── templates/                    # Base templates

│   ├── base.html                 # Base template

│   └── accounts/                 # Auth templates

├── static/                       # Static files (served by Nginx)

│   ├── css/style.css             # Main stylesheet

│   └── js/main.js                # JavaScript

├── media/                        # User uploads

│   ├── professor_pictures/       # Professor photos

│   ├── student_pictures/         # Student photos

│   └── syllabi/                  # Course PDFs

├── manage.py                     # Django management script

├── requirements.txt              # Python dependencies

├── .env                          # Environment variables (not in git)

├── .gitignore                    # Git ignore rules

├── README.md                     # This file

├── DEPLOYMENT_README.md          # Deployment guide

├── QUICK_COMMANDS.md             # Quick reference

└── backup_database.sh            # Database backup script
## 🎯 Features

### Student Features
- ✅ Register and create profile
- ✅ View enrolled courses
- ✅ Track grades and GPA
- ✅ View course syllabi
- ✅ Edit profile information

### Professor Features
- ✅ Manage assigned courses
- ✅ View enrolled students
- ✅ Assign grades
- ✅ Upload course syllabi
- ✅ Edit profile information

### Admin Features
- ✅ Manage all entities (CRUD)
- ✅ Assign professors to courses
- ✅ Manage student enrollments
- ✅ Access admin panel
- ✅ View system statistics

### Technical Features
- ✅ Full REST API
- ✅ Database relationships (1-M, M-M)
- ✅ Search functionality with Q objects
- ✅ File uploads (images, PDFs)
- ✅ Pagination (10-20 items/page)
- ✅ Production deployment
- ✅ Automated backups
- ✅ Gzip compression
- ✅ Static file caching

## 🔄 Relationships Handling

### Student ↔ Course (Many-to-Many)
- Via Enrollment join table
- Enrollment includes grade field
- Each student can enroll in multiple courses
- Each course can have multiple students

### Professor → Course (One-to-Many)
- One professor teaches multiple courses
- Course has FK to professor
- Professor can manage all assigned courses

### Student → Enrollment (One-to-Many)
- One student has multiple enrollments
- Each enrollment is one course

### User → Student/Professor (One-to-One)
- Each student/professor linked to Django User
- User authentication handled by Django

## 🚀 Deployment

### Development
```bash
python3 manage.py runserver 0.0.0.0:8000
```

### Production
```bash
# Gunicorn running on port 8001
# Nginx serving on port 80
# Auto-restart on failure
# Automated daily backups
```

See `DEPLOYMENT_README.md` for complete details.

## 💾 Database Backup & Restore

### Create Backup
```bash
./backup_database.sh
```

### View Backups
```bash
ls -lh backups/
```

### Restore Backup
```bash
gunzip < backups/db_backup_YYYYMMDD_HHMMSS.sql.gz | mysql -u enrollment_user -p university_enrollment
```

## 📝 API Documentation

### Create Student Example
```bash
curl -X POST http://localhost/api/students/ \
  -H "Content-Type: application/json" \
  -d '{
    "user": {"username": "alice", "email": "alice@example.com"},
    "student_id": "STU001",
    "major": "Computer Science",
    "enrollment_year": 2024
  }'
```

### Enroll Student Example
```bash
curl -X POST http://localhost/api/enrollments/ \
  -H "Content-Type: application/json" \
  -d '{
    "student": 1,
    "course": 1
  }'
```

### Get Grade Report Example
```bash
curl http://localhost/api/students/1/grade_report/ | python -m json.tool
```

## 🔧 Troubleshooting

### 502 Bad Gateway
```bash
sudo systemctl status gunicorn_enrollment
sudo journalctl -u gunicorn_enrollment -n 50
```

### Database Connection Error
```bash
mysql -u enrollment_user -p university_enrollment -e "SELECT 1;"
```

### Static Files Not Loading
```bash
python3 manage.py collectstatic --noinput
sudo systemctl restart gunicorn_enrollment
```

See `DEPLOYMENT_README.md` for more troubleshooting.

## 👤 Student Information

- **Name:** Josue Amola
- **Institution:** University of Rwanda
- **Course:** Full-Stack Web Development
- **Project Type:** CRUD System with Relationships
- **Submission Date:** 2024

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Full-stack Django development
- ✅ Database design with relationships
- ✅ REST API development
- ✅ Production deployment
- ✅ Frontend UI/UX design
- ✅ Authentication & authorization
- ✅ File upload handling
- ✅ Search & filtering
- ✅ Automated backups
- ✅ Server configuration

## 📄 License

This project is created for educational purposes at the University of Rwanda.

## 🤝 Support

For issues or questions, contact:
- Email: josue@amola.rw
- GitHub Issues: [Add link to repository]

---

**Last Updated:** June 2024  
**Version:** 1.0.0
