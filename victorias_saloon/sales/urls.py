from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('create/', views.create_sale, name='create_sale'),
    path('sale_list/', views.sale_list, name='sale_list'),
    path('receipt/<int:sale_id>/', views.view_receipt, name='receipt'),
    path('update_payment/<int:sale_id>/', views.update_payment, name='update_payment'),
    path('delete_sale/<int:sale_id>/', views.delete_sale, name='delete_sale'),  # Added delete sale URL
    path('', views.sales_dashboard, name='sales_dashboard'),
]
