# File: views.py
# Author: Varada Rohokale (vroho@bu.edu), 2/13/2026
# Description: Defines class-based views for displaying all Profile
# records and for displaying the details of a single Profile within
# the mini_insta application.

from django.views.generic import ListView, DetailView
from .models import *


class ProfileListView(ListView):
    """Display a list of all Profile records."""

    # data model used to retrieve records from the database
    model = Profile

    # template responsible for rendering the list of profiles
    template_name = "mini_insta/show_all_profiles.html"

    # name used to reference the list of objects in the template
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """Display detailed information for a single Profile record."""

    # data model used to retrieve a specific profile
    model = Profile

    # template responsible for rendering a single profile page
    template_name = "mini_insta/show_profile.html"

    # name used to reference the object in the template
    context_object_name = "profile"

class PostDetailView(DetailView):

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = "post"




