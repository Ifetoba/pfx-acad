from django.urls import path
from . import views

app_name = "courses"

# urlpatterns = [
# path("", CourseListView.as_view(), name="course-list"),
# path("<int:pk>/", CourseDetailView.as_view(), name="course-detail"),
# path("<int:course_id>/enroll/", enroll_course, name="enroll-course"),   
# path("<int:course_id>/lessons/<int:lesson_id>/complete/", complete_lesson, name="complete-lesson"),   
# path("webinars/<int:webinar_id>/register/", register_for_webinar, name="register-webinar"),   
# ]

# from django.urls import path
# from . import views

# app_name = 'courses'

# urlpatterns = [
#     path('', views.CourseListView.as_view(), name='course-list'),
#     path('course/<slug:slug>/', views.CourseDetailView.as_view(), name='course-detail'),
#     path('course/<slug:course_slug>/module/<int:module_order>/', 
#          views.module_detail, name='module-detail'),
#     path('course/<slug:course_slug>/module/<int:module_order>/lesson/<int:lesson_order>/',
#          views.lesson_detail, name='lesson-detail'),
#     path('enroll/<int:course_id>/', views.enroll_course, name='enroll-course'),
#     path('complete-lesson/<slug:course_slug>/<int:module_order>/<int:lesson_order>/',
#          views.complete_lesson, name='complete-lesson'),
    
#     # Webinar URLs
#     path('webinar/<int:webinar_id>/register/',
#          views.register_for_webinar, name='register-webinar'),
# ]

# courses/urls.py
from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Course URLs
    path('', views.CourseListView.as_view(), name='course-list'),
    path('course/<slug:slug>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('course/<slug:course_slug>/module/<int:module_order>/', 
         views.ModuleDetailView.as_view(), name='module-detail'),
    path('course/<slug:course_slug>/module/<int:module_order>/lesson/<int:lesson_order>/',
         views.LessonDetailView.as_view(), name='lesson-detail'),
    
    # Enrollment and Progress URLs
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll-course'),
    path('complete-lesson/<slug:course_slug>/<int:module_order>/<int:lesson_order>/',
         views.complete_lesson, name='complete-lesson'),
    path('my-courses/', views.ProgressDashboardView.as_view(), name='progress-dashboard'),
    
    # Certificate URLs
    path('certificate/<uuid:certificate_id>/', 
         views.CertificateDetailView.as_view(), name='certificate-detail'),
    path('verify-certificate/<uuid:certificate_id>/',
         views.verify_certificate, name='verify-certificate'),
]