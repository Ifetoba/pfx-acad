from .models import CourseEnrollment

def user_courses(request):
    if request.user.is_authenticated:
        return {
            'user_enrolled_courses': CourseEnrollment.objects.filter(
                user=request.user
            ).select_related('course'),
            'user_active_courses': CourseEnrollment.objects.filter(
                user=request.user,
                progress__lt=100
            ).select_related('course')
        }
    return {}