from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    location = models.TextField()
    hours = models.TextField()
    cuisine = models.CharField(max_length=100)
    dietary_options = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    image = models.URLField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurants')


    def __str__(self):
        return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100, default='')
    location = models.TextField(blank=True)
    profile_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    @property
    def owned_lists(self):
        return self.user.owned_lists.all()

    @property
    def shared_lists(self):
        return self.user.shared_lists.all()


class List(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_lists')
    description = models.TextField()
    users_shared_with = models.ManyToManyField(User, related_name='shared_lists')

    def __str__(self):
        return self.name
    

class ListItem(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.restaurant.name} in {self.list.name}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review_text = models.TextField()
    date_posted = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.restaurant.name}"
