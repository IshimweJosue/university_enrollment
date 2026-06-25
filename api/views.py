from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from core.models import Professor, Student, Course, Enrollment
from .serializers import (
    ProfessorSerializer, StudentListSerializer, StudentDetailSerializer,
    StudentGradeReportSerializer, CourseListSerializer, CourseDetailSerializer,
    CourseStudentsSerializer, EnrollmentSerializer
)


class ProfessorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Professor CRUD operations.
    
    List: GET /api/professors/
    Create: POST /api/professors/
    Retrieve: GET /api/professors/{id}/
    Update: PUT /api/professors/{id}/
    Delete: DELETE /api/professors/{id}/
    """
    queryset = Professor.objects.all().select_related('user')
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'employee_id', 'department']
    ordering_fields = ['user__last_name', 'department']
    ordering = ['user__last_name']


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Student CRUD operations.
    
    List: GET /api/students/
    Create: POST /api/students/
    Retrieve: GET /api/students/{id}/
    Update: PUT /api/students/{id}/
    Delete: DELETE /api/students/{id}/
    Grade Report: GET /api/students/{id}/grade_report/
    """
    queryset = Student.objects.all().select_related('user')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__first_name', 'user__last_name', 'student_id', 'major']
    ordering_fields = ['user__last_name', 'major', 'enrollment_year']
    ordering = ['user__last_name']
    filterset_fields = ['major', 'enrollment_year']

    def get_serializer_class(self):
        if self.action == 'grade_report':
            return StudentGradeReportSerializer
        elif self.action == 'retrieve':
            return StudentDetailSerializer
        return StudentListSerializer

    @action(detail=True, methods=['get'])
    def grade_report(self, request, pk=None):
        """
        Get a student's grade report.
        
        Endpoint: GET /api/students/{id}/grade_report/
        Returns: Student info with all courses, grades, and GPA
        """
        student = self.get_object()
        serializer = self.get_serializer(student)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Course CRUD operations.
    
    List: GET /api/courses/
    Create: POST /api/courses/
    Retrieve: GET /api/courses/{id}/
    Update: PUT /api/courses/{id}/
    Delete: DELETE /api/courses/{id}/
    Students: GET /api/courses/{id}/students/
    """
    queryset = Course.objects.all().select_related('professor', 'professor__user')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['course_code', 'title', 'description']
    ordering_fields = ['course_code', 'credits', 'semester']
    ordering = ['course_code']
    filterset_fields = ['semester', 'professor']

    def get_serializer_class(self):
        if self.action == 'students':
            return CourseStudentsSerializer
        elif self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """
        Get all students enrolled in a course.
        
        Endpoint: GET /api/courses/{id}/students/
        Returns: Course details with enrolled students and grades
        """
        course = self.get_object()
        serializer = self.get_serializer(course)
        return Response(serializer.data)


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Enrollment CRUD operations.
    
    List: GET /api/enrollments/
    Create: POST /api/enrollments/
    Retrieve: GET /api/enrollments/{id}/
    Update: PUT /api/enrollments/{id}/
    Delete: DELETE /api/enrollments/{id}/
    """
    queryset = Enrollment.objects.all().select_related('student', 'student__user', 'course', 'course__professor')
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['student__user__first_name', 'student__user__last_name', 'course__course_code']
    ordering_fields = ['enrolled_date', 'grade', 'course__course_code']
    ordering = ['-enrolled_date']
    filterset_fields = ['course', 'student', 'grade']

    def create(self, request, *args, **kwargs):
        """
        Enroll a student in a course.
        
        POST /api/enrollments/
        Body: {
            "student": 1,
            "course": 1
        }
        """
        course_id = request.data.get('course')
        student_id = request.data.get('student')
        
        try:
            course = Course.objects.get(id=course_id)
            if course.is_full():
                return Response(
                    {'error': f'Course {course.course_code} is at maximum capacity!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Course.DoesNotExist:
            return Response(
                {'error': 'Course not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return super().create(request, *args, **kwargs)
