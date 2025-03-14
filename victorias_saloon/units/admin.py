from django.contrib import admin
from .models import Unit

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name','abbreviation','created_at')
    search_fields = ('name','abbreviation')