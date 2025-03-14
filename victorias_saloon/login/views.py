from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing_page')  # Redirect to the landing page after login
        else:
            return render(request, 'login/login.html', {'error': 'Invalid credentials'})
    return render(request, 'login/login.html')

@login_required
def dashboard(request):
    return render(request, 'login/dashboard.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Superuser-only view to add users and assign permissions
@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        is_staff = 'is_staff' in request.POST
        new_user = User.objects.create_user(username, email, password)
        new_user.is_staff = is_staff
        new_user.save()

        # Assign permissions based on form inputs
        if 'can_read' in request.POST:
            permission = Permission.objects.get(codename='view_user')
            new_user.user_permissions.add(permission)
        if 'can_write' in request.POST:
            permission = Permission.objects.get(codename='change_user')
            new_user.user_permissions.add(permission)

        return redirect('dashboard')
    return render(request, 'login/add_user.html')
