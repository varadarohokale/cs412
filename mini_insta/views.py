# File: views.py
# Author: Varada Rohokale (vroho@bu.edu), 2/13/2026
# Description: Define class-based views for the mini_insta app.
# Includes views for listing profiles, showing a single
#  profile, showing a single post, and creating a post.

from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from .models import Photo, Post, Profile
from django.views.generic.edit import UpdateView, DeleteView


class ProfileListView(ListView):
    """Display a list of all Profile records."""

    # Data model used to retrieve records from the database.
    model = Profile

    # Template responsible for rendering the list of profiles.
    template_name = "mini_insta/show_all_profiles.html"

    # Name used to reference the list of objects in the template.
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """Display detailed information for a single Profile record."""

    # Data model used to retrieve a specific Profile.
    model = Profile

    # Template responsible for rendering a single profile page.
    template_name = "mini_insta/show_profile.html"

    # Name used to reference the object in the template.
    context_object_name = "profile"


class PostDetailView(DetailView):
    """Display detailed information for a single Post record."""

    # Data model used to retrieve a specific Post.
    model = Post

    # Template responsible for rendering a single post page.
    template_name = "mini_insta/show_post.html"

    # Name used to reference the object in the template.
    context_object_name = "post"


class CreatePostView(CreateView):
    """Create a new Post for a given Profile, including one Photo."""

    # Form collects a caption (Post) and image_url (Photo).
    form_class = CreatePostForm

    # Template responsible for rendering the create-post form.
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        """Add the Profile to the template context for navigation."""
        context = super().get_context_data(**kwargs)

        # Identify which profile is creating the post.
        profile_pk = self.kwargs["pk"]
        context["profile"] = Profile.objects.get(pk=profile_pk)

        return context

    def form_valid(self, form):
        """Save the Post, then create a related Photo from image_url."""
        profile_pk = self.kwargs["pk"]
        profile = Profile.objects.get(pk=profile_pk)

        # Attach the Post to the correct Profile before saving.
        form.instance.profile = profile

        # Save the Post first so self.object is defined.
        response = super().form_valid(form)

        files = self.request.FILES.getlist("files")
        for f in files:
            Photo.objects.create(post=self.object, image_file=f)

        return response

    def get_success_url(self):
        """Redirect to the newly-created Post's detail page."""
        return reverse("show_post", kwargs={"pk": self.object.pk})

class UpdateProfileView(UpdateView):
    """Update an existing Profile record."""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
   
    

    def form_valid(self, form):
        """Handle the form submission to update an existing Profile."""

        print(f"UpdateProfileView: form.cleaned_data={form.cleaned_data}")
        return super().form_valid(form)

class DeletePostView(DeleteView):
    """Delete an existing Post and redirect back to the creator's Profile."""

    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        """Provide context needed for delete confirmation template."""
        context = super().get_context_data(**kwargs)

        # Post being deleted
        post = self.get_object()
        context["post"] = post

        # Profile who owns the post
        context["profile"] = post.profile

        return context

    def get_success_url(self):
        """Redirect to the Profile page after deleting the Post."""
        # self.object is the Post that was deleted
        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})


class UpdatePostView(UpdateView):
    """Update an existing Post (caption only)."""

    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def form_valid(self, form):
        """Handle form submission to update the Post."""
        print(f"UpdatePostView: form.cleaned_data={form.cleaned_data}")
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to the updated Post's detail page."""
        return reverse("show_post", kwargs={"pk": self.object.pk})