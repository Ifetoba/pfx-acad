from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser,UserProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal to automatically create a UserProfile whenever a new user is created."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """Signal to save the UserProfile whenever the User instance is saved"""
    instance.profile.save()