from django.shortcuts import render, redirect
from .models import Category
from .forms import CategoryForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'categories/category_form.html', {'form': form})

def category_edit(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_form.html', {'form': form})

def category_delete(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()
    return redirect('category_list')


from django.http import HttpResponseForbidden
from accounts.models import AppPermission

def categories_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to view this page.")

    permission = AppPermission.objects.filter(user=request.user, app_name="categories").first()
    if not permission or permission.permission == AppPermission.NO_ACCESS:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if permission.permission == AppPermission.READ:
        return render(request, 'categories/read_only.html')
    elif permission.permission == AppPermission.WRITE:
        return render(request, 'categories/category_list.html')
