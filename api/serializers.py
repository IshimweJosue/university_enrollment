from rest_framework import serializers
from core.models import Professor, Student, Course, Enrollment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    courses_count = serializers.SerializerMethodField()

    class Meta:
        model = Professor
        fields = ['id', 'user', 'employee_id', 'department', 'phone', 'office_location', 'bio', 'courses_count']

    def get_courses_count(self, obj):
        return obj.course_set.count()


class CourseListSerializer(serializers.ModelSerializer):
    professor_name = serializers.CharField(source='professor.user.get_full_name', read_only=True)
    enrollment_count = serializers.SerializerMethodField()
    is_full = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'course_code', 'title', 'credits', 'professor_name', 'semester', 'enrollment_count', 'is_full']

    def get_enrollment_count(self, obj):
        return obj.get_enrollment_count()

    def get_is_full(self, obj):
        return obj.is_full()


class CourseDetailSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer(read_only=True)
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'course_code', 'title', 'description', 'credits', 'professor', 'semester', 'max_students', 'students_count', 'syllabus']

    def get_students_count(self, obj):
        return obj.get_enrollment_count()


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    course_code = serializers.CharField(source='course.course_code', read_only=True)
    professor_name = serializers.CharField(source='course.professor.user.get_full_name', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'course', 'course_code', 'professor_name', 'grade', 'enrolled_date']
        read_only_fields = ['enrolled_date']


class StudentListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    enrollments_count = serializers.SerializerMethodField()
    gpa = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'user', 'student_id', 'major', 'enrollment_year', 'enrollments_count', 'gpa']

    def get_enrollments_count(self, obj):
        return obj.enrollment_set.count()

    def get_gpa(self, obj):
        return obj.get_gpa()


class StudentDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    gpa = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'user', 'student_id', 'major', 'enrollment_year', 'phone', 'bio', 'gpa']

    def get_gpa(self, obj):
        return obj.get_gpa()


class StudentGradeReportSerializer(serializers.ModelSerializer):
    """Serializer for student grade report"""
    user = UserSerializer(read_only=True)
    courses = serializers.SerializerMethodField()
    gpa = serializers.SerializerMethodField()
    total_credits = serializers.SerializerMethodField()
    total_credits_earned = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'user', 'student_id', 'major', 'enrollment_year', 'gpa', 'courses', 'total_credits', 'total_credits_earned']

    def get_courses(self, obj):
        enrollments = obj.enrollment_set.all()
        course_data = []
        for enrollment in enrollments:
            course_data.append({
                'course_code': enrollment.course.course_code,
                'title': enrollment.course.title,
                'credits': enrollment.course.credits,
                'professor': enrollment.course.professor.user.get_full_name() if enrollment.course.professor else 'Unassigned',
                'grade': enrollment.grade,
                'grade_value': enrollment.get_grade_value(),
            })
        return course_data

    def get_gpa(self, obj):
        return obj.get_gpa()

    def get_total_credits(self, obj):
        return sum(e.course.credits for e in obj.enrollment_set.all())

    def get_total_credits_earned(self, obj):
        return sum(
            e.course.credits for e in obj.enrollment_set.all() 
            if e.grade != 'F' and e.grade != 'Pending'
        )


class CourseStudentsSerializer(serializers.ModelSerializer):
    """Serializer for course with enrolled students"""
    professor = ProfessorSerializer(read_only=True)
    enrolled_students = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'course_code', 'title', 'description', 'credits', 'professor', 'semester', 'max_students', 'enrolled_students']

    def get_enrolled_students(self, obj):
        enrollments = obj.enrollment_set.all()
        students_data = []
        for enrollment in enrollments:
            students_data.append({
                'id': enrollment.student.id,
                'name': enrollment.student.user.get_full_name(),
                'student_id': enrollment.student.student_id,
                'major': enrollment.student.major,
                'grade': enrollment.grade,
                'enrolled_date': enrollment.enrolled_date,
            })
        return students_data
