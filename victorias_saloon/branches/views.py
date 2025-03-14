from django.shortcuts import render, redirect, get_object_or_404
from .models import Branch
from .forms import BranchForm

# List all branches
def branch_list(request):
    branches = Branch.objects.all()
    return render(request, 'branches/branch_list.html', {'branches': branches})

# Add a new branch
def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('branches:branch_list')
    else:
        form = BranchForm()
    return render(request, 'branches/add_branch.html', {'form': form})

# Update an existing branch
def update_branch(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect('branches:branch_list')  # Redirect back to the branch list after update
    else:
        form = BranchForm(instance=branch)  # Pre-populate the form with the branch details
    return render(request, 'branches/update_branch.html', {'form': form, 'branch': branch})

def delete_branch(request, pk):
    branch = Branch.objects.get(pk=pk)
    branch.delete()
    return redirect('branches:branch_list')



from django.http import HttpResponseForbidden
from accounts.models import AppPermission

def branches_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to view this page.")

    permission = AppPermission.objects.filter(user=request.user, app_name="branches").first()
    if not permission or permission.permission == AppPermission.NO_ACCESS:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if permission.permission == AppPermission.READ:
        return render(request, 'branches/read_only.html')
    elif permission.permission == AppPermission.WRITE:
        return render(request, 'branches/branch_list.html')
