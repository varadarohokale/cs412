# File: forms.py
# Author: Varada Rohokale (vroho@bu.edu), 3/01/2026
# Description: Define Django forms for the mini_insta application.
# Includes a form for creating a Post and collecting a
# Photo image URL for the new post.

from django import forms

from .models import Post,  Profile


class CreatePostForm(forms.ModelForm):
    """Collect data needed to create a new Post.
    """

    class Meta:
        """Configure the form to save a Post instance."""
        # Connect this form to the Post model so Django can validate and save it.
        model = Post

        # Only the caption is entered by the user for a new Post.
        fields = ["caption"]


class UpdateProfileForm(forms.ModelForm):
    """Collect data needed to update an existing Profile."""

    class Meta:
        """Configure the form to update a Profile instance.
        Do not allow username or join_date to be edited.
        """
        # Connect this form to the Profile model so UpdateView can save updates.
        model = Profile

        # Allow editing only the user-facing fields.
        fields = ["display_name", "profile_image_url", "bio_text"]


class UpdatePostForm(forms.ModelForm):
    """Collect data needed to update an existing Post."""

    class Meta:
        """Configure the form to update a Post instance."""
        # Connect this form to the Post model so UpdateView can save updates.
        model = Post

        # Assignment requirement: only caption can be updated.
        fields = ["caption"]

class CreateProfileForm(forms.ModelForm):
    """Collect data needed to create a new Profile."""

    class Meta:
        """Configure the form to create a Profile instance."""
        model = Profile
        fields = ["username", "display_name", "profile_image_url", "bio_text"]