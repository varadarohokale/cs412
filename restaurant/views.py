# File: views.py
# Author: Varada Rohokale (vroho@bu.edu), 2/6/2026
# Description: Contains view functions for the restaurant web
# application. Handles rendering pages, processing orders,
# validating form data, and generating the order confirmation.

from django.shortcuts import render
import random
from datetime import timedelta
from django.utils import timezone


def main(request):
    """Render the homepage for the restaurant."""
    
    template_name = "restaurant/main.html"
    return render(request, template_name)


def order(request):
    """Render the order page with a randomly selected daily special."""
    
    template_name = "restaurant/order.html"

    # List storing the possible daily specials
    daily_specials = [
        {"name": "Meat Lovers Pizza", "price": 11.99,
         "description": "A hearty, savory pizza topped with pepperoni, pork, italian sausage, bacon, and ham over mozzarella cheese and tomato sauce."},

        {"name": "Neapolitan Pizza", "price": 12.99,
         "description": "A soft, thin-crust pizza originating from Naples, Italy, featuring a cornicione and minimal high-quality toppings."},

        {"name": "Sicilian Pizza", "price": 13.99,
         "description": "A thick-crust rectangular pizza with airy dough, topped with tomato sauce, onions, anchovies, and sheep's milk cheese."},
    ]

    # Randomly select one daily special
    daily_special = random.choice(daily_specials)

    context = {
        "daily_special_name": daily_special["name"],
        "daily_special_price": daily_special["price"],
        "daily_special_description": daily_special["description"],
    }

    return render(request, template_name, context)


def confirmation(request):
    """Process the submitted order form and display confirmation."""
    
    template_name = "restaurant/confirmation.html"

    # Only process the form if it was submitted via POST
    if request.POST:

        # Read customer information from the form
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        instructions = request.POST.get("instructions", "")

        # Retrieve daily special data from hidden fields
        daily_special_name = request.POST.get("daily_special_name", "")
        daily_special_description = request.POST.get("daily_special_description", "")
        daily_special_price = request.POST.get("daily_special_price", "")

    # Validate that the user entered their name
    if not name:
        return render(request, "restaurant/order.html", {
            "error": "Please enter your name.",
            "daily_special_name": daily_special_name,
            "daily_special_description": daily_special_description,
            "daily_special_price": daily_special_price
        })

    # Validate phone number
    if not phone:
        return render(request, "restaurant/order.html", {
            "error": "Please enter your phone number.",
            "daily_special_name": daily_special_name,
            "daily_special_description": daily_special_description,
            "daily_special_price": daily_special_price
        })

    # Validate email
    if not email:
        return render(request, "restaurant/order.html", {
            "error": "Please enter your email address.",
            "daily_special_name": daily_special_name,
            "daily_special_description": daily_special_description,
            "daily_special_price": daily_special_price
        })

    # Dictionary storing menu prices
    prices = {
        "farmhouse": 7.99,
        "margarita": 9.99,
        "nystyle": 11.99,
        "dailyspecial": 13.99,
    }

    # Dictionary storing display names for items
    display_names = {
        "farmhouse": "Veggie Farmhouse Pizza",
        "margarita": "Margarita Pizza",
        "nystyle": "New York Style Pizza",
        "dailyspecial": f"Daily Special: {daily_special_name}",
    }

    # Retrieve ordered items and toppings
    ordered_items = request.POST.getlist("item")
    toppings = request.POST.getlist("options")

    # Ensure toppings are selected if farmhouse pizza is ordered
    if "farmhouse" in ordered_items and not toppings:
        return render(request, "restaurant/order.html", {
            "error": "Please select at least one topping for the Veggie Farmhouse Pizza.",
            "daily_special_name": daily_special_name,
            "daily_special_description": daily_special_description,
            "daily_special_price": daily_special_price,
        })

    # Prevent toppings without ordering farmhouse pizza
    if toppings and "farmhouse" not in ordered_items:
        return render(request, "restaurant/order.html", {
            "error": "Please select the Veggie Farmhouse Pizza before choosing toppings.",
            "daily_special_name": daily_special_name,
            "daily_special_description": daily_special_description,
            "daily_special_price": daily_special_price,
        })

    # Store the final order and calculate total price
    order = []
    total = 0.0

    # Add selected menu items to the order
    for item in ordered_items:
        if item in prices:
            order.append({
                'name': display_names[item],
                'price': prices[item]
            })
            total += prices[item]

    # Add topping cost if farmhouse pizza was ordered
    if "farmhouse" in ordered_items:
        topping_price = 2.0
        toppings_total = len(toppings) * topping_price
        total += toppings_total

        order.append({
            "name": f"Veggie toppings: {', '.join(toppings)}",
            "price": toppings_total,
        })

    # Generate a random ready time between 30–60 minutes
    minutes = random.randint(30, 60)
    ready_dt = timezone.localtime(
        timezone.now() + timedelta(minutes=minutes)
    )
    ready_time_str = ready_dt.strftime("%I:%M %p").lstrip("0")

    context = {
        "customer_name": name,
        "phone": phone,
        "email": email,
        "instructions": instructions,
        "order": order,
        "total": f"{total:.2f}",
        "ready_time": ready_time_str,
    }

    return render(request, template_name, context)
