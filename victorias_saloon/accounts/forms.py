from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import AppPermission

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AppPermissionForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="User")
    app_permissions = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[('employees', 'Employees'),
                 ('customers', 'Customers'),
                 ('suppliers', 'Suppliers'),
                 ('positions', 'Positions'),
                 ('branches', 'Branches'),
                 ('units', 'Units'),
                 ('categories', 'Categories'),
                 ('inventory', 'Inventory'),
                 ('sales', 'Sales'),
                 ('purchases', 'Purchases')],
        label="Select Apps"
    )

    # Define fields for permissions with checkboxes
    permissions = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[('read', 'Read'), ('write', 'Write')],
        label="Permissions"
    )

    def __init__(self, *args, **kwargs):
        super(AppPermissionForm, self).__init__(*args, **kwargs)
        self.fields['app_permissions'].required = False
        self.fields['permissions'].required = False