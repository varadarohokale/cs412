# File: forms.py
# Author: Varada Rohokale (vroho@bu.edu), 2/20/2026
# Description: Define Django forms for the mini_insta application.
# Includes a form for creating a Post and collecting a
# Photo image URL for the new post.

from django import forms

from .models import Post


class CreatePostForm(forms.ModelForm):
    """Collect data needed to create a Post plus one related Photo."""

    # URL for the photo associated with the new post.
    image_url = forms.URLField(label="Image URL", required=True)

    class Meta:
        """Configure the form to save a Post instance."""
        model = Post
        fields = ["caption", "image_url"]
