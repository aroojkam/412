# signals.py - Auto-creates a Profile whenever a new User is created
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# Signal handler to create or update a user profile
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a profile for the new user
        Profile.objects.create(user=instance)
    else:
        # Save existing profile on user update
        instance.profile.save()
