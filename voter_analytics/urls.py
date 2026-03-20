# File: urls.py
# Author: Varada Rohokale (vroho@bu.edu), 3/20/2026
# Description: URL patterns for the voter_analytics application.

from django.urls import path

from . import views

urlpatterns = [
    path("", views.VoterListView.as_view(), name="voters"),
    path("voter/<int:pk>", views.VoterDetailView.as_view(), name="voter"),
    path("graphs", views.GraphsView.as_view(), name="graphs"),
]