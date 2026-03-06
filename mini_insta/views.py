# File: views.py
# Author: Varada Rohokale (vroho@bu.edu), 3/1/2026
# Description: Define class-based views for the mini_insta app.
# Includes views for listing profiles, showing a single
#  profile, showing a single post, and creating a post.

from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView

from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from .models import Photo, Post, Profile, Follow, Like
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

class ProfileLoginRequiredMixin(LoginRequiredMixin):
    """Require login and provide helper methods for the logged in Profile."""

    def get_login_url(self):
        """Return the URL required for login."""
        return reverse("login")

    def get_user_profile(self):
        """Return the Profile associated with the logged in user."""
        return Profile.objects.get(user=self.request.user)

class ProfileListView(ListView):
    """Display a list of all Profile records."""

    # Retrieve all Profile instances.
    model = Profile

    # Render the list of Profiles on this template.
    template_name = "mini_insta/show_all_profiles.html"

    # Use this name to reference the QuerySet in the template.
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        """Add debugging information."""
        if request.user.is_authenticated:
            print(f"ProfileListView.dispatch(): request.user={request.user}")
        else:
            print("ProfileListView.dispatch(): not logged in.")
        return super().dispatch(request, *args, **kwargs)


class ProfileDetailView(DetailView):
    """Display detailed information for a single Profile record."""

    # Retrieve a single Profile using the primary key from the URL.
    model = Profile

    # Render the Profile on this template.
    template_name = "mini_insta/show_profile.html"

    # Use this name to reference the Profile object in the template.
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        """Add the logged in user's Profile and follow status to context."""
        # Begin by retrieving the default context dictionary from DetailView.
        context = super().get_context_data(**kwargs)

        # This if-statement is necessary because follow/unfollow controls
        # should only appear when a user is authenticated.
        if self.request.user.is_authenticated:
            # logged_in_profile is the Profile associated with the
            # authenticated Django User.
            logged_in_profile = Profile.objects.get(user=self.request.user)
            context["logged_in_profile"] = logged_in_profile

            # is_following is True exactly when the logged in user's
            # Profile already follows the Profile currently being displayed.
            context["is_following"] = Follow.objects.filter(
                profile=self.object,
                follower_profile=logged_in_profile,
            ).exists()

        return context


class UpdateProfileView(ProfileLoginRequiredMixin, UpdateView):
    """Update an existing Profile record."""

    # Specify which model object is being updated.
    model = Profile

    # Use the ModelForm that excludes username/join_date.
    form_class = UpdateProfileForm

    # Render the update form on this template.
    template_name = "mini_insta/update_profile_form.html"

    def form_valid(self, form):
        """Handle form submission to update an existing Profile."""
        # Debug print is helpful while developing to confirm expected form values.
        print(f"UpdateProfileView: form.cleaned_data={form.cleaned_data}")

        # Delegate database update + redirect behavior to Django's UpdateView.
        return super().form_valid(form)

    def get_object(self):
        """Return the Profile associated with the logged in user."""
        return self.get_user_profile()



class PostDetailView(DetailView):
    """Display detailed information for a single Post record."""

    # Retrieve a single Post using the primary key from the URL.
    model = Post

    # Render the Post on this template.
    template_name = "mini_insta/show_post.html"

    # Use this name to reference the Post object in the template.
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """Add navigation and like-status context for the displayed Post."""
        # Begin by retrieving the default context dictionary from DetailView.
        context = super().get_context_data(**kwargs)

        # profile is the owner/author of the Post, needed by the template
        # for navigation back to that Profile page.
        context["profile"] = self.get_object().profile

        # This if-statement is necessary because like/unlike controls
        # should only appear when a user is authenticated.
        if self.request.user.is_authenticated:
            # logged_in_profile is the Profile associated with the
            # authenticated Django User.
            logged_in_profile = Profile.objects.get(user=self.request.user)
            context["logged_in_profile"] = logged_in_profile

            # has_liked is True exactly when the logged in user's Profile
            # has already liked the displayed Post.
            context["has_liked"] = Like.objects.filter(
                post=self.object,
                profile=logged_in_profile,
            ).exists()

        return context


