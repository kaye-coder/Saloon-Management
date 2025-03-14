from django.urls import path
from . import views

urlpatterns = [
    path('', views.unit_list, name='unit_list'),
    path('create/', views.unit_create, name='unit_create'),
    path('edit/<int:pk>/', views.unit_edit, name='unit_edit'),
    path('delete/<int:pk>/', views.unit_delete, name='unit_delete'),
path('view/', views.units_view, name='units_view'),  # Read-only view

]
