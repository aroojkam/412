"""
models.py - Defines database models for MiniFB application.
This includes Profile, StatusMessage, Image, and StatusImage models.
"""
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class Profile(models.Model):
    """Model representing a user profile."""
    firstName = models.TextField(blank=False)
    lastName = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)

    image_url = models.URLField(default="https://via.placeholder.com/150", blank=False)

    def get_friends(self):
        """Retrieve all friends of this Profile."""
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        return [f.profile1 if f.profile2 == self else f.profile2 for f in friends]
    
    def __str__(self):
        """String representation of the Profile model."""
        return f'{self.firstName} {self.lastName}'
    
    def get_friends(self):
        """Retrieve all friends of this Profile."""
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        return [f.profile1 if f.profile2 == self else f.profile2 for f in friends]

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

    def get_friend_suggestions(self):
        """Suggest potential friends who are not yet friends with this profile."""
        all_profiles = Profile.objects.exclude(id=self.id)  # Exclude self
        current_friends = self.get_friends()
        friend_suggestions = all_profiles.exclude(id__in=[friend.id for friend in current_friends])
        return friend_suggestions
    
    def get_absolute_url(self):
        """Returns the URL to view this profile instance."""
        return reverse('show_profile', kwargs={'pk': self.pk}) 


    def get_status_messages(self):
        '''Return all of the status messages about this profile.'''
        #filter StatusMessage objects by their profile (foreign key), and order them by timestamp

        messages = StatusMessage.objects.filter(profile=self)
        return messages

    
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

