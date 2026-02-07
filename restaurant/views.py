from django.shortcuts import render
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.

def main(request):
    template_name = "restaurant/main.html"

    return render(request, template_name)

def order(request):
    template_name = "restaurant/order.html"

    custom_items = [
        "Meat Lovers Pizza",
        "Neapolitan Pizza",
        "Sicilian Pizza",
    ]

    custom_descriptions =[
        "A hearty, savory pizza topped with a heavy combination of pepperoni, pork, italian sausage, bacon, and ham over mozzarella cheese and tomato sauce.",
        "A soft, thin-crust pizza originating from Naples, Italy, featuring a cornicione and minimal high-quality toppings like San Marzano tomatoes and mozzarella di bufala.",
        "A thick-crust, rectangular pizza originating from Palermo, Italy, characterized by a airy, focaccia like dough that is crispy on the bottom, topped with a simple tomato sauce, onions, anchovies, and hard sheep's milk cheese. "
    ]

    daily_special_name = random.choice(custom_items)
 
    if daily_special_name == "Meat Lovers Pizza" :
        daily_special_description =  custom_descriptions[0]

    elif daily_special_name ==  "Neapolitan Pizza" :
        daily_special_description =  custom_descriptions[1]

    else:
        daily_special_description =  custom_descriptions[2]
   
    context={
        "daily_special_name" : daily_special_name,
        "daily_special_description" : daily_special_description
    }


    return render(request, template_name, context)

def confirmation(request):

    template_name = "restaurant/confirmation.html"

    if request.POST:
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        email = request.POST.get("email", "")
        instructions = request.POST.get("instructions", "")
        daily_special_name = request.POST.get("daily_special_name", "")
        daily_special_description = request.POST.get("daily_special_description", "")

    if not name:
        return render(request, "restaurant/order.html", {
            "error": "Please enter your name.",
            "daily_special_name": daily_special_name,
            "daily_special_description": daily_special_description,
        })

    if not phone:
        return render(request, "restaurant/order.html", {
            "error": "Please enter your phone number.",
            "daily_special_name": daily_special_name,
            "daily_special_description": daily_special_description,
        })

    if not email:
        return render(request, "restaurant/order.html", {
            "error": "Please enter your email address.",
            "daily_special_name": daily_special_name,
            "daily_special_description": daily_special_description,
        })

    prices = {
        "farmhouse": 7.99,
        "margarita": 9.99,
        "nystyle": 11.99,
        "dailyspecial": 13.99,  
    }

    display_names = {
        "farmhouse": "Veggie Farmhouse Pizza",
        "margarita": "Margarita Pizza",
        "nystyle": "New York Style Pizza",
        "dailyspecial": f"Daily Special: {daily_special_name}",
    }

    ordered_items = request.POST.getlist("item") 
    toppings = request.POST.getlist("options")
    
    if "farmhouse" in ordered_items and not toppings:
        return render(request, "restaurant/order.html", {
            "error": "Please select at least one topping for the Veggie Farmhouse Pizza.",
            "daily_special_name": request.POST.get("daily_special_name"),
            "daily_special_description": request.POST.get("daily_special_description"),
        })

    if toppings and "farmhouse" not in ordered_items:
        return render(request, "restaurant/order.html", {
            "error": "Please select the Veggie Farmhouse Pizza before choosing veggie toppings.",
            "daily_special_name": request.POST.get("daily_special_name", ""),
            "daily_special_description": request.POST.get("daily_special_description", ""),
        })
    
    order = []
    total = 0.0

    for item in ordered_items:
        if item in prices:
            order.append({ 'name': display_names[item], 'price': prices[item]})
            total += prices[item]
    
    if "farmhouse" in ordered_items:
        topping_price = 2.0
        toppings_total = len(toppings) *  topping_price
        total +=  toppings_total

        order.append({
            "name": f"Veggie toppings: {', '.join(toppings)}",
            "price": toppings_total,
        })

    minutes = random.randint(30, 60)
    ready_dt = timezone.localtime(timezone.now() + timedelta(minutes=minutes))
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
