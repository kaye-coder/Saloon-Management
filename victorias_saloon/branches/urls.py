from django.urls import path
from . import views

app_name = 'branches'

urlpatterns = [
    path('', views.branch_list, name='branch_list'),  # List all branches
    path('add/', views.add_branch, name='add_branch'),
    path('update/<int:pk>/', views.update_branch, name='update_branch'),
    path('delete/<int:pk>/', views.delete_branch, name='delete_branch'),
path('view/', views.branches_view, name='branches_view'),  # Read-only view

]
