# File: forms.py
# Author: Varada Rohokale (vroho@bu.edu), 2/20/2026
# Description: Define Django forms for the mini_insta application.
# Includes a form for creating a Post and collecting a
# Photo image URL for the new post.

from django import forms

from .models import Post,  Profile


class CreatePostForm(forms.ModelForm):
    """Collect data needed to create a Post plus one related Photo."""


    class Meta:
        """Configure the form to save a Post instance."""
        model = Post
        fields = ["caption"]

class UpdateProfileForm(forms.ModelForm):
    """Collect data needed to update an existing Profile."""

    class Meta:
        """Configure the form to save a Profile instance. Do not allow username or join_date to be edited."""
        model = Profile
        fields = ["display_name", "profile_image_url", "bio_text"]

class UpdatePostForm(forms.ModelForm):
    """Collect data needed to update an existing Post."""

    class Meta:
        """Configure the form to update a Post instance."""
        model = Post
        fields = ["caption"]