class CreatePostView(ProfileLoginRequiredMixin, CreateView):
    """Create a new Post for a given Profile, including uploaded Photo(s)."""

    # Collect Post data (caption). Photo uploads are handled via request.FILES.
    form_class = CreatePostForm

    # Render the create-post form on this template.
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        """Add the Profile to the template context for navigation."""
        context = super().get_context_data(**kwargs)

        # profile_pk identifies which Profile is creating the new Post.
        context["profile"] = self.get_user_profile()

        return context

    def form_valid(self, form):
        """Save the Post, then create related Photo objects from uploaded files."""
        # profile_pk is the primary key of the Profile creating the Post.
        profile = self.get_user_profile()


        # Attach the Post to the correct Profile before saving it.
        form.instance.profile = profile

        # Save the Post first so self.object (the new Post) exists.
        response = super().form_valid(form)

        # Retrieve 0..many uploaded image files from the multipart form data.
        files = self.request.FILES.getlist("files")

        # Loop is necessary because the user may upload multiple files.
        for uploaded_file in files:
            # Create one Photo record per uploaded file.
            Photo.objects.create(post=self.object, image_file=uploaded_file)

        return response

    def get_success_url(self):
        """Return the URL to display the newly-created Post."""
        # Redirect to the Post detail page for the new Post.
        return reverse("show_post", kwargs={"pk": self.object.pk})


class UpdatePostView(ProfileLoginRequiredMixin, UpdateView):
    """Update an existing Post caption."""

    # Specify which model object is being updated.
    model = Post

    # Only allow editing the caption (per assignment requirements).
    form_class = UpdatePostForm

    # Render the update form on this template.
    template_name = "mini_insta/update_post_form.html"

    def form_valid(self, form):
        """Handle form submission to update the Post caption."""
        # Debug print helps verify the cleaned caption value.
        print(f"UpdatePostView: form.cleaned_data={form.cleaned_data}")

        # Delegate saving/redirect behavior to Django's UpdateView.
        return super().form_valid(form)

    def get_success_url(self):
        """Return the URL to display the updated Post."""
        return reverse("show_post", kwargs={"pk": self.object.pk})
    


class DeletePostView(ProfileLoginRequiredMixin, DeleteView):
    """Delete an existing Post and redirect to the owner's Profile page."""

    # Specify which model object is being deleted.
    model = Post

    # Render the delete confirmation form on this template.
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        """Provide context needed for the delete confirmation template."""
        context = super().get_context_data(**kwargs)

        # Get the Post being deleted so the template can display it.
        post = self.get_object()
        context["post"] = post

        # Also provide the Post owner's Profile so the cancel button can
        # return to the correct profile page.
        context["profile"] = post.profile

        return context

    def get_success_url(self):
        """Return the URL to display after successfully deleting the Post."""
        # After deleting a Post, return to the Profile page of the Post owner.
        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})


class ShowFollowersDetailView(DetailView):
    """Display the followers list for a single Profile."""

    # This is a DetailView because the page is about one Profile.
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    """Display the following list for a single Profile."""

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"



class PostFeedListView(ProfileLoginRequiredMixin, ListView):
    """Display a feed of Posts for a single Profile."""

    # The feed is a list of Post objects, so ListView is appropriate.
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Return the feed Posts for the logged in user's Profile."""
        profile = self.get_user_profile()
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        """Add the logged in user's Profile to context for navigation links."""
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_user_profile()
        return context

class SearchView(ProfileLoginRequiredMixin, ListView):
    """Search Profiles and Posts based on a text query."""

    # Default results template (used when query is present).
    template_name = "mini_insta/search_results.html"

    # Name for the Post results list in the template.
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        """Route requests to search form or results based on query presence."""
        # This if-statement is necessary because the search form page
        # should display when no query parameter is provided.
        if "query" not in self.request.GET:
            # profile_pk identifies which Profile is performing the search.
           
            profile = self.get_user_profile()

            # Render the search form template with required context.
            return render(request, "mini_insta/search.html", {"profile": profile})

        # If a query is present, continue with ListView processing to show results.
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return Posts whose caption contains the query ."""
        # q is the search query text typed by the user.
        q = self.request.GET.get("query", "").strip()

        # If q is empty, return no results rather than all Posts.
        if not q:
            return Post.objects.none()

        # Filter to Posts whose caption contains the query text.
        return Post.objects.filter(caption__icontains=q).order_by("-timestamp")

    def get_context_data(self, **kwargs):
        """Add Profile, query, and matching Profile/Post results to context."""
        context = super().get_context_data(**kwargs)

        # profile_pk identifies which Profile is performing the search.
        profile= self.get_user_profile()
        context["profile"] = profile

        # q is the search query text typed by the user.
        q = self.request.GET.get("query", "").strip()
        context["query"] = q

        # Posts results are already stored in context["posts"] via ListView.
        context["posts"] = context.get("posts", Post.objects.none())

        # This if-statement is necessary to avoid returning all Profiles
        # when the query is empty.
        if q:
            # Match Profiles where the query appears in username, display name, or bio.
            context["profiles"] = Profile.objects.filter(
                Q(username__icontains=q)
                | Q(display_name__icontains=q)
                | Q(bio_text__icontains=q)
            ).order_by("username")
        else:
            context["profiles"] = Profile.objects.none()

        return context

class MyProfileDetailView(ProfileLoginRequiredMixin, DetailView):
    """Display the Profile of the logged in user."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        """Return the Profile associated with the logged in user."""
        return self.get_user_profile()

    def get_context_data(self, **kwargs):
        """Add the logged in user's Profile and follow status to context."""
        context = super().get_context_data(**kwargs)

        # logged_in_profile is the Profile associated with the
        # authenticated Django User.
        logged_in_profile = self.get_user_profile()
        context["logged_in_profile"] = logged_in_profile

        # is_following is False on the user's own Profile page,
        # since a Profile should not follow itself.
        context["is_following"] = False

        return context
    
