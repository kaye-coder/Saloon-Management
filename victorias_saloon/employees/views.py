from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Employee
from .forms import EmployeeForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from accounts.models import AppPermission


def employee_list(request):
    query = request.GET.get('q', '')
    if query:
        employees = Employee.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query)
        )
    else:
        employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees, 'query': query})


def add_employee(request, employee_id=None):
    # If it's an edit operation, fetch the existing employee
    if employee_id:
        employee = Employee.objects.get(pk=employee_id)
    else:
        employee = None

    # Handle form submission for adding or editing employee
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)

        if form.is_valid():
            # Check if the employee already exists based on unique fields
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')

            # Check for existing employee with the same email or phone number
            if employee_id:
                existing_employee = Employee.objects.exclude(id=employee_id).filter(email=email,
                                                                                    phone_number=phone_number).first()
            else:
                existing_employee = Employee.objects.filter(email=email, phone_number=phone_number).first()

            if existing_employee:
                # Add a message indicating the duplicate entry
                messages.error(request, 'An employee with this email or phone number already exists.')
                return redirect('employee:add_employee')

            # Save the new or updated employee
            form.save()
            messages.success(request, 'Employee saved successfully.')
            return redirect('employee:employee_list')

    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/add_employee.html', {'form': form, 'employee': employee})
def confirm_delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee:employee_list')
    return render(request, 'employees/confirm_delete_employee.html', {'employee': employee})

def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee:employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/edit_employee.html', {'form': form, 'employee': employee})

def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('employee:employee_list')  # Redirect to the employee list after deletion

    return render(request, 'employees/confirm_delete_employee.html', {'employee': employee})


def employees_view(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to view this page.")

    permission = AppPermission.objects.filter(user=request.user, app_name="employees").first()
    if not permission or permission.permission == AppPermission.NO_ACCESS:
        return HttpResponseForbidden("You are not authorized to view this page.")

    if permission.permission == AppPermission.READ:
        return render(request, 'employees/read_only.html')
    elif permission.permission == AppPermission.WRITE:
        return render(request, 'employees/employee-list.html')

