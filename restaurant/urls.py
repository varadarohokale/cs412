from django.conf import settings
from django.urls import path 
from . import views  
from django.conf.urls.static import static

urlpatterns = [
    path("", views.main, name="mainpage"),
    path("order/", views.order, name="orderpage"),
    path("confirmation/", views.confirmation, name="confirmationpage")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
 