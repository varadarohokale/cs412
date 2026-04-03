# File: models.py
# Author: Varada Rohokale (vroho@bu.edu), 4/3/2026
# Description: Defines the Joke and Picture data models for the
# dadjokes Django application.

from django.db import models


class Joke(models.Model):
    """Store the text of a joke and contributor information."""

    text = models.TextField()
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable string for this joke."""
        return f"{self.contributor}: {self.text[:40]}"


class Picture(models.Model):
    """Store the URL of a silly image or GIF and contributor information."""

    image_url = models.URLField()
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable string for this picture."""
        return f"{self.contributor}: {self.image_url}"