from django.shortcuts import render, get_object_or_404, redirect
from .models import Supplier
from .forms import SupplierForm  # Assuming you have a SupplierForm for validation

# Add a new supplier
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            # Check if a supplier with the same name, phone, and email already exists
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']

            # Check if any supplier with the same name, phone, or email exists
            if Supplier.objects.filter(name=name, phone_number=phone_number, email=email).exists():
                # Add an error message if supplier already exists
                form.add_error(None, 'Supplier already exists with the same name, phone number, and email.')
                return render(request, 'suppliers/add_supplier.html', {'form': form})

            form.save()
            return redirect('suppliers:supplier_list')
    else:
        form = SupplierForm()

    return render(request, 'suppliers/add_supplier.html', {'form': form})

# Update an existing supplier
def update_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers:supplier_list')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'suppliers/add_supplier.html', {'form': form})

# Delete a supplier with confirmation
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        supplier.delete()
        return redirect('suppliers:supplier_list')

    return render(request, 'suppliers/confirm_delete_supplier.html', {'supplier': supplier})

# Display the list of suppliers with search
def supplier_list(request):
    query = request.GET.get('q', '')
    if query:
        suppliers = Supplier.objects.filter(name__icontains=query)
    else:
        suppliers = Supplier.objects.all()

    return render(request, 'suppliers/supplier_list.html', {'suppliers': suppliers, 'query': query})



from django.http import HttpResponseForbidden
from accounts.models import AppPermission

def suppliers_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to view this page.")

    permission = AppPermission.objects.filter(user=request.user, app_name="suppliers").first()
    if not permission or permission.permission == AppPermission.NO_ACCESS:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if permission.permission == AppPermission.READ:
        return render(request, 'suppliers/read_only.html')
    elif permission.permission == AppPermission.WRITE:
        return render(request, 'suppliers/supplier_list.html')
