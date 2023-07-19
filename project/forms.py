from django import forms
from .models import Project, Supplier, Article, CommercialOffer, Supplier_contact, Client_contact, Order

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
        exclude = ['offer_nbr']

class Supplier_contactForm(forms.ModelForm):
    class Meta:
        model = Supplier_contact
        fields = '__all__'
            
class Client_contactForm(forms.ModelForm):
    class Meta:
        model = Client_contact
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Client_contact
        fields = '__all__'