def logout_confirmation(request):
    """Display a logout confirmation page."""
    return render(request, "mini_insta/logged_out.html")

class CreateProfileView(CreateView):
    """Create a new Profile and a new Django User at the same time."""

    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        """Add the UserCreationForm to the template context."""
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm()
        return context

    def form_valid(self, form):
        """Create the Django User, log them in, attach to Profile, and save."""
        user_form = UserCreationForm(self.request.POST)

        if not user_form.is_valid():
            return self.form_invalid(form)

        user = user_form.save()

        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")

        form.instance.user = user

        return super().form_valid(form)

class FollowProfileView(ProfileLoginRequiredMixin, DetailView):
    """Allow the logged in user's Profile to follow another Profile."""

    # Retrieve the other Profile using the primary key from the URL.
    model = Profile

    def dispatch(self, request, *args, **kwargs):
        """Create a Follow record for the logged in user's Profile."""
        # other_profile is the Profile identified by the pk in the URL.
        other_profile = self.get_object()

        # logged_in_profile is the Profile of the authenticated user.
        logged_in_profile = self.get_user_profile()

        # This if-statement is necessary because a Profile should not
        # be allowed to follow itself.
        if logged_in_profile != other_profile:
            # Only create a Follow record if one does not already exist.
            if not Follow.objects.filter(
                profile=other_profile,
                follower_profile=logged_in_profile,
            ).exists():
                Follow.objects.create(
                    profile=other_profile,
                    follower_profile=logged_in_profile,
                )

        # After creating the Follow, return to the other Profile page.
        return redirect("show_profile", pk=other_profile.pk)


class DeleteFollowProfileView(ProfileLoginRequiredMixin, DetailView):
    """Allow the logged in user's Profile to unfollow another Profile."""

    # Retrieve the other Profile using the primary key from the URL.
    model = Profile

    def dispatch(self, request, *args, **kwargs):
        """Delete the Follow record for the logged in user's Profile."""
        # other_profile is the Profile identified by the pk in the URL.
        other_profile = self.get_object()

        # logged_in_profile is the Profile of the authenticated user.
        logged_in_profile = self.get_user_profile()

        # Delete the matching Follow relationship, if it exists.
        Follow.objects.filter(
            profile=other_profile,
            follower_profile=logged_in_profile,
        ).delete()

        # After deleting the Follow, return to the other Profile page.
        return redirect("show_profile", pk=other_profile.pk)

class LikePostView(ProfileLoginRequiredMixin, DetailView):
    """Allow the logged in user's Profile to like another Profile's Post."""

    # Retrieve the target Post using the primary key from the URL.
    model = Post

    def dispatch(self, request, *args, **kwargs):
        """Create a Like record for the logged in user's Profile."""
        # post is the Post identified by the pk in the URL.
        post = self.get_object()

        # logged_in_profile is the Profile of the authenticated user.
        logged_in_profile = self.get_user_profile()

        # This if-statement is necessary because a Profile should not
        # be allowed to like its own Post.
        if post.profile != logged_in_profile:
            # Only create a Like record if one does not already exist.
            if not Like.objects.filter(
                post=post,
                profile=logged_in_profile,
            ).exists():
                Like.objects.create(
                    post=post,
                    profile=logged_in_profile,
                )

        # After creating the Like, return to the Post page.
        return redirect("show_post", pk=post.pk)


class DeleteLikePostView(ProfileLoginRequiredMixin, DetailView):
    """Allow the logged in user's Profile to remove a like from a Post."""

    # Retrieve the target Post using the primary key from the URL.
    model = Post

    def dispatch(self, request, *args, **kwargs):
        """Delete the Like record for the logged in user's Profile."""
        # post is the Post identified by the pk in the URL.
        post = self.get_object()

        # logged_in_profile is the Profile of the authenticated user.
        logged_in_profile = self.get_user_profile()

        # Delete the matching Like relationship, if it exists.
        Like.objects.filter(
            post=post,
            profile=logged_in_profile,
        ).delete()

        # After deleting the Like, return to the Post page.
        return redirect("show_post", pk=post.pk)