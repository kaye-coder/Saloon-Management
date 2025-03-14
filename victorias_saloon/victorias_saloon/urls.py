from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from logout_app import views as logout_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employees/', include('employees.urls')),  # Employees app URLs      # Sales app URLs
    path('customers/', include('customers.urls')),  # Customers app URLs
    path('suppliers/', include('suppliers.urls')),  # No need to add `namespace` here
    path('positions/', include('positions.urls')),  # Positions app URLs
    path('branches/', include('branches.urls')),
    path('units/', include('units.urls')),
    path('categories/', include('categories.urls')),
    path('inventory/', include('inventory.urls')),
    path('purchases/', include('purchases.urls')),
    # path('', include('login.urls')),  # Login app URLs
    # path('landing/', include('landing.urls')),
path('accounts/', include('accounts.urls')),
path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('accounts/', include('logout_app.urls')),
    path('logout/', logout_views.user_logout, name='logout'),  # Add the logout URL
    path('victoria-saloon-management/', logout_views.victoria_saloon_management, name='victoria_saloon_management'),
    path('stock/', include('stock.urls')),  # Stock app
    path('sales/', include('sales.urls')),  # This includes your sales app URLs

]

