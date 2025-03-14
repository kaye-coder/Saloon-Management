from django.urls import path
from . import views

app_name = 'positions'

urlpatterns = [
    path('', views.position_list, name='position_list'),  # List all positions
    path('edit/<int:pk>/', views.edit_position, name='edit_position'),  # Edit position
    path('create/', views.create_position, name='create_position'),  # Create new position
    path('delete/<int:pk>/', views.delete_position, name='delete_position'),
    path('view/', views.positions_view, name='positions_view'),  # Read-only view
    # Delete position
]
