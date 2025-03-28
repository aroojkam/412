from django.urls import path
from .views import (
    ShowAllProfilesView, ShowProfilePageView, CreateProfileView, 
    CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, 
    UpdateStatusMessageView, CreateFriendView, ShowFriendSuggestionsView, 
    ShowNewsFeedView
)
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),
    path('accounts/login/', lambda request: redirect('/mini_fb/login/')), 
    
    # Profile-related URLs
    path('create_profile/', CreateProfileView.as_view(), name="create_profile"),
    path('profile/update/', UpdateProfileView.as_view(), name="update_profile"),
    
    # Friend-related URLs
    path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
    path('profile/news_feed/', ShowNewsFeedView.as_view(), name="news_feed"),
    path('profile/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name="add_friend"),
    
    # Status message URLs
    path('status/create_status/', CreateStatusMessageView.as_view(), name="create_status"),
    path('status/update/<int:pk>/', UpdateStatusMessageView.as_view(), name="update_status"),
    path('status/delete/<int:pk>/', DeleteStatusMessageView.as_view(), name="delete_status"),
]