from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from users.models import CustomUser

# @receiver(post_save, sender=CustomUser)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created: 
#         subject = "Welcome to PronixFX Academy!"
#         message = f"Hi {instance.full_name}, \n\nWelcome to PronixFX Academy! Get started with your first course today."
#         from_email = settings.DEFAULT_FROM_EMAIL
#         recipient_list = [instance.email]

#         send_mail(subject, message, from_email, recipient_list)

def send_welcome_email(user):
    subject = "Welcome to PronixFX Academy"
    from_email = "noreply@yourdomain.com"
    recipient_list = [user.email]

    html_content = render_to_string("emails/welcome_email.html", {"user": user})
    email = EmailMultiAlternatives(subject, body="Welcome", from_email=from_email, to=recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send