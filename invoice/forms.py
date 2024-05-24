from django import forms
from .models import Invoice, Packing

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client_nbr', 'commission']

class PackingForm(forms.ModelForm):
    class Meta:
        model = Packing
        fields = '__all__'
        exclude = ['invoice']