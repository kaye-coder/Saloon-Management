from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    path('', views.purchase_list, name='list'),
    path('create/', views.create_purchase, name='create'),
    path('<int:purchase_id>/delete/', views.purchase_delete, name='delete'),
path('view/', views.purchases_view, name='purchases_view'),  # Read-only view

]
