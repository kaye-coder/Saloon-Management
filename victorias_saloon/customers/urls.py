from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.customer_list, name='customer_list'),  # Customer list page
    path('add/', views.add_customer, name='add_customer'),  # Add new customer page
    path('edit/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),  # Delete customer page
    path('view/', views.customers_view, name='customers_view'),  # Read-only view

]
