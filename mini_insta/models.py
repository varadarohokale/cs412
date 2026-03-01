# File: models.py
# Author: Varada Rohokale (vroho@bu.edu), 2/13/2026
# Description: Define data models for the mini_insta application.
# Includes Profile, Post, and Photo models, plus
# accessor methods for retrieving related objects.

from django.db import models
from django.urls import reverse

class Profile(models.Model):
    """Represent a user profile within the mini_insta application."""

    # Unique username used to identify the user.
    username = models.TextField(blank=True)

    # Name displayed publicly on the user's profile page.
    display_name = models.TextField(blank=True)

    # URL pointing to the user's profile image.
    profile_image_url = models.URLField(blank=True)

    # A short biography describing the user.
    bio_text = models.TextField(blank=True)

    # Date and time the profile was created/saved.
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of this Profile."""
        return self.username

    def get_all_posts(self):
        """Return a QuerySet of Posts created by this Profile.

        Posts are ordered newest-first by timestamp.
        """
        return Post.objects.filter(profile=self).order_by("-timestamp")
    
    def get_absolute_url(self):
        """Return the URL to display this Profile."""
        return reverse("show_profile", kwargs={"pk": self.pk})


class Post(models.Model):
    """Represent an Instagram-style post created by a Profile."""

    # Profile that created this post (many posts per profile).
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    # Date and time the post was created/saved.
    timestamp = models.DateTimeField(auto_now=True)

    # Optional text caption associated with the post.
    caption = models.TextField(blank=True)

    def __str__(self):
        """Return a string representation of this Post."""
        return f"{self.profile}, {self.timestamp}"

    def get_all_photos(self):
        """Return a QuerySet of Photos associated with this Post."""
        return Photo.objects.filter(post=self).order_by("timestamp")


class Photo(models.Model):
    """Represent a photo associated with a Post."""

    # Post to which this photo belongs (many photos per post).
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="photos",)

    # URL to an image stored on the public web.
    image_url = models.URLField(blank=True)

    # Date and time the photo was created.
    timestamp = models.DateTimeField(auto_now_add=True)

    image_file = models.ImageField(blank=True, null=True) 

    def __str__(self):
        """Return a string representation of this Photo."""
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return "No image"

    def get_image_url(self):
        '''
        Return the URL to the image for this Photo.
        If image_url exists, use it; otherwise use image_file.url.
        '''
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return ""
