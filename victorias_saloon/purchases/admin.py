# admin.py in the purchases app
from django.contrib import admin
from .models import Purchase

admin.site.register(Purchase)
