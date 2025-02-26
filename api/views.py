from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth import get_user_model
from users.models import CustomUser, UserProfile
from authen.models import EmailVerificationToken
from courses.models import (Course, 
     CourseEnrollment, 
    Order, 
    Lesson, 
    CourseProgress, 
    Certificate, 
    Webinar, 
    WebinarRegistration,
)
from api.serializers import (UserSerializer, 
                          UserProfileSerializer,
                          CourseSerializer, 
                          EnrollmentSerializer, 
                          LessonSerializer,
                          CourseProgressSerializer, 
                          CertificateSerializer,
                          OrderSerializer,
                          WebinarSerializer,
                          WebinarRegistrationSerializer)
from .permissions import IsAdmin, IsInstructor

# Create your views here.
class SendVerificationEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.email_token.exists():
            return Response({
                "message": "Verification email already sent."
            },
            status=400
            )
        token = EmailVerificationToken.objects.create(user=user)
        verification_link = f"{settings.FRONTEND_URL}/verify-email/{token.token}"
        send_mail(
            "verify Your Email",
            f"Click the link to verify your email:{verification_link}",
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
        return Response({"message": "Verification email sent."})
    
class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = get_user_model().objects.filter(email=email).first()
        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}"
            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_link}",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        return Response({"message": "If an account exists, a password reset link has been sent."})

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

