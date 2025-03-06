from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage, StatusImage, Image

admin.site.register(Profile)
admin.site.register(StatusMessage)

admin.site.register(StatusImage)
admin.site.register(Image)
