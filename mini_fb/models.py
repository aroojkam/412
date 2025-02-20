from django.db import models

# Create your models here.
from django.db import models

class Profile(models.Model):

    # data attributes of a Profile:
    firstName = models.TextField(blank=False)
    lastName = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image = models.ImageField(blank=False) # image url
    
    def __str__(self):
        return f'{self.firstName}'
