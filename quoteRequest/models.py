from django.db import models
from project.models import Project, Payment, TimeUnit, Currency, Supplier


class QuoteRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    request_nbr = models.CharField(max_length=40,unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def get_total_purchase(self):
        total_purchase = 0
        for order in self.order_set.all():
            total_purchase += order.get_total_purchase()
        return round(total_purchase, 2)

    class Meta:
        db_table = 'quote_request'
        ordering = ['-id']

class SupplierCommand(models.Model):
    command_nbr = models.CharField(max_length=40, unique=True)
    payment_date = models.DateField(blank=True,null=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    delivery_time_interval = models.CharField(max_length=20, blank=True,null=True)
    delivery_time_unit = models.ForeignKey(TimeUnit,on_delete=models.SET_NULL, blank=True,null=True) 
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True,null=True)

    vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    packaging_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    quoteRequest = models.OneToOneField(
        QuoteRequest,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'supplier_command'
        ordering = ['-id']

    
    def get_final_total(self):
        return self.quoteRequest.get_total_purchase() + self.get_fee()
    
    def get_fee(self):
        return self.packaging_fee + self.transport_fee
