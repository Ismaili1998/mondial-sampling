from django import forms
from .models import Project, Supplier, Article, CommercialOffer, Supplier_contact, Buyer, Client_contact

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
        exclude = ['client']

class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = '__all__'
        exclude = ['project']

    
class Client_contactForm(forms.ModelForm):
    class Meta:
        model = Client_contact
        fields = '__all__'
