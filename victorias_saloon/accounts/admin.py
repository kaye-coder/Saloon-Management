from django.contrib import admin
from .models import AppPermission

@admin.register(AppPermission)
class AppPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'app_name', 'permission']
    list_filter = ['app_name', 'permission']
    search_fields = ['user__username', 'app_name']
