# File: forms.py
# Author: Varada Rohokale (vroho@bu.edu), April 30, 2026
# Description: Defines forms for signup and customer profile creation.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Customer


class CustomerSignUpForm(UserCreationForm):
    """Create a Django user and matching customer profile."""

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        """Connect the signup form to Django's User model."""

        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'address',
            'phone_number',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        """Save the User object and create a Customer object."""
        user = super().save(commit=False)

        # Store signup form values on the Django user account.
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        # Save to the database only after Django validates the form.
        if commit:
            user.save()

            # Create the customer profile linked to the saved user.
            Customer.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
            )

        return user