# University Enrollment System - API Documentation

## Base URL
http://192.168.1.200/api/
## Authentication

### Session Authentication
- Use login credentials from the web interface
- Cookies handle authentication automatically

### API Token (Optional)
- Add `Authorization: Token <token>` header for token auth
- Permissions: `IsAuthenticatedOrReadOnly`

## Response Format

All responses are in JSON format.

### Success Response (200)
```json
{
  "id": 1,
  "field1": "value1",
  "field2": "value2"
}
```

### List Response (200)
```json
{
  "count": 10,
  "next": "http://api.example.com/students/?page=2",
  "previous": null,
  "results": [
    { "id": 1, ... },
    { "id": 2, ... }
  ]
}
```

### Error Response (4xx/5xx)
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

## Endpoints

### PROFESSORS

#### List Professors
GET /api/professors/
**Query Parameters:**
- `search`: Search by name, ID, or department
- `ordering`: Order by `last_name` or `department`
- `page`: Page number for pagination

**Example:**
```bash
curl "http://localhost/api/professors/?search=Smith&page=1"
```

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 2,
        "username": "jsmith",
        "email": "john.smith@university.edu",
        "first_name": "John",
        "last_name": "Smith"
      },
      "employee_id": "PROF001",
      "department": "Computer Science",
      "phone": "+1234567890",
      "office_location": "Building A, Room 101",
      "courses_count": 3
    }
  ]
}
```

#### Create Professor
POST /api/professors/
**Body:**
```json
{
  "user": {
    "username": "jdoe",
    "email": "jane.doe@university.edu",
    "first_name": "Jane",
    "last_name": "Doe"
  },
  "employee_id": "PROF002",
  "department": "Mathematics",
  "phone": "+1234567890",
  "office_location": "Building B, Room 201"
}
```

#### Get Professor Details
GET /api/professors/{id}/
#### Update Professor
PUT /api/professors/{id}/

PATCH /api/professors/{id}/
#### Delete Professor
DELETE /api/professors/{id}/
---

### STUDENTS

#### List Students
GET /api/students/
**Query Parameters:**
- `search`: Search by name, student ID
- `major`: Filter by major
- `enrollment_year`: Filter by year
- `ordering`: Order by `last_name` or `major`

**Example:**
```bash
curl "http://localhost/api/students/?major=Computer%20Science&page=1"
```

#### Create Student
POST /api/students/
**Body:**
```json
{
  "user": {
    "username": "alice",
    "email": "alice@student.com",
    "first_name": "Alice",
    "last_name": "Johnson"
  },
  "student_id": "STU001",
  "major": "Computer Science",
  "enrollment_year": 2024
}
```

#### Get Student Grade Report
GET /api/students/{id}/grade_report/
**Response:**
```json
{
  "id": 1,
  "user": {
    "id": 3,
    "username": "alice",
    "email": "alice@student.com",
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
    },
    {
      "course_code": "CS201",
      "title": "Data Structures",
      "credits": 4,
      "professor": "Dr. John Smith",
      "grade": "B",
      "grade_value": 3.0
    }
  ]
}
```

---

### COURSES

#### List Courses
GET /api/courses/

**Query Parameters:**
- `search`: Search by code or title
- `semester`: Filter by semester
- `professor`: Filter by professor ID

**Example:**
```bash
curl "http://localhost/api/courses/?semester=Fall%202024"
```

#### Create Course
POST /api/courses/
**Body:**
```json
{
  "course_code": "CS101",
  "title": "Introduction to Programming",
  "description": "Learn basic programming concepts",
  "credits": 3,
  "professor": 1,
  "semester": "Fall 2024",
  "max_students": 50
}
```

#### Get Course with Enrolled Students
GET /api/courses/{id}/students/
**Response:**
```json
{
  "id": 1,
  "course_code": "CS101",
  "title": "Introduction to Programming",
  "professor": {...},
  "max_students": 50,
  "enrolled_students": [
    {
      "id": 1,
      "name": "Alice Johnson",
      "student_id": "STU001",
      "major": "Computer Science",
      "grade": "A",
      "enrolled_date": "2024-06-01T10:00:00Z"
    }
  ]
}
```

---

### ENROLLMENTS

#### List Enrollments
GET /api/enrollments/

**Query Parameters:**
- `course`: Filter by course ID
- `student`: Filter by student ID
- `grade`: Filter by grade (A, B, C, D, F, Pending)

#### Create Enrollment
POST /api/enrollments/
**Body:**
```json
{
  "student": 1,
  "course": 1
}
```

**Error Response (if course is full):**
```json
{
  "error": "Course CS101 is at maximum capacity!"
}
```

#### Update Enrollment (Grade)
PUT /api/enrollments/{id}/

PATCH /api/enrollments/{id}/
**Body:**
```json
{
  "grade": "A"
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created |
| 204 | No Content - Deletion successful |
| 400 | Bad Request - Invalid parameters |
| 403 | Forbidden - Permission denied |
| 404 | Not Found - Resource not found |
| 500 | Server Error - Internal error |

## Pagination

Responses are paginated with 10 items per page by default.
GET /api/students/?page=2
**Response:**
```json
{
  "count": 50,
  "next": "http://localhost/api/students/?page=3",
  "previous": "http://localhost/api/students/?page=1",
  "results": [...]
}
```

## Search & Filtering

### Search Example
```bash
curl "http://localhost/api/students/?search=John"
```

### Filter Example
```bash
curl "http://localhost/api/enrollments/?grade=A&course=1"
```

---

**Last Updated:** June 2024
