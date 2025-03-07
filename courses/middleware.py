from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from .models import CourseEnrollment

class EnrollmentRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if not hasattr(view_func, 'view_class'):
            return None

        view_class = view_func.view_class

        # Check if view requires enrollment
        if hasattr(view_class, 'requires_enrollment') and view_class.requires_enrollment:
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this content.")
                return redirect(reverse('login'))

            course_slug = view_kwargs.get('course_slug')
            if course_slug:
                is_enrolled = CourseEnrollment.objects.filter(
                    user=request.user,
                    course__slug=course_slug
                ).exists()

                if not is_enrolled:
                    messages.error(
                        request, 
                        "You must be enrolled in this course to access its content."
                    )
                    return redirect('courses:course-detail', slug=course_slug)

        return None