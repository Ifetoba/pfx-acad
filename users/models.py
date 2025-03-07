import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from enum import Enum

# Role Enum and ChoicesS
class RoleENum(Enum):
    STUDENT = "Student"
    INSTRUCTOR = "Instructor"
    ADMIN = "Admin"

ROLE_CHOICES = [(role.name , role.value) for role in RoleENum]

# Create your models here.

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email=email, username=username, password=password, **extra_fields)
    
# Custom Usermodel
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=RoleENum.STUDENT.name)
    is_auth_verified = models.BooleanField(default=False)
    

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def is_admin(self):
        return self.role == RoleENum.ADMIN
    
    def is_instructor(self):
        return self.role == RoleENum.INSTRUCTOR
    
    def get_full_name(self):
        return self.full_name
    
    def get_short_name(self):
        """Returns the first name or full name is no spaces exist."""
        return self.full_name.split(" ")[0] if " " in self.full_name else self.full_name

    def __str__(self):
        return self.email
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, related_name="profile")
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    experience_level = models.CharField(max_length=50, blank=True, null=True) # Beginner, Intermediate, Advanced

    def __str__(self):
        return f"{self.user.email}'s Profile"