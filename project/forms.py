from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Restaurant, Review, List, ListItem, Profile, ListItem
from django.db import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'location', 'profile_image'] 

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'location', 'hours', 'cuisine', 'dietary_options', 'rating', 'image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['name', 'description', 'users_shared_with']
        widgets = {
            'users_shared_with': forms.CheckboxSelectMultiple(),  # Optional
        }

    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        self.fields['users_shared_with'].required = False  # ✅ Make optional

class ListItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ['restaurant', 'note']

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AddToListForm(forms.Form):
    list = forms.ModelChoiceField(queryset=List.objects.none())
    note = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Optional note',
        'class': 'form-control'
    }))

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['list'].queryset = List.objects.filter(
                models.Q(user=user) | models.Q(users_shared_with=user)
            ).distinct()


class AddRestaurantForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ['restaurant', 'note']
        widgets = {
            'restaurant': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
        }
