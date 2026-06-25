from django.contrib import admin
from .models import Professor, Student, Course, Enrollment

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'phone')
    search_fields = ('user__first_name', 'user__last_name', 'employee_id')
    list_filter = ('department', 'created_at')
    fieldsets = (
        ('User Info', {'fields': ('user',)}),
        ('Professor Info', {'fields': ('employee_id', 'department', 'office_location')}),
        ('Contact', {'fields': ('phone',)}),
        ('Profile', {'fields': ('profile_picture', 'bio')}),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'major', 'enrollment_year')
    search_fields = ('user__first_name', 'user__last_name', 'student_id')
    list_filter = ('major', 'enrollment_year', 'created_at')
    fieldsets = (
        ('User Info', {'fields': ('user',)}),
        ('Student Info', {'fields': ('student_id', 'major', 'enrollment_year')}),
        ('Contact', {'fields': ('phone',)}),
        ('Profile', {'fields': ('profile_picture', 'bio')}),
    )

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'title', 'professor', 'semester', 'credits', 'max_students')
    search_fields = ('course_code', 'title')
    list_filter = ('semester', 'credits', 'professor')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Course Info', {'fields': ('course_code', 'title', 'description', 'credits')}),
        ('Instructor', {'fields': ('professor',)}),
        ('Schedule', {'fields': ('semester',)}),
        ('Capacity', {'fields': ('max_students',)}),
        ('Files', {'fields': ('syllabus',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'grade', 'enrolled_date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'course__course_code')
    list_filter = ('grade', 'enrolled_date', 'course__semester')
    readonly_fields = ('enrolled_date', 'updated_at')
    fieldsets = (
        ('Enrollment', {'fields': ('student', 'course')}),
        ('Grade', {'fields': ('grade',)}),
        ('Timestamps', {'fields': ('enrolled_date', 'updated_at'), 'classes': ('collapse',)}),
    )
