# views.py
# This module contains all view logic for the Django project,
# including user authentication, restaurant management, list
# handling (create, edit, share), user profile access, and
# review and note interaction.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views import View
from django.utils.decorators import method_decorator
from .models import Restaurant, List, ListItem, Review, Profile, List, User
from .forms import RestaurantForm, ReviewForm, ListForm, ListItemForm, SignUpForm, ProfileForm, AddToListForm
from django.core.exceptions import PermissionDenied
from django.db import models
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from django.db.models import Q

# Homepage with restaurant search functionality
class RestaurantListView(ListView):
    model = Restaurant
    template_name = "project/home.html"
    context_object_name = "restaurants"

    # Filter restaurants by search query if provided
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                models.Q(name__icontains=q) |
                models.Q(cuisine__icontains=q) |
                models.Q(location__icontains=q) |
                models.Q(dietary_options__icontains=q)
            )
        return queryset
    
     # Include search query in context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

# Restaurant detail page with review and list interaction
@login_required
@require_http_methods(["GET", "POST"])
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    reviews = Review.objects.filter(restaurant=restaurant)
    review_form = ReviewForm()
    list_form = AddToListForm(user=request.user)

    if request.method == 'POST':
        # Handle Review Submission
        if 'submit_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.restaurant = restaurant
                review.save()
                messages.success(request, "Review submitted!")
                return redirect('restaurant-detail', pk=pk)

        # Handle Add to List
        elif 'submit_list' in request.POST:
            list_form = AddToListForm(request.POST, user=request.user)
            if list_form.is_valid():
                selected_list = list_form.cleaned_data['list']
                note = list_form.cleaned_data['note']

                if ListItem.objects.filter(list=selected_list, restaurant=restaurant).exists():
                    messages.warning(request, "This restaurant is already in that list.")
                else:
                    ListItem.objects.create(list=selected_list, restaurant=restaurant, note=note)
                    messages.success(request, "Restaurant added to list!")

                return redirect('restaurant-detail', pk=pk)


        # Handle Removal from List
        elif 'remove_from_list' in request.POST:
            list_id = request.POST.get("list_id")
            try:
                list_obj = List.objects.get(id=list_id)

                if request.user == list_obj.user or request.user in list_obj.users_shared_with.all():
                    ListItem.objects.filter(list=list_obj, restaurant=restaurant).delete()
                    messages.success(request, "Restaurant removed from the list.")
                else:
                    raise PermissionDenied("You don’t have permission to modify this list.")
            except List.DoesNotExist:
                messages.error(request, "List not found.")
            return redirect('restaurant-detail', pk=pk)

    return render(request, 'project/restaurant_detail.html', {
        'restaurant': restaurant,
        'reviews': reviews,
        'form': review_form,
        'list_form': list_form,
    })

# Restaurant creation view (restricted to logged-in users)
class RestaurantCreateView(LoginRequiredMixin, CreateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = "project/restaurant_form.html"
    success_url = "/project/" 

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

# User profile page showing owned and shared lists
@login_required
def profile_view(request):
    user = request.user
    profile = user.profile
    owned_lists = profile.owned_lists
    shared_lists = profile.shared_lists

    return render(request, "project/profile.html", {
        "user": user,
        "profile": profile,
        "lists": owned_lists,
        "shared_lists": shared_lists
    })

# View details of a specific list
@login_required
def list_detail(request, pk):
    list_obj = get_object_or_404(List, pk=pk)

    # Permission check
    if request.user != list_obj.user and request.user not in list_obj.users_shared_with.all():
        raise PermissionDenied("You do not have permission to access this list.")

    items = ListItem.objects.filter(list=list_obj)
    form = ListItemForm()

    if request.method == "POST":

        # Handle Add Restaurant
        if 'note' in request.POST:
            form = ListItemForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.list = list_obj

                if ListItem.objects.filter(list=list_obj, restaurant=item.restaurant).exists():
                    messages.warning(request, "This restaurant is already in this list.")
                else:
                    item.save()
                    messages.success(request, "Restaurant added to the list.")
            return redirect("list-detail", pk=pk)

        # Handle Remove Restaurant
        elif 'remove_item_id' in request.POST:
            item_id = request.POST.get("remove_item_id")
            item = get_object_or_404(ListItem, id=item_id)
            if item.list.user == request.user or request.user in item.list.users_shared_with.all():
                item.delete()
                messages.success(request, "Restaurant removed from the list.")
            else:
                messages.error(request, "You don't have permission to remove this item.")
            return redirect("list-detail", pk=pk)

        # Handle Edit Note
        elif 'edit_item_id' in request.POST:
            item_id = request.POST.get("edit_item_id")
            new_note = request.POST.get("new_note")
            item = get_object_or_404(ListItem, id=item_id)
            if item.list.user == request.user or request.user in item.list.users_shared_with.all():
                item.note = new_note
                item.save()
                messages.success(request, "Note updated successfully.")
            else:
                messages.error(request, "You don't have permission to edit this note.")
            return redirect("list-detail", pk=pk)

        # Handle Share List
        elif 'user_id' in request.POST:
            user_id = request.POST.get("user_id")
            user_to_share = get_object_or_404(User, pk=user_id)
            if user_to_share != list_obj.user and user_to_share not in list_obj.users_shared_with.all():
                list_obj.users_shared_with.add(user_to_share)
                messages.success(request, f"List shared with {user_to_share.username}.")
            else:
                messages.warning(request, f"This list is already shared with {user_to_share.username}.")
            return redirect("list-detail", pk=pk)

    return render(request, "project/list_detail.html", {
        "list": list_obj,
        "items": items,
        "form": form,
        "all_users": User.objects.exclude(id=request.user.id),  # Exclude current user from share options
    })

# View to handle creation of a new list
@login_required
def list_create(request):
    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.user = request.user # Assign current user as owner
            new_list.save()
            form.save_m2m()
            return redirect("profile")
    else:
        form = ListForm()
    return render(request, "project/list_form.html", {"form": form})

# View to handle user sign-up logic
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() # Create the user
            login(request, user) #log them in
            return redirect("restaurant-list")
    else:
        form = SignUpForm()
    return render(request, "project/signup.html", {"form": form})

# View to handle user login logic
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("restaurant-list")
    else:
        form = AuthenticationForm()
    return render(request, "project/login.html", {"form": form})

# Logout the user and redirect to login page
def logout_view(request):
    logout(request)
    return redirect("login")

# View for editing the user's profile
@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'project/edit_profile.html', {'form': form})

