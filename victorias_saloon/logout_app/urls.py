# logout_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.user_logout, name='logout'),  # URL for logout
    path('victoria-saloon-management/', views.victoria_saloon_management, name='victoria_saloon_management'),  # Management page
]
