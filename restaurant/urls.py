# File: urls.py
# Author: Varada Rohokale (vroho@bu.edu), 2/6/2026
# Description: Defines URL routes for the restaurant web
# application and maps them to their corresponding views.

from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


# URL patterns that connect webpage routes to their view functions
urlpatterns = [
    path("", views.main, name="mainpage"),
    path("order/", views.order, name="orderpage"),
    path("confirmation/", views.confirmation, name="confirmationpage"),
]


# Allows Django to serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
