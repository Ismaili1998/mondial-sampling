from django import forms
from .models import Project, Supplier, Article, CommercialOffer

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['created_at', 'updated_at','articles']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ['created_at', 'updated_at']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_at', 'updated_at']

class CommercialOfferForm(forms.ModelForm):
    class Meta:
        model = CommercialOffer
        fields = '__all__'