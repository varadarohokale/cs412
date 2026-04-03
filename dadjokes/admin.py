# File: admin.py
# Author: Varada Rohokale (vroho@bu.edu), 4/3/2026
# Description: Registers the Joke and Picture models with the
# Django admin site.

from django.contrib import admin
from .models import Joke, Picture

admin.site.register(Joke)
admin.site.register(Picture)