# File: urls.py
# Author: Varada Rohokale (vroho@bu.edu), 2/13/2026
# Description: Define URL patterns for the mini_insta application,
# including routes for profiles, posts, and post creation.

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


from .views import *


urlpatterns = [
    # Show all profiles.
    path("", ProfileListView.as_view(), name="show_all_profiles"),

    path("create_profile", CreateProfileView.as_view(), name="create_profile"),

    # Show the logged in user's own profile.
    path("profile", MyProfileDetailView.as_view(), name="show_own_profile"),

    # Show a single public profile by primary key.
    path("profile/<int:pk>", ProfileDetailView.as_view(), name="show_profile"),

    # Update the logged in user's profile.
    path("profile/update", UpdateProfileView.as_view(), name="update_profile"),

    # Create a post for the logged in user's profile.
    path("profile/create_post", CreatePostView.as_view(), name="create_post"),

    # Show the logged in user's feed.
    path("profile/feed", PostFeedListView.as_view(), name="show_feed"),

    # Search as the logged in user.
    path("profile/search", SearchView.as_view(), name="search"),

    # Public post page.
    path("post/<int:pk>", PostDetailView.as_view(), name="show_post"),

    # Owner only post actions.
    path("post/<int:pk>/delete", DeletePostView.as_view(), name="delete_post"),
    path("post/<int:pk>/update", UpdatePostView.as_view(), name="update_post"),

    # Public followers/following pages.
    path("profile/<int:pk>/followers", ShowFollowersDetailView.as_view(), name="show_followers"),
    path("profile/<int:pk>/following", ShowFollowingDetailView.as_view(), name="show_following"),

    # Follow / unfollow another Profile.
    path("profile/<int:pk>/follow", FollowProfileView.as_view(), name="follow_profile"),
    path("profile/<int:pk>/delete_follow", DeleteFollowProfileView.as_view(), name="delete_follow_profile"),

    # Like / unlike another Profile's Post.
    path("post/<int:pk>/like", LikePostView.as_view(), name="like_post"),
    path("post/<int:pk>/delete_like", DeleteLikePostView.as_view(), name="delete_like_post"),

    # REST API endpoints.
    path("api/", ProfileListAPIView.as_view(), name="api_home"),
    path("api/login/", LoginAPIView.as_view(), name="api_login"),
    path("api/profile/", AuthenticatedProfileAPIView.as_view(), name="api_profile"),
    path("api/profile/posts/", AuthenticatedProfilePostsAPIView.as_view(), name="api_profile_posts_auth"),
    path("api/profile/feed/", AuthenticatedProfileFeedAPIView.as_view(), name="api_profile_feed_auth"),
    path("api/post/create/", AuthenticatedCreatePostAPIView.as_view(),name="api_create_post_auth"),

    # Authentication views.
    path("login/", auth_views.LoginView.as_view(template_name="mini_insta/login.html"), name="login"),
    path("logout_confirmation/", logout_confirmation, name="logout_confirmation"),
    path("logout/", auth_views.LogoutView.as_view(next_page="logout_confirmation"), name="logout"),
]
