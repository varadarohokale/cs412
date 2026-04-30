# File: views.py
# Author: Varada Rohokale (vroho@bu.edu)
# Description: Views for listing and viewing details of records in the
# beauty retail web application.

from django.views.generic import ListView, DetailView
from .models import Brand, Product, Customer, Order, OrderItem


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import CustomerSignUpForm
from django.contrib.auth.decorators import login_required

from decimal import Decimal
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.shortcuts import redirect, get_object_or_404

from decimal import Decimal
from django.utils import timezone



class BrandListView(ListView):
    """
    Displays all brands.
    """
    model = Brand
    template_name = 'project/brand_list.html'
    context_object_name = 'brands'


class BrandDetailView(DetailView):
    """
    Displays details for a single brand.
    """
    model = Brand
    template_name = 'project/brand_detail.html'
    context_object_name = 'brand'


class ProductListView(ListView):
    """
    Displays products with search and filtering by category, product type,
    brand, and price.
    """

    
    model = Product
    template_name = 'project/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        """
        Filter products by category, product type, brand, max price, or search.
        """
        products = Product.objects.all()

        category = self.request.GET.get('category')
        product_type = self.request.GET.get('product_type')
        brand = self.request.GET.get('brand')
        max_price = self.request.GET.get('max_price')
        query = self.request.GET.get('q')

        if category:
            products = products.filter(category=category)

        if product_type:
            products = products.filter(product_type__iexact=product_type)

        if brand:
            products = products.filter(brand_id=brand)

        if max_price:
            products = products.filter(price__lte=max_price)

        if query:
            products = products.filter(
                Q(name__icontains=query)
                | Q(brand__name__icontains=query)
                | Q(product_type__icontains=query)
                | Q(category__icontains=query)
            )

        return products.order_by('brand__name', 'name')

    def get_context_data(self, **kwargs):
        """
        Add filter context to the product page.
        """
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all().order_by('name')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_product_type'] = self.request.GET.get('product_type', '')
        context['selected_brand'] = self.request.GET.get('brand', '')
        context['selected_max_price'] = self.request.GET.get('max_price', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ProductDetailView(DetailView):
    """
    Displays details for a single product.
    """
    model = Product
    template_name = 'project/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """
        Add search context so the base template does not break.
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class CustomerListView(ListView):
    """
    Displays all customers.
    """
    model = Customer
    template_name = 'project/customer_list.html'
    context_object_name = 'customers'


class CustomerDetailView(DetailView):
    """
    Displays details for a single customer.
    """
    model = Customer
    template_name = 'project/customer_detail.html'
    context_object_name = 'customer'


class OrderListView(ListView):
    """
    Displays all orders.
    """
    model = Order
    template_name = 'project/order_list.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    """
    Displays details for a single order.
    """
    model = Order
    template_name = 'project/order_detail.html'
    context_object_name = 'order'


class OrderItemListView(ListView):
    """
    Displays all order items.
    """
    model = OrderItem
    template_name = 'project/orderitem_list.html'
    context_object_name = 'orderitems'


class OrderItemDetailView(DetailView):
    """
    Displays details for a single order item.
    """
    model = OrderItem
    template_name = 'project/orderitem_detail.html'
    context_object_name = 'orderitem'

class SignUpView(CreateView):
    """
    Creates a new user account and related customer profile.
    """

    form_class = CustomerSignUpForm
    template_name = 'project/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        Save the user but redirect to login instead of logging in automatically.
        """
        form.save()
        return redirect('login')


class CartView(LoginRequiredMixin, TemplateView):
    """
    Displays the logged-in user's cart stored in the session.
    """

    template_name = 'project/cart.html'

    def get_context_data(self, **kwargs):
        """
        Convert session cart data into product objects and totals.
        """
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        cart_items = []
        total = Decimal('0.00')

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
    """
    Displays only the logged-in user's orders.
    """

    model = Order
    template_name = 'project/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        """
        Return only orders belonging to the logged-in customer.
        """
        customer = Customer.objects.get(user=self.request.user)
        return Order.objects.filter(customer=customer).order_by('-order_date')

def add_to_cart(request, pk):
    """
    Add a selected product and quantity to the session cart.
    """
    cart = request.session.get('cart', {})
    product_id = str(pk)

    quantity = int(request.POST.get('quantity', 1))

    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')

class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'project/order_confirmation.html'

    def post(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})

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
    model = Order
    template_name = 'project/order_confirmation.html'
    context_object_name = 'order'

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return Order.objects.filter(customer=customer)


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Displays the logged-in user's profile and order history.
    """

    model = Customer
    template_name = 'project/profile.html'
    context_object_name = 'customer'

    def get_object(self, queryset=None):
        """
        Return or create the customer linked to the logged-in user.
        """
        customer, created = Customer.objects.get_or_create(
            user=self.request.user,
            defaults={
                'first_name': self.request.user.first_name or self.request.user.username,
                'last_name': self.request.user.last_name or '',
                'email': self.request.user.email or f'{self.request.user.username}@example.com',
                'address': 'Unknown',
                'phone_number': '0000000000',
            }
        )
        return customer

    def get_context_data(self, **kwargs):
        """
        Add order history to the profile page.
        """
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(
            customer=self.object
        ).order_by('-order_date')
        context['search_query'] = self.request.GET.get('q', '')
        return context


def update_cart_item(request, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id = str(pk)
        action = request.POST.get('action')

        if product_id in cart:
            if action == 'increase':
                cart[product_id] += 1
            elif action == 'decrease':
                cart[product_id] -= 1
                if cart[product_id] <= 0:
                    del cart[product_id]
            elif action == 'remove':
                del cart[product_id]

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')