
# File: urls.py
# Author: Varada Rohokale (vroho@bu.edu)
# Description: URL patterns for the beauty retail web application.


from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
path('', ProductListView.as_view(), name='product_list'),

path('products/', ProductListView.as_view(), name='product_list'),
path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

path('signup/', SignUpView.as_view(), name='signup'),
path('login/', LoginView.as_view(template_name='project/login.html'), name='login'),
path('logout/', LogoutView.as_view(next_page='product_list'), name='logout'),

path('profile/', ProfileView.as_view(), name='profile'),
path('cart/', CartView.as_view(), name='cart'),
path('cart/update/<int:pk>/', update_cart_item, name='update_cart_item'),
path('checkout/', CheckoutView.as_view(), name='checkout'),
path('order-confirmation/<int:pk>/', OrderConfirmationView.as_view(), name='order_confirmation'),
path('cart/add/<int:pk>/', add_to_cart, name='add_to_cart'),
path('my-orders/', MyOrdersView.as_view(), name='my_orders'),

path('brands/', BrandListView.as_view(), name='brand_list'),
path('brands/<int:pk>/', BrandDetailView.as_view(), name='brand_detail'),

path('customers/', CustomerListView.as_view(), name='customer_list'),
path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),

path('orders/', OrderListView.as_view(), name='order_list'),
path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),

path('orderitems/', OrderItemListView.as_view(), name='orderitem_list'),
path('orderitems/<int:pk>/', OrderItemDetailView.as_view(), name='orderitem_detail'),
]
