# File: models.py
# Author: Varada Rohokale (vroho@bu.edu), 3/01/2026
# Description: Define data models for the mini_insta application.
# Includes Profile, Post, Photo, Follow, Comment, and Like models,
# along with accessor methods used by views/templates to retrieve
# related objects (posts, feed, followers, likes, and comments).

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    """Represent a user profile within the mini_insta application."""

    # Unique username used to identify the user.
    username = models.TextField(blank=True)

    # Name displayed publicly on the user's profile page.
    display_name = models.TextField(blank=True)

    # URL pointing to the user's profile image (stored on the public web).
    profile_image_url = models.URLField(blank=True)

    # A short biography describing the user.
    bio_text = models.TextField(blank=True)

    # Date and time the profile was created/saved.
    join_date = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of this Profile."""
        return self.username

    def get_all_posts(self):
        """Return all Posts created by this Profile, newest-first."""
        # Filter to only Posts created by this Profile and order newest-first
        # so the profile page shows most recent content first.
        return Post.objects.filter(profile=self).order_by("-timestamp")

    def get_absolute_url(self):
        """Return the URL to display this Profile."""
        # UpdateView uses get_absolute_url when a success URL is not specified.
        return reverse("show_profile", kwargs={"pk": self.pk})

    def get_followers(self):
        """Return a list of Profiles that follow this Profile."""
        # Retrieve Follow edges where *this* profile is the publisher being followed.
        follows = Follow.objects.filter(profile=self)

        # Convert the Follow objects into the follower Profile objects, since
        # templates want a list of Profiles (not a list of Follow records).
        return [follow_edge.follower_profile for follow_edge in follows]

    def get_num_followers(self):
        """Return the number of followers for this Profile."""
        # Count the number of Follow edges pointing to this profile.
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        """Return a list of Profiles that this Profile is following."""
        # Retrieve Follow edges where *this* profile is the subscriber/follower.
        follows = Follow.objects.filter(follower_profile=self)

        # Convert Follow edges into the publisher Profile objects being followed.
        return [follow_edge.profile for follow_edge in follows]

    def get_num_following(self):
        """Return the number of Profiles this Profile is following."""
        # Count the number of Follow edges starting from this profile.
        return Follow.objects.filter(follower_profile=self).count()

    def get_post_feed(self):
        """Return feed Posts from Profiles this Profile is following, newest-first."""
        # Get the list of Profiles this user follows; these are the feed publishers.
        following_profiles = self.get_following()

        # Filter Posts where the Post owner is any of the followed profiles.
        # Order newest-first to match the typical feed ordering.
        return Post.objects.filter(profile__in=following_profiles).order_by(
            "-timestamp"
        )

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
        """Return all Photos associated with this Post, oldest-first."""
        # Photos are ordered oldest-first so the "first" photo is stable.
        return Photo.objects.filter(post=self).order_by("timestamp")

    def get_all_comments(self):
        """Return all Comments associated with this Post, newest-first."""
        # Display newest comments first so recent activity is most visible.
        return Comment.objects.filter(post=self).order_by("-timestamp")

    def get_likes(self):
        """Return all Likes associated with this Post."""
        # A QuerySet is convenient because templates can use .count().
        return Like.objects.filter(post=self)


class Photo(models.Model):
    """Represent a photo associated with a Post."""

    # Post to which this photo belongs (many photos per post).
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="photos",
    )

    # Backwards-compatible URL for images stored on the public web.
    image_url = models.URLField(blank=True)

    # Date and time the photo was created.
    timestamp = models.DateTimeField(auto_now_add=True)

    # Uploaded image file stored in Django's MEDIA_ROOT (Assignment 5).
    image_file = models.ImageField(blank=True, null=True)

    def __str__(self):
        """Return a string representation of this Photo."""
        # Choose a string based on which storage mechanism is used.
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return "No image"

    def get_image_url(self):
        """Return the URL needed to display this Photo image."""
        # This if/else structure is necessary for backwards compatibility:
        # older records may only have image_url; newer records may use image_file.
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return ""

class Follow(models.Model):
    """Represent a follow relationship (edge) between two Profiles."""

    # Profile being followed (publisher).
    # related_name is required because two ForeignKeys point to Profile.
    profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="profile",
    )

    # Profile doing the following (subscriber).
    follower_profile = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="follower_profile",
    )

    # Time the follow started.
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable string for this Follow relationship."""
        # Use display_name when available; fall back to username otherwise.
        follower_name = self.follower_profile.display_name or self.follower_profile.username
        publisher_name = self.profile.display_name or self.profile.username
        return f"{follower_name} follows {publisher_name}"


class Comment(models.Model):
    """Represent a comment made by a Profile on a Post."""

    # Post to which this comment is attached.
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")

    # Profile that authored the comment.
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="comments"
    )

    # Time the comment was created.
    timestamp = models.DateTimeField(auto_now_add=True)

    # Comment content text.
    text = models.TextField(blank=False)

    def __str__(self):
        """Return a readable string for this Comment."""
        # Shorten preview so admin list pages remain readable.
        commenter_name = self.profile.display_name or self.profile.username
        preview = self.text[:30]
        return f"Comment by {commenter_name} on Post {self.post.pk}: {preview}"

class Like(models.Model):
    """Represent a like made by a Profile on a Post."""

    # Post being liked.
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="likes")

    # Profile that liked the Post.
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name="likes"
    )

    # Time the like was created.
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a readable string for this Like."""
        liker_name = self.profile.display_name or self.profile.username
        return f"{liker_name} likes Post {self.post.pk}"