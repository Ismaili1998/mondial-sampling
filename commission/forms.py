from django import forms
from .models import AdvancePayment

class AdvancePaymentForm(forms.ModelForm):
    class Meta:
        model = AdvancePayment
        exclude = ['created_at']

