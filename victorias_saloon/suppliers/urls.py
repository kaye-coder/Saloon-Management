from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('add/', views.add_supplier, name='add_supplier'),
    path('', views.supplier_list, name='supplier_list'),
    path('update/<int:pk>/', views.update_supplier, name='update_supplier'),
    path('delete/<int:pk>/', views.delete_supplier, name='delete_supplier'),
path('view/', views.suppliers_view, name='suppliers_view'),  # Read-only view

]
