# File: views.py
# Author: Varada Rohokale (vroho@bu.edu), 1/29/2026
# Description: Django view functions for the quotes app. Renders the home page
# with a random quote/image, a page showing all quotes/images, and an about page.

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import random, time 

def home(request):
    """Render the home page with a randomly selected quote and image."""

    # Template path for the home page.
    template = "quotes/quote.html"  

    # Store available quote options to randomly choose from.
    quotes_list = [
        "A change is brought about because ordinary people do extraordinary things.",
        "We are the change we have been waiting for.",
        "Our stories may be singular, but our destination is shared.",
    ]

    # Store available image URLs to randomly choose from.
    images_list = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/President_Barack_Obama.jpg/960px-President_Barack_Obama.jpg?20130118131738",
        "https://images.ctfassets.net/l7h59hfnlxjx/5g97MzE205qjO2zX4GyWUf/85530ceb7e80d83ac4b0a2f2eb001869/e91bbc527e3dfe8306537af2cd50674d?q=75&w=1014&fm=webp",
        "https://peopleenespanol.com/thmb/q0bbF-NT9jgJLGuCwfM8ZA8EUjA=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/obama1-2-f100fd55722140faaff5e4d9bd81990d.jpg",
    ]

    # Choose one quote and one image at random for display.
    random_quote = random.choice(quotes_list)
    random_image = random.choice(images_list)

    # Build the template context dictionary used by the HTML template.
    context = {
        "quote": random_quote,
        "image": random_image,
        "current_time": time.ctime(),
    }

    return render(request, template, context)


def show_all(request):
    """Render the page showing all quotes and images."""

    # Template path for the show-all page.
    template = "quotes/show_all.html"  

    # Store all quotes to display on the page.
    quotes_list = [
        "A change is brought about because ordinary people do extraordinary things.",
        "We are the change we have been waiting for.",
        "Our stories may be singular, but our destination is shared.",
    ]

    # Store all image URLs to display on the page.
    images_list = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/President_Barack_Obama.jpg/960px-President_Barack_Obama.jpg?20130118131738",
        "https://images.ctfassets.net/l7h59hfnlxjx/5g97MzE205qjO2zX4GyWUf/85530ceb7e80d83ac4b0a2f2eb001869/e91bbc527e3dfe8306537af2cd50674d?q=75&w=1014&fm=webp",
        "https://peopleenespanol.com/thmb/q0bbF-NT9jgJLGuCwfM8ZA8EUjA=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/obama1-2-f100fd55722140faaff5e4d9bd81990d.jpg",
    ]

    # Map each quote and image to separate context keys for easy use in the template.
    context = {
        "quote1": quotes_list[0],
        "quote2": quotes_list[1],
        "quote3": quotes_list[2],
        "image1": images_list[0],
        "image2": images_list[1],
        "image3": images_list[2],
        "current_time": time.ctime(),
    }

    return render(request, template, context)


def about(request):
    """Render the about page which has information about the author and the person who said the quotes."""

    # Template path for the about page.
    template = "quotes/about.html"  

    # Include the current time so the template can display it.
    context = {"current_time": time.ctime()}

    return render(request, template, context)
