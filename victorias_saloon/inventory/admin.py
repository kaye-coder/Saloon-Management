from django.contrib import admin
from .models import InventoryItem

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'category', 'unit', 'purchasing_cost', 'selling_cost', 'added_on', 'stock')
    search_fields = ('item_name', 'category__name', 'unit__name')
    list_filter = ('category', 'unit')
    ordering = ('item_name',)
    list_per_page = 20  # This limits the number of entries per page in the list view

admin.site.register(InventoryItem, InventoryItemAdmin)
