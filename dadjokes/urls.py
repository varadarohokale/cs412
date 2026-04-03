# File: urls.py
# Author: Varada Rohokale (vroho@bu.edu), 4/3/2026
# Description: Defines the URL routes for the dadjokes app,
# including both standard page views and REST API views.

from django.urls import path

from .views import *

urlpatterns = [
    path('', show_random_page, name='home'),
    path('random', show_random_page, name='random'),
    path('jokes', show_all_jokes, name='jokes'),
    path('joke/<int:pk>', show_joke, name='joke'),
    path('pictures', show_all_pictures, name='pictures'),
    path('picture/<int:pk>', show_picture, name='picture'),

    path('api/', RandomJokeAPIView.as_view(), name='api_home'),
    path('api/random', RandomJokeAPIView.as_view(), name='api_random'),
    path('api/jokes', JokeListAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view(), name='api_joke'),
    path('api/pictures', PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view(), name='api_picture'),
    path('api/random_picture', RandomPictureAPIView.as_view(), name='api_random_picture'),
]