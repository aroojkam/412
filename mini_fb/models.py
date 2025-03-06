"""
models.py - Defines database models for MiniFB application.
This includes Profile, StatusMessage, Image, and StatusImage models.
"""
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """Model representing a user profile."""
    firstName = models.TextField(blank=False)
    lastName = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)

    image_url = models.URLField(default="https://via.placeholder.com/150", blank=False)

    
    
    def __str__(self):
        """String representation of the Profile model."""
        return f'{self.firstName} {self.lastName}'
    
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

