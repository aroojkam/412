from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Restaurant, Profile, List, ListItem, Review

admin.site.register(Restaurant)
admin.site.register(Profile)
admin.site.register(List)
admin.site.register(ListItem)
admin.site.register(Review)
