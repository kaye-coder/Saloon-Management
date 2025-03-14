from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='list'),
    path('edit/', views.inventory_edit, name='edit'),
    path('edit/<int:item_id>/', views.inventory_edit, name='edit'),
    path('delete/<int:item_id>/', views.inventory_delete, name='delete'),
path('view/', views.inventory_view, name='inventory_view'),  # Read-only view

]

