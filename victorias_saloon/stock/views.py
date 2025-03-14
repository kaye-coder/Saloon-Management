from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum,F
from .models import Stock
from .forms import StockForm
from django.forms import modelformset_factory


def stock_list(request):
    # Fetching search query from GET request
    search_query = request.GET.get('search', '')
    if search_query:
        stocks = Stock.objects.filter(name__icontains=search_query)
    else:
        stocks = Stock.objects.all()

    # Annotate the total purchase cost and total selling cost directly in the query
    stocks = stocks.annotate(
        total_purchase_cost=Sum('quantity') * F('purchase_price'),
        total_selling_cost=Sum('quantity') * F('selling_price')
    )

    # Calculate aggregated totals using the `aggregate` function
    total_stock = stocks.aggregate(total=Sum('quantity'))['total'] or 0
    total_purchase_cost = stocks.aggregate(total=Sum('total_purchase_cost'))['total'] or 0
    total_selling_cost = stocks.aggregate(total=Sum('total_selling_cost'))['total'] or 0

    context = {
        'stocks_with_totals': stocks,
        'total_stock': total_stock,
        'total_purchase_cost': total_purchase_cost,
        'total_selling_cost': total_selling_cost,
    }
    return render(request, 'stock/stock_list.html', context)

def stock_create(request):
    StockFormSet = modelformset_factory(Stock, fields=('name', 'quantity', 'purchase_price', 'selling_price'), extra=1)
    if request.method == 'POST':
        formset = StockFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('stock_list')  # Redirect after saving
    else:
        formset = StockFormSet(queryset=Stock.objects.none())  # Create empty formset
    return render(request, 'stock/stock_form.html', {'formset': formset})

def stock_update(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('stock_list')  # Redirect to stock list after update
    else:
        form = StockForm(instance=stock)
    return render(request, 'stock/stock_form.html', {'form': form})

def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == 'POST':
        stock.delete()
        return redirect('stock_list')  # Redirect to stock list after delete
    # If DELETE is not confirmed via POST, it could trigger the modal confirmation or redirect directly
    return redirect('stock_list')  # Directly delete without confirmation page if desired
