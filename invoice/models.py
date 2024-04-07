from django.db import models
from commercialOffer.models import Confirmed_commercialOffer

class Invoice(models.Model):
    invoice_nbr = models.CharField(max_length=40, unique=True)
    client_nbr = models.CharField(max_length=100, unique=True)
    confirmed_commercialOffer = models.OneToOneField(
        Confirmed_commercialOffer,
        on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    class Meta:
        db_table = 'invoice'
        ordering = ['-created_at']
    
    def get_commission(self):
        return self.confirmed_commercialOffer.get_commission()
    
    def get_total_selling_withFee(self):
        return self.confirmed_commercialOffer.get_total_selling_withFee()
    
    def get_currency(self):
        return self.confirmed_commercialOffer.get_currency()
    
class Packing(models.Model):
    invoice = models.OneToOneField(
        Invoice,
        on_delete=models.CASCADE) 
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    length = models.DecimalField(max_digits=8, decimal_places=2)
    width = models.DecimalField(max_digits=8, decimal_places=2)
    height =  models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField()
    comment = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Packing #{self.id} - for {self.invoice} invoice"
    
    def get_weight(self):
        return f"{self.weight} Kg"
    
    def get_size(self):
        return f"{self.width}x{self.height}x{self.length} cm³"
