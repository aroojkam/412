"""
views.py - Defines the views for MiniFB application.
This includes Profile, StatusMessage, and Image upload handling.
"""

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm  
from .models import Profile, StatusMessage, Image, StatusImage, Friend
from django.urls import reverse 
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.core.exceptions import PermissionDenied


class ShowAllProfilesView(ListView):
    """View to display all user profiles."""
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"


class ShowProfilePageView(DetailView):
    """View to display a specific user's profile."""
    model = Profile
    template_name = "mini_fb/show_profile.html"

    def get_context_data(self, **kwargs):
        """Ensure status messages are included in the template context."""
        context = super().get_context_data(**kwargs)
        context['status_messages'] = self.object.get_status_messages()
        context['is_owner'] = self.request.user == self.object.user
        return context


class CreateProfileView(CreateView):
    """View to create a new user profile with an associated user account."""
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_context_data(self, **kwargs):
        """Add UserCreationForm to the context to display both forms."""
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        """Handle form submission for both user creation and profile creation."""
        user_form = UserCreationForm(self.request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            
            # Check if a profile was automatically created by the signal
            try:
                profile = user.profile
                # Update the existing profile with the form data
                for field in form.cleaned_data:
                    setattr(profile, field, form.cleaned_data[field])
                profile.save()
                self.object = profile
            except Profile.DoesNotExist:
                # Create a new profile if one wasn't created
                form.instance.user = user
                self.object = form.save()
                
            login(self.request, user)
            return redirect(self.get_success_url())
        else:
            # If the user form is invalid, re-render the page with errors
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))

    def get_success_url(self):
        """Redirect to the profile page after creating a profile."""
        return reverse('show_profile', kwargs={'pk': self.object.pk})


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """View to handle updating a profile. Requires login."""
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    login_url = '/mini_fb/login/'

    def get_object(self):
        """Find the profile for the logged-in user."""
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        """Redirect to the profile page after submitting the update."""
        return reverse('show_profile', kwargs={'pk': self.object.pk})


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    """View to handle creating a status message with an optional image upload."""
    model = StatusMessage
    fields = ['statusMessage']
    template_name = "mini_fb/create_status_form.html"
    login_url = '/mini_fb/login/'

    def form_valid(self, form):
        """Ensure the status message is linked to the logged-in user's profile."""
        profile = get_object_or_404(Profile, user=self.request.user)
        form.instance.profile = profile
        sm = form.save()

        # Save associated images
        files = self.request.FILES.getlist('files')
        for file in files:
            if file:  # Ensure the file is not empty
                image = Image(profile_fk=profile, image_file=file)
                image.save()
                StatusImage.objects.create(image_fk=image, StatusMessage_fk=sm)

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the profile page after submitting a status message."""
        return reverse('show_profile', kwargs={'pk': self.request.user.profile.pk})


class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    """View to handle updating a status message."""
    model = StatusMessage
    fields = ['statusMessage']
    template_name = "mini_fb/update_status_form.html"
    login_url = '/mini_fb/login/'

    def get_object(self, queryset=None):
        """Ensure that only the owner of the profile can update the status message."""
        status_message = super().get_object(queryset)
        if status_message.profile.user != self.request.user:
            raise PermissionDenied("You are not allowed to edit this status message.")
        return status_message

    def get_success_url(self):
        """Redirect back to the profile after updating a status message."""
        return reverse('show_profile', kwargs={'pk': self.request.user.profile.pk})


class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    """View to handle deleting a status message."""
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = "status_message"
    login_url = '/mini_fb/login/'

    def get_object(self, queryset=None):
        """Ensure that only the owner of the profile can delete the status message."""
        status_message = super().get_object(queryset)
        if status_message.profile.user != self.request.user:
            raise PermissionDenied("You are not allowed to delete this status message.")
        return status_message

    def get_success_url(self):
        """Redirect to the profile page after submitting a delete."""
        return reverse('show_profile', kwargs={'pk': self.request.user.profile.pk})


class CreateFriendView(LoginRequiredMixin, View):
    """View to handle adding a friend."""
    login_url = '/mini_fb/login/'

    def post(self, request, *args, **kwargs):
        """Ensure that only the profile owner can add friends."""
        profile = get_object_or_404(Profile, user=request.user)
        other_profile = get_object_or_404(Profile, pk=kwargs['other_pk'])

        if profile == other_profile:
            messages.error(request, "You cannot add yourself as a friend.")
            return redirect('show_profile', pk=profile.pk)

        profile.friends.add(other_profile)
        messages.success(request, f"You have added {other_profile.firstName} as a friend.")
        return redirect('show_profile', pk=profile.pk)

    # Legacy method - keep for GET requests or convert them to POST
    def get(self, request, *args, **kwargs):
        """Legacy method to support older links."""
        profile = get_object_or_404(Profile, user=request.user)
        other_profile = get_object_or_404(Profile, pk=kwargs['other_pk'])
        
        profile.friends.add(other_profile)
        return redirect('show_profile', pk=profile.pk)


class ShowFriendSuggestionsView(LoginRequiredMixin, ListView):
    """Only allow profile owners to view friend suggestions."""
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "friend_suggestions"
    login_url = '/mini_fb/login/'

    def get_queryset(self):
        """Fetch friend suggestions for the logged-in user."""
        profile = get_object_or_404(Profile, user=self.request.user)
        return Profile.objects.exclude(id=profile.id).exclude(friends=profile)

    def get_context_data(self, **kwargs):
        """Add profile to the context."""
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user)
        return context


class ShowNewsFeedView(LoginRequiredMixin, ListView):
    """Only allow profile owners to view their news feed."""
    template_name = "mini_fb/news_feed.html"
    context_object_name = "news_feed"
    login_url = '/mini_fb/login/'

    def get_queryset(self):
        """Ensure that only the profile owner can view the news feed."""
        profile = get_object_or_404(Profile, user=self.request.user)
        return StatusMessage.objects.filter(profile__in=profile.friends.all()).order_by('-published')

    def get_context_data(self, **kwargs):
        """Add profile to the context."""
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, user=self.request.user)
        return context