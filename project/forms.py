# File: forms.py
# Author: Varada Rohokale (vroho@bu.edu)
# Description: Forms for user authentication and customer profile creation.

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer


class CustomerSignUpForm(UserCreationForm):
    """
    Form to create a Django user and related Customer profile.
    """

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)
    phone_number = forms.CharField(max_length=20)

    class Meta:
        """
        Connect this form to Django's built-in User model.
        """
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
        """
        Save a new User and create a matching Customer profile.
        """
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            Customer.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                address=self.cleaned_data['address'],
                phone_number=self.cleaned_data['phone_number'],
            )

        return user