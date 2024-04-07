from django import forms
from .models import SupplierCommand

class SupplierCommandForm(forms.ModelForm):
    class Meta:
        model = SupplierCommand
        exclude = ['command_nbr', 'quoteRequest']