from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Purchase, InventoryItem, Supplier, Unit, Category
from django.contrib import messages

def purchase_list(request):
    purchases = Purchase.objects.all()
    total_quantity = sum([purchase.quantity for purchase in purchases])
    total_cost = sum([purchase.purchase_price * purchase.quantity for purchase in purchases])

    return render(request, 'purchases/purchase_list.html', {
        'purchases': purchases,
        'total_quantity': total_quantity,
        'total_cost': total_cost,
        'inventory_items': InventoryItem.objects.all(),
        'suppliers': Supplier.objects.all(),
        'units': Unit.objects.all(),
        'categories': Category.objects.all(),
    })


def create_purchase(request):
    if request.method == 'POST':
        item = InventoryItem.objects.get(id=request.POST['inventory_item'])
        supplier = Supplier.objects.get(id=request.POST['supplier'])
        unit = Unit.objects.get(id=request.POST['unit'])
        category = Category.objects.get(id=request.POST['category'])
        quantity = int(request.POST['quantity'])
        purchase_price = float(request.POST['purchase_price'])

        Purchase.objects.create(
            inventory_item=item,
            supplier=supplier,
            unit=unit,
            category=category,
            quantity=quantity,
            purchase_price=purchase_price,
        )

        messages.success(request, "Purchase added successfully.")
        return redirect('purchases:list')

    return render(request, 'purchases/create_purchase.html', {
        'inventory_items': InventoryItem.objects.all(),
        'suppliers': Supplier.objects.all(),
        'units': Unit.objects.all(),
        'categories': Category.objects.all(),
    })


def purchase_delete(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id)

    # If the request method is POST, perform the delete
    if request.method == 'POST':
        purchase.delete()
        messages.success(request, "Purchase deleted successfully.")
        return redirect('purchases:list')  # Redirect back to the purchases list

    # If the request method is GET, render the confirmation page
    return render(request, 'purchases/purchase_confirm_delete.html', {'purchase': purchase})


from django.shortcuts import render
from django.http import HttpResponseForbidden
from accounts.models import AppPermission

def purchases_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to view this page.")

    permission = AppPermission.objects.filter(user=request.user, app_name="purchases").first()
    if not permission or permission.permission == AppPermission.NO_ACCESS:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if permission.permission == AppPermission.READ:
        return render(request, 'purchases/read_only.html')
    elif permission.permission == AppPermission.WRITE:
        return render(request, 'purchases/purchase_list.html')
