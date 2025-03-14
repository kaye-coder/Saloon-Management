from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'branch', 'position']
    search_fields = ['name', 'email', 'phone_number']
