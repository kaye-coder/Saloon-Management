from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from .models import InventoryItem
from .forms import InventoryItemForm
from accounts.models import AppPermission

def inventory_list(request):
    query = request.GET.get('q', '')  # Fetch query parameter if provided
    if query:
        items = InventoryItem.objects.filter(
            Q(item_name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(unit__name__icontains=query)
        )  # Extended search to include related fields
    else:
        items = InventoryItem.objects.all()

    # Calculate total stock and total costs
    total_stock = sum(item.stock for item in items)
    total_purchasing_cost = sum(item.purchasing_cost * item.stock for item in items if item.stock and item.purchasing_cost)
    total_selling_cost = sum(item.selling_cost * item.stock for item in items if item.stock and item.selling_cost)

    # Add total cost per item in a structured format
    item_details = [
        {
            'item': item,
            'total_item_cost': (item.purchasing_cost or 0) * (item.stock or 0),
            'total_purchasing_cost': item.purchasing_cost * item.stock if item.purchasing_cost and item.stock else 0,
            'total_selling_cost': item.selling_cost * item.stock if item.selling_cost and item.stock else 0
        }
        for item in items
    ]

    return render(request, 'inventory/inventory_list.html', {
        'items': item_details,
        'query': query,
        'total_stock': total_stock,
        'total_purchasing_cost': total_purchasing_cost,
        'total_selling_cost': total_selling_cost,
    })


def inventory_edit(request, item_id=None):
    """Create or edit an inventory item."""
    if item_id:
        item = get_object_or_404(InventoryItem, id=item_id)
    else:
        item = None

    form = InventoryItemForm(request.POST or None, instance=item)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('inventory:list')

    return render(request, 'inventory/inventory_edit.html', {'form': form})


def inventory_delete(request, item_id):
    """Delete an inventory item."""
    item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory:list')
    return render(request, 'inventory/inventory_delete.html', {'item': item})


def inventory_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to view this page.")

    permission = AppPermission.objects.filter(user=request.user, app_name="inventory").first()
    if not permission or permission.permission == AppPermission.NO_ACCESS:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if permission.permission == AppPermission.READ:
        return render(request, 'inventory/read_only.html')
    elif permission.permission == AppPermission.WRITE:
        return render(request, 'inventory/inventory_list.html')


# New function to get the selling price of an item
def get_item_price(request):
    item_id = request.GET.get('item_id')
    item = InventoryItem.objects.filter(id=item_id).first()
    if item:
        return JsonResponse({'selling_price': item.selling_cost})
    return JsonResponse({'selling_price': 0})
