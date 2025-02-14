from django.shortcuts import render
from datetime import datetime, timedelta
import random

IMAGES = [
    "restaurants/images/r1.jpg",  # Add more images here
]

# Define menu items
MENU_ITEMS = [
    {"name": "Baklava Pancakes", "price": 10},
    {"name": "Knafeh Pancakes", "price": 11},
    {"name": "Shakshuka", "price": 8},
    {"name": "Omelet", "price": 7},
    {"name": "Coffee", "price": 3},
    {"name": "Chai", "price": 3},
    {"name": "Orange Juice", "price": 2},
    {"name": "Lemonade", "price": 2},
]

def main(request):
    """Display the main restaurant page."""
    return render(request, 'restaurants/main.html', {'image': IMAGES})

def order(request):
    """Display the ordering page."""
    return render(request, 'restaurants/order.html')

def confirmation(request):
    """Process the order submission and display confirmation."""
    if request.method == "POST":
        customer_name = request.POST.get("name")
        customer_email = request.POST.get("email")
        customer_phone = request.POST.get("number")  # Use correct field name from form

        # Retrieve selected food items
        selected_foods = request.POST.getlist("sweet") + request.POST.getlist("savory")
        selected_drinks = request.POST.getlist("drink")

        # Combine all selected items
        selected_items = selected_foods + selected_drinks

        # Calculate total price
        total_price = 0
        for item in selected_items:
            price = float(item.split("$")[-1])  # Extract price from value string
            total_price += price

        # Generate estimated ready time (randomly between 30-60 minutes)
        wait_time = random.randint(30, 60)  # Ensure wait time is between 30-60 min
        current_time = datetime.now()  # Get current local time
        ready_time = current_time + timedelta(minutes=wait_time)
        ready_time_str = ready_time.strftime("%I:%M %p")  # Format as 12-hour time (e.g., 05:30 PM)


        context = {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "order_items": selected_items,
            "total_price": round(total_price, 2),
            "ready_time": ready_time_str,
        }
        return render(request, "restaurants/confirmation.html", context)

    return render(request, "restaurants/confirmation.html", {"error": "Invalid request"})
