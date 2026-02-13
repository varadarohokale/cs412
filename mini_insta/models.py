# File: models.py
# Author: Varada Rohokale (vroho@bu.edu), 2/13/2026
# Description: Defines the Profile data model for the mini_insta
# application. This model stores user information including
# username, display name, profile image URL, biography text,
# and the date the user joined the platform.



from django.db import models


class Profile(models.Model):
    """Represent a user profile within the mini_insta application."""

    # unique username used to identify the user
    username = models.TextField(blank=True)

    # name displayed publicly on the user’s profile page
    display_name = models.TextField(blank=True)

    # URL pointing to the user's profile image
    profile_image_url = models.URLField(blank=True)

    # a short biography describing the user
    bio_text = models.TextField(blank=True)

    # date and time the profile was created
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a simple string representation of the profile."""
        return self.username
