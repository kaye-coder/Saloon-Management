from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ['name', 'email', 'phone_number', 'created_at']

    # Enable search functionality for these fields
    search_fields = ['name', 'email', 'phone_number']

    # Add filters for created_at field in the sidebar
    list_filter = ['created_at']

    # Set the default ordering of customers by created_at (newest first)
    ordering = ['-created_at']

    # Specify which fields to display in the form and their order
    fields = ['name', 'email', 'phone_number', 'created_at']

    # Make created_at read-only in the form
    readonly_fields = ['created_at']
