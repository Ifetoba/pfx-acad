from django.urls import path
from .views import (
    UserProfileAPIView, 
    UserProfileDetailAPIView,
    CourseListAPIView,
    CourseDetailAPIView,
    EnrollCourseAPIView,
    CourseProgressAPIView,
    OrderAPIView,
    WebinarListAPIView,
    WebinarDetailAPIView,
    WebinarRegistrationAPIView,
)

urlpatterns = [
    # User API
    path('profile/', UserProfileAPIView.as_view(), name='api-profile'),
    path('profile/detail/', UserProfileDetailAPIView.as_view(), name='api-profile-detail'),
    
    # Course APIs
    path('courses/', CourseListAPIView.as_view(), name='api-course-list'),
    path('courses/<int:pk>', CourseDetailAPIView.as_view(), name='api-course-detail'),
    path('courses/enroll', EnrollCourseAPIView.as_view(), name='api-enroll-course'),
    path('course/<int:course_id>/progress/', CourseProgressAPIView.as_view(), name='api-course-progress'),
    
    # Payment APIs
    path('orders/', OrderAPIView.as_view(), name='api-orders'),
    
    # Webinars APIs
    path('webinars/', WebinarListAPIView.as_view(), name='api-webinars'),
    path('webinars/<int:pk>/', WebinarDetailAPIView.as_view(), name='api-webinar-detail'),
    path('webinars/register', WebinarRegistrationAPIView.as_view(), name='api-webinar-register'),
]