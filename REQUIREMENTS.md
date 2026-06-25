# Project Requirements

## Functional Requirements

### CRUD Operations
- [x] Create Professor
- [x] Read Professor
- [x] Update Professor
- [x] Delete Professor
- [x] Create Student
- [x] Read Student
- [x] Update Student
- [x] Delete Student
- [x] Create Course
- [x] Read Course
- [x] Update Course
- [x] Delete Course
- [x] Create Enrollment
- [x] Update Enrollment (Grade)
- [x] Delete Enrollment

### Relationships
- [x] Professor (1) ↔ Course (M)
- [x] Student (M) ↔ Course (M) via Enrollment
- [x] Enrollment includes Grade field
- [x] Proper ForeignKey and ManyToManyField usage

### Authentication
- [x] User Registration
- [x] User Login
- [x] User Logout
- [x] Django User Model integration
- [x] Session-based authentication
- [x] Permission classes

### Search & Filtering
- [x] Search Students by name, ID
- [x] Search by Course
- [x] Search by Professor
- [x] Filter using Q objects
- [x] Multiple filter criteria

### File Upload
- [x] Profile pictures (Students/Professors)
- [x] Course syllabus (PDF)
- [x] Proper media directory handling

### REST API
- [x] Professor endpoints (CRUD)
- [x] Student endpoints (CRUD)
- [x] Course endpoints (CRUD)
- [x] Enrollment endpoints (CRUD)
- [x] Grade Report endpoint
- [x] DRF Serializers
- [x] Pagination
- [x] Filtering & Search

## Technical Requirements

### Backend
- [x] Django 4.x
- [x] Django REST Framework
- [x] MySQL Database
- [x] Custom HTML/CSS/JavaScript
- [x] No admin templates for public views

### Database
- [x] At least 3 related tables
- [x] Proper relationships
- [x] Indexes on frequently searched fields
- [x] Default values where appropriate

### Frontend
- [x] HTML5 markup
- [x] CSS3 styling
- [x] Responsive design
- [x] JavaScript interactivity
- [x] Custom UI (not admin templates)

### Deployment
- [x] Nginx web server
- [x] Gunicorn application server
- [x] Ubuntu VM
- [x] Static file serving
- [x] Media file handling

### Documentation
- [x] README.md (100+ lines)
- [x] Deployment guide
- [x] API documentation
- [x] Database schema
- [x] Installation instructions
- [x] 200-300 word reflection on relationships

## Submission Requirements

### Code
- [x] GitHub repository with README
- [x] All code properly commented
- [x] .gitignore configured
- [x] requirements.txt with dependencies

### Database
- [x] MySQL database with proper schema
- [x] Test data included
- [x] Relationships documented
- [x] Backup/restore scripts

### Documentation
- [x] README with project overview
- [x] Installation & deployment guide
- [x] API documentation with examples
- [x] Database schema diagram
- [x] Relationship handling reflection

### Screenshots (for PDF submission)
- [x] Home page
- [x] Admin panel
- [x] Frontend CRUD pages
- [x] Search functionality
- [x] API endpoints
- [x] Mobile responsive view

### Reflection
- [x] 200-300 words on:
  - How relationships are handled
  - Challenges encountered
  - Solutions implemented
  - Lessons learned

