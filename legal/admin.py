from django.contrib import admin
from .models import LegalDocument, UserConsent

# Register your models here.

admin.site.register(LegalDocument)
admin.site.register(UserConsent)