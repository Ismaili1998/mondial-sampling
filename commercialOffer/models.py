from django.db import models
from project.models import Project, TimeUnit, Destination, Currency, Shipping, Transport, Payment

class CommercialOffer(models.Model):
    offer_nbr = models.CharField(max_length=20, unique=True)
    project = models.ForeignKey(Project,on_delete=models.PROTECT)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True)
    margin = models.DecimalField(max_digits=4, decimal_places=2) 

    discount = models.DecimalField(max_digits=4, decimal_places=2, blank=True,null=True)
    shipping = models.ForeignKey(Shipping, on_delete=models.PROTECT, blank=True,null=True)
    transport = models.ForeignKey(Transport,on_delete=models.PROTECT, blank=True,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.PROTECT, blank=True,null=True)
    local_contact = models.BooleanField(default=1)
    confirmed = models.BooleanField(default=0)
    destination = models.ForeignKey(Destination,on_delete=models.PROTECT, blank=True,null=True)
    delivery_time_interval = models.CharField(max_length=20, blank=True,null=True)
    delivery_time_unit = models.ForeignKey(TimeUnit,on_delete=models.PROTECT, blank=True,null=True) 
    duration_in_days = models.IntegerField(blank=True,null=True) 
    valid_date = models.DateField(blank=True,null=True)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True,null=True) 
    transport_fee = models.DecimalField(max_digits=12, decimal_places=2, blank=True,null=True)

    class Meta:
        db_table = 'commercial_offer'
        ordering = ['-id']

    def __str__(self):
        return self.offer_nbr
    
    def get_orders(self):
        orders = []
        for order in self.order_set.all():
            order.selling_price = round(order.article.purchase_price + order.margin * order.article.purchase_price / 100,2)
            order.total_selling_price = round(order.quantity * order.selling_price, 2)
            orders.append(order)
        return orders
    
    def get_total_purchase(self):
        total_purchase = 0
        for order in self.order_set.all():
            total_purchase += order.quantity * order.article.purchase_price
        return round(total_purchase,2)

    def get_total_selling(self):
        total_selling = self.get_total_purchase() + self.get_total_purchase() * self.margin / 100
        return round(total_selling,2)
    
    def get_discounted_price(self):
        if self.discount:
            discounted_price = self.get_total_selling() * (1- self.discount / 100)
            return round(discounted_price,2)
    
    def get_discount_price(self):
        if self.discount:
            discount_price = self.get_total_selling() * (self.discount / 100)
            return round(discount_price,2)

    def get_total_fee(self):
        return (self.transport_fee or 0) + (self.shipping_fee or 0)

    def get_total_selling_withFee(self):
        return (self.get_discounted_price() or self.get_total_selling()) + self.get_total_fee()

class Confirmed_commercialOffer(models.Model):
    confirmation_nbr = models.CharField(max_length=20, unique=True)
    client_nbr = models.CharField(max_length=20, unique=True)
    commission = models.DecimalField(max_digits=4, decimal_places=2)
    commercialOffer = models.OneToOneField(
        CommercialOffer,
        on_delete=models.CASCADE) 
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'confirmed_commercial_offer'
        ordering = ['-id']
    
    def get_commission(self):
        return self.commercialOffer.get_total_selling_withFee() * (self.commission / 100)