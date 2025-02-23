# Create your models here.
from django.db import models

class Profile(models.Model):
    
    from django.db import models

class Profile(models.Model):
    
    firstName = models.TextField(blank=False)
    lastName = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)

    image_url = models.URLField(default="https://via.placeholder.com/150", blank=False)
    
    
    def __str__(self):
        return f'{self.firstName} {self.lastName}'