# File: views.py
# Author: Varada Rohokale (vroho@bu.edu), April 30, 2026
# Description: Defines views for product browsing, user accounts, carts,
# orders, wishlists, and detail pages in the beauty retail application.

from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import *

from .forms import CustomerSignUpForm
from .models import Brand, Customer, Order, OrderItem, Product


class BrandListView(ListView):
    """Display all beauty brands."""

    model = Brand
    template_name = 'project/brand_list.html'
    context_object_name = 'brands'


class BrandDetailView(DetailView):
    """Display details for one beauty brand."""

    model = Brand
    template_name = 'project/brand_detail.html'
    context_object_name = 'brand'


class ProductListView(ListView):
    """Display products with optional search and filters."""

    model = Product
    template_name = 'project/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Return products filtered by the user's selected options."""
        products = Product.objects.all()

        category = self.request.GET.get('category')
        product_type = self.request.GET.get('product_type')
        brand = self.request.GET.get('brand')
        max_price = self.request.GET.get('max_price')
        query = self.request.GET.get('q')

        # Filter by category only when the user selected a category.
        if category:
            products = products.filter(category=category)

        # Filter by product type only when the user selected a type.
        if product_type:
            products = products.filter(product_type__iexact=product_type)

        # Filter by brand only when the user selected a brand.
        if brand:
            products = products.filter(brand_id=brand)

        # Filter by maximum price only when the user entered a price.
        if max_price:
            products = products.filter(price__lte=max_price)

        # Search across product fields only when the user typed a query.
        if query:
            products = products.filter(
                Q(name__icontains=query)
                | Q(brand__name__icontains=query)
                | Q(product_type__icontains=query)
                | Q(category__icontains=query)
            )

        return products.order_by('brand__name', 'name')

    def get_context_data(self, **kwargs):
        """Add filter values to the template context."""
        context = super().get_context_data(**kwargs)

        context['brands'] = Brand.objects.all().order_by('name')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_product_type'] = self.request.GET.get(
            'product_type',
            ''
        )
        context['selected_brand'] = self.request.GET.get('brand', '')
        context['selected_max_price'] = self.request.GET.get('max_price', '')
        context['search_query'] = self.request.GET.get('q', '')

        return context


class ProductDetailView(DetailView):
    """Display details for one beauty product."""

    model = Product
    template_name = 'project/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """Add search context for the base template."""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class CustomerListView(ListView):
    """Display all customers."""

    model = Customer
    template_name = 'project/customer_list.html'
    context_object_name = 'customers'


class CustomerDetailView(DetailView):
    """Display details for one customer."""

    model = Customer
    template_name = 'project/customer_detail.html'
    context_object_name = 'customer'


class OrderListView(ListView):
    """Display all orders."""

    model = Order
    template_name = 'project/order_list.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    """Display details for one order."""

    model = Order
    template_name = 'project/order_detail.html'
    context_object_name = 'order'


class OrderItemListView(ListView):
    """Display all order items."""

    model = OrderItem
    template_name = 'project/orderitem_list.html'
    context_object_name = 'orderitems'


class OrderItemDetailView(DetailView):
    """Display details for one order item."""

    model = OrderItem
    template_name = 'project/orderitem_detail.html'
    context_object_name = 'orderitem'


class SignUpView(CreateView):
    """Create a new user account and customer profile."""

    form_class = CustomerSignUpForm
    template_name = 'project/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Save the form and redirect the user to the login page."""
        form.save()
        return redirect('login')


class CartView(LoginRequiredMixin, TemplateView):
    """Display the logged-in user's session-based cart."""

    template_name = 'project/cart.html'

    def get_context_data(self, **kwargs):
        """Convert session cart data into products, subtotals, and total."""
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        cart_items = []
        total = Decimal('0.00')

        # Build display data for each product stored in the session cart.
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            subtotal = product.price * quantity
            total += subtotal

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })

        context['cart_items'] = cart_items
        context['total'] = total

        return context


