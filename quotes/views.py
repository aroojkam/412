from django.shortcuts import render
import random

# Updated data for Muhammad Ali
QUOTES = [
    "I hated every minute of training, but I said, 'Don't quit. Suffer now and live the rest of your life as a champion.'",
    "Service to others is the rent you pay for your room here on earth.",
    "I am the greatest, I said that even before I knew I was.",
    "Float like a butterfly, sting like a bee. His hands can't hit what his eyes can't see.",
    "Impossible is nothing."
]

IMAGES = [
    "quotes/images/ma1.jpg",
    "quotes/images/ma2.jpg",
    "quotes/images/ma3.jpg"
]

def quote(request):
    """Display a random quote and image."""
    random_quote = random.choice(QUOTES)
    random_image = random.choice(IMAGES)
    return render(request, 'quotes/quote.html', {'quote': random_quote, 'image': random_image})

def show_all(request):
    """Display all quotes and images."""
    return render(request, 'quotes/show_all.html', {'quotes': QUOTES, 'images': IMAGES})

def about(request):
    """Display information about Muhammad Ali and the creator."""
    return render(request, 'quotes/about.html')
