from django.views.generic import ListView, DetailView
from .models import Profile

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):

    model = Profile
    template_name = "mini_fb/show_profile.html"