from django.views.generic import ListView, DetailView, CreateView
from .models import Profile
from django.shortcuts import render
from .forms import CreateProfileForm, CreateStatusMessageForm  
from django.urls import reverse  



class ShowAllProfilesView(ListView):
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):

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
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        status_message = form.save(commit=False)
        status_message.profile = Profile.objects.get(pk=self.kwargs['pk'])
        status_message.save()
        return super().form_valid(form)

    def get_success_url(self):  
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})
    
