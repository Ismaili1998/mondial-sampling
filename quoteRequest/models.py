from django.db import models
from project.models import Project, Payment, TimeUnit, Currency, Supplier


class AbstractQuoteRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    rank = models.IntegerField() 
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def get_total_purchase(self):
        total_purchase = 0
        for order in self.order_set.all():
            total_purchase += order.get_total_purchase()
        return round(total_purchase, 2)
    
    class Meta:
        abstract = True

class QuoteRequest(AbstractQuoteRequest):
    request_nbr = models.CharField(max_length=100,unique=True)
    class Meta:
        db_table = 'quote_request'
        ordering = ['-created_at','-rank']

class SupplierCommand(AbstractQuoteRequest):
    command_nbr = models.CharField(max_length=100, unique=True)
    payment_date = models.DateField(blank=True,null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    delivery_time = models.CharField(max_length=100, blank=True,null=True)
    delivery_time_unit = models.ForeignKey(TimeUnit,on_delete=models.SET_NULL, blank=True,null=True) 
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True,null=True)

    vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    packaging_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        db_table = 'supplier_command'
        ordering = ['-created_at','-rank']

    def get_final_total(self):
        return self.get_total_purchase() + self.get_fee()
    
    def get_fee(self):
        return self.packaging_fee + self.transport_fee
