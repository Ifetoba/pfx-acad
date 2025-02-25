import uuid
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.generic import ListView, DetailView
from .models import (
    Course,
    Lesson,
    CourseEnrollment,
    CourseProgress,
    Certificate,
    Webinar,
    WebinarRegistration,)

# Create your views here.
class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"

class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = CourseEnrollment.objects.get_or_create(user=request.user, course=course) 

    if created:
        CourseProgress.objects.create(user=request.user, course=course)
        message = "Successfull enrolled!"
    else:
        message = "Already enrolled"

    return render(request, 
                  "courses/enrollment_success.html", 
                  {"course": course, "message": message}
                  )

@login_required
def complete_lesson(request, course_id, lesson_id):
    progress = get_object_or_404(CourseProgress, user=request.user, course_id=course_id)
    lesson = get_object_or_404(Lesson, pk=lesson_id, course_id=course_id)

    if lesson not in progress.completed_lessons.all():
        progress.completed_lessons.add(lesson)
        progress.update_progress()

        if progress.progress == 100:
            Certificate.objects.create(user=request.user, course_id=course_id, certificate_id_four=str(uuid.uuid4()))
    return JsonResponse({
        "progress": progress.progress,
        "completed": list(progress.completed_lessons.values("id", "title"))
    })

@login_required
def register_for_webinar(request, webinar_id):
    webinar = get_object_or_404(Webinar, id=webinar_id)

    if webinar.registration_deadline < now():
        return JsonResponse({"error": "Registration closed"}, status=400)
    
    registration, created = WebinarRegistration.objects.get_or_create(user=request.user, webinar=webinar)

    if created:
        return JsonResponse({"message": "Registered successfully!"})
    return JsonResponse({"message": "Already registered."})