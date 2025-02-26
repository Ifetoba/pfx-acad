from rest_framework import serializers
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

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "role", "date_joined"]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["bio", "profile_picture", "experience_level"]

# Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

# Enrollment Serializer
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = ["user", "course", "enrolled_at"]


# Lesson Serializer
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

# Course Progress Serializer
class CourseProgressSerializer(serializers.ModelSerializer):
    completed_lessons = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CourseProgress
        fields = ["user", "course", "completed_lessons", "progress"]

# Certificate Serializer
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ["user", "course", "issued_at", "certificate_id_four"]

# Payment Serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["user", "course", "amount", "is_paid"]

# Webinar Serializer
class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = "__all__"

# Webinar Registration Serializer
class WebinarRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebinarRegistration
        fields = ["user", "webinar", "registered_at"]