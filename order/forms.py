from django import forms
from .models import Article, Order

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_at', 'updated_at', 'projects']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['id']