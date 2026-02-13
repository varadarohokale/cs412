from django.conf import settings
from django.urls import path
from . import views 
from django.conf.urls.static import static 
from .views import ProfileListView, ProfileDetailView

urlpatterns=[
    path('', ProfileListView.as_view() , name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile")
]