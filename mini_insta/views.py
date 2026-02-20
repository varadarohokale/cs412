# File: views.py
# Author: Varada Rohokale (vroho@bu.edu), 2/13/2026
# Description: Defines class-based views for displaying all Profile
# records and for displaying the details of a single Profile within
# the mini_insta application.

from django.views.generic import ListView, DetailView, CreateView
# from .models import *
from .forms import *
from django.urls import reverse 



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

class CreatePostView(CreateView):

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self):

        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile']= profile

        return context 

    def form_valid(self,form):

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

        image_url = form.cleaned_data["image_url"]
        Photo.objects.create(post=self.object, image_url=image_url)

        return super().form_valid(form)
    
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''
 

        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        return reverse('post', kwargs={'pk':pk})
 
 



