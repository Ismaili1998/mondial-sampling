from django import forms
from .models import CommercialOffer, Confirmed_commercialOffer

class CommercialOfferForm(forms.ModelForm):
    class Meta:
        model = CommercialOffer
        exclude = ['offer_nbr', 'confirmed', 'rank']

class Confirmed_commercialOfferForm(forms.ModelForm):
    class Meta:
        model = Confirmed_commercialOffer
        exclude = ['created_at', 'updated_at','confirmation_nbr', 'project', 'rank']