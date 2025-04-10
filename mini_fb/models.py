"""
models.py - Defines database models for MiniFB application.
This includes Profile, StatusMessage, Image, and StatusImage models.
"""
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=True, blank=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    image_url = models.URLField(default="https://via.placeholder.com/150", blank=True)
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    
    def get_friends(self):
        """Get all friends of this profile."""
        return self.friends.all()
    
    def get_news_feed(self):
        """Retrieve status messages from friends, ordered by most recent."""
        friend_ids = [friend.id for friend in self.friends.all()] + [self.id]
        return StatusMessage.objects.filter(profile_id__in=friend_ids).order_by('-published')
    
    def get_absolute_url(self):
        """Return the URL to the profile page."""
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_status_messages(self):
        """Return all status messages posted by this profile."""
        return StatusMessage.objects.filter(profile=self).order_by('-published')
    
    def get_friend_suggestions(self):
        """Suggest potential friends who are not yet friends with this profile."""
        return Profile.objects.exclude(id=self.id).exclude(id__in=[friend.id for friend in self.friends.all()])

    def add_friend(self, other):
        """Add a new friend relationship if it does not already exist."""
        if self == other:
            return  # Prevent self-friending

        # Check if friendship already exists
        existing_friendship = Friend.objects.filter(
            (models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self))
        ).exists()

        if not existing_friendship:
            Friend.objects.create(profile1=self, profile2=other)

@receiver(post_save, sender=User)
def create_or_save_profile(sender, instance, created, **kwargs):
    """Create or update a Profile whenever a User is created."""
    if created:
        Profile.objects.create(user=instance)
    else:
        # Save the profile if it already exists
        if hasattr(instance, 'profile'):
            instance.profile.save()


    
class StatusMessage(models.Model):
    """Model representing a status message posted by a user."""
    statusMessage = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def get_images(self):
        """Retrieve all images associated with this status message."""
        return Image.objects.filter(statusimage__StatusMessage_fk=self)
    
    

class Image(models.Model):
    """Model representing an uploaded image."""
    profile_fk = models.ForeignKey("Profile", on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='status_images/', blank=True)
    time_stamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)  # Caption should be optional


class StatusImage(models.Model):
    """Model linking an Image to a StatusMessage (many-to-many relationship)."""
    image_fk = models.ForeignKey("Image", on_delete=models.CASCADE)
    StatusMessage_fk = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)


class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.profile1.firstName} {self.profile1.lastName} & {self.profile2.firstName} {self.profile2.lastName}"

