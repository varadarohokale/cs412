# File: views.py
# Author: Varada Rohokale (vroho@bu.edu), 4/3/2026
# Description: Defines the standard Django page views and the
# generic class-based REST API views for the dadjokes app.

import random

from django.http import Http404
from django.shortcuts import render

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer


def show_random_page(request):
    """Display one random joke and one random picture."""

    # Retrieve all jokes and pictures so that one of each can be
    # selected at random for the home page.
    all_jokes = Joke.objects.all()
    all_pictures = Picture.objects.all()

    selected_joke = None
    selected_picture = None

    # Choose a random joke only if at least one joke exists.
    if all_jokes.exists():
        selected_joke = random.choice(all_jokes)

    # Choose a random picture only if at least one picture exists.
    if all_pictures.exists():
        selected_picture = random.choice(all_pictures)

    context = {
        'joke': selected_joke,
        'picture': selected_picture,
    }

    return render(request, 'dadjokes/random.html', context)


def show_all_jokes(request):
    """Display all jokes."""

    # Retrieve all jokes ordered from newest to oldest.
    joke_list = Joke.objects.all().order_by('-created_at')

    context = {
        'jokes': joke_list,
    }

    return render(request, 'dadjokes/jokes_list.html', context)


def show_joke(request, pk):
    """Display one joke by primary key."""

    # Attempt to retrieve the requested joke. Raise a 404 error if
    # the joke does not exist.
    try:
        selected_joke = Joke.objects.get(pk=pk)
    except Joke.DoesNotExist:
        raise Http404('Joke not found.')

    context = {
        'joke': selected_joke,
    }

    return render(request, 'dadjokes/joke_detail.html', context)


def show_all_pictures(request):
    """Display all pictures."""

    # Retrieve all pictures ordered from newest to oldest.
    picture_list = Picture.objects.all().order_by('-created_at')

    context = {
        'pictures': picture_list,
    }

    return render(request, 'dadjokes/pictures_list.html', context)


def show_picture(request, pk):
    """Display one picture by primary key."""

    # Attempt to retrieve the requested picture. Raise a 404 error if
    # the picture does not exist.
    try:
        selected_picture = Picture.objects.get(pk=pk)
    except Picture.DoesNotExist:
        raise Http404('Picture not found.')

    context = {
        'picture': selected_picture,
    }

    return render(request, 'dadjokes/picture_detail.html', context)


class JokeListAPIView(generics.ListCreateAPIView):
    """Return all jokes or create a new joke."""

    queryset = Joke.objects.all().order_by('-created_at')
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveAPIView):
    """Return one joke by primary key."""

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListAPIView):
    """Return all pictures."""

    queryset = Picture.objects.all().order_by('-created_at')
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    """Return one picture by primary key."""

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomJokeAPIView(APIView):
    """Return one random joke."""

    def get(self, request):
        """Handle a GET request for one random joke."""

        # Retrieve all jokes so that one can be selected at random.
        all_jokes = Joke.objects.all()

        # Return an error response if no jokes exist.
        if not all_jokes.exists():
            return Response({'error': 'No jokes found.'}, status=404)

        selected_joke = random.choice(all_jokes)
        serializer = JokeSerializer(selected_joke)

        return Response(serializer.data)


class RandomPictureAPIView(APIView):
    """Return one random picture."""

    def get(self, request):
        """Handle a GET request for one random picture."""

        # Retrieve all pictures so that one can be selected at random.
        all_pictures = Picture.objects.all()

        # Return an error response if no pictures exist.
        if not all_pictures.exists():
            return Response({'error': 'No pictures found.'}, status=404)

        selected_picture = random.choice(all_pictures)
        serializer = PictureSerializer(selected_picture)

        return Response(serializer.data)