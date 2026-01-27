from django.urls import path 
from django.conf import settings
from . import views 
from django.conf.urls.static import static 


urlpatterns =[
    path("", views.home, name="homepage"),
    path("show_all/", views.show_all, name="showallpage"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)