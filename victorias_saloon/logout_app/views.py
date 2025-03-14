# logout_app/views.py
from django.shortcuts import redirect, render
from django.contrib.auth import logout

# View to log out the user and redirect to Victoria's Saloon Management page
def user_logout(request):
    logout(request)
    return redirect('victoria_saloon_management')  # Redirect to the management page

# View to render the Victoria's Saloon Management page
def victoria_saloon_management(request):
    return render(request, 'victoria_saloon_management.html')
