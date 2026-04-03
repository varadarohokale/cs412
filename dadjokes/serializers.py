# File: serializers.py
# Author: Varada Rohokale (vroho@bu.edu), 4/3/2026
# Description: Defines serializer classes used to convert Joke and
# Picture model objects to and from JSON for the REST API.

from rest_framework import serializers
from .models import Joke, Picture


class JokeSerializer(serializers.ModelSerializer):
    """Serialize Joke model objects for the REST API."""

    class Meta:
        """Specify the model and fields for Joke serialization."""

        model = Joke
        fields = ['id', 'text', 'contributor', 'created_at']


class PictureSerializer(serializers.ModelSerializer):
    """Serialize Picture model objects for the REST API."""

    class Meta:
        """Specify the model and fields for Picture serialization."""

        model = Picture
        fields = ['id', 'image_url', 'contributor', 'created_at']