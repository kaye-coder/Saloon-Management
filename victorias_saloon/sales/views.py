from django.shortcuts import render, redirect, get_object_or_404
from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemForm
from inventory.models import InventoryItem
from branches.models import Branch
from customers.models import Customer
from django.http import HttpResponse
from decimal import Decimal
from django.contrib import messages
from django.db import IntegrityError


# Create Sale View
def create_sale(request):
    if request.method == "POST":
        branch_id = request.POST.get("branch")
        customer_id = request.POST.get("customer")
        item_ids = request.POST.getlist("item[]")
        quantities = request.POST.getlist("quantity[]")
        total_amount = request.POST.get("total_amount")
        amount_paid = request.POST.get("amount_paid")

        # Convert to Decimal
        total_amount = Decimal(total_amount) if total_amount else Decimal(0)
        amount_paid = Decimal(amount_paid) if amount_paid else Decimal(0)
        balance = total_amount - amount_paid

        # Fetch selected branch and customer (if any)
        branch = Branch.objects.get(id=branch_id) if branch_id else None
        customer = Customer.objects.get(id=customer_id) if customer_id else None

        # Check if there is enough stock for each item
        for i in range(len(item_ids)):
            item = get_object_or_404(InventoryItem, id=item_ids[i])
            quantity = int(quantities[i])

            if item.stock < quantity:
                messages.error(request, f"Not enough stock for item: {item.item_name}. Only {item.stock} available.")
                return redirect('sales:create_sale')

        try:
            # Create the Sale record
            sale = Sale.objects.create(
                branch=branch,
                customer=customer,
                total_price=total_amount,
                paid=amount_paid,
                balance=balance
            )

            # Loop through each item to create SaleItem records
            for i in range(len(item_ids)):
                item = get_object_or_404(InventoryItem, id=item_ids[i])
                quantity = int(quantities[i])
                selling_price = item.selling_cost  # Fetch selling price automatically
                total_price = quantity * selling_price

                # Deduct the quantity from inventory stock
                item.stock -= quantity
                item.save()

                SaleItem.objects.create(
                    sale=sale,
                    item=item,
                    quantity_sold=quantity,
                    selling_price=selling_price,
                    total_price=total_price
                )

            # Redirect to the receipt view for the newly created sale
            return redirect("sales:receipt", sale_id=sale.id)

        except IntegrityError:
            messages.error(request, "There was an error creating the sale. Please try again.")
            return redirect('sales:create_sale')

    # Fetch all branches, customers, and inventory items for dropdowns
    branches = Branch.objects.all()
    customers = Customer.objects.all()
    inventory_items = InventoryItem.objects.all()

    return render(request, "sales/create_sale.html", {
        "branches": branches,
        "customers": customers,
        "inventory_items": inventory_items
    })

# Update Payment View
def update_payment(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)

    if request.method == "POST":
        amount_paid = Decimal(request.POST.get("amount_paid", 0))
        sale.paid += amount_paid
        sale.balance = sale.total_price - sale.paid
        sale.save()
        return redirect('sales:receipt', sale_id=sale.id)

    return render(request, 'sales/update_payment.html', {'sale': sale})


def sale_list(request):
    # Sort sales by sale_date in descending order so the most recent ones appear first
    sales = Sale.objects.all().order_by('-sale_date')

    # Calculate totals
    total_balance = sum(sale.balance for sale in sales)
    total_items_sold = sum(item.quantity_sold for sale in sales for item in sale.sale_items.all())
    total_loss = sum(sale.balance for sale in sales if sale.balance > 0)

    return render(request, 'sales/sale_list.html', {
        'sales': sales,
        'total_balance': total_balance,
        'total_items_sold': total_items_sold,
        'total_loss': total_loss,
    })

# Receipt View
def view_receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'sales/view_receipt.html', {'sale': sale})


# Delete Sale View
def delete_sale(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    sale.delete()
    return redirect('sales:sale_list')


# Sales Dashboard View
def sales_dashboard(request):
    return render(request, 'sales/sales_dashboard.html')
