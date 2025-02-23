from django.views.generic import ListView, DetailView
from .models import Profile

class ShowAllProfilesView(ListView):
    """View to display all user profiles in a list.
    
    This view retrieves all Profile objects from the database and 
    passes them to the template for display.
    """
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

class ShowProfilePageView(DetailView):
    """View to display a single user profile.
    
    This view retrieves a specific Profile object based on the primary key
    and passes it to the template for detailed display.
    """
    model = Profile
    template_name = "mini_fb/show_profile.html"