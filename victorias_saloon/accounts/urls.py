from django.urls import path
from .views import add_user, manage_users, manage_permissions, delete_permission  # Add missing imports
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('manage-permissions/', manage_permissions, name='manage_permissions'),  # Manage Permissions
    path('add-user/', add_user, name='add_user'),  # Add a new user
    path('manage-users/', manage_users, name='manage_users'),  # Manage users
    path('login/', views.custom_login, name='login'),  # Login page
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard page
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout functionality
    path('delete-permission/<int:permission_id>/', delete_permission, name='delete_permission'),  # Delete permission by ID
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('logout/', views.custom_logout, name='logout'),
    path('logout/', views.user_logout, name='logout'),  # URL for logout
    path('victoria-saloon-management/', views.victoria_saloon_management, name='victoria_saloon_management'),

]
