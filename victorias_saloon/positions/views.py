from django.shortcuts import render, get_object_or_404, redirect
from .models import Position
from .forms import PositionForm

# List positions
def position_list(request):
    positions = Position.objects.all()
    return render(request, 'positions/position_list.html', {'positions': positions})

# Edit position
def edit_position(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            return redirect('positions:position_list')
    else:
        form = PositionForm(instance=position)
    return render(request, 'positions/edit_position.html', {'form': form, 'position': position})

# Create new position
def create_position(request):
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('positions:position_list')
    else:
        form = PositionForm()
    return render(request, 'positions/edit_position.html', {'form': form, 'position': None})

# Delete position
def delete_position(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        position.delete()
        return redirect('positions:position_list')
    return redirect('positions:position_list')



from django.http import HttpResponseForbidden
from .models import Position
from accounts.models import AppPermission


def positions_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to view this page.")

    permission = AppPermission.objects.filter(user=request.user, app_name="positions").first()
    if not permission or permission.permission == AppPermission.NO_ACCESS:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if permission.permission == AppPermission.READ:
        positions = Position.objects.all()  # Fetch all positions
        return render(request, 'positions/read_only.html', {'positions': positions})

    return HttpResponseForbidden("You are not authorized to view this page.")
