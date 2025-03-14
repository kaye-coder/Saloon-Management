from django.contrib import admin
from .models import Stock

from django.contrib import admin
from .models import Stock

class StockAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit', 'purchase_price', 'selling_price', 'quantity']
    list_filter = ['category', 'unit']
    search_fields = ['name']

admin.site.register(Stock, StockAdmin)