# Edit list (name and description)
@login_required
@require_POST
def edit_list(request, pk):
    list_obj = get_object_or_404(List, pk=pk)

    if request.user != list_obj.user:
        messages.error(request, "You do not have permission to edit this list.")
        return redirect('list-detail', pk=pk)

    name = request.POST.get("name", "").strip()
    description = request.POST.get("description", "").strip()

    if name:
        list_obj.name = name
        list_obj.description = description
        list_obj.save()
        messages.success(request, "List updated successfully.")
    else:
        messages.error(request, "List name cannot be empty.")

    return redirect('list-detail', pk=pk)


# Delete list
@login_required
@require_POST
def delete_list(request, pk):
    list_obj = get_object_or_404(List, pk=pk)

     # Only owner can delete
    if request.user != list_obj.user:
        messages.error(request, "You do not have permission to delete this list.")
        return redirect('list-detail', pk=pk)

    list_obj.delete()
    messages.success(request, "List deleted.")
    return redirect('profile')


# Share list with another user
@login_required
@require_POST
def share_list(request, pk):
    list_obj = get_object_or_404(List, pk=pk)
    # Only owner can share
    if request.user != list_obj.user:
        messages.error(request, "You can only share lists you created.")
        return redirect('list-detail', pk=pk)

    user_id = request.POST.get("user_id")
    try:
        user = User.objects.get(pk=user_id)

        if user == request.user:
            messages.warning(request, "You cannot share the list with yourself.")
        elif list_obj.users_shared_with.filter(pk=user.pk).exists():
            messages.info(request, f"This list is already shared with {user.username}.")
        else:
            list_obj.users_shared_with.add(user)
            messages.success(request, f"List shared with {user.username}.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")

    return redirect('list-detail', pk=pk)

# Alternate list creation view with redirect to list detail
@login_required
def list_add(request):
    if request.method == "POST":
        form = ListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.user = request.user
            new_list.save()
            form.save_m2m()  
            messages.success(request, "List created successfully.")
            return redirect("list-detail", pk=new_list.pk)
    else:
        form = ListForm()

    return render(request, "project/list_form.html", {"form": form})

# View for publicly viewing another user's profile
@login_required
def public_profile(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(Profile, user=target_user)

    # Lists shared by target_user with the logged-in user
    shared_lists = List.objects.filter(user=target_user, users_shared_with=request.user)

    # If you're viewing your own profile, show all your created lists too
    created_lists = List.objects.filter(user=target_user) if request.user == target_user else None

    return render(request, "project/public_profile.html", {
        "target_user": target_user,
        "profile": profile,
        "shared_lists": shared_lists,
        "created_lists": created_lists,
    })

# View to edit a restaurant (only if current user created it)
@login_required
def edit_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    if restaurant.user != request.user:
        raise PermissionDenied("You can only edit restaurants you added.")

    if request.method == 'POST':
        form = RestaurantForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, "Restaurant updated successfully.")
            return redirect('restaurant-detail', pk=restaurant.pk)
    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'project/restaurant_form.html', {'form': form})

# View to display a list of all users (excluding current user)
@login_required
def user_list_view(request):
    query = request.GET.get('q', '')
    users = User.objects.exclude(id=request.user.id)

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(profile__name__icontains=query) |
            Q(profile__location__icontains=query) |  # search by profile location
            Q(owned_lists__name__icontains=query)
        ).distinct()

    return render(request, 'project/user_list.html', {
        'users': users,
        'query': query
    })

