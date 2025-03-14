from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import AppPermission
from .forms import CustomUserCreationForm, AppPermissionForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout



def manage_permissions(request):
    if not request.user.is_superuser:
        return redirect('dashboard')  # Redirect if not a superuser

    if request.method == 'POST':
        form = AppPermissionForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            apps = form.cleaned_data['app_permissions']  # Corrected field name
            permissions = form.cleaned_data['permissions']

            # For each selected app, assign the corresponding permissions
            for app in apps:
                for permission in permissions:
                    # Update or create permissions for each app and permission combination
                    AppPermission.objects.update_or_create(
                        user=user,
                        app_name=app,
                        defaults={'permission': permission}
                    )

            return redirect('manage_permissions')  # Redirect to the same page to see updates

    else:
        form = AppPermissionForm()

    permissions = AppPermission.objects.all()
    return render(request, 'accounts/manage_permissions.html', {
        'form': form,
        'permissions': permissions,
    })


def add_user(request):
    if not request.user.is_superuser:
        return redirect('dashboard')  # Only superusers can add users

    if request.method == "POST":
        user_form = CustomUserCreationForm(request.POST)
        permission_form = AppPermissionForm(request.POST)

        if user_form.is_valid() and permission_form.is_valid():
            user = user_form.save()

            # Save the user's permission
            app_permission = permission_form.save(commit=False)
            app_permission.user = user
            app_permission.save()

            return redirect('manage_users')  # Redirect to user management page
    else:
        user_form = CustomUserCreationForm()
        permission_form = AppPermissionForm()

    return render(request, 'accounts/add_user.html', {
        'user_form': user_form,
        'permission_form': permission_form
    })


def manage_users(request):
    if not request.user.is_superuser:
        return redirect('dashboard')  # Only superusers can access this page

    users = User.objects.all()
    return render(request, 'accounts/manage_users.html', {
        'users': users,
    })


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after successful login
        else:
            return HttpResponse("Invalid credentials", status=401)

    return render(request, 'accounts/login.html')


@login_required
def dashboard(request):
    # Get all apps the user has access to
    permissions = AppPermission.objects.filter(user=request.user)

    allowed_apps = []
    for permission in permissions:
        if permission.permission == 'read' or permission.permission == 'write':
            allowed_apps.append(permission.app_name)

    # You can also include logic to filter out the permission type (read/write) if needed
    return render(request, 'accounts/dashboard.html', {'allowed_apps': allowed_apps})


def delete_permission(request, permission_id):
    if not request.user.is_superuser:
        return redirect('dashboard')  # Only superusers can access this page

    # Find and delete the permission object based on the provided ID
    try:
        permission = AppPermission.objects.get(id=permission_id)
        permission.delete()
    except AppPermission.DoesNotExist:
        pass  # If permission doesn't exist, silently fail

    return redirect('manage_permissions')


def home(request):
    # Define the home page (a placeholder)
    return render(request, 'home.html')  # Ensure the home.html template exists


def edit_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('home')  # Only superusers can access this page

    user = get_object_or_404(User, id=user_id)

    # Fetching user's existing permissions and storing them in a list
    user_permissions = []
    for permission in user.app_permissions.all():
        user_permissions.append({'app_name': permission.app_name, 'permission': permission.permission})

    # Get all available apps
    apps = AppPermission.objects.all()  # Get all the available apps

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, instance=user)
        permission_form = AppPermissionForm(request.POST)

        if user_form.is_valid() and permission_form.is_valid():
            user_form.save()

            # Handle permissions (save or update the app permissions)
            for app_name in request.POST.getlist('permissions'):
                permission_type = request.POST.get(f'permissions_{app_name}')
                if permission_type:
                    AppPermission.objects.update_or_create(
                        user=user,
                        app_name=app_name,
                        defaults={'permission': permission_type}
                    )

            return redirect('manage_users')  # Redirect back to manage users page
    else:
        user_form = CustomUserCreationForm(instance=user)
        permission_form = AppPermissionForm()

    return render(request, 'accounts/edit_user.html', {
        'user_form': user_form,
        'permission_form': permission_form,
        'user': user,
        'apps': apps,  # Ensure 'apps' is defined
        'user_permissions': user_permissions  # Passing the user_permissions list
    })

# Delete User View
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect('manage_users')
    return render(request, 'accounts/confirm_delete_user.html', {'user': user})


def custom_logout(request):
    # Log out the user
    logout(request)

    # Redirect to login page
    return redirect('login')

def user_logout(request):
    logout(request)
    return redirect('victoria_saloon_management')  # Redirect to the management page

def victoria_saloon_management(request):
    return render(request, 'accounts/victoria_saloon_management.html')