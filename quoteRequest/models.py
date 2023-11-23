from django.db import models
from project.models import Project, Payment, TimeUnit, Currency, Supplier


class QuoteRequest(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    request_nbr = models.CharField(max_length=20,unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        db_table = 'quoteRequest'
        ordering = ['-id']

class SupplierCommand(models.Model):
    command_nbr = models.CharField(max_length=20, unique=True)
    payment_date = models.DateField(blank=True,null=True)
    delivery_time_interval = models.CharField(max_length=20, blank=True,null=True)
    delivery_time_unit = models.ForeignKey(TimeUnit,on_delete=models.PROTECT, blank=True,null=True) 
    payment = models.ForeignKey(Payment,on_delete=models.PROTECT, blank=True,null=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True)

    vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    packaging_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)

    quoteRequest = models.OneToOneField(
        QuoteRequest,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        db_table = 'supplier_command'
        ordering = ['-id']

    def get_total_purchase(self):
        total_purchase = 0
        for order in self.quoteRequest.order_set.all():
            total_purchase += order.get_total_purchase()
        return round(total_purchase, 2)
    
    def get_final_total(self):
        return self.get_total_purchase() + self.get_fee()
    
    def get_fee(self):
        return (self.packaging_fee + self.transport_fee) or 0
