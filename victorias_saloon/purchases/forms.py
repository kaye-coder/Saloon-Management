from django import forms
from .models import Purchase

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['inventory_item', 'supplier', 'quantity', 'purchase_price', 'unit', 'category']
