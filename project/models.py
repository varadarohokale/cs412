# File: models.py
# Author: Varada Rohokale (vroho@bu.edu), April 30, 2026
# Description: Defines the data models for the beauty retail web application.

from django.contrib.auth.models import User
from django.db import models


class Brand(models.Model):
    """Represent a beauty brand."""

    name = models.CharField(max_length=100)

    def __str__(self):
        """Return the brand name."""
        return self.name


class Product(models.Model):
    """Represent a beauty product sold in the store."""

    CATEGORY_CHOICES = [
        ('makeup', 'Makeup'),
        ('skincare', 'Skincare'),
        ('fragrance', 'Fragrance'),
        ('hair', 'Hair'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    product_type = models.CharField(max_length=100)
    shade = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', blank=True)

    def __str__(self):
        """Return the product name and brand."""
        return f"{self.name} ({self.brand.name})"


class Customer(models.Model):
    """Represent a customer profile linked to a Django user."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        """Return the customer's full name."""
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    """Represent an order placed by a customer."""

    STATUS_CHOICES = [
        ('cart', 'Cart'),
        ('processing', 'Processing'),
        ('complete', 'Complete'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        """Return the order number and customer."""
        return f"Order #{self.pk} - {self.customer}"


class OrderItem(models.Model):
    """Represent a product and quantity inside an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Return the product name and quantity."""
        return f"{self.product.name} x {self.quantity}"