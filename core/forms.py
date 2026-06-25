from django import forms
from django.contrib.auth.models import User
from .models import Professor, Student, Course, Enrollment

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password != password_confirm:
            raise forms.ValidationError("Passwords don't match!")
        return cleaned_data


class ProfessorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField()

    class Meta:
        model = Professor
        fields = ['employee_id', 'department', 'phone', 'office_location', 'profile_picture', 'bio']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        
        professor = super().save(commit=False)
        professor.user = self.user
        if commit:
            professor.save()
        return professor


class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = ['student_id', 'major', 'enrollment_year', 'phone', 'profile_picture', 'bio']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        
        student = super().save(commit=False)
        student.user = self.user
        if commit:
            student.save()
        return student


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_code', 'title', 'description', 'credits', 'professor', 'semester', 'max_students', 'syllabus']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'course_code': forms.TextInput(attrs={'placeholder': 'e.g., CS101'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Introduction to Programming'}),
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'grade']


class CourseEnrollmentForm(forms.ModelForm):
    """Simplified enrollment form - student selects courses"""
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Courses to Enroll"
    )

    class Meta:
        model = Enrollment
        fields = []

    def save(self, student, commit=True):
        courses = self.cleaned_data.get('courses', [])
        enrollments = []
        for course in courses:
            enrollment, created = Enrollment.objects.get_or_create(
                student=student,
                course=course
            )
            enrollments.append(enrollment)
        return enrollments


class SearchForm(forms.Form):
    """Search form for filtering students, courses, professors"""
    SEARCH_CHOICES = [
        ('all', 'All'),
        ('student', 'By Student'),
        ('course', 'By Course'),
        ('professor', 'By Professor'),
    ]
    
    search_type = forms.ChoiceField(choices=SEARCH_CHOICES, widget=forms.RadioSelect)
    query = forms.CharField(max_length=100, required=False)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=False)
    professor = forms.ModelChoiceField(queryset=Professor.objects.all(), required=False)
