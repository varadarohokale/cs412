# File: admin.py
# Author: Varada Rohokale (vroho@bu.edu)
# Description: Registers models for the Django admin site.


from django.contrib import admin
from .models import Brand, Product, Customer, Order, OrderItem

admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)