from django import forms
from .models import Profile, StatusMessage



class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['firstName', 'lastName', 'city', 'email', 'image_url']

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['statusMessage']