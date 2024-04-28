from django.db import models
from project.models import Project, TimeUnit, Destination, Currency, Shipping, Transport, Payment

class AbstractCommercialOffer(models.Model):
    client_nbr = models.CharField(max_length=100, null=True, blank=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    rank = models.IntegerField() 
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL,null=True)

    discount = models.DecimalField(max_digits=4, decimal_places=2, blank=True, default=0)
    shipping = models.ForeignKey(Shipping, on_delete=models.SET_NULL, blank=True,null=True)
    transport = models.ForeignKey(Transport,on_delete=models.SET_NULL, blank=True,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True,null=True)
    local_contact = models.BooleanField(default=1)
    confirmed = models.BooleanField(default=0)
    destination = models.ForeignKey(Destination,on_delete=models.SET_NULL, blank=True,null=True)
    delivery_time = models.CharField(max_length=100, blank=True,null=True)
    delivery_time_unit = models.ForeignKey(TimeUnit,on_delete=models.SET_NULL, blank=True,null=True)
    warranty_period = models.CharField(max_length=200, blank=True,null=True) 
    duration_in_days = models.IntegerField(blank=True,null=True) 
    payment_date = models.DateField(blank=True,null=True)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0) 
    transport_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

    def get_orders(self):
        return self.order_set.all()
    
    def get_total_purchase(self):
        total_purchase = 0
        for order in self.get_orders():
            total_purchase += order.get_total_purchase()
        return round(total_purchase,2)

    def get_total_selling(self):
        total_selling = 0
        for order in self.get_orders():
            total_selling += order.get_total_selling()
        return round(total_selling, 2)

    def get_discounted_price(self):
        if self.discount:
            discounted_price = self.get_total_selling() * (1- self.discount / 100)
            return round(discounted_price,2)
        return 0.00
    
    def get_discount_price(self):
        if self.discount:
            discount_price = self.get_total_selling() * (self.discount / 100)
            return round(discount_price,2)
        return 0.00
    
    def get_total_fee(self):
        return self.transport_fee  + self.shipping_fee 

    def get_total_selling_withFee(self):
        return (self.get_discounted_price() or self.get_total_selling()) + self.get_total_fee()
   

class CommercialOffer(AbstractCommercialOffer):
    offer_nbr = models.CharField(max_length=100, unique=True)
    class Meta:
        db_table = 'commercialOffer'
        ordering = ['-rank']

    def __str__(self):
        return self.offer_nbr
    
class Confirmed_commercialOffer(AbstractCommercialOffer):
    confirmation_nbr = models.CharField(max_length=100, unique=True)
    commission = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        db_table = 'confirmed_commercialOffer'
        ordering = ['-rank']

    def get_commission(self):
        commission = self.get_total_selling_withFee() * (self.commission / 100)
        return round(commission, 2)
    
  