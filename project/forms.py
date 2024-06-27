from django import forms
from .models import Project, Client, Supplier, Supplier_contact, Representative, Buyer

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['created_at', 'updated_at']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['created_at', 'updated_at', 'rank']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ['created_at', 'updated_at']

class Supplier_contactForm(forms.ModelForm):
    class Meta:
        model = Supplier_contact
        fields = '__all__'
            
class RepresentativeForm(forms.ModelForm):
    class Meta:
        model = Representative
        fields = '__all__'

class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = '__all__'
