from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from .models import Unit
from .forms import UnitForm


def unit_list(request):
    units = Unit.objects.all()
    return render(request, 'units/unit_list.html', {'units': units})

def unit_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        abbreviation = request.POST.get('abbreviation')
        if name and abbreviation:
            Unit.objects.create(name=name, abbreviation=abbreviation)
            return redirect('unit_list')
    return render(request, 'units/unit_form.html')

def unit_edit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)

    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('unit_list')  # Redirect to the list view after saving
    else:
        form = UnitForm(instance=unit)

    return render(request, 'units/edit_unit.html', {'form': form, 'unit': unit})
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    unit.delete()
    return redirect('unit_list')



from django.http import HttpResponseForbidden
from accounts.models import AppPermission

def units_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to view this page.")

    permission = AppPermission.objects.filter(user=request.user, app_name="units").first()
    if not permission or permission.permission == AppPermission.NO_ACCESS:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if permission.permission == AppPermission.READ:
        return render(request, 'units/read_only.html')
    elif permission.permission == AppPermission.WRITE:
        return render(request, 'units/unit_list.html')
