# Create your models here.
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    
    firstName = models.TextField(blank=False)
    lastName = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)

    image_url = models.URLField(default="https://via.placeholder.com/150", blank=False)
    
    
    def __str__(self):
        return f'{self.firstName} {self.lastName}'
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk}) 


    def get_status_messages(self):
        '''Return all of the status messages about this profile.'''
        #filter StatusMessage objects by their profile (foreign key), and order them by timestamp

        messages = StatusMessage.objects.filter(profile=self)
        return messages

    
class StatusMessage (models.Model):

    statusMessage = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.statusMessage}'