from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import random, time 

# Create your views here.
def home(request):

    template = "quotes/quote.html"

    quotes_list = [
        "A change is brought about because ordinary people do extraordinary things.",
        "We are the change we have been waiting for.",
        "Our stories may be singular, but our destination is shared."
    ]

    images_list = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/President_Barack_Obama.jpg/960px-President_Barack_Obama.jpg?20130118131738",
        "https://images.ctfassets.net/l7h59hfnlxjx/5g97MzE205qjO2zX4GyWUf/85530ceb7e80d83ac4b0a2f2eb001869/e91bbc527e3dfe8306537af2cd50674d?q=75&w=1014&fm=webp",
        "https://peopleenespanol.com/thmb/q0bbF-NT9jgJLGuCwfM8ZA8EUjA=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/obama1-2-f100fd55722140faaff5e4d9bd81990d.jpg",

    ]

    random_quote = random.choice(quotes_list)
    random_image = random.choice(images_list)

    context = {
        "quote": random_quote,
        "image": random_image,
        'current_time': time.ctime(),
    }
 
    return render (request, template, context)

def show_all(request):

    template = "quotes/show_all.html"

    quotes_list = [
        "A change is brought about because ordinary people do extraordinary things.",
        "We are the change we have been waiting for.",
        "Our stories may be singular, but our destination is shared."
    ]

    images_list = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/President_Barack_Obama.jpg/960px-President_Barack_Obama.jpg?20130118131738",
        "https://images.ctfassets.net/l7h59hfnlxjx/5g97MzE205qjO2zX4GyWUf/85530ceb7e80d83ac4b0a2f2eb001869/e91bbc527e3dfe8306537af2cd50674d?q=75&w=1014&fm=webp",
        "https://peopleenespanol.com/thmb/q0bbF-NT9jgJLGuCwfM8ZA8EUjA=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/obama1-2-f100fd55722140faaff5e4d9bd81990d.jpg",

    ]

    context = {
        "quote1": quotes_list[0],
        "quote2": quotes_list[1],
        "quote3": quotes_list[2],
        "image1": images_list[0],
        "image2": images_list[1],
        "image3": images_list[2],
        'current_time': time.ctime(),
    }

    return render (request, template, context)