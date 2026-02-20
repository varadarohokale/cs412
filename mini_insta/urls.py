# File: urls.py
# Author: Varada Rohokale (vroho@bu.edu), 2/13/2026
# Description: Defines URL patterns for the mini_insta application,
# including routes for displaying all profiles and for displaying
# a single profile.


from django.urls import path
from .views import *


# define URL patterns that map browser requests to view classes.
urlpatterns = [

    # route the default URL '' to the ProfileListView
    path( "", ProfileListView.as_view(), name="show_all_profiles"),

    # route profile/<int:pk> to the ProfileDetailView
    # the primary key pk determines which profile to display
    path( "profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile",),
    path("post/<int:pk>", PostDetailView.as_view(), name="show_post"),
    path("profile/<int:pk>/create_post", CreatePostView.as_view(), name="create_post"),

]
