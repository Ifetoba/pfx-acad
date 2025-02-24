from django.http import HttpResponseForbidden

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin():
            return HttpResponseForbidden("Access denied: Admins Only")
        return view_func(request, *args, **kwargs)
    return wrapper

def instructor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_instructor():
            return HttpResponseForbidden("Access denied: Instructors only")
        return view_func(request, *args, **kwargs)
    return wrapper