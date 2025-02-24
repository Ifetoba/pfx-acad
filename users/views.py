from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .decorators import admin_required, instructor_required
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm
from courses.models import Course, CourseEnrollment, Order

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user) # Create an empty profile for new users
            login(request, user)
            return redirect('users:profile')
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request=request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('users:profile')
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form":form})

@login_required
def logout(request):
    logout(request=request)
    return redirect("users:signout")

@login_required
def profile(request):
    return render(request, "users/profile.html", {"profile": request.user.profile})



@login_required
@admin_required
def admin_dashboard(request):
    total_courses = Course.objects.count()
    total_students = CourseEnrollment.objects.values('user').distinct().count()
    total_revenue = Order.objects.filter(is_paid=True).aggregate(total=models.Sum('amount'))['total'] or 0

    context = {
        "total_courses": total_courses,
        "total_students": total_students,
        "total_revenue": total_revenue,
    }

    return render(request, "users/admin_dashboard.html", context=context)

@login_required
@instructor_required
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)
    student_count = CourseEnrollment.objects.filter(course__in=courses).values('user').distinct().count()

    context = {
        "courses": courses,
        "student_count": student_count,
    }
    return render(request, "users/instructor_dashboard.html", context=context)