from django.db import models
from commercialOffer.models import AbstractCommercialOffer

class Invoice(AbstractCommercialOffer):
    invoice_nbr = models.CharField(max_length=40, unique=True)
    client_nbr = models.CharField(max_length=100)
    commission = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = 'invoice'
        ordering = ['-created_at']
    
    def get_commission(self):
        commission = self.get_total_selling_withFee() * self.commission
        return round(commission, 2)
    
    
class Packing(models.Model):
    invoice = models.OneToOneField(
        Invoice,
        on_delete=models.CASCADE) 
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    length = models.DecimalField(max_digits=8, decimal_places=2)
    width = models.DecimalField(max_digits=8, decimal_places=2)
    height =  models.DecimalField(max_digits=8, decimal_places=2)
    nbr_packages = models.IntegerField()
    comment = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Packing #{self.id} - for {self.invoice} invoice"
    
    def get_weight(self):
        return f"{self.weight} Kg"
    
    def get_size(self):
        return f"{self.width}x{self.height}x{self.length} cm³"
