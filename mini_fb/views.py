"""
views.py - Defines the views for MiniFB application.
This includes Profile, StatusMessage, and Image upload handling.
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm  
from .models import Profile, StatusMessage, Image, StatusImage
from django.urls import reverse 

from django.views.generic.edit import CreateView
from django.views import View


class ShowAllProfilesView(ListView):
    """View to display all user profiles."""
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    """View to display a specific user's profile."""
    model = Profile
    template_name = "mini_fb/show_profile.html"

class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Profile object (POST)
    '''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"


class CreateStatusMessageView(CreateView):
    """View to handle creating a status message with an optional image upload."""
    model = StatusMessage
    fields = ['statusMessage']
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        """Add profile data to the template context."""
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """Handle form submission for status messages with images."""
        sm = form.save(commit=False)
        sm.profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        sm.save()

        # Save associated images
        files = self.request.FILES.getlist('files')
        for file in files:
            if file:  # Ensure the file is not empty
                image = Image(profile_fk=sm.profile, image_file=file)
                image.save()
                StatusImage.objects.create(image_fk=image, StatusMessage_fk=sm)

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the profile page after submitting a status message."""
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})

    
class UpdateProfileView(UpdateView):
    """View to handle updating a profile."""
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_success_url(self):
        """Redirect to the profile page after submitting the update."""
        return reverse('show_profile', kwargs={'pk': self.object.pk})

    
class DeleteStatusMessageView(DeleteView):
    """View to handle deleting a status message."""
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status_message"

    def get_success_url(self):
        """Redirect to the profile page after submitting a delete."""
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    

class UpdateStatusMessageView(UpdateView):
    """View to handle updating a status message"""
    model = StatusMessage
    fields = ['statusMessage']
    template_name = "mini_fb/update_status_form.html"

    def get_success_url(self):
        """Redirect to the profile page after submitting an update."""
        print(f"DEBUG: Profile PK = {self.object.profile.pk}")  # Debugging
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


class CreateFriendView(View):
    """View to handle adding a friend."""

    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])
        profile.add_friend(other_profile)
        return redirect(reverse('show_profile', kwargs={'pk': profile.pk}))
    

class ShowFriendSuggestionsView(DetailView):
    """View to show friend suggestions."""
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context
    

class ShowNewsFeedView(DetailView):
    """View to show the news feed for a profile."""
    model = Profile
    template_name = "mini_fb/news_feed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.object.get_news_feed()
        return context