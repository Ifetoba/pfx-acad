from .models import EmailVerificationToken
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView)

# Create your views here.
def verify_email(request, token):
    try:
        verification_token = EmailVerificationToken.object.get(token=token)
        user = verification_token.user
        user.is_active = True
        user.save()
        verification_token.delete()
        messages.success(request, "Email verified successfully. Continue to access platform.")
    except EmailVerificationToken.DoesNotExist:
        messages.error(request, "Invalid or expired token.")
    return redirect("users:signin")
