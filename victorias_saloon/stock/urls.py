from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_list, name='stock_list'),
    path('create/', views.stock_create, name='stock_create'),
    path('update/<int:pk>/', views.stock_update, name='stock_update'),
    path('delete/<int:pk>/', views.stock_delete, name='stock_delete'),
]
