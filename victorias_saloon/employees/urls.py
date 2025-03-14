from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.employee_list, name='employee_list'),  # Root path for 'employees/'
    path('list/', views.employee_list, name='employee_list'),
    path('add/', views.add_employee, name='add_employee'),
    path('edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('delete/<int:pk>/', views.delete_employee, name='delete_employee'),
path('view/', views.employees_view, name='employees_view'),  # Read-only view



]
