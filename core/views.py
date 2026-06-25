from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages

from .models import Professor, Student, Course, Enrollment
from .forms import (ProfessorForm, StudentForm, CourseForm, EnrollmentForm, 
                    SearchForm, CourseEnrollmentForm, UserForm)


# ==================== HOME & DASHBOARD ====================

def home(request):
    """Home page"""
    context = {
        'total_professors': Professor.objects.count(),
        'total_students': Student.objects.count(),
        'total_courses': Course.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
    }
    return render(request, 'core/home.html', context)


@login_required
def dashboard(request):
    """User dashboard"""
    try:
        professor = Professor.objects.get(user=request.user)
        context = {
            'user_type': 'professor',
            'professor': professor,
            'courses': professor.course_set.all(),
        }
        return render(request, 'core/dashboard_professor.html', context)
    except Professor.DoesNotExist:
        pass
    
    try:
        student = Student.objects.get(user=request.user)
        context = {
            'user_type': 'student',
            'student': student,
            'enrollments': student.enrollment_set.all(),
        }
        return render(request, 'core/dashboard_student.html', context)
    except Student.DoesNotExist:
        pass
    
    return render(request, 'core/dashboard.html')


# ==================== PROFESSOR CRUD ====================

class ProfessorListView(LoginRequiredMixin, ListView):
    model = Professor
    template_name = 'core/professor_list.html'
    context_object_name = 'professors'
    paginate_by = 10

    def get_queryset(self):
        queryset = Professor.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(employee_id__icontains=search) |
                Q(department__icontains=search)
            )
        return queryset.select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class ProfessorDetailView(LoginRequiredMixin, DetailView):
    model = Professor
    template_name = 'core/professor_detail.html'
    context_object_name = 'professor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = self.object.course_set.all()
        return context


class ProfessorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Professor
    form_class = ProfessorForm
    template_name = 'core/professor_form.html'
    success_url = reverse_lazy('professor_list')

    def test_func(self):
        return self.request.user.is_staff

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user if hasattr(self.request.user, 'professor') else None
        return kwargs

    def form_valid(self, form):
        if not form.user:
            username = form.cleaned_data['email'].split('@')[0]
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': form.cleaned_data['email'],
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                }
            )
            form.user = user
        
        messages.success(self.request, 'Professor created successfully!')
        return super().form_valid(form)


class ProfessorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Professor
    form_class = ProfessorForm
    template_name = 'core/professor_form.html'
    success_url = reverse_lazy('professor_list')

    def test_func(self):
        return self.request.user.is_staff or self.request.user == self.get_object().user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Professor updated successfully!')
        return super().form_valid(form)


class ProfessorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Professor
    template_name = 'core/professor_confirm_delete.html'
    success_url = reverse_lazy('professor_list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Professor deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==================== STUDENT CRUD ====================

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'core/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        queryset = Student.objects.all()
        search = self.request.GET.get('search')
        course_id = self.request.GET.get('course')
        professor_id = self.request.GET.get('professor')

        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(student_id__icontains=search)
            )
        
        if course_id:
            queryset = queryset.filter(enrollment__course_id=course_id).distinct()
        
        if professor_id:
            queryset = queryset.filter(enrollment__course__professor_id=professor_id).distinct()

        return queryset.select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['courses'] = Course.objects.all()
        context['professors'] = Professor.objects.all()
        return context


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'core/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = self.object.enrollment_set.all()
        context['gpa'] = self.object.get_gpa()
        return context


class StudentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'core/student_form.html'
    success_url = reverse_lazy('student_list')

    def test_func(self):
        return self.request.user.is_staff

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = None
        return kwargs

    def form_valid(self, form):
        username = form.cleaned_data['email'].split('@')[0]
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': form.cleaned_data['email'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
            }
        )
        form.user = user
        messages.success(self.request, 'Student created successfully!')
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'core/student_form.html'
    success_url = reverse_lazy('student_list')

    def test_func(self):
        return self.request.user.is_staff or self.request.user == self.get_object().user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.object.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Student updated successfully!')
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Student
    template_name = 'core/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Student deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==================== COURSE CRUD ====================

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'core/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        queryset = Course.objects.all()
        search = self.request.GET.get('search')
        semester = self.request.GET.get('semester')

        if search:
            queryset = queryset.filter(
                Q(course_code__icontains=search) |
                Q(title__icontains=search)
            )
        
        if semester:
            queryset = queryset.filter(semester=semester)

        return queryset.select_related('professor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['semesters'] = Course.objects.values_list('semester', flat=True).distinct()
        return context


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'core/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = self.object.enrollment_set.all()
        context['student_count'] = self.object.get_enrollment_count()
        return context


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'core/course_form.html'
    success_url = reverse_lazy('course_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Course created successfully!')
        return super().form_valid(form)


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'core/course_form.html'
    success_url = reverse_lazy('course_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully!')
        return super().form_valid(form)


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    template_name = 'core/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Course deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==================== ENROLLMENT CRUD ====================

class EnrollmentListView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'core/enrollment_list.html'
    context_object_name = 'enrollments'
    paginate_by = 20

    def get_queryset(self):
        queryset = Enrollment.objects.all()
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                Q(student__user__first_name__icontains=search) |
                Q(student__user__last_name__icontains=search) |
                Q(course__course_code__icontains=search)
            )

        return queryset.select_related('student', 'course')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class EnrollmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'core/enrollment_form.html'
    success_url = reverse_lazy('enrollment_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        course = form.cleaned_data['course']
        if course.is_full():
            messages.error(self.request, f'Course {course.course_code} is at maximum capacity!')
            return self.form_invalid(form)
        
        messages.success(self.request, 'Student enrolled successfully!')
        return super().form_valid(form)


class EnrollmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'core/enrollment_form.html'
    success_url = reverse_lazy('enrollment_list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Enrollment updated successfully!')
        return super().form_valid(form)


class EnrollmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Enrollment
    template_name = 'core/enrollment_confirm_delete.html'
    success_url = reverse_lazy('enrollment_list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Enrollment deleted successfully!')
        return super().delete(request, *args, **kwargs)
