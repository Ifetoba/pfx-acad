from django.urls import path
from .views import CourseListView, CourseDetailView, enroll_course, complete_lesson, register_for_webinar

app_name = "courses"

urlpatterns = [
path("", CourseListView.as_view(), name="course-list"),
path("<int:pk>/", CourseDetailView.as_view(), name="course-detail"),
path("<int:course_id>/enroll/", enroll_course, name="enroll-course"),   
path("<int:course_id>/lessons/<int:lesson_id>/complete/", complete_lesson, name="lesson-complete"),   
path("webinars/<int:webinar_id>/register/", register_for_webinar, name="register-webinar"),   
]