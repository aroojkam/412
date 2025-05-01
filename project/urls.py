# urls.py
# This file maps URL patterns to corresponding views across the app.
# It includes paths for user authentication, profile handling,
# restaurant CRUD operations, list management, and shared views.
# All route names are defined with the `name` parameter for use in templates and redirects.



from django.urls import path
from . import views
from .views import (
    RestaurantListView, restaurant_detail, RestaurantCreateView,
    profile_view, list_detail, list_create,
    signup_view, login_view, logout_view,
    edit_profile, edit_list, share_list, delete_list, user_list_view
)

urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurant/<int:pk>/', restaurant_detail, name='restaurant-detail'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit-profile'), 
    path('list/add/', list_create, name='list-add'),
    path('list/<int:pk>/', list_detail, name='list-detail'),
    path('list/<int:pk>/edit/', edit_list, name='edit-list'),
    path('list/<int:pk>/delete/', delete_list, name='delete-list'),
    path('list/<int:pk>/share/', share_list, name='share-list'),
    path("user/<int:user_id>/", views.public_profile, name="public-profile"),
    path('restaurant/<int:pk>/edit/', views.edit_restaurant, name='restaurant-edit'),
    path("restaurant/add/", RestaurantCreateView.as_view(), name="restaurant-add"),
    path("users/", user_list_view, name="user-list"),
]
