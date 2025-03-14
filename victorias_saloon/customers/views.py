from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Customer
from .forms import CustomerForm
from django.http import HttpResponseRedirect


# View to display the customer list
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

# View to add a new customer
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        # Validate and save customer
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            # Check if the customer with the same name and email already exists
            if Customer.objects.filter(name=name, email=email).exists():
                messages.error(request, 'Customer with this name and email already exists.')
                return redirect('customers:add_customer')

            # Save the customer if it's not a duplicate
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('customers:customer_list')
        else:
            messages.error(request, 'There was an error with the form submission.')
            print(form.errors)  # This is for debugging purposes to check the errors in the form

    else:
        form = CustomerForm()

    return render(request, 'customers/add_customer.html', {'form': form})


def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)

        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customers:customer_list')
        else:
            messages.error(request, 'There was an error with the form submission.')

    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/add_customer.html', {'form': form})

def delete_customer(request, customer_id):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, id=customer_id)
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


from django.http import HttpResponseForbidden
from accounts.models import AppPermission

def customers_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to view this page.")

    permission = AppPermission.objects.filter(user=request.user, app_name="customers").first()
    if not permission or permission.permission == AppPermission.NO_ACCESS:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if permission.permission == AppPermission.READ:
        return render(request, 'customers/read_only.html')
    elif permission.permission == AppPermission.WRITE:
        return render(request, 'customers/customer_list.html')
