from django import forms
from .models import Unit

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name', 'abbreviation']

    def __init__(self, *args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)