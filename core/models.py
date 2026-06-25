from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q

class Professor(models.Model):
    """Model for Professor entity"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    office_location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='professor_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"


class Student(models.Model):
    """Model for Student entity"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    major = models.CharField(max_length=100)
    enrollment_year = models.IntegerField()
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='student_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

    def get_gpa(self):
        """Calculate GPA from all enrollments"""
        enrollments = self.enrollment_set.all()
        if not enrollments.exists():
            return 0.0
        total_grade = sum(e.grade for e in enrollments if e.grade)
        return round(total_grade / enrollments.count(), 2)


class Course(models.Model):
    """Model for Course entity"""
    course_code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.CharField(
        max_length=20,
        choices=[
            ('Fall 2024', 'Fall 2024'),
            ('Spring 2025', 'Spring 2025'),
            ('Summer 2025', 'Summer 2025'),
        ]
    )
    max_students = models.IntegerField(default=50)
    syllabus = models.FileField(upload_to='syllabi/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course_code']

    def __str__(self):
        return f"{self.course_code} - {self.title}"

    def get_enrollment_count(self):
        return self.enrollment_set.count()

    def is_full(self):
        return self.get_enrollment_count() >= self.max_students


class Enrollment(models.Model):
    """Join table for Student-Course with grades"""
    GRADE_CHOICES = [
        ('A', 'A (4.0)'),
        ('B', 'B (3.0)'),
        ('C', 'C (2.0)'),
        ('D', 'D (1.0)'),
        ('F', 'F (0.0)'),
        ('Pending', 'Pending'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES, default='Pending')
    enrolled_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')
        ordering = ['-enrolled_date']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.course_code}"
