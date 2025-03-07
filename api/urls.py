from django.urls import path, include
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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

# API Documentation settings
schema_view = get_schema_view(
    openapi.Info(
        title="PFX Academy API",
        default_version="v1",
        description="API documentation for PronixFX Academy",
        terms_of_service="https://www.pronixfx.com/legal/terms/", # Project's term of service page
        contact=openapi.Contact(email="contact@pronixfx.com"), # Contact details for project
    ),
    public=True
)

router = routers.DefaultRouter()

urlpatterns = [
    path("api/", include(router.urls)),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),

    # Token API
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

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