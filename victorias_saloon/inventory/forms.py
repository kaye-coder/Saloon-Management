from django import forms
from .models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['item_name', 'category', 'unit', 'purchasing_cost', 'selling_cost', 'stock']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purchasing_cost'].widget = forms.NumberInput(attrs={'step': '0.01'})
        self.fields['selling_cost'].widget = forms.NumberInput(attrs={'step': '0.01'})
