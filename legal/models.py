from django.db import models
from users.models import CustomUser

# Create your models here.
class LegalDocument(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    version = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (v{self.version})"
    
class UserConsent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    document = models.ForeignKey(LegalDocument, on_delete=models.CASCADE)
    accepted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} accepted {self.document.title}"
