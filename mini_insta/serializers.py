# File: serializers.py
# Author: Varada Rohokale (vroho@bu.edu), 4/10/2026
# Description: Define serializers for the mini_insta REST API.
# Includes serializers for Profile, Photo, and Post objects
# so they can be converted to JSON for API responses.

from rest_framework import serializers

from .models import Photo, Post, Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serialize a Profile object for the REST API."""

    num_followers = serializers.SerializerMethodField()
    num_following = serializers.SerializerMethodField()
    num_posts = serializers.SerializerMethodField()

    class Meta:
        """Specify the model and fields for Profile serialization."""
        model = Profile
        fields = [
            "id",
            "username",
            "display_name",
            "profile_image_url",
            "bio_text",
            "join_date",
            "num_followers",
            "num_following",
            "num_posts",
        ]

    def get_num_followers(self, profile):
        """Return the number of followers for this Profile."""
        return profile.get_num_followers()

    def get_num_following(self, profile):
        """Return the number of Profiles this Profile follows."""
        return profile.get_num_following()

    def get_num_posts(self, profile):
        """Return the number of Posts created by this Profile."""
        return profile.get_all_posts().count()


class PhotoSerializer(serializers.ModelSerializer):
    """Serialize a Photo object for the REST API."""

    image = serializers.SerializerMethodField()

    class Meta:
        """Specify the model and fields for Photo serialization."""
        model = Photo
        fields = [
            "id",
            "image",
            "timestamp",
        ]

    def get_image(self, photo):
        """Return the displayable URL for a Photo image."""
        # Resolve the image URL using the model helper method so the serializer
        # supports both older image_url records and newer uploaded image_file
        # records.
        image_url = photo.get_image_url()

        # A Photo may not yet have a
        # usable image path.
        if not image_url:
            return ""

        # request is used to build an absolute URL for media files so the
        # mobile app can load images correctly.
        request = self.context.get("request")

        # Serializers may sometimes
        # be used without a request in the context.
        if request is not None:
            return request.build_absolute_uri(image_url)

        return image_url


class PostSerializer(serializers.ModelSerializer):
    """Serialize a Post object, including nested Profile and Photo data."""

    profile = ProfileSerializer(read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)
    num_likes = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()

    class Meta:
        """Specify the model and fields for Post serialization."""
        model = Post
        fields = [
            "id",
            "profile",
            "timestamp",
            "caption",
            "photos",
            "num_likes",
            "num_comments",
        ]

    def get_num_likes(self, post):
        """Return the total number of likes on the Post."""
        return post.get_likes().count()

    def get_num_comments(self, post):
        """Return the total number of comments on the Post."""
        return post.get_all_comments().count()