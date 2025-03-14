from django.contrib import admin
from .models import Supplier


class SupplierAdmin(admin.ModelAdmin):
    search_fields = ['name', 'phone_number', 'email']
    list_display = ['name', 'phone_number', 'email']
    ordering = ['name']


admin.site.register(Supplier, SupplierAdmin)



from django.contrib import admin

# Override the admin site header and title for the whole project
admin.site.site_header = "Victorious Admin"
admin.site.site_title = "Victorious Admin Portal"
admin.site.index_title = "Welcome to the Victorious Admin Portal"
