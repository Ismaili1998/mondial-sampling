from django.db import models
from commercialOffer.models import CommercialOffer
# Create your models here.
class Invoice(models.Model):
    invoice_nbr = models.CharField(max_length=20, unique=True)
    client_nbr = models.CharField(max_length=20, unique=True)
    commercialOffer = models.OneToOneField(
        CommercialOffer,
        on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    class Meta:
        db_table = 'invoice'
        ordering = ['-id']
    
    def get_commission(self):
        return self.commercialOffer.get_total_selling_withFee() * (self.commission / 100)
    
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
