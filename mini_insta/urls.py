# File: urls.py
# Author: Varada Rohokale (vroho@bu.edu), 2/13/2026
# Description: Define URL patterns for the mini_insta application,
# including routes for profiles, posts, and post creation.

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from .views import CreatePostView,PostDetailView, ProfileDetailView, ProfileListView, UpdateProfileView, DeletePostView, UpdatePostView


urlpatterns = [
    # Show all profiles.
    path("", ProfileListView.as_view(), name="show_all_profiles"),

    # Show a single profile by primary key.
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile"),

    # Show a single post by primary key.
    path("post/<int:pk>", PostDetailView.as_view(), name="show_post"),

    # Create a post for a specific profile.
    path( "profile/<int:pk>/create_post", CreatePostView.as_view(), name="create_post"),

    path("profile/<int:pk>/update", UpdateProfileView.as_view(), name="update_profile"),

    path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),

    path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)