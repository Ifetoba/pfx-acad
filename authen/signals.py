from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from users.models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created: 
        subject = "Welcome to PronixFX Academy!"
        message = f"Hi {instance.full_name}, \n\nWelcome to PronixFX Academy! Get started with your first course today."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list)