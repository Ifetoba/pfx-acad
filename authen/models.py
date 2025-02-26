import uuid
from django.db import models
from users.models import CustomUser

# Create your models here.

class EmailVerificationToken(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="email_token")
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verification token for {self.user.email}"
