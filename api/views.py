from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import generics, permissions
from users.models import CustomUser, UserProfile
from courses.models import (Course, 
     CourseEnrollment, 
    Order, 
    Lesson, 
    CourseProgress, 
    Certificate, 
    Webinar, 
    WebinarRegistration,
)
from .serializers import (UserSerializer, 
                          UserProfileSerializer,
                          CourseSerializer, 
                          EnrollmentSerializer, 
                          LessonSerializer,
                          CourseProgressSerializer, 
                          CertificateSerializer,
                          OrderSerializer,
                          WebinarSerializer,
                          WebinarRegistrationSerializer)

# Create your views here.
class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class EnrollCourseAPIView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CourseProgressAPIView(generics.RetrieveAPIView):
    queryset = CourseProgress.objects.all()
    serializer_class = CourseProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return CourseProgress.objects.get(user=self.request.user, course_id=self.kwargs["course_id"])

class CertificateListAPIView(generics.ListAPIView):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(user=self.request.user)

class OrderAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
class WebinarListAPIView(generics.ListAPIView):
    queryset = Webinar.objects.filter(date__gte=now()).order_by("date")
    serializer_class = WebinarSerializer

class WebinarDetailAPIView(generics.RetrieveAPIView):
    queryset = Webinar.objects.all()
    serializer_class = WebinarSerializer

class WebinarRegistrationAPIView(generics.CreateAPIView):
    serializer_class = WebinarRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