class MyOrdersView(LoginRequiredMixin, ListView):
    """Display orders belonging to the logged-in user."""

    model = Order
    template_name = 'project/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        """Return only the logged-in customer's orders."""
        customer = Customer.objects.get(user=self.request.user)
        return Order.objects.filter(customer=customer).order_by('-order_date')


def add_to_cart(request, pk):
    """Add a selected product and quantity to the session cart."""
    cart = request.session.get('cart', {})
    product_id = str(pk)
    quantity = int(request.POST.get('quantity', 1))

    # Increase quantity when the product is already in the cart.
    if product_id in cart:
        cart[product_id] += quantity

    # Add the product when it is not already in the cart.
    else:
        cart[product_id] = quantity

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


class CheckoutView(LoginRequiredMixin, TemplateView):
    """Create an order from the logged-in user's cart."""

    template_name = 'project/order_confirmation.html'

    def post(self, request, *args, **kwargs):
        """Create order and order items from the current cart."""
        cart = request.session.get('cart', {})

        # Do not create an order when the cart is empty.
        if not cart:
            return redirect('cart')

        customer = Customer.objects.get(user=request.user)

        order = Order.objects.create(
            customer=customer,
            order_date=timezone.now().date(),
            total_price=Decimal('0.00'),
            status='complete',
        )

        total = Decimal('0.00')

        # Convert each session cart item into an OrderItem record.
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            subtotal = product.price * quantity
            total += subtotal

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                subtotal=subtotal,
            )

        order.total_price = total
        order.save()

        request.session['cart'] = {}
        request.session.modified = True

        return redirect('order_confirmation', pk=order.pk)


class OrderConfirmationView(LoginRequiredMixin, DetailView):
    """Display confirmation for one of the logged-in user's orders."""

    model = Order
    template_name = 'project/order_confirmation.html'
    context_object_name = 'order'

    def get_queryset(self):
        """Limit order confirmations to the logged-in customer."""
        customer = Customer.objects.get(user=self.request.user)
        return Order.objects.filter(customer=customer)


class ProfileView(LoginRequiredMixin, DetailView):
    """Display the logged-in user's customer profile and orders."""

    model = Customer
    template_name = 'project/profile.html'
    context_object_name = 'customer'

    def get_object(self, queryset=None):
        """Return or create the customer linked to the logged-in user."""
        customer, created = Customer.objects.get_or_create(
            user=self.request.user,
            defaults={
                'first_name': (
                    self.request.user.first_name
                    or self.request.user.username
                ),
                'last_name': self.request.user.last_name or '',
                'email': (
                    self.request.user.email
                    or f'{self.request.user.username}@example.com'
                ),
                'address': 'Unknown',
                'phone_number': '0000000000',
            }
        )

        return customer

    def get_context_data(self, **kwargs):
        """Add the logged-in customer's order history to the profile."""
        context = super().get_context_data(**kwargs)

        context['orders'] = Order.objects.filter(
            customer=self.object
        ).order_by('-order_date')
        context['search_query'] = self.request.GET.get('q', '')

        return context


def update_cart_item(request, pk):
    """Increase, decrease, or remove an item from the session cart."""

    # Only update the cart after the user submits a cart form.
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(pk)
        action = request.POST.get('action')

        # Only modify the product if it already exists in the cart.
        if product_id in cart:

            # Increase the quantity by one.
            if action == 'increase':
                cart[product_id] += 1

            # Decrease the quantity and remove it if it reaches zero.
            elif action == 'decrease':
                cart[product_id] -= 1

                # Remove the product when quantity is no longer positive.
                if cart[product_id] <= 0:
                    del cart[product_id]

            # Remove the product entirely from the cart.
            elif action == 'remove':
                del cart[product_id]

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')


class WishlistView(LoginRequiredMixin, TemplateView):
    """Display products saved in the user's session wishlist."""

    template_name = 'project/wishlist.html'

    def get_context_data(self, **kwargs):
        """Convert wishlist product IDs into Product objects."""
        context = super().get_context_data(**kwargs)
        wishlist = self.request.session.get('wishlist', [])

        context['products'] = Product.objects.filter(id__in=wishlist)

        return context


def add_to_wishlist(request, pk):
    """Add one product to the session wishlist."""
    wishlist = request.session.get('wishlist', [])

    # Add the product only if it is not already in the wishlist.
    if pk not in wishlist:
        wishlist.append(pk)

    request.session['wishlist'] = wishlist
    request.session.modified = True

    return redirect('wishlist')


def remove_from_wishlist(request, pk):
    """Remove one product from the session wishlist."""
    wishlist = request.session.get('wishlist', [])

    # Remove the product only if it currently exists in the wishlist.
    if pk in wishlist:
        wishlist.remove(pk)

    request.session['wishlist'] = wishlist
    request.session.modified = True

    return redirect('wishlist')