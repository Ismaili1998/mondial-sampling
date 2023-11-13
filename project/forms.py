from django import forms
from .models import Project, Supplier, Article, CommercialOffer, Supplier_contact, Client_contact, SupplierCommand, Confirmed_commercialOffer, Invoice, Packing

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['created_at', 'updated_at']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ['created_at', 'updated_at']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_at', 'updated_at', 'project']

class CommercialOfferForm(forms.ModelForm):
    class Meta:
        model = CommercialOffer
        exclude = ['offer_nbr', 'confirmed']

class Confirmed_commercialOfferForm(forms.ModelForm):
    class Meta:
        model = Confirmed_commercialOffer
        exclude = ['created_at', 'updated_at','confirmation_nbr', 'commercialOffer']

class SupplierCommandForm(forms.ModelForm):
    class Meta:
        model = SupplierCommand
        exclude = ['command_nbr', 'quoteRequest']

class Supplier_contactForm(forms.ModelForm):
    class Meta:
        model = Supplier_contact
        fields = '__all__'
            
class Client_contactForm(forms.ModelForm):
    class Meta:
        model = Client_contact
        fields = '__all__'

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client_nbr']

class PackingForm(forms.ModelForm):
    class Meta:
        model = Packing
        fields = '__all__'
        exclude = ['invoice']