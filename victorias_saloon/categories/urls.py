from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('create/', views.category_create, name='category_create'),
    path('edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('delete/<int:pk>/', views.category_delete, name='category_delete'),
path('view/', views.categories_view, name='categories_view'),  # Read-only view

]
